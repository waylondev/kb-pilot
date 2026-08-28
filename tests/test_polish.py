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
    return validate_structure.make_fence_checker(
        validate_structure.find_code_fence_regions(lines)
    )


class TestFenceGuard(unittest.TestCase):
    """A `#` inside a fenced block is code, not heading material.

    Same hazard as kb-ingest's parser, and the same consequence: mistaking one for
    a heading invents issues the LLM would then "fix". validate_structure.py owns a
    second copy of this parser, so it is pinned here independently.
    """

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
        regions = validate_structure.find_code_fence_regions(["```", "## never a heading"])
        self.assertEqual(regions, [(1, 2)])

    def test_tilde_fence_only_closes_with_tilde(self):
        # A backtick fence must not close a ~~~ block, or everything between them
        # is treated as prose and any `#` in it becomes a heading.
        lines = ["~~~", "## not a heading", "```", "## still not", "~~~"]
        regions = validate_structure.find_code_fence_regions(lines)
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


class TestScoring(unittest.TestCase):
    """The mechanical score covers 70 of the 100 pts; the rest is the LLM's.

    The point of pinning this is the no-double-charge rule: every issue the script
    deducts for must name the dimension it was deducted from, or the LLM charges
    the same defect twice in its semantic pass.
    """

    def test_mechanical_weights_total_seventy(self):
        self.assertEqual(sum(validate_structure.MAX_WEIGHT.values()), 70)

    def test_every_issue_type_has_a_penalty_and_a_dimension(self):
        for issue_type, dimension in validate_structure.ISSUE_DIMENSION.items():
            self.assertIn(issue_type, validate_structure.PENALTY, issue_type)
            self.assertIn(dimension, validate_structure.MAX_WEIGHT, issue_type)

    def test_deduction_never_drives_a_dimension_below_zero(self):
        scores = dict(validate_structure.MAX_WEIGHT)
        noisy = ["heading_jump"] * 50
        for issue_type in noisy:
            dim = validate_structure.ISSUE_DIMENSION[issue_type]
            scores[dim] = max(0, scores[dim] - validate_structure.PENALTY[issue_type])
        self.assertEqual(scores["heading_continuity"], 0)


class TestDriftTokens(unittest.TestCase):
    def test_missing_structured_figure_is_caught(self):
        truth = "Annual fee is HK$6,000."
        final = "Annual fee is six thousand."
        missing = check_drift.extract_tokens(truth, check_drift.TOKEN_PATTERNS) - \
            check_drift.extract_tokens(final, check_drift.TOKEN_PATTERNS)
        self.assertIn("HK$6,000", missing)

    def test_present_figure_is_not_reported(self):
        truth = "Annual fee is HK$6,000."
        final = "## Fees\n\nAnnual fee is HK$6,000."
        missing = check_drift.extract_tokens(truth, check_drift.TOKEN_PATTERNS) - \
            check_drift.extract_tokens(final, check_drift.TOKEN_PATTERNS)
        self.assertEqual(missing, set())

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
