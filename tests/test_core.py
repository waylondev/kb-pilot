"""
Regression tests for the kb-pilot core path (kb-ingest scripts).

Stdlib `unittest` only — no third-party dependencies. These pin down the
failures that are *silent*: a parser that invents a section from a `#` inside a
fenced code block, truncates the enclosing section's line range, or carries a
stale summary forward without telling anyone — rather than the loud crashes
that get caught on the first run.

Run:
    python tests/test_core.py
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

# Import the kb-ingest scripts (stdlib-only, each guarded by `if __name__ == "__main__"`).
_KROOT = Path(__file__).resolve().parents[1]
_KB_INGEST_SCRIPTS = _KROOT / ".agents" / "skills" / "kb-ingest" / "scripts"
sys.path.insert(0, str(_KB_INGEST_SCRIPTS))

import build_tree  # noqa: E402
import check_source  # noqa: E402


class _TempTreeTestCase(unittest.TestCase):
    """Base case: a self-cleaning temp dir for a source file + tree.json."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.src = self.root / "doc.md"
        self.out = self.root / "tree.json"

    def write_src(self, text: str) -> None:
        self.src.write_text(text, encoding="utf-8")


class TestFenceDetection(_TempTreeTestCase):
    """A `#` inside a fenced code block is a comment, not heading material."""

    def _titles(self, tree: dict) -> list:
        titles = []

        def walk(nodes):
            for n in nodes:
                titles.append(n["title"])
                walk(n.get("children", []))

        walk(tree["nodes"])
        return titles

    def test_heading_inside_fence_is_not_a_node(self):
        self.write_src(
            "# Real Title\n\n"
            "## Real Section\n\n"
            "```markdown\n## Phantom section\ntext\n```\n\n"
            "## After\n"
        )
        tree = build_tree.parse_headings(self.src)

        self.assertEqual(self._titles(tree), ["Real Section", "After"])
        # The enclosing section's end_line must span the fence (line 9), not be
        # truncated ahead of the phantom heading that a naive parser would invent.
        self.assertEqual(tree["nodes"][0]["end_line"], 9)

    def test_heading_inside_fence_is_not_the_title(self):
        self.write_src(
            "```python\n# fake title in code\nx = 1\n```\n\n"
            "# Real Title\n\n## Section\n"
        )
        self.assertEqual(build_tree.infer_title(self.src), "Real Title")


class TestFillingsCarryover(_TempTreeTestCase):
    """Re-ingest must *report* what it inherited, not swallow it silently."""

    def test_reports_inherited_fillings_and_source_change(self):
        self.write_src("# T\n\n## A\n\nfee is 100\n\n## B\n\ncontent\n")
        first = build_tree.build(str(self.src), str(self.out), source_path="doc.md")
        self.assertEqual(first["reused_fillings"], 0)
        self.assertFalse(first["source_changed"])

        # Simulate the LLM having filled summary/keywords on the first pass.
        tree = json.loads(self.out.read_text(encoding="utf-8"))
        tree["summary"] = "doc-level summary"
        tree["nodes"][0]["summary"] = "section A summary"
        tree["nodes"][0]["keywords"] = ["fee"]
        self.out.write_text(json.dumps(tree, ensure_ascii=False), encoding="utf-8")

        # A structure-preserving edit: change a number, keep every heading.
        self.write_src("# T\n\n## A\n\nfee is 200\n\n## B\n\ncontent\n")
        second = build_tree.build(str(self.src), str(self.out), source_path="doc.md")

        self.assertEqual(second["reused_fillings"], 1)
        self.assertTrue(second["reused_doc_summary"])
        self.assertTrue(second["source_changed"])


class TestSourceDrift(_TempTreeTestCase):
    """Drift is a checksum question: a value edit keeps the line count identical."""

    def _ingest(self, text: str) -> None:
        self.write_src(text)
        build_tree.build(str(self.src), str(self.out), source_path="doc.md")

    def test_drift_detected_by_checksum_not_line_count(self):
        self._ingest("# T\n\n## A\n\nfee is 100\n")
        self.write_src("# T\n\n## A\n\nfee is 500\n")

        result = check_source.check(str(self.src), str(self.out))
        self.assertTrue(result["drifted"])
        self.assertFalse(result["line_count_changed"])

    def test_unchanged_source_reports_no_drift(self):
        self._ingest("# T\n\n## A\n\nfee is 100\n")

        result = check_source.check(str(self.src), str(self.out))
        self.assertFalse(result["drifted"])
        self.assertTrue(result["trustworthy"])

    def test_missing_checksum_reports_unknown(self):
        self.write_src("# T\n\n## A\n\nfee is 100\n")
        # A hand-written tree.json that predates the source_sha256 field.
        self.out.write_text('{"doc_id":"doc_001","total_lines":4}', encoding="utf-8")

        result = check_source.check(str(self.src), str(self.out))
        self.assertTrue(result["checksum_unknown"])
        self.assertFalse(result["trustworthy"])


if __name__ == "__main__":
    unittest.main(verbosity=2)