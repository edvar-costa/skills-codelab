# Skill: Security Scan

## Objective
Your goal as the QA Engineer is to perform a dedicated security audit on the generated application. This skill runs as a mandatory sub-task within `audit_code.md` (Phase 2C). Any OWASP Top 10 violation or critical vulnerability is an automatic blocker.

## Rules of Engagement
- **Run Before Reporting**: Execute all automated scan commands before writing the report.
- **Blockers are Non-Negotiable**: Security blockers must be resolved before any PR is opened.
- **No Direct Fixes**: Report all findings in `bug_report.md`. Delegate fixes to the Engineer.

---

## Instructions

### Phase 1 — Dependency Vulnerability Scan

**[BLOCKER if HIGH/CRITICAL] Dependency Audit**
- For Node.js projects: run `npm audit --audit-level=high`.
- For Python projects: run `pip-audit`.
- Capture the full output.
- Any HIGH or CRITICAL severity vulnerability is a blocker.
- MODERATE and LOW are warnings.
- Record the package name, CVE ID, severity, and recommended fix version.

---

### Phase 2 — OWASP Top 10 Manual Check

**[BLOCKER] A01 — Broken Access Control**
- Verify that every route requiring authentication has an auth middleware applied.
- Verify that ownership checks exist: a user cannot read or modify another user's resources (IDOR).
  - Pattern to check: `if (resource.userId !== req.user.id) throw ForbiddenError`.
- Check for any admin routes that are not protected by a role/permission check.

**[BLOCKER] A03 — Injection**
- Search the codebase for any raw SQL string concatenation or interpolation.
  - Pattern: `` `SELECT * FROM users WHERE id = ${userId}` `` — this is a blocker.
- Verify that all ORM/query builder calls use parameterized inputs.
- For NoSQL (MongoDB): verify no `$where` clauses with user-supplied strings.

**[BLOCKER] A07 — Identification and Authentication Failures**
- Verify JWT implementation:
  - Token expiry is set and is 15 minutes or less for access tokens.
  - Token signature is verified server-side on every protected request.
  - Algorithm is explicitly set to `HS256` or `RS256` — never `none`.
- Verify password hashing: `bcrypt` cost ≥ 12 or `argon2id`.
- Verify that failed login attempts do not reveal whether the email or password was wrong (use generic "Invalid credentials").

**[WARNING] A02 — Cryptographic Failures**
- Verify no sensitive data (passwords, tokens, PII) is logged in plaintext.
- Verify that cookies storing tokens are `httpOnly: true` and `secure: true` (in production).
- Check for any hardcoded secrets or API keys in source files.

**[WARNING] A05 — Security Misconfiguration**
- Verify CORS is configured with an explicit `origin` allowlist — not `*`.
- Verify HTTP security headers are present. Check for `helmet` (Express) or equivalent:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Strict-Transport-Security` (HTTPS environments)
  - `Content-Security-Policy`
- Verify that detailed error messages (stack traces) are suppressed in production.

**[BLOCKER] A09 — Security Logging and Monitoring Failures**
- Verify that authentication events are logged: successful logins, failed logins, token refresh.
- Verify that authorization failures (403) are logged with user context.
- Verify no authentication endpoint is missing rate limiting middleware.

---

### Phase 3 — Rate Limiting Verification

**[BLOCKER] Auth Endpoint Rate Limiting**
- Confirm that the following routes have rate limiting applied:
  - `POST /auth/login`
  - `POST /auth/register`
  - `POST /auth/refresh`
  - Any password reset or OTP endpoint.
- Verify that the rate limiter returns HTTP 429 with a `Retry-After` header.

**[WARNING] General Rate Limiting**
- Verify that a general rate limiter is applied to all public API routes (not just auth).

---

### Phase 4 — Secrets in Code Check

**[BLOCKER] Hardcoded Secrets**
- Scan all source files for strings that look like secrets:
  - Strings longer than 20 characters assigned to variables named `secret`, `password`, `key`, `token`, `api_key`.
  - Any JWT secret or database password not read from `config.ts`/`config.py`.
- Verify `.env` is in `.gitignore`.
- Verify no `.env` file with real values is committed: run `git ls-files | grep -E "\.env$"`.

---

### Phase 5 — Report
Append all findings to `production_artifacts/bug_report.md` under a new section:

```
## Security Scan — [timestamp]
### Blockers
- [ ] SEC-1: [file:line or package name] — [description] [BLOCKER]

### Warnings
- [ ] SEC-W1: [file] — [description] [WARNING]

### Dependency Scan Output
[Paste npm audit / pip-audit summary here]

### Summary
X security blockers, Y security warnings.
```

Notify the Engineer of all blockers and wait for fixes before re-auditing.
