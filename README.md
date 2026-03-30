# Autonomous AI Developer Pipeline

Pipeline autônomo de desenvolvimento de software usando agentes de IA. Um único comando transforma uma ideia em aplicação deployada, passando por spec, código, refatoração, testes, auditoria de qualidade/performance/segurança e deploy — com gates de aprovação humana em pontos críticos.

---

## Compatibilidade de IDEs

Este pipeline foi projetado para funcionar em dois ambientes:

| IDE | Como o `/startcycle` funciona | Configuração necessária |
|---|---|---|
| **Antigravity IDE** | Lê `.agents/workflows/startcycle.md` nativamente | Nenhuma — funciona ao abrir o projeto |
| **Claude Code** | Lê `.claude/commands/startcycle.md` como slash command | Nenhuma — arquivo já incluído no projeto |

> **Ambos os arquivos estão sincronizados e contêm o mesmo pipeline.** Não é necessário nenhum passo manual independente do IDE usado.

### Adicionando novos workflows

| IDE | Onde criar o arquivo |
|---|---|
| Antigravity | `.agents/workflows/<nome>.md` |
| Claude Code | `.claude/commands/<nome>.md` |

Se quiser que um novo workflow funcione nos dois, crie nos dois diretórios.

---

## Pré-requisitos

| Ferramenta | Versão | Uso |
|---|---|---|
| [Antigravity IDE](https://antigravity.dev) ou Claude Code | — | Executa o pipeline |
| Node.js | v18+ | Stacks JavaScript/TypeScript |
| Python | 3.10+ | Stacks Python |
| Git | — | Controle de versão |
| [GitHub CLI (`gh`)](https://cli.github.com) | — | Abertura automática de PRs |
| gcloud CLI | — | Deploy no Cloud Run (opcional) |

---

## Estrutura do Projeto

```
skills-codelab/
├── .agents/                        # Configuração para Antigravity IDE
│   ├── agents.md                   # Definição das personas do time
│   ├── skills/                     # Capacidades individuais de cada agente
│   │   ├── code_standards.md       # Padrões obrigatórios de código
│   │   ├── write_specs.md          # PM cria especificação técnica
│   │   ├── generate_code.md        # Engineer gera o código
│   │   ├── refactor.md             # Engineer auto-revisa o código
│   │   ├── write_tests.md          # Engineer escreve testes
│   │   ├── audit_code.md           # QA audita funcionalidade
│   │   ├── performance_audit.md    # QA audita performance
│   │   ├── security_scan.md        # QA audita segurança (OWASP)
│   │   ├── git_workflow.md         # DevOps gerencia branches
│   │   ├── review_pr.md            # DevOps abre Pull Request
│   │   ├── deploy_app.md           # DevOps faz deploy local
│   │   ├── deploy_cloud_run.md     # DevOps faz deploy no Cloud Run
│   │   ├── rollback.md             # DevOps reverte em caso de falha
│   │   └── session_log.md          # Formato do log entre agentes
│   └── workflows/
│       └── startcycle.md           # Orquestrador (Antigravity)
├── .claude/                        # Configuração para Claude Code
│   └── commands/
│       └── startcycle.md           # Orquestrador (Claude Code) — mesmo pipeline
├── production_artifacts/           # Artefatos gerados pelo pipeline
│   ├── Technical_Specification.md
│   ├── bug_report.md
│   └── session_log.md
└── app_build/                      # Código gerado (destino legado)
```

---

## Como Usar

### Comando principal

```
/startcycle "<sua ideia>"
```

**Exemplos:**
```
/startcycle "API REST de gerenciamento de tarefas com autenticação JWT"
/startcycle "Sistema de chat em tempo real para suporte ao cliente"
/startcycle "Dashboard de métricas com gráficos e filtros por período"
```

---

## Fluxo do Pipeline

```
/startcycle "<ideia>"
      │
      ▼
┌─────────────────────────────────────────┐
│  STEP 1 — Especificação                 │
│  @pm → write_specs.md                   │
│  Gera: Technical_Specification.md       │
│  Inclui: FRs, NFRs, schema, API contract│
└──────────────┬──────────────────────────┘
               │
        GATE 1: Você aprova a spec?
        (pode editar o arquivo com comentários)
               │
               ▼
┌─────────────────────────────────────────┐
│  STEP 2 — Git Setup                     │
│  @devops → git_workflow.md              │
│  Cria branch: feat/<nome-da-feature>    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  STEP 3 — Implementação                 │
│  @engineer → code_standards.md (leitura)│
│  @engineer → generate_code.md           │
│  Gera: src/ com controllers, services,  │
│  repositories, config, middlewares      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  STEP 3.5 — Refatoração                 │
│  @engineer → refactor.md               │
│  DRY, SOLID, naming, hygiene, JSDoc     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  STEP 4 — Testes                        │
│  @engineer → write_tests.md             │
│  Unit tests + Integration tests (80%+)  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  STEP 5 — Auditoria QA                  │
│  @qa → audit_code.md                   │
│    ├─ Alinhamento com spec              │
│    ├─ Bug hunting funcional             │
│    ├─ [2B] performance_audit.md         │
│    │    N+1, paginação, async, leaks    │
│    └─ [2C] security_scan.md            │
│         OWASP, CVEs, JWT, secrets       │
│                                         │
│  Se blocker → Engineer corrige → loop   │
│  Gera: bug_report.md                   │
└──────────────┬──────────────────────────┘
               │
        GATE 2: Você aprova o deploy?
               │
               ▼
┌─────────────────────────────────────────┐
│  STEP 6 — Pull Request                  │
│  @devops → review_pr.md                 │
│  Abre PR: feat/<branch> → main          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  STEP 7 — Deploy                        │
│  @devops → deploy_app.md               │
│  Se falhar → rollback.md               │
│  Reporta: URL final                     │
└─────────────────────────────────────────┘
```

---

## O Time de Agentes

### @pm — Product Manager
Transforma ideias vagas em especificações técnicas rigorosas. Nunca escreve código. Sempre aguarda aprovação antes de seguir.

### @engineer — Full-Stack Engineer
Implementa o código seguindo a spec aprovada e os padrões em `code_standards.md`. Responde a bug reports do QA e corrige todos os blockers reportados.

### @qa — QA Engineer
Audita o código sem corrigir diretamente. Gera `bug_report.md` com blockers e warnings. Executa auditoria funcional, de performance e de segurança. Só aprova quando zero blockers em todas as categorias.

### @devops — DevOps Master
Gerencia Git, abre PRs, faz deploy local ou no Cloud Run, e executa rollback automático em caso de falha.

---

## Gates de Aprovação Humana

O pipeline possui **2 pontos onde você precisa agir**:

| Gate | Momento | O que fazer |
|---|---|---|
| Gate 1 | Após a spec ser gerada | Revisar `production_artifacts/Technical_Specification.md`. Digitar "Aprovado" ou adicionar comentários no arquivo para revisão |
| Gate 2 | Após a auditoria QA | Revisar o PR aberto. Digitar "Aprovado" ou "LGTM" para iniciar o deploy |

---

## Padrões de Código Aplicados

O `code_standards.md` garante que todo código gerado siga:

- **TypeScript**: `strict: true`, sem `any`, Zod para validação
- **Python**: type hints obrigatórios, Pydantic para validação, mypy strict
- **Arquitetura**: Controller → Service → Repository (sem cruzamento de camadas)
- **Config**: único arquivo `config.ts`/`config.py` com validação na startup
- **Erros**: middleware centralizado, envelope padrão `{ error: { code, message } }`
- **Logging**: estruturado com contexto `{ userId, endpoint, statusCode, durationMs }`
- **Database**: UUID + timestamps, queries parametrizadas, indexes, sem N+1
- **Auth**: JWT 15min, refresh httpOnly, bcrypt cost≥12, rate limiting
- **Nomenclatura**: `camelCase` funções, `PascalCase` classes, `SCREAMING_SNAKE` constantes

---

## Auditoria de Performance (Automática)

O QA verifica automaticamente:

| Check | Severidade |
|---|---|
| N+1 queries (query dentro de loop) | BLOCKER |
| Endpoints de lista sem paginação | BLOCKER |
| I/O síncrono em handlers de request | BLOCKER |
| Conexões DB sem graceful shutdown | BLOCKER |
| `await` sequenciais que poderiam ser `Promise.all` | WARNING |
| Indexes faltando em colunas de query | WARNING |
| SELECT * quando apenas poucos campos são usados | WARNING |
| Ausência de compressão de resposta | WARNING |

---

## Auditoria de Segurança (Automática)

O QA executa `npm audit`/`pip-audit` e verifica OWASP Top 10:

| Check | Severidade |
|---|---|
| CVEs HIGH/CRITICAL nas dependências | BLOCKER |
| Rotas sem auth middleware (broken access control) | BLOCKER |
| SQL injection / interpolação de string em query | BLOCKER |
| JWT com algo `none` ou expiry > 15min | BLOCKER |
| Secrets hardcoded no código | BLOCKER |
| Endpoints de auth sem rate limiting | BLOCKER |
| CORS com wildcard `*` | WARNING |
| Headers de segurança ausentes (helmet) | WARNING |
| Stack trace exposto em produção | WARNING |

---

## Artefatos Gerados

Após o pipeline, `production_artifacts/` contém:

| Arquivo | Conteúdo |
|---|---|
| `Technical_Specification.md` | Spec completa aprovada pelo PM e por você |
| `bug_report.md` | Relatório completo da auditoria (funcional + performance + segurança) |
| `session_log.md` | Log de decisões de todos os agentes, com timestamps e handoffs |

---

## Deploy no Cloud Run (Opcional)

Para fazer deploy na nuvem ao invés de local, após o Gate 2 instrua o DevOps:

```
use deploy_cloud_run.md instead of deploy_app.md
```

O agente executará `gcloud run deploy --source .` e retornará a URL pública.

**Requisito:** `gcloud` CLI instalado e autenticado com `gcloud auth login`.

---

## Rollback Manual

Se precisar reverter após um deploy com problema:

```
execute rollback.md
```

O DevOps irá:
1. Listar os últimos commits com `git log --oneline -10`
2. Apresentar o plano de rollback para sua confirmação
3. Executar `git revert` (mantém histórico) e re-deployar

---

## Troubleshooting

**Pipeline parou sem motivo aparente**
Verifique `production_artifacts/session_log.md` — o último agente logou o motivo da parada.

**QA em loop infinito de correções**
Abra `production_artifacts/bug_report.md` e leia os blockers. Você pode orientar o Engineer diretamente: "corrija apenas o item #3, os outros são aceitáveis".

**Deploy falhou**
O rollback é executado automaticamente. Verifique o log do terminal e o `session_log.md` para o motivo.

**Spec gerada não reflete o que eu queria**
Abra `production_artifacts/Technical_Specification.md`, adicione comentários em português diretamente no arquivo, e diga ao PM: "revise com base nos comentários". O loop de revisão é automático.
