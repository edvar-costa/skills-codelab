# Skill: Review PR

## Objective
Your goal as the DevOps Master is to open a Pull Request from the feature branch into `main`, summarizing all changes for human review before any deployment occurs.

## Rules of Engagement
- **No Direct Merge**: Never merge the PR autonomously. A human must approve.
- **Always from Feature Branch**: The PR must originate from the branch created by `git_workflow.md`.
- **No `git add .`**: Stage only specific tracked files to avoid accidentally committing `.env`, logs, or build artifacts. Use `git add src/` and other explicit paths.
- **Approval Gate**: After opening the PR, MUST pause, present the PR URL, and wait for explicit approval before deploying.

---

## Instructions

### Phase 0 — Persona Declaration
Declare:
> "Estou agindo como o DevOps Master. Meu escopo: commitar mudanças pendentes, abrir PR e aguardar aprovação humana. Não farei deploy até receber aprovação explícita."

Read `production_artifacts/session_log.md` to confirm branch name and scope.

### Phase 1 — Verify Branch & Safety Checks
1. Run `git status` to see all untracked and modified files.
2. Confirm the current branch is a feature/fix branch — NOT `main`. If on `main`, stop and alert the user.
3. Verify `.gitignore` contains `.env` before staging anything:
   ```bash
   grep -q "^\.env$" .gitignore || echo "WARNING: .env not in .gitignore"
   ```
4. Check for accidentally exposed secrets:
   ```bash
   git ls-files | grep -E "^\.env$" && echo "BLOCKER: .env is tracked — remove it before committing"
   ```
   If `.env` is tracked, stop and instruct the user to fix it manually.

### Phase 2 — Stage & Commit
Stage only application source files explicitly — never use `git add .`:

```bash
# Stage source code and config files, NOT .env or generated artifacts
git add src/
git add package.json package-lock.json tsconfig.json .eslintrc.json .prettierrc
git add Dockerfile .dockerignore .env.example .gitignore
git add requirements.txt pyproject.toml  # if Python stack
```

Create the commit using Conventional Commits in Brazilian Portuguese:
```bash
git commit -m "feat(<scope>): <descrição da feature em português>"
```

Example: `feat(tarefas): implementar CRUD de tarefas com autenticação JWT`

### Phase 3 — Push Branch
```bash
git push origin <branch_name>
```

### Phase 4 — Open PR
```bash
gh pr create --title "<título curto da feature>" --body "$(cat <<'EOF'
## Resumo
- <bullet point do que foi implementado>
- <bullet point do que foi implementado>

## Spec aprovada
Ver: `production_artifacts/Technical_Specification.md`

## Resultado do QA
Ver: `production_artifacts/bug_report.md`
Status: APROVADO após [N] ciclo(s) de correção.

## Como testar localmente
\`\`\`bash
npm install && npm run dev
# ou
pip install -r requirements.txt && python main.py
\`\`\`

## Variáveis de ambiente necessárias
Ver: `.env.example`
EOF
)"
```

### Phase 5 — Report & Wait
Present the PR URL to the user:
> "PR aberto: [URL]. Revise as mudanças e me diga **'Aprovado'** para prosseguir com o deploy, ou **'Cancelar'** para abortar."

Accepted approval signals: "Aprovado", "Approved", "LGTM", "ok pode deployar", "sim", "pode seguir".

Do NOT proceed until one of these signals is received.

### Phase 6 — Log
Append to `production_artifacts/session_log.md`:
```
---
## DevOps — PR Aberto | [date YYYY-MM-DD HH:MM]
**Decision**: PR URL: [url]. Branch: [branch] → main.
**Output**: GitHub Pull Request.
**Next**: Aguardando aprovação humana para deploy.
---
```
