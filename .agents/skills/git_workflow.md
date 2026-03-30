# Skill: Git Workflow

## Objective
Your goal is to manage the Git lifecycle for every new feature or bug fix to ensure the `main` branch remains stable and work is isolated.

## Instructions
1.  **Sync with Main**: Before starting any work, ensure you are on the `main` branch and it is up to date.
    -   Command: `git checkout main` followed by `git pull origin main`.
2.  **Create Feature Branch**: Create a new branch with a descriptive name based on the task/feature.
    -   Naming Convention: `feat/task-name` or `fix/bug-name`.
    -   Command: `git checkout -b <branch_name>`.
3.  **Validate State**: Confirm that the work directory is clean before the Engineer starts coding.
4.  **Handoff**: Once the branch is created, notify the next agent (Engineer or QA) that the environment is ready for implementation on the specific branch.

## Rules of Engagement
- **No Direct Push to Main**: Never commit directly to the `main` branch.
- **Mensagens de Commit em Português**: Todas as mensagens de commit devem ser escritas em Português Brasileiro, seguindo o padrão **Conventional Commits** (ex: `feat(login): adicionar validação de e-mail`).
- **Atomic Commits**: Ensure commits are small and descriptive.
