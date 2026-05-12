# Repository Guidelines

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

## Coding Style & Naming Conventions

- Use `<formatter-or-linter>` for formatting; do not hand-format large diffs.
- Follow `<language/framework-specific project convention>`.
- Name `<components/functions/files>` using `<naming-pattern>`.
- Prefer existing project patterns over introducing new abstractions.

## Testing Guidelines

- Add or update tests for behavior changes.
- Prefer focused tests during development; run `<full-verification-command>` before finalizing broad changes.
- Place new tests near the code they cover unless the existing pattern says otherwise.
- For bug fixes, include a regression test when practical.

## Done Criteria

A change is complete when:
- Relevant tests pass or failures are documented with a plan.
- Lint and typecheck are clean, or blockers are explicitly noted.
- The build succeeds or the breakage is acknowledged and tracked.

## Commit & Pull Request Guidelines

- Commit messages follow `<commit-style>`.
- PRs should include: summary, test evidence, linked issue, and screenshots for UI changes.
- Keep diffs focused; avoid unrelated refactors.

## Security & Configuration

- Never commit secrets, tokens, private keys, or real credentials.
- Use `<env-file-example>` for local configuration.
- Ask before adding production dependencies or changing deployment/security-sensitive code.

## Dates & Document Headers

- Obtain timestamps from the shell (`date`, `Get-Date`); never invent them. Standalone documents (reports, plans, assessments) carry a `> Created: YYYY-MM-DD HH:MM` line near the top.

## Tracking Files

- `SESSION_LOG.md`: append concise per-session entries after file changes or unresolved issues; one timestamp may group related changes; for bugfixes, record symptom, root cause, pitfall, and final fix when reusable.
- `TODO.md`: user-governed, agent-assisted backlog; do not read or edit by default; suggest updates and apply them only after user approval.
- `CHANGELOG.md`: release-facing changelog; only update for user-visible or release-relevant changes.
