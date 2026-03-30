# Skill: Performance Audit

## Objective
Your goal as the QA Engineer is to perform a dedicated performance analysis of the generated code. This skill runs as a mandatory sub-task within `audit_code.md` (Phase 2B). Performance blockers are treated with the same severity as functional bugs.

## Rules of Engagement
- **Read Before Auditing**: Read `production_artifacts/Technical_Specification.md` first to understand expected data scale.
- **Blockers vs. Warnings**: Items marked [BLOCKER] must be resolved before the pipeline proceeds. Items marked [WARNING] are reported but do not block.
- **No Direct Fixes**: Report findings to the Engineer via `bug_report.md`. Do not edit source files yourself.

---

## Instructions

### Phase 1 — Database & Query Analysis

**[BLOCKER] N+1 Query Detection**
- Search the source code for any loop (`for`, `forEach`, `map`, `while`) that contains a database call, ORM query, or repository method call inside its body.
- Pattern to find: `await repo.findById(item.id)` inside a `for` loop, or `.map(async (item) => await db.query(...))`.
- If found: report the file, line number, and instruct the Engineer to replace with a batched query, join, or `Promise.all` with a single bulk fetch.

**[BLOCKER] Missing Pagination**
- Inspect every API endpoint or service method that returns a list (array) of records.
- Verify that every list endpoint accepts and enforces `page`/`limit` or `cursor`/`limit` parameters.
- An endpoint returning an unbounded list is a blocker.

**[WARNING] Missing Database Indexes**
- Review the database schema or migration files.
- Verify that every foreign key column has a corresponding index.
- Verify that every column appearing in a `WHERE`, `ORDER BY`, or `JOIN ON` clause in the codebase has an index.
- Report missing indexes as warnings with the column name and table.

**[WARNING] Missing Query Projection**
- Check ORM calls for `SELECT *` or equivalent (e.g., Prisma `findMany` without `select`, SQLAlchemy without `.options(load_only(...))`).
- If a query fetches all columns when only 2-3 are used, flag as a warning.

---

### Phase 2 — Async & I/O Analysis

**[BLOCKER] Synchronous Operations on Async Paths**
- Search for any use of synchronous file I/O (`fs.readFileSync`, `fs.writeFileSync`) outside of application startup/config loading.
- Search for any `execSync` or `spawnSync` in request handlers.
- All I/O inside request handlers must be async.

**[WARNING] Missing `Promise.all` for Independent Async Operations**
- Look for multiple sequential `await` calls in the same function where the operations are independent.
  ```typescript
  // BAD — sequential when they could be parallel
  const user = await userRepo.findById(id);
  const settings = await settingsRepo.findByUserId(id);

  // GOOD
  const [user, settings] = await Promise.all([
    userRepo.findById(id),
    settingsRepo.findByUserId(id),
  ]);
  ```
- Flag as a warning when 2+ independent awaits appear in sequence.

---

### Phase 3 — Payload & Response Analysis

**[WARNING] Large Payload Responses**
- Inspect API responses that return nested or deeply populated objects.
- If a response includes fields the spec does not require the client to receive (e.g., password hash, internal metadata), flag it.
- Recommend adding explicit `select`/projection or a DTO transformation layer.

**[WARNING] Missing Response Compression**
- Check if the server has response compression middleware configured (e.g., `compression` for Express, `GZipMiddleware` for FastAPI).
- Flag as a warning if absent.

---

### Phase 4 — Frontend Performance (skip if API-only)

**[WARNING] Unnecessary Re-renders (React/Next.js)**
- Search for components receiving object or array props created inline (e.g., `<Component data={{ key: value }} />`).
- Search for event handlers defined inline inside render (e.g., `onClick={() => handler()}`).
- Verify that expensive computations inside components use `useMemo`.
- Verify that stable function references use `useCallback`.

**[WARNING] Unoptimized Images**
- If using Next.js, verify `<Image>` from `next/image` is used instead of bare `<img>` tags.
- Check that images have explicit `width` and `height` props.

---

### Phase 5 — Memory Leak Analysis

**[BLOCKER] Unclosed Connections**
- Search for database connection pool initialization that lacks a graceful shutdown handler.
- Verify that `SIGTERM` and `SIGINT` handlers close DB connections and HTTP server.
- Check Redis/queue clients for `.disconnect()` or `.quit()` in shutdown paths.

**[WARNING] Missing useEffect Cleanup (React)**
- Search for `useEffect` hooks that set up subscriptions, intervals, or event listeners.
- Verify each has a return cleanup function that removes the subscription/clears the interval.

---

### Phase 6 — Report
Append all findings to `production_artifacts/bug_report.md` under a new section:

```
## Performance Audit — [timestamp]
### Blockers
- [ ] PERF-1: [file:line] — [description] [BLOCKER]

### Warnings
- [ ] PERF-W1: [file] — [description] [WARNING]

### Summary
X performance blockers, Y performance warnings.
```

Notify the Engineer of any blockers and wait for fixes before re-auditing.
