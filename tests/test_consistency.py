#!/usr/bin/env python3
"""Cross-skill contract tests.

The skills are published independently and carry no runtime dependency on each
other. kb-chat's `check_source.py` is a *copy* of the routine owned by kb-ingest.
Copies drift silently — one side changes, the other keeps validating clean and
parsing wrong. These tests pin the behaviour of the copy to the original using the
same boundary cases a future edit is most likely to break, so a change on either
side turns red until both are updated. Consistency is enforced here, not by a
shared import.
"""

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "kb-ingest" / "scripts"))
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "kb-chat" / "scripts"))

import build_tree  # kb-ingest: the owner
import check_source  # kb-chat's copy — behaviour-pinned to kb-ingest's below


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