#!/usr/bin/env python3
"""Cross-skill contract tests.

The three skills are published independently and carry no runtime dependency on
each other. kb-polish's `markdown_skeleton.py` and kb-chat's `check_source.py`
are therefore *copies* of routines owned by kb-ingest. Copies drift silently —
one side changes, the other keeps validating clean and parsing wrong. These tests
pin the behaviour of the copies to the originals using the same boundary cases a
future edit is most likely to break, so a change on either side turns red until
both are updated. Consistency is enforced here, not by a shared import.
"""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "kb-polish" / "scripts"))
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "kb-ingest" / "scripts"))
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "kb-chat" / "scripts"))

import build_tree  # kb-ingest: the owner
import check_source  # kb-chat's copy — behaviour-pinned to kb-ingest's below
import markdown_skeleton  # kb-polish's copy


def _load_module(name: str, path: Path):
    """Load a script as a module from an explicit path (for the second copy)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ingest_check_source = _load_module(
    "ingest_check_source",
    ROOT / ".agents" / "skills" / "kb-ingest" / "scripts" / "check_source.py",
)


class TestHeadingContract(unittest.TestCase):
    """kb-polish's heading() must classify exactly like kb-ingest's."""

    CASES = [
        "# Title",          # H1
        "## Section",       # H2
        "### Sub",          # H3
        "#### Deep",        # H4
        "##### Deeper",     # H5
        "###### Deepest",   # H6
        "####### seven",    # 7 #s: not a heading (CommonMark)
        "### ",             # empty title: not a heading
        "#",                # no title: not a heading
        "## Title ##",      # trailing #s stripped from title
        "## Title ###",     # longer trailing sequence, stripped
        "#heading",         # no space after #: paragraph, not a heading
        "    # indented",   # 4-space indent: not a heading (not up to 3)
        "  # two spaces",   # up to 3 leading spaces: still a heading
        "# heading  ",      # trailing whitespace trimmed
        "## A | B",         # pipe in title is fine
        "# `code` title",   # backticks in title are fine
        "普通中文标题",      # non-ASCII title (no leading #): not a heading
        "## 中文标题",       # non-ASCII ATX heading
    ]

    def test_classification_and_text_agree(self):
        for line in self.CASES:
            a = markdown_skeleton.heading(line)
            b = build_tree.heading(line)
            self.assertEqual(
                a, b,
                f"heading() disagrees on {line!r}: kb-polish={a!r} kb-ingest={b!r}",
            )


class TestFenceContract(unittest.TestCase):
    """kb-polish's fence detection must return the same regions as kb-ingest's."""

    DOCS = [
        # simple fence
        ["```", "x", "```"],
        # tilde fence
        ["~~~", "x", "~~~"],
        # backtick fence must not close a tilde block
        ["~~~", "## not a heading", "```", "## still not", "~~~"],
        # unterminated fence runs to EOF
        ["```", "## never a heading"],
        # info string with a backtick is not a fence opener
        ["```python `bad`", "## still a heading"],
        # longer closing fence is valid
        ["```", "x", "````"],
        # shorter closing fence does not close
        ["````", "x", "```", "## still inside"],
        # 3+ leading spaces is not a fence
        ["    ```", "## a heading"],
        # 1-3 leading spaces is a fence
        ["  ```", "## not a heading", "  ```"],
        # two fences in one document
        ["```", "a", "```", "", "~~~", "b", "~~~"],
    ]

    def test_regions_agree(self):
        for doc in self.DOCS:
            a = markdown_skeleton.find_code_fence_regions(doc)
            b = build_tree.find_code_fence_regions(doc)
            self.assertEqual(
                a, b,
                f"fence regions disagree on {doc!r}: kb-polish={a!r} kb-ingest={b!r}",
            )


class TestCheckSourceContract(unittest.TestCase):
    """kb-chat's copy of check_source must report the same drift facts."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.src = self.tmp / "doc.md"
        self.tree = self.tmp / "tree.json"
        self.src.write_text("# T\n\n## A\n\nfee 100\n", encoding="utf-8")

    def _tree(self, sha):
        return {"doc_id": "doc_001", "source_sha256": sha, "total_lines": 5}

    def test_no_drift_agrees(self):
        import hashlib
        sha = hashlib.sha256(self.src.read_bytes()).hexdigest()
        self.tree.write_text(json.dumps(self._tree(sha)), encoding="utf-8")
        a = check_source.check(str(self.src), str(self.tree))
        self.assertEqual(a["drifted"], False)
        self.assertEqual(a["trustworthy"], True)

    def test_value_edit_keeps_line_count_but_drifts(self):
        self.tree.write_text(
            json.dumps(self._tree("0" * 64)), encoding="utf-8"
        )
        a = check_source.check(str(self.src), str(self.tree))
        self.assertEqual(a["drifted"], True)          # checksum catches it
        self.assertEqual(a["line_count_changed"], False)  # line count would not

    def test_missing_source_fails_both_ways(self):
        with self.assertRaises(FileNotFoundError):
            check_source.check(str(self.tmp / "nope.md"), str(self.tree))

    def test_ingest_copy_reports_same_facts(self):
        """kb-ingest's copy must report byte-identical drift facts on the same input.

        Both skills carry their own check_source.py (no runtime import between
        skills); the two copies are pinned here. Docstrings may differ — the
        contract is behaviour, not bytes (e2e-hy4 P0-1: the copies drifted in
        prose only, and a byte-equality test would have failed on an edit that
        changed nothing semantic).
        """
        import hashlib
        sha = hashlib.sha256(self.src.read_bytes()).hexdigest()
        self.tree.write_text(json.dumps(self._tree(sha)), encoding="utf-8")

        for tree_sha, label in [
            (sha, "no drift"),
            ("0" * 64, "value edit"),
        ]:
            self.tree.write_text(json.dumps(self._tree(tree_sha)), encoding="utf-8")
            a = check_source.check(str(self.src), str(self.tree))
            b = ingest_check_source.check(str(self.src), str(self.tree))
            for key in ("drifted", "trustworthy", "line_count_changed",
                        "checksum_unknown", "current_total_lines",
                        "recorded_total_lines"):
                self.assertEqual(
                    a.get(key), b.get(key),
                    f"copies disagree on {key!r} for {label}: "
                    f"kb-chat={a.get(key)!r} kb-ingest={b.get(key)!r}",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
