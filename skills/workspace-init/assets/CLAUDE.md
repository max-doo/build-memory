# CLAUDE.md

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

## Repository Map

- `<dir>/`: `<purpose>`
- `<dir>/`: `<purpose>`
- `<dir>/`: `<purpose>`
- `<dir>/`: generated code; do not edit directly.
- `<dir>/`: tests and fixtures.

## Common Commands

- Install dependencies: `<command>`
- Start dev server: `<command>`
- Run lint: `<command>`
- Run typecheck: `<command>`
- Run unit tests: `<command>`
- Run a single test: `<command example>`
- Build: `<command>`
- Database migration: `<command>`

Prefer targeted tests while iterating. Before finalizing a broad code change, run `<final-verification-command>`.

## Working Rules

- Explore first: read the relevant files and existing tests before editing.
- Prefer existing patterns over new abstractions.
- Keep changes scoped to the requested task.
- Do not modify generated files in `<generated-dir>`; update `<source-of-truth>` instead.
- Ask before adding new production dependencies.
- For behavior changes, add or update tests.
- For UI changes, include screenshot or manual verification notes when possible.
- End implementation tasks with: changed files, what changed, validation commands run, and any follow-up items.

## Code Conventions

- Formatting is handled by `<formatter>`.
- Linting is handled by `<linter>`.
- Use `<naming convention>` for `<files/components/functions>`.
- Follow `<project-specific convention that is not obvious from defaults>`.
- Avoid `<anti-pattern specific to this repo>`.

## Architecture Constraints

- `<module/service>` owns `<responsibility>`.
- `<module/service>` must not import from `<forbidden layer>`.
- Public API compatibility matters for `<clients/users>`.
- Authentication/authorization logic lives in `<path>`.
- Feature flags are defined in `<path>`.

## Testing and Verification

- New behavior should have tests near `<test location convention>`.
- Bug fixes should include regression tests when practical.
- Do not skip failing tests without explaining the failure.
- If verification cannot be run locally, state why and provide the exact command the user should run.

## Security and Secrets

- Never commit secrets, credentials, private keys, or real customer data.
- Use `<example env file>` as the template for local environment variables.
- Treat changes under `<security-sensitive-paths>` as security-sensitive.
- Ask before changing auth, permissions, encryption, billing, or deployment configuration.

## Dates & Document Headers

- Obtain timestamps from the shell (`date`, `Get-Date`); never invent them. Standalone documents (reports, plans, assessments) carry a `> Created: YYYY-MM-DD HH:MM` line near the top.

## Tracking Files

- `SESSION_LOG.md`: append concise per-session entries after file changes or unresolved issues; one timestamp may group related changes.
- `TODO.md`: user-governed backlog; do not read or edit by default unless requested.
- `CHANGELOG.md`: release-facing changelog; only update for user-visible or release-relevant changes.

## Known Gotchas

- `<gotcha 1>`
- `<gotcha 2>`
- `<gotcha 3>`
