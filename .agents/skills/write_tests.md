# Skill: Write Tests

## Objective
Your goal as the Full-Stack Engineer is to write a comprehensive test suite and **execute it**, verifying results with real terminal output before handing off to QA.

## Rules of Engagement
- **Spec-Driven**: Every functional requirement (FR-N) in `Technical_Specification.md` must have at least one corresponding test.
- **Save Location**: Save all test files co-located with their modules (e.g., `src/__tests__/`, `tests/`).
- **No Mocking Business Logic**: Mock only external dependencies (databases, third-party APIs). Test real business logic.
- **Coverage Target**: Minimum 80% coverage on service/business logic layers. This must be verified mechanically, not estimated.
- **Real Execution Required**: You MUST run the test suite and paste the raw terminal output into `session_log.md`. Reporting results without executing is a blocker.

---

## Instructions

### Phase 1 — Plan
1. Read `production_artifacts/Technical_Specification.md` and list all functional requirements (FR-N).
2. Read all files in `./src` to understand the structure.
3. Map each FR to: unit tests (service layer) and integration tests (routes/endpoints).

### Phase 2 — Write Unit Tests
- Test every service method in isolation.
- Mock repositories and external APIs via the framework's mock utilities.
- Cover: happy path, edge cases, and expected error conditions for each method.
- Example pattern (Node.js/Jest):
  ```typescript
  // BAD — tests implementation details
  expect(service.method).toHaveBeenCalledWith(x)

  // GOOD — tests inputs and outputs
  const result = await service.createUser({ email: 'a@b.com' })
  expect(result.id).toBeDefined()
  expect(result.email).toBe('a@b.com')
  ```

### Phase 3 — Write Integration Tests
- Test every route/endpoint with realistic inputs.
- Use: `supertest` (Express/Fastify), `pytest` + `httpx` (FastAPI), etc.
- Verify: correct HTTP status codes, response shape matches spec API Contract, error envelope format.

### Phase 4 — Execute and Verify (MANDATORY)

**Step 4.1 — Run with coverage flag:**
- Node.js: `npx jest --coverage --json --outputFile=coverage-report.json`
- Python: `pytest --cov=src --cov-report=json --cov-report=term`

**Step 4.2 — If tests fail:**
- Read the failure output carefully.
- Fix either the test (if it was wrong) or the source code (if the test found a bug).
- Re-run until all tests pass. A failing test suite is a hard blocker — do not proceed to QA.

**Step 4.3 — Parse and verify coverage:**
- Read the coverage output from the terminal or `coverage-report.json`.
- Extract the real coverage % for the `services/` directory (or equivalent business logic layer).
- If coverage is below 80%, write more tests and re-run. Do not round up or estimate.

**Step 4.4 — Paste raw output into session_log:**
After all tests pass, append the following to `production_artifacts/session_log.md`:

```
---
## Engineer — Tests Written | [date YYYY-MM-DD HH:MM]
**Decision**: [X] unit tests, [Y] integration tests. Service coverage: Z% (verified).
**Terminal Output**:
[PASTE THE ACTUAL TEST RUNNER OUTPUT HERE — do not summarize]
**Output**: Test files in [directory]. All passing.
**Next**: QA audit can begin.
---
```

> If you cannot execute the test suite (e.g., missing runtime), this is a blocker. Report it to the user immediately — do NOT fake results.
