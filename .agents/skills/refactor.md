# Skill: Refactor

## Objective
Your goal as the Full-Stack Engineer is to perform a critical self-review pass on all generated code immediately after `generate_code.md` and before `write_tests.md`. You are your own harshest reviewer. The goal is to deliver code that would pass a senior engineer's PR review without a single comment.

## Rules of Engagement
- **Read Everything First**: Do not start editing until you have re-read every file you generated.
- **Small Atomic Changes**: Apply one type of improvement at a time (DRY, then naming, then SOLID, etc.).
- **No Scope Creep**: Do not add new features or change business logic. Refactor only.
- **Log All Changes**: Every meaningful change must be logged to `production_artifacts/session_log.md`.

---

## Instructions

### Phase 1 — Full Re-Read
1. Read `production_artifacts/Technical_Specification.md` to recall the intent.
2. Read every file you generated in `./src` (or equivalent source directory).
3. Read `.agents/skills/code_standards.md` again as your review checklist.
4. Make a written list of all issues found before touching any file.

### Phase 2 — DRY Pass
- Identify any logic duplicated across two or more files.
- Extract duplicated logic into shared utility functions, middleware, or base classes.
- Verify that shared utilities are imported, not copy-pasted.
- Common patterns to extract: response formatting helpers, validation schemas, error constructors.

### Phase 3 — SOLID Pass
- **Single Responsibility**: Read each class and function. If its description needs "and", refactor it.
- **Dependency Injection**: Verify that services receive their repositories via constructor parameters, not by instantiating them internally.
- **Interface Segregation**: If an interface or type has methods that not all implementations use, split it.
- No service should be responsible for both business logic AND sending HTTP responses.

### Phase 4 — Consistency Pass
- Verify every error thrown follows the same structure defined in `code_standards.md`.
- Verify every async function has proper error propagation (no swallowed `catch` blocks with empty bodies).
- Verify every log call includes the required context fields.
- Verify `config.ts`/`config.py` is the single source for all env var reads — search for any raw `process.env` or `os.environ` that slipped through.

### Phase 5 — Hygiene Pass
- Remove all unused imports.
- Remove all dead code (commented-out blocks, unreachable branches).
- Verify naming: functions are `camelCase`/`snake_case`, classes are `PascalCase`, constants are `SCREAMING_SNAKE_CASE`.
- Verify file names follow the stack's convention (`kebab-case.ts` / `snake_case.py`).
- Ensure every public function has a JSDoc / docstring comment describing its purpose, params, and return value.

### Phase 6 — Log & Handoff
After all passes are complete, write to `production_artifacts/session_log.md`:

```
---
## Engineer — Refactor Complete | [timestamp]
**Decision**: Refactored [N] files. Key changes: [brief list of what was changed and why].
**Output**: Updated source files in [directory].
**Next**: Code meets code_standards.md. Ready for write_tests.md.
---
```

Notify the pipeline that refactoring is complete and the codebase is ready for test authoring.
