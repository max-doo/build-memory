# Workspace Memory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the lightweight cross-agent project memory layer described in `plans/2026-05-21-workspace-memory-design.md`.

**Architecture:** Keep `SESSION_LOG.md` as the single recent-log entry point and add `.memory/session_log.py` as the only recommended writer. The script owns lock acquisition, structured appends, 7-day archival, malformed-log refusal, and lesson-candidate hints; the build-memory skill templates and references describe this contract for both English and Chinese generated workspaces.

**Tech Stack:** Python 3 standard library, Markdown templates, PowerShell verification commands on Windows, `unittest` for regression tests.

> Created: 2026-05-22 00:48

---

## File Structure

- Create: `.memory/session_log.py` - repo-local implementation of the session log writer used for dogfooding and copied by the skill template.
- Create: `.memory/KNOWLEDGE.md` - repo-local example of the long-term memory file.
- Create: `.memory/sessions/.gitkeep` - keeps the archive directory present.
- Create: `tests/test_session_log.py` - standard-library regression tests for parsing, append formatting, archival, lock handling, and lesson hints.
- Modify: `skills/build-memory/assets/AGENTS.md` - English rule template with the new memory-layer rules.
- Modify: `skills/build-memory-zh/assets/AGENTS.md` - Chinese rule template with equivalent memory-layer rules.
- Modify: `skills/build-memory/assets/SESSION_LOG.md` - English recent-log template using script-owned formatting.
- Modify: `skills/build-memory-zh/assets/SESSION_LOG.md` - Chinese recent-log template using script-owned formatting.
- Modify: `skills/build-memory/SKILL.md` - English skill workflow: copy `.memory/` assets, recommend script appends, preserve `CLAUDE.md` as `@AGENTS.md` stub.
- Modify: `skills/build-memory-zh/SKILL.md` - Chinese skill workflow with the same behavior.
- Modify: `skills/build-memory/reference/tracking-files-guide.md` - canonical tracking-file rules for the new memory layer.
- Modify: `skills/build-memory-zh/reference/tracking-files-guide.md` - Chinese canonical tracking-file rules.
- Modify: `README.md` - product-facing overview and usage command.
- Modify: `README-zh.md` - Chinese overview and usage command.
- Modify: `CHANGELOG.md` - release-facing entry for the memory-layer enhancement.

---

### Task 1: Add Session Log Writer Regression Tests

**Files:**
- Create: `tests/test_session_log.py`

- [ ] **Step 1: Create the test file**

Write this complete file:

```python
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".memory"))

import session_log


class SessionLogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".memory" / "sessions").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write_log(self, text):
        (self.root / "SESSION_LOG.md").write_text(text, encoding="utf-8")

    def read_log(self):
        return (self.root / "SESSION_LOG.md").read_text(encoding="utf-8")

    def test_append_creates_structured_entry(self):
        args = session_log.EntryArgs(
            agent="codex",
            done="确定写入脚本接口",
            context="保持 SESSION_LOG.md 为最近入口。",
            decision="脚本统一处理锁和归档。",
            added=[".memory/session_log.py"],
            modified=["AGENTS.md", "README.md"],
            removed=[],
            lesson="锁写入比手工追加更稳。",
            unresolved="补充 README 示例。",
            now=session_log.parse_now("2026-05-22T23:42:00"),
        )

        with redirect_stdout(io.StringIO()) as stdout:
            session_log.run(self.root, args)

        content = self.read_log()
        self.assertIn("## 2026-05-22", content)
        self.assertIn("### 23:42 | codex", content)
        self.assertIn("- done: 确定写入脚本接口", content)
        self.assertIn("- context: 保持 SESSION_LOG.md 为最近入口。", content)
        self.assertIn("- decision: 脚本统一处理锁和归档。", content)
        self.assertIn("  - `.memory/session_log.py`", content)
        self.assertIn("- lesson: 锁写入比手工追加更稳。", content)
        self.assertIn("- unresolved: 补充 README 示例。", content)
        self.assertIn("Session log updated.", stdout.getvalue())

    def test_archives_blocks_older_than_recent_window(self):
        self.write_log(
            "# Session Log\n\n"
            "## 2026-05-10\n\n"
            "### 09:00 | codex\n\n"
            "- done: old work\n"
            "- lesson: old lesson\n\n"
            "## 2026-05-18\n\n"
            "### 10:00 | codex\n\n"
            "- done: recent work\n"
        )
        args = session_log.EntryArgs(
            agent="codex",
            done="new work",
            context=None,
            decision=None,
            added=[],
            modified=[],
            removed=[],
            lesson=None,
            unresolved=None,
            now=session_log.parse_now("2026-05-22T11:00:00"),
        )

        with redirect_stdout(io.StringIO()) as stdout:
            session_log.run(self.root, args)

        content = self.read_log()
        archive = self.root / ".memory" / "sessions" / "2026-05-10.md"
        self.assertNotIn("## 2026-05-10", content)
        self.assertIn("## 2026-05-18", content)
        self.assertIn("## 2026-05-22", content)
        self.assertTrue(archive.exists())
        self.assertIn("- done: old work", archive.read_text(encoding="utf-8"))
        self.assertIn("Lesson candidates detected:", stdout.getvalue())
        self.assertIn("2026-05-10: old lesson", stdout.getvalue())

    def test_appends_to_existing_archive_without_overwrite(self):
        self.write_log("# Session Log\n\n## 2026-05-10\n\n### 09:00 | codex\n\n- done: old work\n")
        archive = self.root / ".memory" / "sessions" / "2026-05-10.md"
        archive.write_text("# 2026-05-10\n\n### 08:00 | claude\n\n- done: earlier work\n", encoding="utf-8")
        args = session_log.EntryArgs(
            agent="codex",
            done="new work",
            context=None,
            decision=None,
            added=[],
            modified=[],
            removed=[],
            lesson=None,
            unresolved=None,
            now=session_log.parse_now("2026-05-22T11:00:00"),
        )

        session_log.run(self.root, args)

        archive_content = archive.read_text(encoding="utf-8")
        self.assertIn("- done: earlier work", archive_content)
        self.assertIn("- done: old work", archive_content)

    def test_malformed_heading_refuses_rewrite(self):
        self.write_log("# Session Log\n\n## Yesterday\n\n- freeform entry\n")
        args = session_log.EntryArgs(
            agent="codex",
            done="new work",
            context=None,
            decision=None,
            added=[],
            modified=[],
            removed=[],
            lesson=None,
            unresolved=None,
            now=session_log.parse_now("2026-05-22T11:00:00"),
        )

        with self.assertRaisesRegex(session_log.SessionLogError, "Unsupported second-level heading"):
            session_log.run(self.root, args)

    def test_busy_lock_fails_without_modifying_log(self):
        self.write_log("# Session Log\n")
        lock = self.root / ".memory" / "SESSION_LOG.lock"
        lock.write_text("busy", encoding="utf-8")
        args = session_log.EntryArgs(
            agent="codex",
            done="new work",
            context=None,
            decision=None,
            added=[],
            modified=[],
            removed=[],
            lesson=None,
            unresolved=None,
            now=session_log.parse_now("2026-05-22T11:00:00"),
            lock_timeout_seconds=0,
        )

        with self.assertRaisesRegex(session_log.SessionLogError, "SESSION_LOG.md is busy"):
            session_log.run(self.root, args)
        self.assertEqual("# Session Log\n", self.read_log())

    def test_cli_accepts_repeated_and_delimited_paths(self):
        parsed = session_log.parse_args(
            [
                "--done",
                "new work",
                "--added",
                "a.py;b.py",
                "--added",
                "c.py",
                "--modified",
                "d.py,e.py",
                "--now",
                "2026-05-22T12:00:00",
            ]
        )

        self.assertEqual(["a.py", "b.py", "c.py"], parsed.added)
        self.assertEqual(["d.py", "e.py"], parsed.modified)
        self.assertEqual(date(2026, 5, 22), parsed.now.date())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail before implementation**

Run:

```powershell
python -m unittest tests.test_session_log -v
```

Expected: FAIL or ERROR because `.memory/session_log.py` does not exist.

- [ ] **Step 3: Commit tests**

```powershell
git add tests/test_session_log.py
git commit -m "test: cover workspace memory session log writer"
```

---

### Task 2: Implement `.memory/session_log.py`

**Files:**
- Create: `.memory/session_log.py`
- Create: `.memory/KNOWLEDGE.md`
- Create: `.memory/sessions/.gitkeep`
- Test: `tests/test_session_log.py`

- [ ] **Step 1: Create memory directories and files**

Create `.memory/sessions/`, then add:

```md
# Knowledge

Long-term reusable project lessons and decisions live here. Do not load this file by default; read it only for recurring issues, debugging, architecture decisions, or tasks that clearly depend on prior project experience.
```

Create `.memory/sessions/.gitkeep` as an empty file.

- [ ] **Step 2: Write the implementation**

Write `.memory/session_log.py` with these public names used by tests: `SessionLogError`, `EntryArgs`, `parse_now`, `parse_args`, and `run`.

```python
from __future__ import annotations

import argparse
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path


DATE_HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$")
ANY_H2 = re.compile(r"^##\s+(.+?)\s*$")
RECENT_DAYS = 7
DEFAULT_LOCK_TIMEOUT_SECONDS = 10.0
LOCK_POLL_SECONDS = 0.2


class SessionLogError(RuntimeError):
    pass


@dataclass
class EntryArgs:
    agent: str
    done: str
    context: str | None = None
    decision: str | None = None
    added: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    lesson: str | None = None
    unresolved: str | None = None
    now: datetime = field(default_factory=datetime.now)
    lock_timeout_seconds: float = DEFAULT_LOCK_TIMEOUT_SECONDS


@dataclass
class DateBlock:
    day: date
    heading: str
    body: list[str]


def split_paths(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        for part in re.split(r"[;,]", value):
            cleaned = part.strip()
            if cleaned:
                result.append(cleaned)
    return result


def parse_now(value: str | None) -> datetime:
    if not value:
        return datetime.now()
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise SessionLogError("--now must use ISO format like 2026-05-22T23:42:00") from exc


def parse_args(argv: list[str] | None = None) -> EntryArgs:
    parser = argparse.ArgumentParser(description="Append a structured entry to SESSION_LOG.md.")
    parser.add_argument("--agent", default="codex")
    parser.add_argument("--done", required=True)
    parser.add_argument("--context")
    parser.add_argument("--decision")
    parser.add_argument("--added", action="append", default=[])
    parser.add_argument("--modified", action="append", default=[])
    parser.add_argument("--removed", action="append", default=[])
    parser.add_argument("--lesson")
    parser.add_argument("--unresolved")
    parser.add_argument("--now")
    parser.add_argument("--lock-timeout-seconds", type=float, default=DEFAULT_LOCK_TIMEOUT_SECONDS)
    ns = parser.parse_args(argv)
    return EntryArgs(
        agent=ns.agent,
        done=ns.done,
        context=ns.context,
        decision=ns.decision,
        added=split_paths(ns.added),
        modified=split_paths(ns.modified),
        removed=split_paths(ns.removed),
        lesson=ns.lesson,
        unresolved=ns.unresolved,
        now=parse_now(ns.now),
        lock_timeout_seconds=ns.lock_timeout_seconds,
    )


def acquire_lock(lock_path: Path, timeout_seconds: float):
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout_seconds
    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"pid={os.getpid()}\n".encode("utf-8"))
            os.close(fd)
            return
        except FileExistsError as exc:
            if time.monotonic() >= deadline:
                raise SessionLogError("SESSION_LOG.md is busy; rerun the command later.") from exc
            time.sleep(LOCK_POLL_SECONDS)


def release_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass


def parse_session_log(text: str) -> tuple[list[str], list[DateBlock]]:
    lines = text.splitlines()
    first_h2 = next((index for index, line in enumerate(lines) if line.startswith("## ")), len(lines))
    preamble = lines[:first_h2]
    blocks: list[DateBlock] = []
    index = first_h2
    while index < len(lines):
        line = lines[index]
        match = DATE_HEADING.match(line)
        if not match:
            h2 = ANY_H2.match(line)
            if h2:
                raise SessionLogError(f"Unsupported second-level heading in SESSION_LOG.md: {line}")
            raise SessionLogError(f"Unexpected content before a date heading in SESSION_LOG.md: {line}")
        start = index
        index += 1
        while index < len(lines) and not lines[index].startswith("## "):
            index += 1
        blocks.append(
            DateBlock(
                day=date.fromisoformat(match.group(1)),
                heading=lines[start],
                body=lines[start + 1 : index],
            )
        )
    return preamble, blocks


def default_preamble() -> list[str]:
    return [
        "# Session Log",
        "",
        "<!--",
        "Recent 7-day collaboration log. Use `python .memory/session_log.py` to append entries; do not edit this file manually.",
        "Older date blocks are archived to `.memory/sessions/YYYY-MM-DD.md` by the writer script.",
        "-->",
    ]


def render_path_list(label: str, paths: list[str]) -> list[str]:
    if not paths:
        return []
    return [f"- {label}:"] + [f"  - `{path}`" for path in paths]


def render_entry(args: EntryArgs) -> list[str]:
    lines = [f"### {args.now:%H:%M} | {args.agent}", "", f"- done: {args.done}"]
    if args.context:
        lines.append(f"- context: {args.context}")
    if args.decision:
        lines.append(f"- decision: {args.decision}")
    lines.extend(render_path_list("added", args.added))
    lines.extend(render_path_list("modified", args.modified))
    lines.extend(render_path_list("removed", args.removed))
    if args.lesson:
        lines.append(f"- lesson: {args.lesson}")
    if args.unresolved:
        lines.append(f"- unresolved: {args.unresolved}")
    return lines


def archive_block(root: Path, block: DateBlock) -> list[str]:
    archive_dir = root / ".memory" / "sessions"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"{block.day.isoformat()}.md"
    archived_lines = [f"# {block.day.isoformat()}", *block.body]
    if archive_path.exists() and archive_path.read_text(encoding="utf-8").strip():
        existing = archive_path.read_text(encoding="utf-8").rstrip()
        archive_path.write_text(existing + "\n\n" + "\n".join(block.body).strip() + "\n", encoding="utf-8")
    else:
        archive_path.write_text("\n".join(archived_lines).rstrip() + "\n", encoding="utf-8")
    return extract_lessons(block.day, block.body)


def extract_lessons(day: date, lines: list[str]) -> list[str]:
    lessons: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- lesson:"):
            lesson = stripped.removeprefix("- lesson:").strip()
            if lesson:
                lessons.append(f"{day.isoformat()}: {lesson}")
    return lessons


def render_log(preamble: list[str], blocks: list[DateBlock]) -> str:
    output = list(preamble)
    for block in sorted(blocks, key=lambda item: item.day):
        while output and output[-1] == "":
            output.pop()
        output.extend(["", block.heading])
        output.extend(block.body)
    return "\n".join(output).rstrip() + "\n"


def run(root: Path, args: EntryArgs) -> None:
    if not args.done.strip():
        raise SessionLogError("--done cannot be empty.")
    memory_dir = root / ".memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    lock_path = memory_dir / "SESSION_LOG.lock"
    acquire_lock(lock_path, args.lock_timeout_seconds)
    try:
        log_path = root / "SESSION_LOG.md"
        text = log_path.read_text(encoding="utf-8") if log_path.exists() else "\n".join(default_preamble()) + "\n"
        preamble, blocks = parse_session_log(text)
        cutoff = args.now.date() - timedelta(days=RECENT_DAYS - 1)
        kept: list[DateBlock] = []
        lesson_candidates: list[str] = []
        for block in blocks:
            if block.day < cutoff:
                lesson_candidates.extend(archive_block(root, block))
            else:
                kept.append(block)

        today = args.now.date()
        entry = render_entry(args)
        for block in kept:
            if block.day == today:
                block.body = block.body + [""] + entry
                break
        else:
            kept.append(DateBlock(day=today, heading=f"## {today.isoformat()}", body=[""] + entry))

        if args.lesson:
            recent_lessons = []
            for block in kept:
                recent_lessons.extend(extract_lessons(block.day, block.body))
            if len(recent_lessons) >= 3:
                lesson_candidates.extend(recent_lessons[-3:])

        log_path.write_text(render_log(preamble or default_preamble(), kept), encoding="utf-8")
    finally:
        release_lock(lock_path)

    print("Session log updated.")
    if lesson_candidates:
        print("Lesson candidates detected:")
        for lesson in lesson_candidates:
            print(f"- {lesson}")
        print("Consider promoting stable lessons to `.memory/KNOWLEDGE.md`.")


def main(argv: list[str] | None = None) -> int:
    try:
        run(Path.cwd(), parse_args(argv))
    except SessionLogError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 3: Run focused tests**

```powershell
python -m unittest tests.test_session_log -v
```

Expected: all six tests pass.

- [ ] **Step 4: Run the script manually in the repo**

```powershell
python .memory/session_log.py --done "Implemented workspace memory writer" --context "Dogfood the new script in build-memory." --decision "Use script-owned writes for SESSION_LOG.md." --added ".memory/session_log.py" --added ".memory/KNOWLEDGE.md" --modified "SESSION_LOG.md" --lesson "The writer must refuse malformed date headings instead of rewriting arbitrary Markdown."
```

Expected: `Session log updated.` and a structured entry appears under today's `SESSION_LOG.md`.

- [ ] **Step 5: Commit implementation**

```powershell
git add .memory/session_log.py .memory/KNOWLEDGE.md .memory/sessions/.gitkeep SESSION_LOG.md
git commit -m "feat: add workspace memory session log writer"
```

---

### Task 3: Update English Skill Templates and Rules

**Files:**
- Modify: `skills/build-memory/assets/AGENTS.md`
- Modify: `skills/build-memory/assets/SESSION_LOG.md`
- Modify: `skills/build-memory/SKILL.md`
- Modify: `skills/build-memory/reference/tracking-files-guide.md`

- [ ] **Step 1: Update `assets/AGENTS.md` tracking rules**

Replace the existing `## Tracking Files` section with:

```md
## Tracking Files

- `SESSION_LOG.md`: recent 7-day collaboration log. Read it directly when recent context is needed.
- Use `python .memory/session_log.py` to append session notes; do not edit `SESSION_LOG.md` manually.
- The script automatically handles the current time, file-lock retries, structured appends, and archival of date blocks older than 7 days. If the lock remains busy after retrying, rerun the command later.
- `.memory/KNOWLEDGE.md`: long-term reusable lessons and decisions. Read it only for recurring issues, debugging, architecture decisions, or tasks that clearly depend on prior project experience.
- `.memory/sessions/`: archived daily session logs older than the recent window. Do not read by default unless tracing older history.
- `TODO.md`: user-governed, agent-assisted backlog; do not read or edit by default. Suggest updates and apply them only after user approval.
- `CHANGELOG.md`: release-facing changelog; update only for user-facing or release-relevant changes.
```

- [ ] **Step 2: Update `assets/SESSION_LOG.md`**

Replace the body with:

```md
# Session Log

<!--
Recent 7-day collaboration log.

Rules:
- Use `python .memory/session_log.py` to append entries; do not edit this file manually.
- The writer script handles timestamps, file-lock retries, structured formatting, and archival.
- Older date blocks are moved to `.memory/sessions/YYYY-MM-DD.md`.
-->
```

- [ ] **Step 3: Update `SKILL.md` managed file list**

In the overview and creation workflow, expand the generated file set from five files to five root files plus `.memory/` support files. The relevant text should state:

```md
Create or refine five managed root files and one support directory: `AGENTS.md`, `CLAUDE.md`, `SESSION_LOG.md`, `TODO.md`, optional `CHANGELOG.md`, and `.memory/`.

`.memory/` contains `session_log.py`, `KNOWLEDGE.md`, and `sessions/`. The script is the only recommended writer for `SESSION_LOG.md`.
```

Also update the `SESSION_LOG.md` row in the file-role table to:

```md
| `SESSION_LOG.md` | Recent 7-day agent collaboration log; append only through `.memory/session_log.py` | — |
```

Add this implementation rule under "Create missing files":

```md
When `SESSION_LOG.md` is created, also create `.memory/session_log.py`, `.memory/KNOWLEDGE.md`, and `.memory/sessions/`. Copy the tested script from this repository's `.memory/session_log.py` exactly, then translate only the Markdown comments in generated templates when needed. Do not translate Python option names or output strings.
```

- [ ] **Step 4: Update `reference/tracking-files-guide.md` SESSION_LOG section**

Add this paragraph to §3.2 after the creation rules:

```md
For workspaces using the optimized memory layer, `SESSION_LOG.md` remains the single recent-log entry point but is no longer manually edited. Agents append entries with `python .memory/session_log.py --done "..."`, optionally passing `--context`, `--decision`, `--added`, `--modified`, `--removed`, `--lesson`, and `--unresolved`. The script keeps only the recent 7-day window in `SESSION_LOG.md`, archives older date blocks to `.memory/sessions/YYYY-MM-DD.md`, and uses `.memory/SESSION_LOG.lock` to avoid concurrent writes.
```

Add this short note to §5:

```md
When `.memory/session_log.py` is present, AGENTS.md should mention the script instead of telling agents to manually append to `SESSION_LOG.md`.
```

- [ ] **Step 5: Verify English text changes**

Run:

```powershell
Select-String -Path 'skills\build-memory\assets\AGENTS.md','skills\build-memory\SKILL.md','skills\build-memory\reference\tracking-files-guide.md' -Pattern 'session_log.py','7-day','KNOWLEDGE.md'
```

Expected: matches in all three files.

- [ ] **Step 6: Commit English template changes**

```powershell
git add skills/build-memory/assets/AGENTS.md skills/build-memory/assets/SESSION_LOG.md skills/build-memory/SKILL.md skills/build-memory/reference/tracking-files-guide.md
git commit -m "docs: document workspace memory writer in English skill"
```

---

### Task 4: Update Chinese Skill Templates and Rules

**Files:**
- Modify: `skills/build-memory-zh/assets/AGENTS.md`
- Modify: `skills/build-memory-zh/assets/SESSION_LOG.md`
- Modify: `skills/build-memory-zh/SKILL.md`
- Modify: `skills/build-memory-zh/reference/tracking-files-guide.md`

- [ ] **Step 1: Update `assets/AGENTS.md` tracking rules**

Replace the existing tracking section with:

```md
## 跟踪文件

- `SESSION_LOG.md`：最近 7 天协作日志；需要近期上下文时可直接读取。
- 使用 `python .memory/session_log.py` 追加 session 记录；不要手工编辑 `SESSION_LOG.md`。
- 脚本会自动处理当前时间、文件锁重试、结构化追加和 7 天前日期块归档；若重试后仍无法获得锁，稍后重新运行命令。
- `.memory/KNOWLEDGE.md`：长期可复用经验和决策；仅在处理反复问题、调试、架构决策或当前任务明显依赖项目历史经验时读取。
- `.memory/sessions/`：超过最近窗口的每日归档日志；默认不读取，除非需要追溯更早历史。
- `TODO.md`：用户授权下由 AI 辅助维护的项目级待办；默认不读取、不编辑，必要时建议新增或勾选条目，并在用户同意后更新。
- `CHANGELOG.md`：release 变更日志；只记录用户可见或发布相关变化。
```

- [ ] **Step 2: Update `assets/SESSION_LOG.md`**

Replace the body with:

```md
# Session Log

<!--
最近 7 天协作日志。

规则：
- 使用 `python .memory/session_log.py` 追加记录；不要手工编辑本文件。
- 写入脚本负责时间戳、文件锁重试、结构化格式和归档。
- 更早日期块会迁移到 `.memory/sessions/YYYY-MM-DD.md`。
-->
```

- [ ] **Step 3: Update `SKILL.md`**

Add the Chinese equivalent of the English workflow rule:

```md
创建或精炼五个根目录托管文件和一个支持目录：`AGENTS.md`、`CLAUDE.md`、`SESSION_LOG.md`、`TODO.md`、可选的 `CHANGELOG.md`，以及 `.memory/`。

`.memory/` 包含 `session_log.py`、`KNOWLEDGE.md` 和 `sessions/`。脚本是 `SESSION_LOG.md` 的唯一推荐写入口。
```

Update the `SESSION_LOG.md` role row to:

```md
| `SESSION_LOG.md` | 最近 7 天 Agent 协作日志；只通过 `.memory/session_log.py` 追加 | — |
```

Add this creation rule:

```md
创建 `SESSION_LOG.md` 时，同时创建 `.memory/session_log.py`、`.memory/KNOWLEDGE.md` 和 `.memory/sessions/`。从本仓库 `.memory/session_log.py` 原样复制经过测试的脚本；只翻译生成模板中的 Markdown 注释，不翻译 Python 参数名或输出字符串。
```

- [ ] **Step 4: Update `reference/tracking-files-guide.md`**

Add:

```md
采用优化记忆层的工作区中，`SESSION_LOG.md` 仍然是最近日志的单一入口，但不再手工编辑。Agent 使用 `python .memory/session_log.py --done "..."` 追加记录，并可按需传入 `--context`、`--decision`、`--added`、`--modified`、`--removed`、`--lesson` 和 `--unresolved`。脚本只在 `SESSION_LOG.md` 保留最近 7 天窗口，将更早日期块归档到 `.memory/sessions/YYYY-MM-DD.md`，并使用 `.memory/SESSION_LOG.lock` 避免并发写冲突。
```

Add:

```md
当 `.memory/session_log.py` 存在时，AGENTS.md 应说明使用脚本追加日志，而不是要求 Agent 手工编辑 `SESSION_LOG.md`。
```

- [ ] **Step 5: Verify Chinese text changes**

Run:

```powershell
Select-String -Path 'skills\build-memory-zh\assets\AGENTS.md','skills\build-memory-zh\SKILL.md','skills\build-memory-zh\reference\tracking-files-guide.md' -Pattern 'session_log.py','最近 7 天','KNOWLEDGE.md'
```

Expected: matches in all three files.

- [ ] **Step 6: Commit Chinese template changes**

```powershell
git add skills/build-memory-zh/assets/AGENTS.md skills/build-memory-zh/assets/SESSION_LOG.md skills/build-memory-zh/SKILL.md skills/build-memory-zh/reference/tracking-files-guide.md
git commit -m "docs: document workspace memory writer in Chinese skill"
```

---

### Task 5: Update README Usage Documentation

**Files:**
- Modify: `README.md`
- Modify: `README-zh.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Update `README.md` memory-layer description**

In the section that explains `SESSION_LOG.md`, replace manual-append language with:

````md
`SESSION_LOG.md` is the recent 7-day collaboration journal. Agents append to it through:

```bash
python .memory/session_log.py \
  --done "Implemented project memory writer" \
  --context "Keep recent context light while preserving older history." \
  --decision "Use SESSION_LOG.md as the recent entry point and archive older date blocks." \
  --modified "AGENTS.md" \
  --lesson "Script-owned writes avoid concurrent manual append conflicts."
```

The writer handles timestamps, file-lock retries, structured formatting, and archival to `.memory/sessions/YYYY-MM-DD.md`. `.memory/KNOWLEDGE.md` stores stable reusable lessons and decisions, but agents should read it only when the current task needs older project experience.
````

- [ ] **Step 2: Update `README-zh.md` memory-layer description**

Use this equivalent:

````md
`SESSION_LOG.md` 是最近 7 天协作日志。Agent 通过脚本追加记录：

```bash
python .memory/session_log.py \
  --done "实现项目记忆写入脚本" \
  --context "在保持近期上下文轻量的同时保留历史记录。" \
  --decision "SESSION_LOG.md 作为最近入口，更早日期块自动归档。" \
  --modified "AGENTS.md" \
  --lesson "脚本统一写入可以避免多个 Agent 手工追加产生冲突。"
```

写入脚本负责时间戳、文件锁重试、结构化格式和 `.memory/sessions/YYYY-MM-DD.md` 归档。`.memory/KNOWLEDGE.md` 存放稳定、可复用的经验和决策，但 Agent 只应在当前任务需要旧项目经验时读取。
````

- [ ] **Step 3: Update `CHANGELOG.md`**

Under `[Unreleased]`, add:

```md
### Added

- Added a lightweight `.memory/session_log.py` writer design for structured session logging, lock-protected appends, 7-day recent logs, archived daily history, and optional long-term knowledge promotion.
```

If an `### Added` heading already exists under `[Unreleased]`, add only the bullet under that heading.

- [ ] **Step 4: Verify documentation references**

Run:

```powershell
Select-String -Path 'README.md','README-zh.md','CHANGELOG.md' -Pattern 'session_log.py','KNOWLEDGE.md','7-day','最近 7 天'
```

Expected: README files mention command usage and Knowledge behavior; changelog mentions the new writer capability.

- [ ] **Step 5: Commit documentation**

```powershell
git add README.md README-zh.md CHANGELOG.md
git commit -m "docs: explain optimized workspace memory layer"
```

---

### Task 6: End-to-End Skill Output Verification

**Files:**
- Verify only unless test failures require fixes in prior files.

- [ ] **Step 1: Run the unit suite**

```powershell
python -m unittest discover -s tests -v
```

Expected: all session log tests pass.

- [ ] **Step 2: Create a temporary generated workspace**

```powershell
$tmp = Join-Path $env:TEMP 'build-memory-memory-e2e'
if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Recurse -Force }
New-Item -ItemType Directory -Path $tmp | Out-Null
Copy-Item -LiteralPath 'skills\build-memory\assets\AGENTS.md' -Destination (Join-Path $tmp 'AGENTS.md')
Copy-Item -LiteralPath 'skills\build-memory\assets\CLAUDE.md' -Destination (Join-Path $tmp 'CLAUDE.md')
Copy-Item -LiteralPath 'skills\build-memory\assets\SESSION_LOG.md' -Destination (Join-Path $tmp 'SESSION_LOG.md')
New-Item -ItemType Directory -Path (Join-Path $tmp '.memory\sessions') -Force | Out-Null
Copy-Item -LiteralPath '.memory\session_log.py' -Destination (Join-Path $tmp '.memory\session_log.py')
Set-Location $tmp
python .memory/session_log.py --done "E2E generated workspace log append" --modified "AGENTS.md" --lesson "Generated workspaces use script-owned session logging."
```

Expected: command prints `Session log updated.`

- [ ] **Step 3: Inspect generated output**

```powershell
Get-Content -LiteralPath (Join-Path $tmp 'SESSION_LOG.md')
Test-Path -LiteralPath (Join-Path $tmp '.memory\session_log.py')
Test-Path -LiteralPath (Join-Path $tmp '.memory\sessions')
Select-String -Path (Join-Path $tmp 'AGENTS.md') -Pattern 'python .memory/session_log.py','KNOWLEDGE.md'
```

Expected: `SESSION_LOG.md` contains a dated structured entry, `.memory/session_log.py` and `.memory/sessions` exist, and `AGENTS.md` points agents to the writer script.

- [ ] **Step 4: Return to repo and inspect git diff**

```powershell
Set-Location 'C:\Project\build-memory'
git diff --stat
git status --short
```

Expected: only intended memory-layer, test, template, reference, README, and changelog files are changed.

- [ ] **Step 5: Final commit or squash**

If using one commit per task, no action is needed. If using a single feature commit instead, run:

```powershell
git add .memory tests skills README.md README-zh.md CHANGELOG.md SESSION_LOG.md
git commit -m "feat: add optimized workspace memory layer"
```

---

## Self-Review

- Spec coverage: The plan implements the design's single `SESSION_LOG.md` entry point, script-owned writes, lock retry behavior, 7-day archival, append-only archives, malformed-log refusal, `KNOWLEDGE.md` as on-demand long-term memory, lesson-candidate output, and AGENTS/CLAUDE mounting rules.
- Placeholder scan: The plan contains concrete file paths, commands, expected outputs, code, and exact text blocks. The string `TODO.md` appears only as the managed backlog filename.
- Type consistency: The test imports and implementation define the same public names: `SessionLogError`, `EntryArgs`, `parse_now`, `parse_args`, and `run`.
- Execution risk: The only destructive command appears in an isolated temp directory during E2E verification. Do not run it from the repository root with `$tmp` unset.
