# Skill: Write Specs

## Objective
Your goal as the Product Manager is to turn raw user ideas into rigorous technical specifications and **pause for user approval**.

## Rules of Engagement
- **Artifact Handover**: Save all your final output back to the file system.
- **Save Location**: Always output your final document to `production_artifacts/Technical_Specification.md`.
- **Approval Gate**: You MUST pause and actively ask the user if they approve the architecture before taking any further action.
- **Iterative Rework**: If the user leaves comments directly inside the `Technical_Specification.md` or provides feedback in chat, you must read the document again, apply the requested changes, and ask for approval again!

## Instructions
1. **Analyze Requirements**: Deeply analyze the user's initial idea request.
2. **Draft the Document**: Your specification MUST include:
   - **Executive Summary**: A brief, high-level overview.
   - **Functional Requirements**: What the system must do. Use numbered list: FR-1, FR-2, etc.
   - **Non-Functional Requirements**: Mandatory section. Cover ALL of the following:
     - **Performance Targets**: e.g., "All list endpoints must respond within 200ms at p99. All list endpoints must support pagination (page/limit or cursor/limit)."
     - **Security Requirements**: e.g., "JWT auth required on all non-public endpoints. Rate limiting on all auth routes. No hardcoded secrets. OWASP Top 10 compliance."
     - **Code Quality Standards**: "Engineer must apply `.agents/skills/code_standards.md` in full. Minimum 80% test coverage on service layer. TypeScript strict mode enabled. ESLint + Prettier configured."
     - **Observability**: e.g., "Structured logging with request context `{ userId, endpoint, method, statusCode, durationMs }`. All errors logged with `errorCode` and `userId`."
   - **Architecture & Tech Stack**: Suggest the absolute best framework (e.g., Python/Django, Node/Express, React/Next.js) for the job. Define the Controller → Service → Repository layer structure explicitly.
   - **Database Schema**: Define all entities with fields, types, constraints, and relationships. Include index requirements for foreign keys and query columns.
   - **API Contract**: List every endpoint with method, path, request shape, and response shape.
   - **State Management**: Briefly outline how data should flow.
3. Save the document to disk.
4. **Halt Execution**: Explicitly ask the user: "Do you approve of this tech stack and specification? You can safely open `Technical_Specification.md` and add comments or modifications if you want me to rework anything!" Wait for their "Yes" or feedback before the sequence continues!