# workspace-init

> **Externalize memory. Preserve context. Keep agents aligned.**
>
> This skill turns your project itself into a shared working memory that survives across sessions and across agents.

---

## The Problem: Memory Gaps in Human-Agent Collaboration

When you work with Claude, Codex, or other AI coding assistants over time, you hit the same friction points again and again:

- **Every new session starts from zero.** You re-explain the tech stack, naming conventions, and key directories.
- **Context windows are finite.** The agent remembers the last suggestion within a session, but forgets everything across sessions.
- **Multiple agents, one project, no shared history.** Codex and Claude work in isolation. What one learned, the other doesn't know.
- **Work notes scatter across chat history.** Decisions made, problems encountered, paths explored and abandoned — all lost when the chat scrolls away.

These are not file-management problems. They are **memory problems**.

`workspace-init` solves them by externalizing your collaboration context into a small set of lightweight, role-separated files. The project itself becomes the persistent memory layer — so every session starts where the last one left off, and every agent works from the same shared context.

---

## How It Works: Five Files, One Shared Memory

The skill inspects your workspace and creates or refines five managed files:

| File | Role in the shared memory | Audience |
|------|---------------------------|----------|
| `AGENTS.md` | **Shared project rules** — directory conventions, tech stack, testing rules, prohibitions | Codex, Cursor, etc. |
| `CLAUDE.md` | **Claude's project rules** — key paths, common commands, project shortcuts | Claude Code |
| `CHANGELOG.md` | **Release history** — user-visible changes at version granularity | Developers, users |
| `SESSION_LOG.md` | **Collaboration journal** — decisions made, problems hit, debugging context | Developers, agents |
| `TODO.md` | **User-governed backlog** — what to do next, what's already done | Developers, agents |

Each file has one clear, distinct role. This avoids the common failure mode of one file accumulating everything until it becomes unreadable.

---

## Principles

### Inspect first, write second

The skill never invents content. It first examines your project:

- Top-level directory structure
- Build manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, etc.)
- Real commands declared in `Makefile` or CI configs
- Any existing equivalent files (e.g. `agent.md`, `WORKLOG.md`)

**Commands and paths are never fabricated.** When a fact cannot be confirmed from the repository, the skill leaves a `TODO: confirm` marker and tells you what to fill in.

### No silent rewrites

When a file already exists, the skill compares it against the spec:

- **Minor issues** (wording, stale commands, a missing single-line note) → fixed in place
- **Major issues** (wrong file role, cross-references between files, length more than twice the recommended limit) → **explicit user approval is required before any change**

### Independence

`AGENTS.md` and `CLAUDE.md` do not reference each other. A small amount of duplicated facts between the two is acceptable — each file is self-contained for its own audience.

---

## What This Means for Your Workflow

### Reduced session startup cost

Agent context is finite, but project background is unbounded. Stable background knowledge moves into files; each session loads a few hundred words instead of starting from zero.

### Traceable and reviewable

`SESSION_LOG.md` and `CHANGELOG.md` do not replace `git history`. They capture the **why** — the context behind a design decision, the path taken during a hard debugging session. They also make project retrospectives possible, turning individual experiences into shared lessons learned. These are the things `git log` does not preserve.

---

## Installation

This skill follows the cross-agent `SKILL.md` standard, so the same folder works in Claude Code, Codex, Cursor, and Google Antigravity. Drop the `workspace-init/` folder into the appropriate skills directory for each tool.

### Claude Code

| Scope | Path | Availability |
|-------|------|--------------|
| Personal (recommended) | `~/.claude/skills/workspace-init/` | All your projects |
| Project | `<repo>/.claude/skills/workspace-init/` | Only inside this repo |

On Windows, `~` resolves to `C:\Users\<you>`.

### OpenAI Codex (CLI / IDE)

| Scope | Path | Availability |
|-------|------|--------------|
| Global | `~/.codex/skills/workspace-init/` | All your projects |
| Project | `<repo>/.agents/skills/workspace-init/` | Only inside this repo |

`CODEX_HOME` overrides `~/.codex` if set. Restart Codex after adding a skill.

### Cursor

| Scope | Path | Availability |
|-------|------|--------------|
| Project (recommended) | `<repo>/.cursor/skills/workspace-init/` | Only inside this repo |

A global `~/.cursor/skills/` directory is not officially documented; project scope is the reliable choice. Reload the workspace (`Cmd/Ctrl+Shift+P → Developer: Reload Window`) after adding a skill.

### Google Antigravity

| Scope | Path | Availability |
|-------|------|--------------|
| Global | `~/.gemini/antigravity/skills/workspace-init/` | All your projects |
| Workspace | `<workspace-root>/.agent/skills/workspace-init/` | Only inside this workspace |

### Verifying the install

After copying, the directory should look like:

```
<install-root>/workspace-init/
├── SKILL.md
├── README.md
├── assets/
└── reference/
```

The folder must contain `SKILL.md` directly — do not nest it one level deeper, or the agent will not detect the skill.

---

## Usage

### Basic invocation

In Claude Code or Codex, run:

```
/workspace-init
```

The skill takes over from there. You only need to answer its confirmation questions.

### First-time initialization

A typical first-run flow looks like this:

**Step 1 — pick a language**

The skill asks: which language for the files?

- For Chinese, say "用中文"
- For English, say "use English"
- If you do not specify, it asks rather than guessing.

**Step 2 — inspect the workspace**

The skill scans your project:
- Lists top-level directories
- Identifies the tech stack from `package.json`, `pyproject.toml`, etc.
- Collects available script commands
- Checks for existing equivalent files

**Step 3 — generate files**

Based on the inspection, the skill creates whichever of the five files are missing. Content is grounded in real project facts; commands are not invented. Anything that cannot be confirmed is marked `TODO: confirm` for you to fill in later.

For example, you might see:

> `CLAUDE.md` was created, but the test command could not be confirmed from the repository. Find the `TODO: confirm` marker in the file and replace it with your actual test command.

**Step 4 — review the result**

The skill ends with a concise report:
- Which files were **created**
- Which files were **refined**
- Which files were **left alone**
- Which changes are **pending your decision**

---

### Ongoing maintenance

When the project changes (a new test framework, a new build command), re-run `/workspace-init`:

**The skill compares existing files against the spec and classifies each gap:**

| Change type | Handling | Examples |
|-------------|----------|----------|
| Minor | Edit in place, then report | Update a stale command, add a missing status label |
| Major | Ask first, then act | Wrong file role, `AGENTS.md` references `CLAUDE.md`, file exceeds length limit |

**You can always say "skip" or "leave it"** — no suggestion is forced.

---

### Day-to-day use of each file

These files are not decoration. They become part of your normal workflow.

**`AGENTS.md` + `CLAUDE.md` — project rules**

Claude Code / Codex automatically reads `CLAUDE.md` and `AGENTS.md` from your project, aligning on project conventions.

**`SESSION_LOG.md` — a collaboration journal for humans**

After meaningful agent sessions, the skill can append an entry:

```markdown
## 2026-05-04
- Decision: drop the ORM, use hand-written SQL
  - Reason: queries are too complex; ORM-generated SQL has poor performance
- Issue: Docker build fails on Windows due to path separators
  - Fix: replace backslashes with forward slashes in `COPY` directives
```

This is context `git log` does not preserve. Three months later when you return to maintain the code, you will be glad it is here.

**`TODO.md` — your task board**

`TODO.md` is a simple Markdown kanban:

```markdown
## Pending
- [ ] Refactor user authentication module
- [ ] Increase unit test coverage to 80%

## Done
- [x] Upgrade dependencies to latest versions
```

You and the agent both maintain it, but you hold the steering wheel.

**`CHANGELOG.md` — release-facing version history**

Records release-level changes only, not every commit. Suited to open-source projects or anything where users need to understand what changed:

```markdown
## v1.2.0 — 2026-05-01
### Added
- Bulk import support

### Fixed
- Encoding issue during export
```

---

### Manual updates

If you want to update only one file, ask the agent directly:

- "Update AGENTS.md with the new API conventions."
- "Append the decision we just made to SESSION_LOG."
- "Mark that refactor item as done in TODO.md."

The skill recognizes these requests and routes them to the corresponding flow.

---

### Working with version control

The generated files are intended to be committed:

```bash
git add AGENTS.md CLAUDE.md CHANGELOG.md SESSION_LOG.md TODO.md
git commit -m "chore: init agent workspace tracking files"
```

This way the team shares one consistent agent rule set, and new contributors onboard their agents instantly.

---

## When to use

- Starting a new project with Claude Code for the first time
- Noticing the agent repeatedly asks the same baseline questions
- A team uses multiple AI assistants and needs a shared spec
- The project has accumulated ad-hoc notes (`notes.md`, `ai-context.md`) and needs a clean structure
- You want to revisit past collaboration with the agent, but the chat history has rolled off

---

## When not to use

- You expect a fully autonomous, no-confirmation agent housekeeper — this skill requires user input on key decisions.
- You expect these files to replace code comments or architecture documentation — they are collaboration aids, not technical docs.
- The project has an extremely short lifecycle — initialization itself has a cost.

---

## File specs at a glance

| File | Recommended length | Key constraint |
|------|--------------------|----------------|
| `AGENTS.md` | 200–400 words | General-purpose; does not reference other rule files |
| `CLAUDE.md` | ≤150 lines | Self-contained; targets Claude Code sessions |
| `CHANGELOG.md` | Grows per release | Records release-level changes only, not daily commits |
| `SESSION_LOG.md` | Append-only | Timestamped entries per session; can record debugging context |
| `TODO.md` | Maintained dynamically | `Pending` / `Done` only; no `In progress` |

---

## License

MIT
