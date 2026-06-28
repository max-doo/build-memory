import importlib.util
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "build-memory"
    / "assets"
    / ".memory"
    / "session_log.py"
)


def load_session_log_module():
    spec = importlib.util.spec_from_file_location("session_log", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SessionLogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.module = load_session_log_module()

    def tearDown(self):
        self.tmp.cleanup()

    def test_appends_structured_entry_under_current_date(self):
        self.module.append_session_note(
            root=self.root,
            now=datetime(2026, 5, 28, 9, 30),
            done="Added project memory writer",
            context="Keep recent agent context small.",
            decision="Use a locked script as the recommended write path.",
            modified=["AGENTS.md", "SESSION_LOG.md"],
            lesson="Scripted writes reduce concurrent append conflicts.",
            agent="codex",
        )

        content = (self.root / "SESSION_LOG.md").read_text(encoding="utf-8")

        self.assertIn("## 2026-05-28", content)
        self.assertIn("### 09:30 | codex", content)
        self.assertIn("- done: Added project memory writer", content)
        self.assertIn("- context: Keep recent agent context small.", content)
        self.assertIn(
            "- decision: Use a locked script as the recommended write path.",
            content,
        )
        self.assertIn("- modified:\n  - `AGENTS.md`\n  - `SESSION_LOG.md`", content)
        self.assertIn(
            "- lesson: Scripted writes reduce concurrent append conflicts.",
            content,
        )

    def test_archives_date_blocks_older_than_recent_window(self):
        (self.root / "SESSION_LOG.md").write_text(
            "# Session Log\n\n"
            "## 2026-05-19\n\n"
            "### 10:00 | claude\n\n"
            "- done: Old work\n"
            "- lesson: Old reusable lesson\n\n"
            "## 2026-05-22\n\n"
            "### 11:00 | codex\n\n"
            "- done: Recent work\n",
            encoding="utf-8",
        )

        result = self.module.append_session_note(
            root=self.root,
            now=datetime(2026, 5, 28, 12, 0),
            done="New work",
            agent="codex",
        )

        current = (self.root / "SESSION_LOG.md").read_text(encoding="utf-8")
        archived = (
            self.root / ".memory" / "sessions" / "2026-05-19.md"
        ).read_text(encoding="utf-8")

        self.assertNotIn("## 2026-05-19", current)
        self.assertIn("## 2026-05-22", current)
        self.assertIn("## 2026-05-28", current)
        self.assertIn("## 2026-05-19", archived)
        self.assertIn("- done: Old work", archived)
        self.assertIn("Old reusable lesson", "\n".join(result.lesson_candidates))

    def test_lock_timeout_leaves_existing_lock_in_place(self):
        memory_dir = self.root / ".memory"
        memory_dir.mkdir()
        lock_path = memory_dir / "SESSION_LOG.lock"
        lock_path.write_text("busy", encoding="utf-8")

        with self.assertRaises(TimeoutError):
            with self.module.session_lock(memory_dir, wait_seconds=0, poll_seconds=0):
                pass

        self.assertTrue(lock_path.exists())

    def test_recent_lesson_threshold_reports_candidates(self):
        (self.root / "SESSION_LOG.md").write_text(
            "# Session Log\n\n"
            "## 2026-05-26\n\n"
            "### 12:00 | codex\n\n"
            "- lesson: Third\n\n"
            "### 11:00 | codex\n\n"
            "- lesson: Second\n\n"
            "### 10:00 | codex\n\n"
            "- lesson: First\n",
            encoding="utf-8",
        )

        result = self.module.append_session_note(
            root=self.root,
            now=datetime(2026, 5, 28, 13, 0),
            done="Fourth lesson-bearing work",
            lesson="Fourth",
            agent="codex",
        )

        self.assertEqual(["Fourth", "Third", "Second", "First"], result.lesson_candidates)

    def test_existing_unparseable_log_is_not_rewritten(self):
        log_path = self.root / "SESSION_LOG.md"
        original = "# Session Log\n\nold free-form notes without date blocks\n"
        log_path.write_text(original, encoding="utf-8")

        with self.assertRaises(ValueError):
            self.module.append_session_note(
                root=self.root,
                now=datetime(2026, 5, 28, 14, 0),
                done="Should not append",
                agent="codex",
            )

        self.assertEqual(original, log_path.read_text(encoding="utf-8"))

    def test_validate_memory_index_detects_missing_routes(self):
        memory_dir = self.root / ".memory"
        memory_dir.mkdir(exist_ok=True)
        (memory_dir / "KNOWLEDGE.md").write_text(
            "# Knowledge\n\n### 1. API Request Rules\n\n### 2. Unrouted Section\n",
            encoding="utf-8",
        )
        (memory_dir / "INDEX.md").write_text(
            "# Index\n\n| api-client | api/ | ### 1. API Request Rules | note |\n",
            encoding="utf-8",
        )

        gaps = self.module.validate_memory_index(self.root)
        self.assertEqual(["2. Unrouted Section"], gaps)

    def test_main_prints_warning_on_index_gap(self):
        memory_dir = self.root / ".memory"
        memory_dir.mkdir(exist_ok=True)
        (memory_dir / "KNOWLEDGE.md").write_text(
            "# Knowledge\n\n### 1. API Rules\n\n### 2. Unrouted Bug\n",
            encoding="utf-8",
        )
        (memory_dir / "INDEX.md").write_text(
            "# Index\n\n| api | api/ | ### 1. API Rules | note |\n",
            encoding="utf-8",
        )
        (self.root / "SESSION_LOG.md").write_text("# Session Log\n", encoding="utf-8")

        import io
        from unittest.mock import patch

        test_args = ["session_log.py", "--done", "test task"]
        with patch.object(sys, "argv", test_args), patch("os.getcwd", return_value=str(self.root)), patch("pathlib.Path.cwd", return_value=self.root), patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            exit_code = self.module.main()

        output = mock_stdout.getvalue()
        self.assertEqual(0, exit_code)
        self.assertIn("MEMORY INDEX MISMATCH DETECTED", output)
        self.assertIn("- ### 2. Unrouted Bug", output)


if __name__ == "__main__":
    unittest.main()

