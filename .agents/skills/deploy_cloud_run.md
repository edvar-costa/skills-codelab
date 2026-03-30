# Skill: Deploy to Cloud Run

## Objective
Your goal as DevOps is to package the application into a container and deploy it to Google Cloud Run with proper environment variable configuration.

## Rules of Engagement
- **Env Vars are Mandatory**: Never deploy without configuring all required environment variables. A deploy without env vars will crash immediately.
- **Public Access is Conditional**: Allow unauthenticated access only for public-facing web apps. For internal APIs, require authentication (`--no-allow-unauthenticated`).
- **Verify Before Reporting**: Always run a health check on the returned URL before reporting success to the user.

---

## Instructions

### Phase 1 — Pre-Deploy Verification
1. Confirm `Dockerfile` and `.dockerignore` exist at the project root. If missing, stop and instruct the Engineer to generate them via `generate_code.md` Phase 3.
2. Read `production_artifacts/Technical_Specification.md` to identify:
   - All required environment variables (from the NFR / Database Schema sections)
   - Whether the app is public-facing or internal
3. Read `.env.example` to get the full list of required env vars.
4. Verify `gcloud` is authenticated: run `gcloud auth list`. If not authenticated, instruct the user to run `gcloud auth login` and wait.

### Phase 2 — Configure Environment Variables
Before deploying, set all required env vars using Secret Manager or inline flags.

**Option A — Using GCP Secret Manager (recommended for production secrets)**:
```bash
# Create secrets for sensitive values
echo -n "your-db-url" | gcloud secrets create DATABASE_URL --data-file=-
echo -n "your-jwt-secret" | gcloud secrets create JWT_SECRET --data-file=-

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding DATABASE_URL \
  --member="serviceAccount:[PROJECT-NUMBER]-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

**Option B — Inline env vars (acceptable for non-sensitive config)**:
```bash
gcloud run deploy [SERVICE_NAME] --source . \
  --set-env-vars="NODE_ENV=production,PORT=8080" \
  --set-secrets="DATABASE_URL=DATABASE_URL:latest,JWT_SECRET=JWT_SECRET:latest"
```

Ask the user: "Para os valores reais das variáveis de ambiente (DATABASE_URL, JWT_SECRET, etc.), você prefere usar GCP Secret Manager (recomendado) ou fornecer os valores agora para eu configurar inline?"

Wait for the user's response before proceeding.

### Phase 3 — Deploy
Navigate to the project root and run:

```bash
gcloud run deploy [SERVICE_NAME] \
  --source . \
  --region=us-central1 \
  --port=8080 \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10 \
  [--allow-unauthenticated | --no-allow-unauthenticated]
```

- Set `[SERVICE_NAME]` from the spec's Executive Summary (kebab-case).
- Set `--allow-unauthenticated` only if the spec indicates a public web app. Otherwise use `--no-allow-unauthenticated`.
- If prompted for region, select `us-central1` (or the region specified in the spec).

### Phase 4 — Post-Deploy Health Check
After receiving the Cloud Run URL:
1. Run `curl -s -o /dev/null -w "%{http_code}" [CLOUD_RUN_URL]/health` (or the health endpoint defined in the spec).
2. If the response is `200`: the deploy is healthy.
3. If the response is `500` or connection refused: the app crashed — immediately execute `rollback.md`.

### Phase 5 — Report
Output to the user:
```
Deploy concluído!
URL: [CLOUD_RUN_URL]
Health check: [200 OK | FAILED]
Região: [region]
Instâncias: min=0, max=10
```

Update `production_artifacts/session_log.md`:
```
---
## DevOps — Cloud Run Deploy | [date YYYY-MM-DD HH:MM]
**Decision**: Deployed to Cloud Run. Region: [region]. Public: [yes/no].
**Output**: [CLOUD_RUN_URL]
**Next**: Pipeline complete. Monitor via GCP Console.
---
```
