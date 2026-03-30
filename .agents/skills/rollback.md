# Skill: Rollback

## Objective
Your goal as the DevOps Master is to safely revert the application to the last known stable state when a deployment fails or a critical issue is detected.

## Rules of Engagement
- **Never Delete History**: Use `git revert`, never `git reset --hard` on shared branches.
- **Confirm Before Acting**: Always present the rollback plan to the user and wait for confirmation.
- **Match the Deploy Target**: Local deploy → revert and restart locally. Cloud Run deploy → revert and re-deploy to Cloud Run.
- **Log Everything**: Every rollback action must be recorded in `production_artifacts/session_log.md`.

---

## Instructions

### Phase 1 — Diagnose
1. Identify the failure: read terminal output, error logs, or user description.
2. Determine the last stable commit:
   ```bash
   git log --oneline -10
   ```
3. Identify the commit hash before the failed change.
4. Present the plan to the user:
   ```
   Plano de rollback:
   - Atual (quebrado): <hash> — <mensagem>
   - Alvo (estável):  <hash> — <mensagem>
   Confirma o rollback? (sim/não)
   ```
5. Wait for explicit confirmation before proceeding.

---

### Phase 2A — Rollback: Local Deploy

Use when the original deploy was done via `deploy_app.md`.

**Revert the commit(s):**
```bash
# Revert only the last commit
git revert HEAD --no-edit

# Or revert a range back to a specific stable commit
git revert <bad_commit>..HEAD --no-edit

git push origin <branch_name>
```

**Restore and verify:**
1. Stop the currently running local server (kill the process on the port).
2. Re-run install + start from `deploy_app.md`:
   ```bash
   cd <project_root>
   npm install && npm run dev
   # or: pip install -r requirements.txt && python main.py
   ```
3. Confirm the app is responding on localhost.

---

### Phase 2B — Rollback: Cloud Run Deploy

Use when the original deploy was done via `deploy_cloud_run.md`.

**Revert the commit(s):**
```bash
git revert HEAD --no-edit
git push origin <branch_name>
```

**Re-deploy the reverted code to Cloud Run:**
```bash
gcloud run deploy [SERVICE_NAME] \
  --source . \
  --region=us-central1
```

> This re-deploys using the reverted source. Cloud Run will build a new revision from the stable code and route traffic to it automatically.

**Verify:**
```bash
curl -s -o /dev/null -w "%{http_code}" [CLOUD_RUN_URL]/health
```
Expected: `200`. If still failing, escalate to the user.

---

### Phase 3 — Report
Report to the user:
> "Rollback concluído. Aplicação restaurada ao estado estável.
> URL: [localhost or Cloud Run URL]
> Commit revertido: [bad_hash] → [stable_hash]"

### Phase 4 — Log
Append to `production_artifacts/session_log.md`:
```
---
## DevOps — Rollback | [date YYYY-MM-DD HH:MM]
**Decision**: Revertido de [bad_hash] para [stable_hash]. Deploy target: [local|cloud-run].
**Motivo**: [descrição do erro].
**Output**: Aplicação restaurada em [URL].
**Next**: Investigar causa raiz antes de re-deployar.
---
```
