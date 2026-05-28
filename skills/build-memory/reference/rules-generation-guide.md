# Rules Generation Guide

This document specifies how to generate a high-quality, cross-agent project memory layer. 

Past practices often split the preferences of OpenAI Codex (structured, directory-based, command-heavy) and Anthropic Claude Code (context engineering, WHAT/WHY/HOW, progressive disclosure) into two separate philosophies. In this project, we **combine their strengths into a unified approach**.

We adopt a **Single Source of Truth** architecture: a unified `AGENTS.md` carries all project context, conventions, and commands. It leverages high structural clarity and rich context, acting as the ultimate weapon for any agent starting work. Meanwhile, `CLAUDE.md` serves merely as a lightweight stub.

## 1. Unified Generation Procedure

Fusing Codex's rigorous structure with Claude's context engineering, we distill the following 8-step generation method:

**Step 1: Codebase Onboarding (WHAT and WHY)**
Read `README.md`, `docs/`, architecture docs, and top-level directories. Clearly define the project's purpose, its primary audience, and the problems it solves to prevent agents from modifying code blindly without the big picture.

**Step 2: Identify Tech Stack & Command Sources (From Truth)**
Read `package.json`, `pyproject.toml`, `Cargo.toml`, `Makefile`, CI configurations, etc. Extract actual commands for build, test, dev, and lint. **Never invent commands**. Specify hard constraints, e.g., "Use pnpm, do not use npm."

**Step 3: Extract Directory Structure & Architecture Boundaries**
Examine the codebase to document where core source, tests, shared utilities, and configs live. Explicitly point out generated code paths (which shouldn't be hand-edited) and key module responsibilities.

**Step 4: Extract Code Conventions & Test Rules**
Only record conventions that are "project-specific" or "easy to get wrong". Check test frameworks and naming patterns, and explicitly state "which verification commands must be run after a change." Do not include vacuous statements like "write clean code" or "write lots of tests."

**Step 5: Identify Failure Modes & Gotchas**
Record areas where agents or new team members commonly make mistakes (e.g., wrong package manager, failing to update a schema, breaking monorepo boundaries, missing a feature flag).

**Step 6: Externalize Memory via Tracking Files**
Configure the agent to maintain collaboration journals in `SESSION_LOG.md` and synchronize progress in `TODO.md`. This bridges the isolation gap between multiple sessions.

**Step 7: Progressive Disclosure**
Long framework tutorials, massive workflows, or giant API specs waste context window space. Use `@` imports to defer these details to `docs/` or `.claude/skills/`, loading them only on demand. Keep the main rules concise.

**Step 8: Review & Prune**
Ensure a clean file structure. If you spot stale rules, broken commands, or sensitive secrets, clean them up immediately. Treat the rules file like source code.

## 2. Content Guidelines

When authoring rules, adhere to the following table:

| Include | Exclude |
|---------|---------|
| Project purpose and core architecture (WHAT & WHY) | Verbatim copies of the README |
| Stable facts and constraints needed every session | Details relevant only to a transient task |
| Commands that can't be easily guessed | Copy-pasting every single script from package.json |
| Project-specific architecture constraints and gotchas | "Please write high-quality and maintainable code" |
| Rules for using tracking files (SESSION_LOG / TODO) | API keys, actual production tokens |
| `@`-references to detailed rule docs (e.g., `@docs/testing.md`) | Long, complex single-task workflows |

## 3. Templates

### 3.1 The Core Fact Repository: `AGENTS.md`

All critical instructions live here:

```md
# Repository Guidelines

## Project Overview
This repository is `<project-name>`, a `<one-sentence purpose>`.
The primary users are `<user/customer/system>`.
The main product surfaces are `<web-app/api/cli/mobile/etc>`.

## Tech Stack
- Language/runtime: `<language and version>`
- Frameworks: `<frameworks>`
- Package manager: `<package-manager>`
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
- `<test-command>`: run the standard test suite.

## Coding Style & Naming Conventions
- Use `<formatter-or-linter>` for formatting; do not hand-format large diffs.
- Follow `<language/framework-specific project convention>`.
- Prefer existing project patterns over introducing new abstractions.

## Architecture Constraints
- `<module/service>` owns `<responsibility>`.
- `<module/service>` must not import from `<forbidden layer>`.
- Authentication/authorization logic lives in `<path>`.

## Working Rules & Testing Guidelines
- Explore first: read the relevant files and existing tests before editing.
- Add or update tests for behavior changes near `<test location convention>`.
- Do not skip failing tests without explaining the failure.
- End implementation tasks with: changed files, what changed, validation commands run, and any follow-up items.

## Tracking Files
- `SESSION_LOG.md`: append concise per-session entries after file changes or unresolved issues; record bug symptoms and root causes when reusable.
- `TODO.md`: user-governed, agent-assisted backlog; do not read or edit by default; suggest updates and apply them only after user approval.
- `CHANGELOG.md`: release-facing changelog; only update for release-relevant changes.

## Known Gotchas
- `<gotcha 1>`
- `<gotcha 2>`
```

### 3.2 The Minimalist Entry: `CLAUDE.md`

Ensure synchronization through a one-way import:

```md
# CLAUDE.md

Please read @AGENTS.md for all repository guidelines, tech stack, commands, and architecture constraints.

## Claude Code specific instructions

- Use `/clear` between unrelated tasks.
- For non-trivial changes, first inspect relevant files, then propose a short plan, then edit.
- Use Plan Mode for broad refactors, migrations, architecture changes, or tasks touching more than 5 files.
```

## 4. Avoiding Redundancy and Circular Dependencies

Never reference `@CLAUDE.md` from `AGENTS.md`. Imports must be strictly one-way (`CLAUDE.md` -> `AGENTS.md`).
If a note needs to be known by all agents, it should not appear in `CLAUDE.md`; instead, move it to `AGENTS.md`. This is the bottom line for keeping the memory layer healthy.
