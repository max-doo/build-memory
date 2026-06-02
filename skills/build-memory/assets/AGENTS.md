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

- `SESSION_LOG.md`: recent 7-day collaboration log; read directly when recent context is needed. Manually appending or overwriting session entries is prohibited by default; the only allowed manual edit: after a lesson has been written to KNOWLEDGE.md, modify the corresponding `- lesson:` tag to `- lesson(promoted):`.
- After adding, deleting, or modifying files, run `python .memory/session_log.py` to append a log. Required argument: the operation performed (`--done`/`added`/`modified`/`removed`). Optional arguments(if necessary): high-value experience or pitfalls(`--lesson`), context (`--context`), and key decisions (`--decision`). The script automatically handles timestamps, file lock retries, archiving of older entries, and structured entry formatting.
- `.memory/KNOWLEDGE.md`: long-term reusable lessons and decisions. Read it only for recurring issues, debugging, architecture decisions, or when the current task likely depends on prior project experience. **NOTE: After running the `session_log.py` script, if the terminal outputs the prompt `Consider promoting stable lessons to .memory/KNOWLEDGE.md.`, you MUST immediately read those lessons and proactively extract and append them to `.memory/KNOWLEDGE.md`.**
- `.memory/sessions/`: archived daily session logs older than the recent window. Do not read by default unless tracing older history.
- `TODO.md`: user-governed, agent-assisted backlog; do not read or edit by default; if a session ends with unresolved items, suggest the user update TODO and apply changes only after user approval.
- `CHANGELOG.md`: Release-oriented changelog, updated for release-specific changes or when recording milestones.
## Known Gotchas

- Keep only high-frequency gotchas that must be followed every session here, ideally 3-7 bullets.
- Promote lessons from `.memory/KNOWLEDGE.md` into this section when they are recurring across tasks, costly when missed, not obvious from code structure, and expressible as one concrete operating rule.
- Keep other long-term lessons, debugging notes, and stable decisions in `.memory/KNOWLEDGE.md`; read that file first for recurring issues, debugging, architecture decisions, or tasks that clearly depend on prior project history.
