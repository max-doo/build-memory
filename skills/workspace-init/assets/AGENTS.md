# Repository Guidelines

## Project Overview

This repository is `<project-name>`, a `<one-sentence purpose>`.
The primary users are `<user/customer/system>`.
The main product surfaces are `<web-app/api/cli/mobile/etc>`.

## Tech Stack

- Language/runtime: `<language and version>`
- Frameworks: `<frameworks>`
- Package manager: `<npm/pnpm/yarn/bun/poetry/uv/cargo/go/etc>`
- Database/storage: `<database/storage>`
- Test stack: `<test frameworks>`
- Deployment/runtime: `<deployment target>`

IMPORTANT: Use `<package-manager>` for dependency operations. Do not use `<disallowed-package-manager>`.

## Project Structure & Module Organization

- Source code lives in `<src-or-app-dir>/`.
- Tests live in `<test-dir>/` and follow the `<naming-pattern>` convention.
- Shared utilities are in `<shared-dir>/`.
- Configuration and deployment files are in `<config-or-infra-dir>/`.
- Do not edit generated directories such as `<generated-dir>/`.

## Build, Test, and Development Commands

- `<install-command>`: install dependencies.
- `<dev-command>`: start the local development server.
- `<build-command>`: create a production build.
- `<lint-command>`: run lint checks.
- `<typecheck-command>`: run type checks.
- `<test-command>`: run the standard test suite.
- `<single-test-command example>`: run a targeted test while iterating.
- `<migration-command>`: database migration.

## Coding Style & Naming Conventions

- Use `<formatter-or-linter>` for formatting; do not hand-format large diffs.
- Follow `<language/framework-specific project convention>`.
- Name `<components/functions/files>` using `<naming-pattern>`.
- Prefer existing project patterns over introducing new abstractions.
- Avoid `<anti-pattern specific to this repo>`.

## Architecture Constraints

- `<module/service>` owns `<responsibility>`.
- `<module/service>` must not import from `<forbidden layer>`.
- Public API compatibility matters for `<clients/users>`.
- Authentication/authorization logic lives in `<path>`.
- Feature flags are defined in `<path>`.

## Working Rules

- Explore first: read the relevant files and existing tests before editing.
- Keep changes scoped to the requested task.
- Ask before adding new production dependencies.
- End implementation tasks with: changed files, what changed, validation commands run, and any follow-up items.

## Testing Guidelines

- Add or update tests for behavior changes near `<test location convention>`.
- Prefer focused tests during development; run `<full-verification-command>` before finalizing broad changes.
- For bug fixes, include a regression test when practical.
- Do not skip failing tests without explaining the failure.
- If verification cannot be run locally, state why and provide the exact command the user should run.

## Done Criteria

A session or task is considered complete when:
- **Requirements Met**: All aspects of the user's original request have been fully implemented without omissions.
- **Scope Minimized**: Diffs have been reviewed to ensure changes are strictly scoped to the task, with no unrelated file modifications or accidental formatting.
- **Validation Passed**: Relevant tests, linting, and type checks pass; if blocked, reasons and mitigation plans are explicitly documented.
- **Risks Evaluated**: Potential side effects or blast radius of critical changes have been assessed and communicated.
- **Build Succeeds**: The project builds successfully, or any breakage is acknowledged and tracked.

## Commit & Pull Request Guidelines

- Commit messages follow `<commit-style>`.
- PRs should include: summary, test evidence, linked issue, and screenshots for UI changes.
- Keep diffs focused; avoid unrelated refactors.

## Security & Configuration

- Never commit secrets, tokens, private keys, or real credentials.
- Use `<env-file-example>` for local configuration.
- Treat changes under `<security-sensitive-paths>` as security-sensitive.
- Ask before changing auth, permissions, encryption, billing, or deployment configuration.

## Dates & Document Headers

- Obtain timestamps from the shell (`date`, `Get-Date`); never invent them. Standalone documents (reports, plans, assessments) carry a `> Created: YYYY-MM-DD HH:MM` line near the top.

## Tracking Files

- `SESSION_LOG.md`: append concise per-session entries after file changes or unresolved issues; one timestamp may group related changes; for bugfixes, record symptom, root cause, pitfall, and final fix when reusable.
- `TODO.md`: user-governed, agent-assisted backlog; do not read or edit by default; if a session ends with unresolved items, suggest the user update TODO and apply changes only after user approval.
- `CHANGELOG.md`: release-facing changelog; only update for user-visible or release-relevant changes.

## Known Gotchas

- `<gotcha 1>`
- `<gotcha 2>`
- `<gotcha 3>`
