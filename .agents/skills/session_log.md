# Skill: Session Log

## Objective
Maintain a running log of all decisions and handoffs during a `/startcycle` execution. Every agent reads it at the start and writes to it at the end of their phase.

## Rules of Engagement
- **Append Only**: Never overwrite previous entries — always append below the last entry.
- **Every Agent Writes**: Each persona MUST write to this log at the end of their phase.
- **Read Before Acting**: Every persona MUST read this log at the start of their phase to align with prior decisions.
- **Save Location**: Always at `production_artifacts/session_log.md`.
- **Re-runs**: If `/startcycle` is run again, do NOT overwrite this file. Append a separator `---` and a new pipeline start marker.

## Timestamps
Use the format `YYYY-MM-DD HH:MM` (e.g., `2026-03-30 14:35`). Obtain the current date/time from the system or environment if available. If not available, write `[datetime unavailable]` — never invent a timestamp.

## Source Directory Convention
All generated application code lives in `./src`. References to `app_build/` are deprecated and should be ignored.

---

## Log Format

Each entry:
```
---
## [Persona] — [Phase] | [YYYY-MM-DD HH:MM]
**Decision**: <key decision made>
**Output**: <artifact produced>
**Next**: <what the next agent must know or do>
---
```

---

## Templates Per Agent

### @pm — after write_specs
```
---
## PM — Spec Aprovada | [YYYY-MM-DD HH:MM]
**Decision**: Tech stack: [framework]. Arquitetura: [descrição]. Cloud deploy: [sim/não].
**Output**: production_artifacts/Technical_Specification.md
**Next**: Engineer deve usar [framework]. Estrutura de API definida na seção API Contract da spec.
---
```

### @devops — after git_workflow
```
---
## DevOps — Branch Criada | [YYYY-MM-DD HH:MM]
**Decision**: Branch: [branch_name]. Base: main.
**Output**: Branch pronta para implementação.
**Next**: Engineer trabalha na branch [branch_name]. NÃO tocar em main.
---
```

### @engineer — after generate_code
```
---
## Engineer — Código Gerado | [YYYY-MM-DD HH:MM]
**Decision**: [N] arquivos gerados. Entry point: [file]. Stack: [framework]. Dockerfile: [sim/não].
**Output**: Arquivos em ./src. Configs na raiz do projeto.
**Next**: Executando refactor.md antes de write_tests.md.
---
```

### @engineer — after refactor
```
---
## Engineer — Refactor Concluído | [YYYY-MM-DD HH:MM]
**Decision**: [N] arquivos refatorados. Principais mudanças: [lista breve].
**Output**: Arquivos atualizados em ./src.
**Next**: Código atende code_standards.md. Pronto para write_tests.md.
---
```

### @engineer — after write_tests
```
---
## Engineer — Testes Escritos | [YYYY-MM-DD HH:MM]
**Decision**: [X] testes unitários, [Y] testes de integração. Cobertura real: Z% (verificada).
**Terminal Output**: [COLAR OUTPUT BRUTO DO TEST RUNNER AQUI]
**Output**: Arquivos de teste em [diretório]. Todos passando.
**Next**: Auditoria QA pode começar.
---
```

### @qa — after audit_code (functional + performance + security)
```
---
## QA — Auditoria Concluída | [YYYY-MM-DD HH:MM]
**Decision**: Status: APROVADO | PROBLEMAS ENCONTRADOS | ESCALADO (3 ciclos)
**Output**: production_artifacts/bug_report.md (seções: funcional + performance + segurança)
**Ciclos**: [N] ciclos de correção com o Engineer.
**Next**: [Se aprovado] DevOps pode abrir PR. [Se problemas] Engineer deve corrigir blockers do bug_report.md. [Se escalado] Aguardando decisão do usuário.
---
```

### @devops — after review_pr
```
---
## DevOps — PR Aberto | [YYYY-MM-DD HH:MM]
**Decision**: PR URL: [url]. Branch: [branch] → main.
**Output**: GitHub Pull Request.
**Next**: Aguardando aprovação humana para deploy.
---
```

### @devops — after deploy
```
---
## DevOps — Deploy Concluído | [YYYY-MM-DD HH:MM]
**Decision**: Stack: [framework]. Destino: [local|cloud-run]. Health check: [OK|FALHOU].
**Output**: [localhost URL ou Cloud Run URL]
**Next**: Pipeline completo. Monitorar via logs/GCP Console.
---
```

### @devops — after rollback
```
---
## DevOps — Rollback | [YYYY-MM-DD HH:MM]
**Decision**: Revertido de [bad_hash] para [stable_hash]. Destino: [local|cloud-run].
**Motivo**: [descrição do erro].
**Output**: Aplicação restaurada em [URL].
**Next**: Investigar causa raiz antes de re-deployar.
---
```
