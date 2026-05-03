#!/usr/bin/env python3
"""
Agente — Autonomous AI Developer Pipeline
Usa Claude Code CLI e Gemini CLI — sem API keys, sem cobrança por token.
Uso: agente "descrição da feature"
"""

from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# ─── Configuração ────────────────────────────────────────────────────────────

AGENTE_HOME = Path.home() / ".agente"
SKILLS_DIR  = AGENTE_HOME / "skills"
AGENTS_MD   = AGENTE_HOME / "agents.md"

PIPELINES: dict[str, tuple[str, list[str]]] = {
    "1": ("Full Cycle: PM → Engineer → QA → DevOps", ["pm", "engineer", "qa", "devops"]),
    "2": ("Spec + Code: PM → Engineer",               ["pm", "engineer"]),
    "3": ("Só Spec: PM",                              ["pm"]),
    "4": ("Só QA",                                    ["qa"]),
    "5": ("Só DevOps",                                ["devops"]),
}

# Skills carregados para cada agente (na ordem de uso)
AGENT_SKILLS: dict[str, list[str]] = {
    "pm":       ["write_specs.md"],
    "engineer": ["code_standards.md", "generate_code.md", "refactor.md", "write_tests.md"],
    "qa":       ["audit_code.md", "performance_audit.md", "security_scan.md"],
    "devops":   ["git_workflow.md", "review_pr.md", "deploy_app.md",
                 "deploy_cloud_run.md", "rollback.md", "session_log.md"],
}

# CLI e modelo por agente
# claude CLI: usa "claude -p <prompt> --model <model>"
# gemini CLI: usa "gemini <prompt>"
AGENT_CLI: dict[str, tuple[str, str]] = {
    "pm":       ("claude", "claude-sonnet-4-5"),
    "engineer": ("claude", "claude-sonnet-4-5"),
    "qa":       ("gemini", "gemini-2.5-pro"),
    "devops":   ("gemini", "gemini-2.5-pro"),
}

# Fallback: se Gemini falhar, usa claude CLI com haiku
CLAUDE_FALLBACK_MODEL = "claude-haiku-4-5"

# Gates de aprovação humana
GATES: dict[str, str] = {
    "pm":  "Gate 1 — Especificação gerada. Revise antes do Engineer começar.",
    "qa":  "Gate 2 — QA concluído. Revise antes do deploy.",
}

APPROVE_TOKENS = {"ok", "sim", "aprovado", "lgtm", "pode seguir", "pode continuar", "approved", "yes"}
REJECT_TOKENS  = {"cancelar", "não", "nao", "abort", "cancel", "no"}

# ─── Verificação de CLIs ──────────────────────────────────────────────────────

def _check_clis() -> None:
    claude_ok = _cmd_exists("claude")
    gemini_ok = _cmd_exists("gemini")

    if not claude_ok:
        print("❌  Claude Code CLI não encontrado.")
        print("    Instale em: https://claude.ai/code")
        sys.exit(1)

    if not gemini_ok:
        print("⚠️   Gemini CLI não encontrado.")
        print("    QA e DevOps usarão fallback: claude-haiku.")
        print("    Para instalar: https://github.com/google-gemini/gemini-cli")
        print()


def _cmd_exists(cmd: str) -> bool:
    try:
        subprocess.run([cmd, "--version"], capture_output=True, timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

# ─── Helpers de leitura ───────────────────────────────────────────────────────

def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def load_agents_md() -> str:
    return _read(AGENTS_MD)


def load_skills(agent: str) -> str:
    parts: list[str] = []
    for filename in AGENT_SKILLS.get(agent, []):
        content = _read(SKILLS_DIR / filename)
        if content:
            parts.append(f"## [{filename}]\n\n{content}")
    return "\n\n---\n\n".join(parts)


def build_prompt(agent: str, idea: str, prev_output: str) -> str:
    agents_content = load_agents_md()
    skills_content = load_skills(agent)

    parts: list[str] = []
    if agents_content:
        parts.append(agents_content)
    if skills_content:
        parts.append(f"## Skills disponíveis para @{agent}:\n\n{skills_content}")
    parts.append(f"## Feature / Ideia:\n{idea}")
    if prev_output.strip():
        parts.append(f"## Output do agente anterior (use como contexto direto):\n{prev_output}")
    parts.append(
        f"\nExecute agora sua função como @{agent}. "
        "Comunique-se com o usuário em Português Brasileiro."
    )
    return "\n\n---\n\n".join(parts)

# ─── Chamadas aos CLIs ────────────────────────────────────────────────────────

def call_claude_cli(agent: str, model: str, idea: str, prev_output: str) -> str:
    prompt = build_prompt(agent, idea, prev_output)
    result = subprocess.run(
        ["claude", "-p", prompt, "--model", model],
        capture_output=True,
        text=True,
        timeout=600,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or "claude CLI falhou sem mensagem de erro")
    return result.stdout.strip()


def call_gemini_cli(agent: str, idea: str, prev_output: str) -> str:
    prompt = build_prompt(agent, idea, prev_output)
    result = subprocess.run(
        ["gemini", prompt],
        capture_output=True,
        text=True,
        timeout=600,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or "gemini CLI falhou sem mensagem de erro")
    return result.stdout.strip()


def run_agent(agent: str, idea: str, prev_output: str) -> tuple[str, str, str]:
    """
    Executa o agente via CLI.
    Retorna (output, cli_usado, model_usado).
    """
    cli, model = AGENT_CLI[agent]

    show_agent_header(agent, cli, model)

    if cli == "claude":
        output = call_claude_cli(agent, model, idea, prev_output)
        return output, cli, model

    # Gemini com fallback para claude-haiku
    try:
        output = call_gemini_cli(agent, idea, prev_output)
        return output, "gemini", model
    except Exception as exc:
        print(f"\n  ⚠️  Gemini falhou: {exc}")
        print(f"  ↩️  Usando fallback: claude CLI / {CLAUDE_FALLBACK_MODEL}")
        show_agent_header(agent, "claude (fallback)", CLAUDE_FALLBACK_MODEL)
        output = call_claude_cli(agent, CLAUDE_FALLBACK_MODEL, idea, prev_output)
        return output, f"claude-fallback", CLAUDE_FALLBACK_MODEL

# ─── UI / Terminal ────────────────────────────────────────────────────────────

def show_menu() -> tuple[str, list[str]]:
    print()
    print("╔══════════════════════════════════════════╗")
    print("║       AGENTE — Pipeline Autônomo de IA   ║")
    print("╚══════════════════════════════════════════╝")
    print()
    for key, (label, _) in PIPELINES.items():
        print(f"  [{key}] {label}")
    print()
    while True:
        choice = input("Selecione o modo [1-5]: ").strip()
        if choice in PIPELINES:
            return PIPELINES[choice]
        print("  Opção inválida. Digite um número de 1 a 5.")


def show_agent_header(agent: str, cli: str, model: str) -> None:
    print()
    print(f"{'─' * 52}")
    print(f"  🤖  @{agent}  |  {cli} / {model}")
    print(f"{'─' * 52}")


def show_output_preview(agent: str, output: str) -> None:
    print()
    print(f"  📄  Saída de @{agent}:")
    print(f"  {'─' * 48}")
    lines = output.strip().splitlines()
    for line in lines[:50]:
        print(f"  {line}")
    if len(lines) > 50:
        print(f"  ... (+{len(lines) - 50} linhas não exibidas)")


def approval_gate(gate_msg: str, preview: str) -> bool:
    print()
    print("=" * 52)
    print(f"  🚦  {gate_msg}")
    print("=" * 52)
    lines = preview.strip().splitlines()
    for line in lines[:40]:
        print(f"  {line}")
    if len(lines) > 40:
        print(f"  ... (+{len(lines) - 40} linhas omitidas)")
    print()
    print("  Continuar: ok / sim / aprovado / lgtm / pode seguir")
    print("  Cancelar:  cancelar / abort / não")
    print()
    while True:
        resp = input("  > ").strip().lower()
        if resp in APPROVE_TOKENS:
            return True
        if resp in REJECT_TOKENS:
            return False
        print("  Resposta não reconhecida. Digite 'ok' ou 'cancelar'.")

# ─── Session Log ──────────────────────────────────────────────────────────────

def append_session_log(log_path: Path, agent: str, cli: str, model: str, output: str) -> None:
    """Salva apenas a decisão final do agente (sem raciocínio interno)."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    summary   = output.strip()[:800].replace("\n", " ")
    entry = (
        f"\n---\n"
        f"## @{agent} ({cli}/{model}) — {timestamp}\n"
        f"**Resumo**: {summary}\n"
        f"---\n"
    )
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(entry)

# ─── Resumo final ─────────────────────────────────────────────────────────────

def print_summary(run_log: list[tuple[str, str, str]]) -> None:
    print()
    print("╔══════════════════════════════════════════╗")
    print("║           RESUMO DO CICLO                 ║")
    print("╠══════════════════════════════════════════╣")
    for agent, cli, model in run_log:
        print(f"║  @{agent:<10}  {cli:<16}  {model:<18}║")
    print("╚══════════════════════════════════════════╝")
    print()
    print("  (tokens não disponíveis via CLI — sem cobrança extra)")
    print()

# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    _check_clis()

    if len(sys.argv) < 2:
        print("Uso: agente \"<descrição da feature>\"")
        print("Exemplo: agente \"CRUD de tarefas com autenticação JWT\"")
        sys.exit(1)

    idea = " ".join(sys.argv[1:])

    label, agents = show_menu()
    print()
    print(f"  ✅  Modo: {label}")
    print(f"  📋  Agentes: {' → '.join('@' + a for a in agents)}")
    print(f"  💡  Feature: {idea}")

    # Session log no projeto atual
    log_path = Path.cwd() / "production_artifacts" / "session_log.md"
    if not log_path.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_path.write_text(
            f"# Session Log\n\n"
            f"Pipeline iniciado: {timestamp}\n"
            f"Feature: {idea}\n"
            f"Modo: {label}\n\n",
            encoding="utf-8",
        )

    run_log: list[tuple[str, str, str]] = []
    prev_output = ""

    for i, agent in enumerate(agents):
        output, cli_used, model_used = run_agent(agent, idea, prev_output)
        run_log.append((agent, cli_used, model_used))

        show_output_preview(agent, output)
        append_session_log(log_path, agent, cli_used, model_used, output)

        is_last = (i == len(agents) - 1)
        if agent in GATES and not is_last:
            approved = approval_gate(GATES[agent], output)
            if not approved:
                print()
                print("  ❌  Pipeline cancelado pelo usuário.")
                print_summary(run_log)
                sys.exit(0)

        # Próximo agente recebe APENAS o output deste, não o histórico completo
        prev_output = output

    print()
    print("  ✅  Pipeline concluído!")
    print(f"  📁  Session log: {log_path}")
    print_summary(run_log)


if __name__ == "__main__":
    main()
