#!/usr/bin/env bash
# Instala o comando global `agente` em ~/.agente/
# Uso: bash install.sh

set -e

AGENTE_HOME="$HOME/.agente"
SKILLS_SRC="$(cd "$(dirname "$0")/.agents/skills" && pwd)"
AGENTS_MD="$(cd "$(dirname "$0")/.agents" && pwd)/agents.md"
SCRIPT_SRC="$(cd "$(dirname "$0")" && pwd)/startcycle.py"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   Instalando AGENTE — Pipeline de IA     ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# 1. Criar diretórios
mkdir -p "$AGENTE_HOME/skills"
echo "  ✔  Diretório $AGENTE_HOME criado"

# 2. Copiar skills
cp "$SKILLS_SRC/"*.md "$AGENTE_HOME/skills/"
echo "  ✔  Skills copiados para $AGENTE_HOME/skills/"

# 3. Copiar agents.md
cp "$AGENTS_MD" "$AGENTE_HOME/agents.md"
echo "  ✔  agents.md copiado"

# 4. Copiar startcycle.py (da raiz do repo se existir, senão de ~/.agente se já tiver)
if [ -f "$SCRIPT_SRC" ]; then
  cp "$SCRIPT_SRC" "$AGENTE_HOME/startcycle.py"
  echo "  ✔  startcycle.py copiado"
else
  echo "  ⚠  startcycle.py não encontrado na raiz do repo."
  echo "     Copie manualmente para $AGENTE_HOME/startcycle.py"
fi

# 5. Criar wrapper shell
cat > "$AGENTE_HOME/agente" << 'EOF'
#!/usr/bin/env bash
exec python3 "$HOME/.agente/startcycle.py" "$@"
EOF
chmod +x "$AGENTE_HOME/agente"
echo "  ✔  Comando 'agente' criado em $AGENTE_HOME/agente"

# 6. Criar wrapper .bat (Windows CMD)
cat > "$AGENTE_HOME/agente.bat" << 'EOF'
@echo off
python "%USERPROFILE%\.agente\startcycle.py" %*
EOF
echo "  ✔  agente.bat criado (Windows CMD)"

# 7. Adicionar ao PATH no ~/.bashrc (se ainda não estiver)
BASHRC="$HOME/.bashrc"
if ! grep -q 'agente' "$BASHRC" 2>/dev/null; then
  echo '' >> "$BASHRC"
  echo '# Agente — Autonomous AI Developer Pipeline' >> "$BASHRC"
  echo 'export PATH="$HOME/.agente:$PATH"' >> "$BASHRC"
  echo "  ✔  PATH atualizado em $BASHRC"
else
  echo "  ✔  PATH já configurado em $BASHRC"
fi

# 8. Verificar Claude Code CLI
echo ""
if command -v claude &>/dev/null; then
  echo "  ✔  Claude Code CLI detectado: $(command -v claude)"
else
  echo "  ❌  Claude Code CLI não encontrado."
  echo "     Instale em: https://claude.ai/code"
  echo "     O pipeline não funcionará sem ele."
fi

# 9. Verificar Gemini CLI
echo ""
if command -v gemini &>/dev/null; then
  echo "  ✔  Gemini CLI detectado: $(command -v gemini)"
else
  echo "  ⚠  Gemini CLI não encontrado."
  echo "     Instale em: https://github.com/google-gemini/gemini-cli"
  echo "     Sem ele, QA e DevOps usarão fallback claude-haiku (sem custo extra)."
fi

echo ""
echo "  ✅  Instalação concluída!"
echo ""
echo "  Recarregue o terminal e use:"
echo "    agente \"descrição da feature\""
echo ""
echo "  Ou sem recarregar:"
echo "    source ~/.bashrc && agente \"descrição da feature\""
echo ""
