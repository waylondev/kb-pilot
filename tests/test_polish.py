"""
Regression tests for the kb-polish parts that run on the standard library alone.

Stdlib `unittest` only — no third-party dependencies, so this file runs anywhere
`test_core.py` does. It covers the two stdlib-only scripts (`validate_structure.py`,
`check_drift.py`) and the verifier registry, which is importable without pulling in
pymupdf or striprtf because the plugins import their heavy dependency lazily.

What it deliberately does not cover: per-format conversion quality. That needs
`firecrawl-anydoc` / `pymupdf` / `striprtf` and a corpus of real documents. Per
AGENTS.md, when that run happens its runner belongs in `tests/` too.

As in `test_core.py`, the target is failures that are *silent*: a validator that
invents an issue from a `#` inside a fenced code block, a drift check that reports
zero because no structured pattern matched, or a registry that drifts out of sync
with the format matrix the docs promise.

Run:
    python tests/test_polish.py
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

_KROOT = Path(__file__).resolve().parents[1]
_KB_POLISH_SCRIPTS = _KROOT / ".agents" / "skills" / "kb-polish" / "scripts"
sys.path.insert(0, str(_KB_POLISH_SCRIPTS))

import check_drift  # noqa: E402
import validate_structure  # noqa: E402
from verifiers import (  # noqa: E402
    REGISTRY,
    find_verifier,
    supported_extensions,
)


def _fence_checker(lines):
    skeleton = validate_structure.skeleton_parser()
    return skeleton.make_fence_checker(skeleton.find_code_fence_regions(lines))


class TestFenceGuard(unittest.TestCase):
    """A `#` inside a fenced block is code, not heading material.

    Mistaking one for a heading invents issues the LLM would then "fix". kb-polish
    borrows the parser from kb-ingest's build_tree.py instead of keeping a second
    copy, so these tests drive that borrowed routine through kb-polish's validators.
    """

    def test_the_borrowed_parser_is_reachable(self):
        # Path derivation is the fragile half of borrowing: the sibling's address is
        # derived from this script's own location, never hard-coded.
        parser = validate_structure.skeleton_parser()
        self.assertTrue(hasattr(parser, "find_code_fence_regions"))
        self.assertTrue(hasattr(parser, "make_fence_checker"))
        self.assertEqual(
            parser.find_code_fence_regions(["```", "x", "```"]),
            [(1, 3)],
        )

    def test_heading_inside_fence_creates_no_jump(self):
        lines = ["# T", "", "## A", "", "```python", "#### deep note", "x = 1", "```"]
        issues = validate_structure.validate_heading_continuity(lines, _fence_checker(lines))
        self.assertEqual(issues, [])

    def test_heading_inside_fence_creates_no_duplicate(self):
        lines = ["## A", "", "```", "## A", "```"]
        issues = validate_structure.validate_duplicate_headings(lines, _fence_checker(lines))
        self.assertEqual(issues, [])

    def test_heading_inside_fence_creates_no_second_h1(self):
        lines = ["# Real Title", "", "```bash", "# fake title in code", "```"]
        issues = validate_structure.validate_single_h1(lines, _fence_checker(lines))
        self.assertEqual(issues, [])

    def test_unterminated_fence_runs_to_end_of_file(self):
        regions = validate_structure.skeleton_parser().find_code_fence_regions(
            ["```", "## never a heading"]
        )
        self.assertEqual(regions, [(1, 2)])

    def test_tilde_fence_only_closes_with_tilde(self):
        # A backtick fence must not close a ~~~ block, or everything between them
        # is treated as prose and any `#` in it becomes a heading.
        lines = ["~~~", "## not a heading", "```", "## still not", "~~~"]
        regions = validate_structure.skeleton_parser().find_code_fence_regions(lines)
        self.assertEqual(regions, [(1, 5)])


class TestMechanicalChecks(unittest.TestCase):
    def test_multiple_h1_is_reported_with_the_first_one_kept(self):
        lines = ["# Main", "", "body", "# Second block"]
        issues = validate_structure.validate_single_h1(lines, _fence_checker(lines))
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["type"], "multiple_h1")
        self.assertEqual(issues[0]["line"], 4)

    def test_table_column_mismatch_is_reported_at_the_data_row(self):
        lines = ["| a | b |", "|---|---|", "| 1 |"]
        issues = validate_structure.validate_tables(lines, _fence_checker(lines))
        self.assertEqual([i["type"] for i in issues], ["table_col_mismatch"])

    def test_well_formed_table_reports_nothing(self):
        lines = ["| a | b |", "|---|---|", "| 1 | 2 |"]
        self.assertEqual(validate_structure.validate_tables(lines, _fence_checker(lines)), [])

    def test_mixed_list_markers_are_reported(self):
        lines = ["- one", "* two"]
        issues = validate_structure.validate_lists(lines, _fence_checker(lines))
        self.assertEqual([i["type"] for i in issues], ["list_marker_mixed"])


class TestDriftTokens(unittest.TestCase):
    """The check must work on any corpus without knowing which corpus it is."""

    def test_missing_structured_figure_is_caught(self):
        truth = "Annual fee is ¥6,000 and the rate is 3.5%."
        final = "Annual fee is six thousand and the rate is three percent."
        missing = check_drift.extract_tokens(truth, check_drift.TOKEN_PATTERNS) - \
            check_drift.extract_tokens(final, check_drift.TOKEN_PATTERNS)
        self.assertEqual(missing, {"¥6,000", "3.5%"})

    def test_present_figure_is_not_reported(self):
        truth = "Annual fee is ¥6,000."
        final = "## Fees\n\nAnnual fee is ¥6,000."
        missing = check_drift.extract_tokens(truth, check_drift.TOKEN_PATTERNS) - \
            check_drift.extract_tokens(final, check_drift.TOKEN_PATTERNS)
        self.assertEqual(missing, set())

    def test_no_corpus_vocabulary_is_baked_into_the_patterns(self):
        # A skill is shared; the documents it runs on are not. Vocabulary from one
        # corpus (a local currency word, a statutory period, a product name) must be
        # supplied with --extra-pattern, never hard-coded. This asserts against what
        # the script actually matches with, not against its comments.
        joined = "".join(check_drift.TOKEN_PATTERNS)
        for token in ("人民幣", "月息", "HK", "US\\$", "信用卡", "card", "年", "天"):
            self.assertNotIn(token, joined, token)

    def test_corpus_patterns_can_be_supplied_without_touching_the_skill(self):
        # The escape hatch that makes the rule above affordable: a corpus's own
        # figures come in as extra patterns and are checked the same way.
        patterns = check_drift.TOKEN_PATTERNS + [r"人民幣\s?[\d,]+元"]
        truth = "罰款為人民幣500元。"
        final = "罰款為 500 。"
        missing = check_drift.extract_tokens(truth, patterns) - \
            check_drift.extract_tokens(final, patterns)
        self.assertEqual(missing, {"人民幣500元"})

    def test_bare_numbers_keep_the_check_from_being_a_no_op(self):
        # A document with no currency or percentages would otherwise match nothing
        # and report zero drift no matter how much was lost.
        truth = "Section 12 applies."
        final = "Section 12 applies."
        self.assertTrue(check_drift.extract_tokens(truth, [check_drift.GENERIC_NUMERIC]))
        self.assertEqual(
            check_drift.extract_tokens(truth, [check_drift.GENERIC_NUMERIC]),
            check_drift.extract_tokens(final, [check_drift.GENERIC_NUMERIC]),
        )

    def test_subsumed_tokens_are_dropped(self):
        # The currency patterns overlap by design: HK$6,000 also yields $6,000.
        # Reporting both is noise.
        self.assertEqual(
            check_drift.drop_subsumed(["HK$6,000", "$6,000", "500"]),
            ["HK$6,000", "500"],
        )


class TestVerifierRegistry(unittest.TestCase):
    """The registry is what `extract_verify.py --list` prints — it must match the
    format matrix the docs promise, and stay importable without the heavy deps."""

    def test_supported_extensions_match_the_documented_matrix(self):
        expected = {
            ".pdf",
            ".docx", ".docm",
            ".pptx", ".pptm", ".ppsx", ".ppsm",
            ".xlsx", ".xlsm",
            ".odt", ".ods", ".odp",
            ".epub",
            ".rtf",
            ".csv",
        }
        self.assertEqual(set(supported_extensions()), expected)

    def test_formats_without_a_lightweight_plugin_are_declared_gaps(self):
        # workflow.md documents .doc/.ppt/.xls/.xlsb as known gaps. If one of them
        # starts resolving, either the gap was filled (update the doc) or the
        # registry is wrong (fix the registry) — either way, the test should hear.
        for ext in (".doc", ".ppt", ".xls", ".xlsb"):
            self.assertIsNone(find_verifier(Path("x" + ext)), ext)

    def test_extensions_are_mutually_exclusive(self):
        claimed = [ext for v in REGISTRY for ext in v.extensions]
        self.assertEqual(len(claimed), len(set(claimed)))

    def test_third_party_dependencies_are_declared_per_plugin(self):
        # --list reads dependency off the plugin, so a wrong value there silently
        # misinforms whoever is about to install something.
        deps = {v.name: v.dependency for v in REGISTRY}
        self.assertEqual(deps["pdf"], "pymupdf")
        self.assertEqual(deps["rtf"], "striprtf")
        self.assertEqual(deps["docx"], "")
        self.assertEqual(deps["csv"], "")

    def test_every_supported_extension_resolves_to_a_named_plugin(self):
        for ext in supported_extensions():
            verifier = find_verifier(Path("x" + ext))
            self.assertIsNotNone(verifier, ext)
            self.assertTrue(verifier.name, ext)


if __name__ == "__main__":
    unittest.main(verbosity=2)
