# Skill: Code Standards

## Objective
Define non-negotiable coding standards that the Full-Stack Engineer MUST read and internalize before writing a single line of code. These standards are stack-aware: apply the relevant sections based on the language/framework in `Technical_Specification.md`.

## Rules of Engagement
- **Mandatory Pre-Coding Read**: The Engineer MUST read this file completely before executing `generate_code.md`.
- **No Exceptions**: Every item below is a blocker in the QA phase if violated.
- **Stack Awareness**: TypeScript/Node rules apply to TS/JS stacks. Python rules apply to Python stacks. Architecture rules are universal.

---

## TypeScript / Node.js Stack

### Strict Mode
- Always enable `"strict": true` in `tsconfig.json`.
- Also enable: `"noUncheckedIndexedAccess": true`, `"exactOptionalPropertyTypes": true`.
- Never use `any`. Use `unknown` and type-narrow, or define explicit interfaces.

### Linting & Formatting
- Project root MUST include `.eslintrc.json` and `.prettierrc`.
- ESLint config must extend: `eslint:recommended`, `plugin:@typescript-eslint/recommended`.
- Prettier defaults: `"semi": true`, `"singleQuote": true`, `"printWidth": 100`, `"trailingComma": "all"`.
- Add lint and format scripts to `package.json`: `"lint": "eslint src --ext .ts"`, `"format": "prettier --write src"`.

### Environment Config
- Create `src/config.ts` that reads all env vars via a single validated object.
- Never use `process.env.VAR_NAME` scattered across the codebase — only inside `config.ts`.
- Validate all required vars at startup using Zod: if a required var is missing, throw and exit.

```typescript
// src/config.ts — required pattern
import { z } from 'zod';

const envSchema = z.object({
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
});

export const config = envSchema.parse(process.env);
```

---

## Python Stack

### Type Hints
- All function signatures MUST include type hints (PEP 484).
- Use `from __future__ import annotations` at the top of every module.
- Run `mypy --strict` as part of the lint step.

### Linting & Formatting
- Project root MUST include `pyproject.toml` with `[tool.ruff]` and `[tool.black]` sections.
- Run `ruff check .` and `black --check .` before any commit.

### Environment Config
- Use a `config.py` module with Pydantic `BaseSettings`.
- Never use `os.environ["VAR"]` scattered inline.

```python
# config.py — required pattern
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    port: int = 8000
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Universal Architecture Rules (All Stacks)

### Naming Conventions
- Functions and variables: `camelCase` (TS/JS) / `snake_case` (Python).
- Classes and interfaces: `PascalCase` in all stacks.
- Constants: `SCREAMING_SNAKE_CASE` in all stacks.
- Files: `kebab-case.ts` or `snake_case.py` — consistent per stack.
- Do not abbreviate names unless universally understood (e.g., `id`, `url`, `dto`).

### Controller → Service → Repository Pattern
Every feature MUST be structured in three layers. No exceptions.

```
Controller  — HTTP only. Parse request, call service, return response. Zero business logic.
Service     — All business logic. No direct DB calls.
Repository  — All DB interactions. No business logic.
```

- Controllers may NOT import repository classes directly.
- Services may NOT import HTTP request/response objects.
- Repositories may NOT contain conditional business rules.

### Input Validation
- TypeScript: Validate all incoming request bodies/params with **Zod** at the controller layer before passing to the service.
- Python: Validate all incoming data with **Pydantic** models. Never pass raw dicts to services.
- Validation failure must return HTTP 422 with the standard error envelope.

### Error Handling
- Centralized error middleware handles all exceptions. Never catch and silently swallow errors.
- Never expose stack traces in responses when `NODE_ENV === 'production'` / `environment === 'production'`.
- All thrown errors must carry a machine-readable `code` string (e.g., `"USER_NOT_FOUND"`).
- Error response shape is always:
  ```json
  { "error": { "code": "MACHINE_READABLE_CODE", "message": "Human readable message" } }
  ```

### Logging
- Use structured logging. Never use bare `console.log` (TS) or `print` (Python) in production paths.
- Every log entry for a request context MUST include: `{ userId, endpoint, method, statusCode, durationMs }`.
- Error log entries MUST include: `{ userId, endpoint, errorCode, stack (dev only) }`.
- Recommended libraries: `pino` (Node.js), `structlog` (Python).

### Database & Query Rules
- Every table/collection needs: `id` (UUID v4), `created_at`, `updated_at`.
- No raw SQL string interpolation — parameterized queries or ORM only.
- Index all foreign key columns and all columns used in `WHERE` or `ORDER BY` clauses.
- **N+1 queries are a hard blocker**: Always use joins, `include`/`select` (Prisma), `joinedload` (SQLAlchemy), or dataloaders.
- Wrap all operations touching more than one table in a transaction.

### Security Baseline
- JWT access token expiry: 15 minutes maximum.
- Refresh token: 7 days, stored in httpOnly cookie only.
- Password hashing: `bcrypt` cost factor 12 minimum, or `argon2id`.
- Rate limiting MUST be applied to all authentication endpoints.
- CORS: configure an explicit `origin` allowlist — never use wildcard `*` in production.

### SOLID Principles Checklist
- **Single Responsibility**: Each class/module does one thing. If you need "and" to describe it, split it.
- **Open/Closed**: Extend behavior via composition/interfaces, not by modifying existing classes.
- **Liskov Substitution**: Subtypes must be substitutable for their base types without breaking callers.
- **Interface Segregation**: Prefer many small, specific interfaces over one large general one.
- **Dependency Inversion**: High-level modules depend on abstractions (interfaces), not concrete implementations. Pass dependencies via constructor injection.
