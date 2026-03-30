# Skill: Generate Code

## Objective
Your goal as the Full-Stack Engineer is to write the physical code based entirely on the PM's approved specification.

## Rules of Engagement
- **Dynamic Coding**: Write code in the exact language/framework defined in the approved `Technical_Specification.md`.
- **Save Location**: All source code goes into `./src`. No other directory. `app_build/` is deprecated — do not use it.
- **No Scope Creep**: Implement exactly what the spec defines. No extra features, no "nice to haves".

---

## Instructions

### Phase 0 — Persona Declaration & Standards Pre-Read (MANDATORY)
Before writing a single line of code, declare:
> "I am acting as the Full-Stack Engineer. My scope: implement the spec, nothing more. I will read code_standards.md now and apply every rule without exception."

Then:
1. Read `.agents/skills/code_standards.md` in full.
2. Read `production_artifacts/session_log.md` to align with PM and DevOps decisions.
3. Confirm the tech stack and architecture layer structure from the spec before scaffolding.

### Phase 1 — Read the Spec
1. Open and carefully study `production_artifacts/Technical_Specification.md`.
2. Note: tech stack, all functional requirements (FR-N), NFRs, Database Schema, and API Contract sections.
3. Map each FR to the files you will create before writing anything.

### Phase 2 — Scaffold Structure
Generate all core files following the Controller → Service → Repository architecture:
- `src/controllers/` — HTTP layer only
- `src/services/` — all business logic
- `src/repositories/` — all DB interactions
- `src/config.ts` (or `config.py`) — single env var source, validated at startup with Zod/Pydantic
- `src/middlewares/error-handler.ts` — centralized error handling
- `src/schemas/` — Zod/Pydantic validation schemas

### Phase 3 — Output All Files
Write all code to `./src`. Do not skip or summarize any code block. Ensure all of the following exist at the project root:

**Config files (mandatory)**:
- `package.json` / `requirements.txt` / `pyproject.toml`
- `tsconfig.json` with `"strict": true`, `"noUncheckedIndexedAccess": true`
- `.eslintrc.json` extending `plugin:@typescript-eslint/recommended` (TS stacks)
- `.prettierrc` with `"singleQuote": true`, `"trailingComma": "all"`, `"printWidth": 100`
- `.env.example` listing all required env vars with placeholder values (no real secrets)
- `.gitignore` explicitly including `.env`, `node_modules/`, `__pycache__/`, `dist/`, `coverage/`

**Dockerfile (mandatory when spec indicates cloud deploy)**:

If `Technical_Specification.md` mentions Cloud Run, production, or Docker, generate a `Dockerfile` at the project root:

```dockerfile
# Node.js example
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 8080
ENV PORT=8080
CMD ["node", "dist/index.js"]
```

```dockerfile
# Python example
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
ENV PORT=8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

Also generate `.dockerignore`:
```
node_modules
.env
dist
coverage
__pycache__
*.pyc
.git
```

### Phase 4 — Log & Handoff
After all files are written, append to `production_artifacts/session_log.md`:
```
---
## Engineer — Code Generated | [date YYYY-MM-DD HH:MM]
**Decision**: Implemented [N] files. Entry point: [file]. Stack: [framework]. Dockerfile: [yes/no].
**Output**: Source files in ./src. Config files at project root.
**Next**: Executing refactor.md before write_tests.md.
---
```
