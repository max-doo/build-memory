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

- Explore first: For non-trivial changes, first inspect relevant files and existing tests, then propose a short plan, then edit.
- Use Plan Mode for broad refactors, migrations, architecture changes, or tasks touching more than 5 files.
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
- **Lessons Promoted**: Stable lessons prompted in the terminal after running `session_log.py` have been promoted to `.memory/KNOWLEDGE.md`.

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

## Memory Layer

- `SESSION_LOG.md`: Recent 7-day collaboration log; read when recent context is needed. Manual edits forbidden except changing `- lesson:` to `- lesson(promoted):` after promoting to KNOWLEDGE.md.
- `.memory/INDEX.md`: Knowledge routing index; when encountering complex tasks, debugging, or needing historical context, **read this file first** to find matching section anchors by keywords.
- `.memory/KNOWLEDGE.md`: Long-term reusable experience and decisions; NEVER read in full. **Must read INDEX.md first**, then read ONLY the routed `###` section in this file. When `session_log.py` prompts to promote lessons, immediately append them here, add a routing entry in `INDEX.md`, and update the log tag to `- lesson(promoted):`; **if new experience contradicts old knowledge, update or overwrite the old entry in place to maintain a conflict-free single source of truth.**
- `.memory/sessions/`: Daily archived logs beyond the recent window; do not read by default.
- `TODO.md`: User-driven, agent-assisted backlog; do not read or edit by default.
- `CHANGELOG.md`: Release-facing change log; update on release or milestone changes.

## Known Gotchas

- Keep high-frequency, universal, lethal rules here (strictly 3-5 rules max).
- Only promote lessons from `.memory/KNOWLEDGE.md` to this section if violating them causes immediate fatal errors or irreversible damage before L1 routing occurs.
- Domain-specific debugging tips, API rules, and architectural notes must stay in `.memory/KNOWLEDGE.md` and be accessed via `.memory/INDEX.md`.
