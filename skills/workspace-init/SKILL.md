---
name: workspace-init
description: Initialize or refine agent workspace tracking and rule files. Use when (1) the user runs `/workspace-init` or asks to initialize a workspace, (2) creating or updating AGENTS.md / CLAUDE.md / CHANGELOG.md / SESSION_LOG.md / TODO.md, (3) auditing existing rule or tracking files for quality issues, (4) adding missing managed files to a project, (5) the user asks about workspace conventions, session logs, backlogs, or changelogs.
---

# Workspace Initialization

Create or refine five managed files at the project root: `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, `SESSION_LOG.md`, `TODO.md`.

Three non-negotiable rules:
- **Independence.** `AGENTS.md` and `CLAUDE.md` stay independent. Never add `@AGENTS.md` to `CLAUDE.md` (or vice versa). Some duplicated facts between the two are acceptable.
- **No silent rewrites.** Never overwrite or delete existing content without explicit user approval.
- **Real time.** Before writing any timestamp into a managed file, obtain the current date/time from the system via a shell command (`date`, `date -Iseconds`, `Get-Date`, etc.). Do not invent timestamps from memory.

Templates ship in English only under `assets/`. Translate to the target language at write time.

## Workflow

### 1. Pick the language

For files being **created**:
- **Explicit directive** ("use English", "用中文", "create in Japanese") → that language.
- **Substantive user input** (instructions or context beyond a bare invocation, in any language) → detect the language of that content.
- **Bare invocation** (just `/workspace-init`, "init workspace", or similar with no further requirements) → **ASK the user** which language. Do not guess.

For files being **refined**, keep the existing file's language; do not translate.

### 2. Inspect the workspace

Before any write, gather facts:
- Top-level files and directories
- Package manager / language / framework (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.)
- Real commands from `package.json` scripts, `Makefile`, CI configs
- Existing managed files and likely aliases (`agent.md`, `WORKLOG.md`, `.agent/log.md`, etc.)

**Empty workspace detection.** If the inspection finds no source directory, no package manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.), no build/test config (`Makefile`, `tsconfig.json`, …), and no CI configuration — i.e. only `.git`, README, license, or dotfiles — STOP before writing any managed file. Ask the user to choose:

1. Skip workspace init for now.
2. Describe the planned project (language, framework, intent) so meaningful defaults can be filled in.
3. Create minimal scaffold files with prominent `TODO: empty workspace` markers and a leading comment noting the workspace was empty at init time.

Do not auto-fill placeholders in an empty workspace; the resulting noise outweighs the value.

Never invent commands or paths. If a placeholder cannot be filled from the repo, leave a `TODO: confirm` marker and tell the user.

### 3. Create missing files

For each missing file:
1. Read the English template at `assets/<filename>`.
2. Translate fixed text (headings, comments, labels) into the target language.
3. Substitute placeholders with verified facts from Step 2.
4. Write to the project root.

| File | Role | Target |
|------|------|--------|
| `AGENTS.md` | Repository guidelines for any code agent | 200–400 words |
| `CLAUDE.md` | Claude-specific project memory; **self-contained** (no `@AGENTS.md`) | ≤150 lines |
| `CHANGELOG.md` | Release-facing; version-level entries only | — |
| `SESSION_LOG.md` | Agent operational log; per-session timestamped entries | — |
| `TODO.md` | User-governed backlog; `Pending` / `Done` only (no `In progress`) | — |

### 4. Refine existing files

For each existing managed file:

1. Read it in full.
2. Compare against the spec. Read only the relevant sections:
   - For `CHANGELOG.md`, `SESSION_LOG.md`, `TODO.md`: see `reference/tracking-files-guide.md`
     - §2 CHANGELOG definition and rules
     - §3 SESSION_LOG definition and rules
     - §4 TODO definition and rules
     - §7 Decision checklists
   - For `AGENTS.md`, `CLAUDE.md`: see `reference/rules-generation-guide.md`
     - §1 AGENTS.md generation guide
     - §2 CLAUDE.md generation guide
     - §3 Differential writing (AGENTS.md vs CLAUDE.md)
     - §6 Appendix: content decision table
3. Classify the gap:
   - **Minor** — wording fixes, a stale command, a missing one-line tracking-file note, harmless extras. Edit in place.
   - **Major** — wrong file role (e.g. `CLAUDE.md` is just a session log), one file imports the other (`@AGENTS.md` / `@CLAUDE.md`), file >2× recommended length, or whole sections contradict the spec.
4. **Major gaps require user confirmation before any edit.** Present a short summary of issues and proposed changes; wait for approval, skip, or item-by-item direction.

### 5. Report

End with a concise report: **created**, **refined**, **left alone**, **pending decision**.

## Assets and references

- `assets/<filename>` — English templates for the five managed files.
- `reference/tracking-files-guide.md` — full rules for `CHANGELOG.md`, `SESSION_LOG.md`, `TODO.md`.
  - §2 CHANGELOG: release-facing, version-level timestamps, when to create
  - §3 SESSION_LOG: agent operational log, per-session entries, bugfix context
  - §4 TODO: user-governed backlog, Pending/Done only, no "In progress"
  - §7 Decision checklists: what belongs in each tracking file
- `reference/rules-generation-guide.md` — full rules for `AGENTS.md`, `CLAUDE.md`.
  - §1 AGENTS.md: Codex-style repository guidelines, 200–400 words
  - §2 CLAUDE.md: Claude Code session onboarding, ≤150 lines, self-contained
  - §3 Differential writing: how AGENTS.md and CLAUDE.md differ, independence rules
  - §6 Appendix: content decision table (what goes where)

Read the relevant reference sections before refining a file with non-trivial differences from the template.
