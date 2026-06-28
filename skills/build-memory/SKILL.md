---
name: build-memory
description: Initialize or refine agent workspace tracking and rule files. Use when (1) the user runs `/build-memory` or asks to initialize a workspace, (2) creating or updating AGENTS.md / CLAUDE.md / CHANGELOG.md / SESSION_LOG.md / TODO.md, (3) auditing existing rule or tracking files for quality issues, (4) adding missing managed files to a project, (5) the user asks about workspace conventions, session logs, backlogs, or changelogs.
---

# Build Memory

Create or refine five managed files at the project root: `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, `SESSION_LOG.md`, `TODO.md`, plus the lightweight `.memory/` support directory for stable session-log writes and long-term lessons.

Four non-negotiable rules:
- **Single Source of Truth.** All generic project rules, commands, and tech stack MUST be written in `AGENTS.md`. `CLAUDE.md` serves only as a minimalist entry point and MUST include a `@AGENTS.md` reference. Do NOT duplicate specific commands or rules in `CLAUDE.md`.
- **Scripted session writes.** Agents SHOULD append session notes with `python .memory/session_log.py` instead of manually editing `SESSION_LOG.md`; the script handles locking, 7-day archival, and structured formatting.
- **No silent rewrites.** Never overwrite or delete existing content without explicit user approval.
- **Real time.** Before writing any timestamp into a managed file, obtain the current date/time from the system via a shell command (`date`, `date -Iseconds`, `Get-Date`, etc.). Do not invent timestamps from memory.

Templates ship in English only under `assets/`. Translate to the target language at write time.

## Workflow

### 1. Pick the language

For files being **created**:
- **Explicit directive** ("use English", "用中文", "create in Japanese") → that language.
- **Substantive user input** (instructions or context beyond a bare invocation, in any language) → detect the language of that content.
- **Bare invocation** (just `/build-memory`, "init workspace", or similar with no further requirements) → **ASK the user** which language. Do not guess.

For files being **refined**, keep the existing file's language; do not translate.

### 2. Phase 1: Audit & Propose (Mandatory Approval Gate)

Before any write or modification, gather facts:
- Top-level files and directories
- Package manager / language / framework (`package.json`, `pyproject.toml`, etc.)
- Real commands from configuration scripts
- **Read in full** all existing managed rule files in the workspace (whether standard `AGENTS.md` or legacy `.cursor/rules`, `CLAUDE.md`, etc.).
- Check if `.memory/INDEX.md` exists and verify whether all `###` sections in `.memory/KNOWLEDGE.md` are routed in `INDEX.md`.

**Empty workspace detection.** If the inspection finds no source directory, no package manifest, and no build config—i.e. only `.git`, README, etc.—STOP before writing any managed file. Ask the user to choose:
1. Skip for now.
2. Describe the planned project so meaningful defaults can be filled in.
Do not auto-fill placeholders blindly.

For non-empty workspaces, output a clear `Refactoring Plan` detailing:
1. Which infrastructure pieces are missing and will be physically copied (e.g., `.memory/session_log.py`).
2. Which existing custom business rules, evaluation principles, or architecture constraints were discovered, along with a **commitment to preserve them completely**.
3. How `AGENTS.md` and `CLAUDE.md` will be reorganized.

<HARD-GATE>
You MUST STOP and wait for the user's explicit approval. Do NOT proceed with any modifications or file writes until approval is granted.
</HARD-GATE>

### 3. Phase 2: Infrastructure Scaffolding

Once the user approves, **your very first step must always be copying the physical assets.**
- Regardless of whether old or non-standard rule folders exist in the project, you **MUST** fully copy the `assets/.memory/` directory and its internal scripts to the project root.
- Copy `.memory/INDEX.md` if missing.
- Never "borrow" or "adapt to" legacy frameworks. The standard `.memory` directory and `session_log.py` are non-negotiable infrastructure.

### 4. Phase 3: Differential Merging (Strict Zones)

When creating missing files or refining existing ones, you must follow the rule of "Differential Merging" with strict zones. **The overall structure MUST align with the template's skeleton (Headings)**, but the content is handled differently by zone:

**Strict Zone (Memory Layer)**:
- For the `## Memory Layer` section in `AGENTS.md`, you **MUST** copy the content from the `assets/AGENTS.md` template exactly, 100% verbatim. No omissions, custom rewriting, or deletions are allowed, otherwise the memory system scripts will fail.
- Ensure `CLAUDE.md` is strictly pruned to contain only the `@AGENTS.md` reference, preventing rule duplication.

**Baseline Zone (Generic Rules)**:
- For generic operational sections like `## Working Rules` and `## Done Criteria`, you should **completely retain the standard expressions from the template**.
- If the legacy rules contain project-specific completion criteria or unique working disciplines, you MUST **append** them to the end of the template's content. Never overwrite custom discipline with generic template text.

**Flexible Zone (Project Rules)**:
- Existing core business principles or architectural constraints must be mapped to their appropriate headings. They **MUST NEVER be silently deleted** in the name of template alignment.
- If legacy rules cannot fit neatly into the template's headings, you MUST create custom headings for them (e.g., `## Custom Project Rules`) and preserve them entirely. Complete, dogmatic rewrites are forbidden.

For creating other missing files: read the `assets/` templates, translate headings if necessary, and substitute placeholders with verified facts.
**Cold Start Seeding**: If the workspace contains a `.git` directory and you are creating `SESSION_LOG.md` for the very first time, you SHOULD run `git log -n 5 --since="7 days ago" --oneline` to extract recent context. Synthesize this into a brief historical background and immediately run `python .memory/session_log.py --done "Recent context imported from Git history: [your summary]"` to seed the initial memory layer.
Never invent commands or timestamps. Never overwrite an existing `.memory/KNOWLEDGE.md` or manually edit `SESSION_LOG.md` (which must be edited via the script) without explicit approval.

| File | Role | Target |
|------|------|--------|
| `AGENTS.md` | Main repository guidelines for all code agents (contains all rules, stacks, commands) | 200–400 words |
| `CLAUDE.md` | Claude minimalist entry point; **MUST** include `@AGENTS.md` reference | 1–3 lines |
| `CHANGELOG.md` | Release-facing; version-level entries only | — |
| `SESSION_LOG.md` | Agent operational log; per-session timestamped entries | — |
| `TODO.md` | User-governed backlog; `Pending` / `Done` only (no `In progress`) | — |
| `.memory/session_log.py` | Recommended session-log writer with lock retries, 7-day archival, and lesson candidate hints | — |
| `.memory/KNOWLEDGE.md` | Long-term reusable lessons and durable decisions; read on demand only | — |

### 5. Report

End with a concise report: **created**, **refined**, **left alone**, **pending decision**.

## Assets and references

- `assets/<filename>` — English templates for the five managed files.
- `assets/.memory/` — support script, long-term knowledge template, and archive directory placeholder.
- `reference/tracking-files-guide.md` — full rules for `CHANGELOG.md`, `SESSION_LOG.md`, `TODO.md`.
  - §2 CHANGELOG: release-facing, version-level timestamps, when to create
  - §3 SESSION_LOG: agent operational log, per-session entries, bugfix context
  - §4 TODO: user-governed backlog, Pending/Done only, no "In progress"
  - §7 Decision checklists: what belongs in each tracking file
- `reference/rules-generation-guide.md` — full rules for `AGENTS.md`, `CLAUDE.md`.
  - §1 AGENTS.md: Main repository guidelines, 200–400 words
  - §2 CLAUDE.md: Claude Code minimalist entry point, only referencing AGENTS.md
  - §3 Master-Mirror Pattern: single source of truth rules for AGENTS.md and CLAUDE.md
  - §6 Appendix: content decision table (what goes where)

Read the relevant reference sections before refining a file with non-trivial differences from the template.
