---
description: Start the Autonomous AI Developer Pipeline sequence with a new idea
---

When the user types `/startcycle <idea>`, orchestrate the full development lifecycle strictly using `.agents/agents.md` and `.agents/skills/`.

Before starting, initialize `production_artifacts/session_log.md` as an empty file.

---

### Execution Sequence:

---

**Step 1 — Specification (Gate 1: Human Approval)**

Declare:
> "Estou agindo como o Product Manager. Meu escopo: criar a especificação técnica e aguardar aprovação. Não escreverei código nem criarei branches."

- Execute the `write_specs.md` skill using `<idea>`.
- *(Loop until the user explicitly approves. Accepted signals: "Aprovado", "Approved", "LGTM", "ok", "sim", "pode seguir", "pode continuar". If the user adds comments to `Technical_Specification.md`, re-read and revise — do NOT advance until approval is received.)*
- After approval, append the PM entry to `session_log.md` per `session_log.md` format.

---

**Step 2 — Git Setup**

Declare:
> "Estou agindo como o DevOps Master. Meu escopo: criar a branch de feature. Não escreverei código nem abrirei PRs ainda."

- Execute the `git_workflow.md` skill to create a feature branch based on the spec's feature name.
- Append the DevOps branch entry to `session_log.md`.

---

**Step 3 — Implementation**

Declare:
> "Estou agindo como o Full-Stack Engineer. Meu escopo: ler code_standards.md e gerar o código da spec. Não criarei branches nem abrirei PRs."

- Read `.agents/skills/code_standards.md` completely (also required inside `generate_code.md` Phase 0).
- Execute the `generate_code.md` skill. All code goes into `./src`. Do NOT use `app_build/`.
- Append the Engineer code entry to `session_log.md`.

---

**Step 3.5 — Refactor (Mandatory)**

*(Continuing as Full-Stack Engineer — no persona switch)*

- Execute the `refactor.md` skill. Do NOT skip this step.
- Append the Engineer refactor entry to `session_log.md`.

---

**Step 4 — Tests**

*(Continuing as Full-Stack Engineer — no persona switch)*

- Execute the `write_tests.md` skill.
- Tests MUST be executed in the terminal. Paste the raw output into `session_log.md`. Do not report results without running them.
- Append the Engineer tests entry to `session_log.md`.

---

**Step 5 — QA Audit (Max 3 cycles)**

Declare:
> "Estou agindo como o QA Engineer. Meu escopo: auditar o código, gerar bug_report.md e delegar correções. Não editarei arquivos de código. Máximo 3 ciclos de correção."

- Execute the `audit_code.md` skill, including mandatory sub-tasks:
  - Phase 2B: `performance_audit.md`
  - Phase 2C: `security_scan.md`
- *(If blockers found AND cycle < 3: notify Engineer, wait for fixes, re-audit all phases.)*
- *(If cycle = 3 and blockers remain: escalate to user — do NOT loop further.)*
- Append the QA entry to `session_log.md`.

---

**Step 6 — PR Review (Gate 2: Human Approval)**

Declare:
> "Estou agindo como o DevOps Master. Meu escopo: verificar segurança do staging, commitar arquivos específicos e abrir o PR. Não farei merge nem deploy sem aprovação explícita."

- Execute the `review_pr.md` skill.
- *(Wait for explicit approval. Accepted signals: "Aprovado", "Approved", "LGTM", "ok pode deployar", "sim", "pode seguir". Do NOT deploy on ambiguous responses.)*
- Append the DevOps PR entry to `session_log.md`.

---

**Step 7 — Deploy**

*(Continuing as DevOps Master — no persona switch)*

- Execute `deploy_app.md` (local) or `deploy_cloud_run.md` (cloud), based on what the spec's NFR section specifies.
- If deployment fails: immediately execute `rollback.md` matching the deploy target (local or Cloud Run).
- Append the DevOps deploy entry to `session_log.md`.
- Report the final URL to the user and declare the pipeline complete.

---

### On Failure at Any Step:
- Stop immediately.
- Append a failure entry to `session_log.md` with the step name and error.
- Report to the user in Portuguese what failed and the available options: retry, rollback, or manual fix.
