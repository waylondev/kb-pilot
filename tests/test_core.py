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

import contextlib
import io
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
import build_manifest  # noqa: E402
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
        self.assertEqual(build_tree.first_h1(self.src), "Real Title")

    def test_no_h1_reports_empty_rather_than_the_file_stem(self):
        # A caller must be able to tell "no H1" from "title is the file stem",
        # otherwise a previously authored title gets overwritten by a stem.
        self.write_src("## Section only\n\ntext\n")
        self.assertEqual(build_tree.first_h1(self.src), "")


class TestRecordFields(_TempTreeTestCase):
    """title and domain are re-derived every ingest — never inherited.

    Both sit on the semantic side of the skeleton/flesh line, and both are a
    single value, so there is no cost argument for carrying one forward the way
    there is for a document's worth of summaries. What the script owes instead is
    a report of what it just dropped.
    """

    def test_domain_is_not_inherited_and_the_loss_is_reported(self):
        self.write_src("# T\n\n## A\n\ntext\n")
        build_tree.build(str(self.src), str(self.out), source_path="doc.md", domain="api")

        self.write_src("# T\n\n## A\n\ntext changed\n")
        second = build_tree.build(str(self.src), str(self.out), source_path="doc.md")

        self.assertEqual(second["domain"], "")
        # Reported, so the caller can re-supply it rather than never finding out.
        self.assertEqual(second["previous_domain"], "api")

    def test_domain_is_re_supplied_each_ingest(self):
        self.write_src("# T\n\n## A\n\ntext\n")
        build_tree.build(str(self.src), str(self.out), source_path="doc.md", domain="api")

        second = build_tree.build(str(self.src), str(self.out), source_path="doc.md", domain="billing")

        self.assertEqual(second["domain"], "billing")
        self.assertEqual(second["previous_domain"], "api")

    def test_title_comes_from_the_flag_then_h1_then_stem(self):
        self.write_src("# From H1\n\n## A\n\ntext\n")
        explicit = build_tree.build(str(self.src), str(self.out), source_path="doc.md",
                                    title="From flag")
        self.assertEqual(explicit["title_source"], "flag")
        self.assertEqual(explicit["title"], "From flag")

        h1 = build_tree.build(str(self.src), str(self.out), source_path="doc.md")
        self.assertEqual(h1["title_source"], "h1")
        self.assertEqual(h1["title"], "From H1")

        self.write_src("## A\n\nno h1 here\n")
        stem = build_tree.build(str(self.src), str(self.out), source_path="doc.md")
        self.assertEqual(stem["title_source"], "stem")
        self.assertEqual(stem["title"], "doc")

    def test_h1_change_replaces_the_previous_title(self):
        # The source restated its title; the old one is only remembered, not kept.
        self.write_src("# Original\n\n## A\n\ntext\n")
        build_tree.build(str(self.src), str(self.out), source_path="doc.md")

        self.write_src("# Renamed\n\n## A\n\ntext\n")
        second = build_tree.build(str(self.src), str(self.out), source_path="doc.md")

        self.assertEqual(second["title"], "Renamed")
        self.assertEqual(second["previous_title"], "Original")

    def test_title_replaced_by_the_source_is_announced(self):
        # Last run set a title deliberately; this run passes no --title, so the
        # H1 wins and the previous value is gone. Three documents promise that a
        # dropped value is announced on stderr, so it has to be said out loud.
        self.write_src("# Plain H1\n\n## A\n\ntext\n")
        build_tree.build(str(self.src), str(self.out), source_path="doc.md",
                         title="Authored Title")

        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            second = build_tree.build(str(self.src), str(self.out), source_path="doc.md")

        self.assertEqual(second["title"], "Plain H1")
        self.assertEqual(second["previous_title"], "Authored Title")
        self.assertIn("title", buf.getvalue())
        self.assertIn("Authored Title", buf.getvalue())

    def test_fillings_are_still_carried_over(self):
        # The contrast that makes the rule above coherent: summaries cost a
        # re-read to regenerate, so those *are* inherited (and reported).
        self.write_src("# T\n\n## A\n\nfee is 100\n")
        build_tree.build(str(self.src), str(self.out), source_path="doc.md", domain="api")
        tree = json.loads(self.out.read_text(encoding="utf-8"))
        tree["nodes"][0]["summary"] = "section A summary"
        self.out.write_text(json.dumps(tree, ensure_ascii=False), encoding="utf-8")

        second = build_tree.build(str(self.src), str(self.out), source_path="doc.md")

        self.assertEqual(second["reused_fillings"], 1)
        self.assertEqual(second["domain"], "")


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


class _TempKbTestCase(unittest.TestCase):
    """Base case: a temp knowledge base with a .kb/index/ tree."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.kb = Path(self._tmp.name)
        (self.kb / ".kb" / "index").mkdir(parents=True)

    def ingest(self, rel_path: str, text: str, **fields) -> Path:
        src = self.kb / rel_path
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text(text, encoding="utf-8")
        out = self.kb / ".kb" / "index" / Path(rel_path).with_suffix("") / "tree.json"
        build_tree.build(str(src), str(out), source_path=rel_path, **fields)
        return out

    def fill(self, tree_path: Path, top: list, nested: list = None) -> None:
        """Simulate the LLM having filled keywords on a tree.json's nodes."""
        tree = json.loads(tree_path.read_text(encoding="utf-8"))
        tree["nodes"][0]["keywords"] = top
        if nested is not None and tree["nodes"][0]["children"]:
            tree["nodes"][0]["children"][0]["keywords"] = nested
        tree_path.write_text(json.dumps(tree, ensure_ascii=False), encoding="utf-8")

    def manifest(self) -> list:
        return json.loads((self.kb / ".kb" / "manifest.json").read_text(encoding="utf-8"))


class TestManifest(_TempKbTestCase):
    """The manifest is kb-chat Step 1's only input — pin down its shape."""

    def test_tags_come_from_top_level_sections_only(self):
        # Sub-section keywords stay in tree.json for localization. If they leak
        # into the manifest, routing gets noisy and the manifest grows unbounded.
        tree = self.ingest("docs/api/auth.md", "# T\n\n## Overview\n\n### Nested\n\nx\n")
        self.fill(tree, top=["jwt", "overview"], nested=["expiry", "sub-only"])

        build_manifest.build(str(self.kb))

        self.assertEqual(self.manifest()[0]["tags"], ["jwt", "overview"])

    def test_entry_fields_map_to_the_document_record(self):
        tree = self.ingest("docs/api/auth.md", "# T\n\n## A\n\nx\n",
                           title="API Auth", domain="api")
        tree_data = json.loads(tree.read_text(encoding="utf-8"))
        tree_data["summary"] = "How auth works"
        tree.write_text(json.dumps(tree_data, ensure_ascii=False), encoding="utf-8")

        result = build_manifest.build(str(self.kb))

        entry = self.manifest()[0]
        self.assertEqual(entry["doc_id"], tree_data["doc_id"])
        self.assertEqual(entry["title"], "API Auth")
        self.assertEqual(entry["domain"], "api")
        self.assertEqual(entry["summary"], "How auth works")
        self.assertEqual(entry["path"], "docs/api/auth.md")
        self.assertEqual(entry["updated_at"], tree_data["ingested_at"])
        self.assertEqual(result["document_count"], 1)

    def test_doc_ids_are_assigned_and_stable_without_the_cli(self):
        # doc_id is part of the skeleton, so build() resolves it itself — a
        # caller that bypasses the CLI must not get an empty doc_id.
        first = self.ingest("docs/a.md", "# A\n\n## S\n\nx\n")
        second = self.ingest("docs/b.md", "# B\n\n## S\n\nx\n")
        self.assertEqual(json.loads(first.read_text(encoding="utf-8"))["doc_id"], "doc_001")
        self.assertEqual(json.loads(second.read_text(encoding="utf-8"))["doc_id"], "doc_002")

        self.ingest("docs/a.md", "# A\n\n## S\n\nedited\n")
        self.assertEqual(json.loads(first.read_text(encoding="utf-8"))["doc_id"], "doc_001")

    def test_missing_index_root_is_an_error_not_an_empty_manifest(self):
        # Silently writing an empty manifest would make kb-chat report "not
        # mentioned in the documents" for a knowledge base that is simply unset.
        (self.kb / ".kb" / "index").rmdir()
        with self.assertRaises(FileNotFoundError):
            build_manifest.build(str(self.kb))

    def test_empty_index_is_an_error_not_an_empty_manifest(self):
        # The directory exists but holds nothing. `[]` is indistinguishable from
        # "this knowledge base has no documents", so kb-chat would answer "not
        # mentioned" for a knowledge base that still has sources.
        with self.assertRaises(build_manifest.EmptyIndexError):
            build_manifest.build(str(self.kb))
        self.assertFalse((self.kb / ".kb" / "manifest.json").exists())

    def test_all_unreadable_trees_is_an_error_not_an_empty_manifest(self):
        corrupt = self.kb / ".kb" / "index" / "docs" / "broken" / "tree.json"
        corrupt.parent.mkdir(parents=True, exist_ok=True)
        corrupt.write_text("{ not json", encoding="utf-8")

        with self.assertRaises(build_manifest.EmptyIndexError):
            build_manifest.build(str(self.kb))
        self.assertFalse((self.kb / ".kb" / "manifest.json").exists())

    def test_unreadable_tree_is_skipped_without_losing_the_rest(self):
        self.ingest("docs/good.md", "# Good\n\n## A\n\nx\n")
        corrupt = self.kb / ".kb" / "index" / "docs" / "broken" / "tree.json"
        corrupt.parent.mkdir(parents=True, exist_ok=True)
        corrupt.write_text("{ not json", encoding="utf-8")

        result = build_manifest.build(str(self.kb))

        # The good document still lands, and the skip is reported rather than
        # silently absorbed — "how much did I drop" must be answerable.
        entries = self.manifest()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["title"], "Good")
        self.assertEqual(len(result["skipped_unreadable"]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)