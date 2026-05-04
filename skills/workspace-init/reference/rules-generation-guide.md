# Rules Generation Guide

This document specifies how to generate `AGENTS.md` and `CLAUDE.md` for a project. The two files serve different agents and follow different conventions, so they are described separately. The first section covers `AGENTS.md` per OpenAI Codex's official guidance; the second covers `CLAUDE.md` per Anthropic's documentation and community practice.

## 1. Generating `AGENTS.md` (OpenAI Codex Guidance)

### 1.1 Background

Per OpenAI Codex documentation, `AGENTS.md` is the persistent project instruction file that Codex reads before starting work. Codex merges instructions hierarchically: global, repository root, and any `AGENTS.md` along the path to the current working directory; files closer to the working directory appear later and may override earlier ones. The system also recognizes `AGENTS.override.md` for higher-priority overrides, configurable fallback file names, and a default 32 KiB cap on project documentation size. ([OpenAI Developers][1])

The Codex `/init` command generates an `AGENTS.md` scaffold in the current directory, which then requires manual review and adaptation to repository conventions. ([OpenAI Developers][2]) The published `/init` prompt in the Codex repository requests a contributor guide titled "Repository Guidelines" of approximately 200–400 words, covering project structure, build/test/development commands, code style, testing conventions, commit and PR conventions, with optional sections for security, configuration, architecture, or agent-specific instructions. ([GitHub][3])

### 1.2 Generation Procedure

**Step 1 — Determine scope.** Place `AGENTS.md` at the repository root for ordinary projects. For monorepos or multi-service repositories, keep shared rules at the root and place service-local rules in `services/payments/AGENTS.md` or `AGENTS.override.md`. Do not consolidate all subproject rules into the root file.

**Step 2 — Survey project structure.** Inspect directory layout via `tree -L 2` or equivalent, excluding generated paths such as `node_modules`, `dist`, `.next`, `target`, `build`, `.venv`. The objective is to identify locations of source code, tests, documentation, scripts, configuration, and deployment files.

**Step 3 — Identify the tech stack and authoritative command sources.** Read `package.json`, `pnpm-workspace.yaml`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`, `Makefile`, `justfile`, `Dockerfile`, `.github/workflows/*`, and `README.md`. Extract build, test, lint, typecheck, and dev commands from existing scripts and CI configurations rather than inferring from the tech stack.

**Step 4 — Extract code conventions.** Read formatter, linter, and type-checker configurations (e.g. ESLint, Prettier, Biome, Ruff, Black, mypy, tsconfig, rustfmt, golangci-lint). Document only project-specific conventions or items that are easy to get wrong; do not document language fundamentals.

**Step 5 — Identify testing conventions.** Examine the test directory, naming patterns, test framework, whether unit-test-first is preferred, presence of e2e tests, coverage requirements, and slow-test labels. State clearly which verification command should be run after a change.

**Step 6 — Examine git history and PR practice.** Summarize recent commits to determine whether the project uses Conventional Commits, scope tags, issue numbers, PR descriptions, screenshots, or changelog discipline. Do not fabricate team workflows.

**Step 7 — Write short, explicit, executable rules.** The Codex `/init` prompt recommends 200–400 words; this length suits a root `AGENTS.md`. Use layered files for complex projects rather than expanding a single file. ([GitHub][3])

**Step 8 — Manual review.** Verify that all commands actually exist, rules are stable, no secrets are leaked, no paths are stale, and no vacuous rules such as "write clean code" remain.

### 1.3 Content Guidelines

| Include | Exclude |
|---------|---------|
| Project structure and key directories | Per-file explanations |
| build/test/lint/dev commands | Tool documentation in full |
| Project-specific code style | Standard language facts |
| Test framework, test naming, verification requirements | Vacuous statements like "write more tests" |
| Commit, PR, and review conventions | Transient task plans |
| Security and configuration notes | API keys, passwords, real tokens |
| Architectural constraints and known pitfalls | Volatile roadmaps |
| Subdirectory-specific override rules | All service rules merged into the root file |

### 1.4 `AGENTS.md` Template

```md
# Repository Guidelines

## Project Structure & Module Organization

- Source code lives in `<src-or-app-dir>/`.
- Tests live in `<test-dir>/` and follow the `<naming-pattern>` convention.
- Shared utilities are in `<shared-dir>/`.
- Configuration and deployment files are in `<config-or-infra-dir>/`.
- Do not edit generated directories such as `<generated-dir-1>/`, `<generated-dir-2>/`.

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

## Commit & Pull Request Guidelines

- Commit messages follow `<commit-style>`, for example `<example-commit>`.
- PRs should include: summary, test evidence, linked issue, and screenshots for UI changes.
- Keep diffs focused; avoid unrelated refactors.

## Security & Configuration

- Never commit secrets, tokens, private keys, or real credentials.
- Use `<env-file-example>` for local configuration.
- Ask before adding production dependencies or changing deployment/security-sensitive code.

## Agent-Specific Instructions

- Before editing, inspect the relevant files and existing patterns.
- After changes, run the smallest relevant verification command, then the broader suite when warranted.
- If a command fails, report the exact command and failure summary.
```

## 2. Generating `CLAUDE.md` (Official and Community Practice)

### 2.1 Background

Per Anthropic documentation, `CLAUDE.md` is the persistent instruction file that Claude Code reads at every session start, used for project-level, personal, or organizational context. It is appropriate for build commands, coding conventions, workflows, and project architecture. Documentation emphasizes that `CLAUDE.md` is context rather than enforced configuration: shorter and more specific files yield more reliable adherence. ([Claude][4])

The Claude `/init` command analyzes the codebase and generates an initial `CLAUDE.md` containing build commands, test instructions, and detected project conventions. When `CLAUDE.md` already exists, `/init` proposes improvements rather than overwriting. Setting `CLAUDE_CODE_NEW_INIT=1` enables an interactive multi-stage flow that configures `CLAUDE.md`, skills, and hooks. ([Claude][4])

Best-practice guidance is more prescriptive: `CLAUDE.md` has no fixed format but must be short and readable; include only information broadly applicable to every session. The official guidance states that if removing a line would not cause Claude to err, the line should be removed; occasional domain knowledge or workflows should live in skills rather than polluting every session. ([Claude][5])

Community practice aligns with official guidance but emphasizes context engineering. HumanLayer's recommendation treats `CLAUDE.md` as an onboarding document for Claude covering WHAT, WHY, and HOW: what the project is, why it is organized as it is, and how Claude should build and verify. Less is more—use progressive disclosure rather than embedding all commands, conventions, and code snippets, and prefer pointers to authoritative files. ([HumanLayer][6])

### 2.2 Generation Procedure

**Step 1 — Onboard the repository before writing rules.** Read `README.md`, `docs/`, architecture documentation, primary package manifests, CI configuration, and top-level directories. The goal is to give Claude a model of "what this project is, where the main modules live, and how to verify changes."

**Step 2 — Identify the tech stack.** Record language, framework, package manager, database, test framework, build system, and deployment method. Include only details that affect Claude's decisions: for example, "this project uses pnpm, not npm," or "the API schema is generated from OpenAPI; do not edit the generated client by hand."

**Step 3 — Identify working commands.** Five to eight high-value commands suffice: install, dev, lint, typecheck, unit test, e2e, build, database migration. Commands must come from package scripts, Makefile, CI, or official docs.

**Step 4 — Identify project architecture and boundaries.** Document module responsibilities, data flow, important invariants, and compatibility requirements. Do not document the purpose of every file; Claude can read files itself.

**Step 5 — Identify failure modes for Claude.** Examples include: package manager choice, generated code, migration procedures, test environment dependencies, asynchronous tasks, permission models, feature flags, monorepo workspace boundaries. These outperform generic instructions like "write high-quality code."

**Step 6 — Defer content to other locations.** Per Claude documentation, `.claude/rules/` supports topic- or path-scoped rules, skills support reusable workflows, and hooks suit deterministic per-action behavior. Do not consolidate everything into `CLAUDE.md`. ([Claude][7])

**Step 7 — Use `@` imports for progressive disclosure.** `CLAUDE.md` supports `@path/to/file` imports. Prefer pointers over inlined long content to avoid drift and context bloat. ([Claude][5])

**Step 8 — Constrain length and prune continuously.** Treat `CLAUDE.md` as code: when Claude repeats a mistake, add a rule; when a rule no longer affects behavior, remove it; when Claude ignores a rule, the file is usually too long or the wording is ambiguous. ([Claude][5]) The `.claude` documentation recommends a target of under 200 lines: longer files load but reduce adherence. ([Claude][8])

### 2.3 Content Guidelines

| Include | Exclude |
|---------|---------|
| Project purpose and core architecture | Verbatim copies of the README |
| Stable rules Claude needs every session | Information relevant only to a transient task |
| Commands not easy to derive from the code | Every script in `package.json` copied line by line |
| Package manager, test strategy, verification commands | Generic language tutorials |
| Project-specific constraints and pitfalls | "Write clean code" |
| Generated code, migration, security boundaries | Secrets, real accounts, production tokens |
| `@` references to authoritative docs | Long API documentation excerpts |
| Information that must survive context compaction | Volatile roadmaps and schedules |

### 2.4 `CLAUDE.md` Template

```md
# CLAUDE.md

## Project Overview

This repository is `<project-name>`, a `<one-sentence purpose>`.
The primary users are `<user/customer/system>`.
The main product surfaces are `<web-app/api/cli/mobile/etc>`.

For general setup and product context, read @README.md.
For deeper architecture, read @docs/architecture.md when relevant.

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

For monorepo workspace details, read @<workspace-config-file>.

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
- Authentication/authorization logic lives in `<path>`; do not duplicate it elsewhere.
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

## Context Management

- Keep summaries of changed files and test commands when compacting.
- Use @docs/<specific-doc>.md for detailed procedures instead of copying them here.
- If a workflow is long or task-specific, propose moving it to `.claude/skills/` or `.claude/rules/`.

## Known Gotchas

- `<gotcha 1>`
- `<gotcha 2>`
- `<gotcha 3>`
```

### 2.5 Optional Sections

#### Claude Code workflow guidance

Recommended phrasing:

```md
## Claude Code specific instructions

### Workflow

- For non-trivial changes, first inspect relevant files, then propose a short plan, then edit.
- Use Plan Mode for broad refactors, migrations, architecture changes, or tasks touching more than 5 files.
- Before editing, identify the smallest set of files required.
- Do not perform unrelated cleanup while implementing a requested change.
```

This section is appropriate for Claude Code behavior requirements, but should not contain general engineering rules; those belong in `AGENTS.md`.

#### Context management

Reduces blind file reads, context waste, and excessive output:

```md
### Context management

- Prefer targeted file reads over scanning the whole repository.
- Summarize large files before making changes.
- Do not paste long command outputs into the final response; summarize key failures and fixes.
- When context is insufficient, inspect nearby files before asking for clarification.
```

#### Tool usage

Specifies tool-use strategy within the project:

```md
### Tool usage

- Use search tools before editing unfamiliar modules.
- Use project skills for repeated multi-step workflows.
- Use subagents for large read-heavy investigations, security review, or cross-module analysis.
- Do not use broad automated rewrites unless the task explicitly requires them.
```

Do not embed tool configuration itself in `CLAUDE.md`—permissions, hooks, MCP server configuration, etc. These belong in their respective configuration files.

#### Skills and subagents

When a project has Claude skills or subagents, indicate when each is used:

```md
### Skills and subagents

- Use the `pr-review` skill for pull request review tasks.
- Use the `migration-reviewer` subagent for database migration changes.
- Use the `security-reviewer` subagent for authentication, authorization, payment, and secret-handling changes.
```

Do not embed full skill workflows in `CLAUDE.md`. Complex flows belong in `.claude/skills/<skill-name>/SKILL.md`.

#### Final response format

Specifies the report format Claude Code uses on task completion:

```md
### Final response format

For implementation tasks, end with:

- Changed files
- What changed
- Validation commands run
- Known risks or follow-up items
```

A standardized format produces stable output and simplifies human review.

## 3. Differential Authoring: `AGENTS.md` vs `CLAUDE.md`

`AGENTS.md` resembles a Codex repo-level contributor guide. Per the OpenAI `/init` prompt, it should be short, structured, and contributor-oriented, focused on directories, commands, tests, style, commits, and PR conventions. ([GitHub][3])

`CLAUDE.md` resembles Claude Code session onboarding and behavioral constraints. It tells Claude not only how to contribute code but also the project's WHY, WHAT, and HOW, and which context to load progressively via `@`, rules, skills, and hooks. Anthropic explicitly recommends that `CLAUDE.md` contain only broadly applicable content; occasional domain knowledge and workflows should be moved to skills. ([Claude][5])

For projects supporting both Codex and Claude Code, the recommended structure is:

```txt
repo/
  AGENTS.md              # Cross-agent core repository rules; contributor-oriented
  CLAUDE.md              # Claude Code entry point; may reference AGENTS.md
  docs/
    architecture.md
    testing.md
    release.md
  .claude/
    rules/
      frontend.md
      backend.md
      migrations.md
    skills/
      fix-ci/
        SKILL.md
```

Example `CLAUDE.md` reference pattern:

```md
# CLAUDE.md

Read @AGENTS.md for shared repository guidelines.

Additional Claude Code instructions:

- Use `/clear` between unrelated tasks.
- When compacting, preserve the list of modified files, decisions, and verification commands.
- For long workflows, prefer relevant `.claude/skills/` or `.claude/rules/` files over expanding this file.
```

The guiding principle: keep root files limited to "stable facts and rules every agent must know at the start of every task"; defer details, tutorials, long workflows, and one-off tasks to docs, rules, skills, or hooks. This is more reliable than concentrating everything into a single long Markdown file.

## 4. Independent Authoring (No Cross-References)

`CLAUDE.md` need not import `AGENTS.md`; the two rule sets may remain fully independent.

More precisely:

- `AGENTS.md` is the project rule file read by Codex and AGENTS.md-compatible agents.
- `CLAUDE.md` is the project memory file read by Claude Code.

Claude Code does not natively require `AGENTS.md`. It is loaded as context only when `CLAUDE.md` explicitly imports it via `@AGENTS.md`. To prevent any coupling, omit the import.

Independent maintenance suits the following situations:

| Scenario | Recommendation |
|----------|----------------|
| Different workflows desired for Codex and Claude | Maintain independently |
| Different tool capabilities, preferences, or command conventions | Maintain independently |
| Avoid Claude inheriting Codex-specific instructions | Do not `@AGENTS.md` |
| Team prefers explicit, less implicit context | Maintain independently |
| Substantial overlap and high maintenance cost | Consider shared references |

A risk to manage: when files diverge over time, rules drift. Examples:

```txt
AGENTS.md: use pnpm
CLAUDE.md: use npm
```

```txt
AGENTS.md: do not edit generated/
CLAUDE.md: omits the rule; Claude may modify generated/
```

When maintaining independently, adopt "semantic independence with structural alignment": the files do not reference each other, but their section structures align so that human synchronization is straightforward.

Recommended structure:

```txt
repo/
  AGENTS.md
  CLAUDE.md
```

`AGENTS.md` (Codex-oriented):

```md
# Repository Guidelines

## Project Structure
...

## Build, Test, and Development Commands
...

## Coding Style
...

## Testing Guidelines
...

## Commit and PR Guidelines
...

## Agent-Specific Instructions
...
```

`CLAUDE.md` (Claude-oriented):

```md
# CLAUDE.md

## Project Overview
...

## Tech Stack
...

## Repository Map
...

## Common Commands
...

## Working Rules
...

## Code Conventions
...

## Testing and Verification
...

## Known Gotchas
...
```

For tool isolation without divergence, do not `@AGENTS.md` from `CLAUDE.md`, but ensure both files draw from the same sources of truth—`README.md`, `docs/architecture.md`, `package.json`, CI configuration—rather than referencing each other. This preserves independence while preventing long-term drift.

## 5. Appendix: Content Decision Tables

### 5.1 Content That Belongs

| Type | Example | Recommended File |
|------|---------|------------------|
| Tech stack | `Next.js + TypeScript + PostgreSQL` | `AGENTS.md` |
| Package manager | `Use pnpm, not npm or yarn` | `AGENTS.md` |
| Startup command | `pnpm dev` | `AGENTS.md` |
| Test command | `pnpm test -- path/to/file.test.ts` | `AGENTS.md` |
| Architecture boundary | `UI must not import database clients` | `AGENTS.md` |
| High-risk constraint | `Do not delete migrations without approval` | `AGENTS.md` |
| Done criteria | `Relevant checks must pass or blockers documented` | `AGENTS.md` |
| Claude working style | `Use Plan Mode for broad refactors` | `CLAUDE.md` |
| Claude subagent strategy | `Use security-reviewer for auth changes` | `CLAUDE.md` |
| Claude output format | `Changed files / Validation / Risks` | `CLAUDE.md` |

### 5.2 Content That Does Not Belong

| Type | Reason | Correct Location |
|------|--------|------------------|
| Long framework tutorials | Wastes context, becomes stale | `docs/` or external documentation |
| Transient requirements | Pollutes long-term rules | Current task prompt |
| Personal preferences | Not suited to team sharing | User-level or local files |
| Secrets, tokens, credentials | Security risk | Outside the repository |
| Permission configuration | Natural language is not a hard constraint | settings / sandbox / hooks |
| Complex workflows | Long files reduce adherence | `.claude/skills/` |
| Path-scoped rules | Loaded every session, wastes context | `.claude/rules/` |
| Subagent persona definitions | Bloats the main file | `.claude/agents/` or `.codex/agents/` |
| Duplicated rules | Increases conflict probability | Remove or merge |
| Stale rules | Misleads the agent | Periodic cleanup |

---

## References

[1]: https://developers.openai.com/codex/guides/agents-md "Custom instructions with AGENTS.md – Codex | OpenAI Developers"
[2]: https://developers.openai.com/codex/cli/slash-commands "Slash commands in Codex CLI | OpenAI Developers"
[3]: https://github.com/openai/codex/blob/main/codex-rs/tui/prompt_for_init_command.md "codex/codex-rs/tui/prompt_for_init_command.md at main · openai/codex · GitHub"
[4]: https://code.claude.com/docs/en/memory "How Claude remembers your project - Claude Code Docs"
[5]: https://code.claude.com/docs/en/best-practices "Best practices for Claude Code - Claude Code Docs"
[6]: https://www.humanlayer.dev/blog/writing-a-good-claude-md "Writing a good CLAUDE.md | HumanLayer Blog"
[7]: https://code.claude.com/docs/en/claude-directory "Explore the .claude directory - Claude Code Docs"
[8]: https://code.claude.com/docs/en/claude-directory "Explore the .claude directory - Claude Code Docs"
