#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
validate_structure.py — mechanical Markdown structure validation.

Deterministic layer: checks only mechanical "skeleton" issues (heading jumps, table
column counts, code blocks, image paths, etc.) and outputs a structured issue list for the LLM.
Severity is the LLM's judgment; this script does no semantic judgment and no scoring.

Usage:
    python validate_structure.py raw.md

Output (stdout):
    {"ok": true, "issues": [...]}

Exit codes:
    0  success
    1  bad args or file not found
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Issue types are typed strings (not free text) so the LLM can group and weigh
# them. The script reports mechanical facts; severity is the LLM's call.

# The heading/fence rules are borrowed from kb-ingest when it sits next to this
# skill — never copied, never required. With kb-ingest installed the heading
# checks run in full; without it they are skipped and reported in the `skipped`
# list, so a standalone kb-polish still works, it just validates less. The
# borrow is optional on purpose: the skills are published independently.
_SKELETON = None
_heading = None  # bound to kb-ingest's build_tree.heading by _load_skeleton()


def _load_skeleton():
    """Load kb-ingest's `build_tree` module if it sits next to this skill, else None."""
    global _SKELETON, _heading
    if _SKELETON is not None:
        return _SKELETON
    # …/kb-polish/scripts/validate_structure.py -> parents[2] is .agents/skills/
    ingest_scripts = Path(__file__).resolve().parents[2] / "kb-ingest" / "scripts"
    if not (ingest_scripts / "build_tree.py").is_file():
        return None
    sys.path.insert(0, str(ingest_scripts))
    import build_tree
    _SKELETON = build_tree
    _heading = build_tree.heading
    return _SKELETON


def validate_heading_continuity(lines: list[str], is_inside_code) -> list[dict]:
    issues = []
    prev_level = None
    for i, line in enumerate(lines, 1):
        if is_inside_code(i):
            continue
        h = _heading(line)
        if not h:
            continue
        level = h[0]
        if prev_level is not None and level > prev_level + 1:
            issues.append({
                "type": "heading_jump",
                "line": i,
                "detail": f"heading level jump: {prev_level} -> {level}",
                "text": line.strip(),
            })
        prev_level = level
    return issues


def validate_duplicate_headings(lines: list[str], is_inside_code) -> list[dict]:
    seen = {}
    issues = []
    for i, line in enumerate(lines, 1):
        if is_inside_code(i):
            continue
        h = _heading(line)
        if not h:
            continue
        text = h[1]
        if text in seen:
            issues.append({
                "type": "duplicate_heading",
                "line": i,
                "detail": f"duplicate heading (first at line {seen[text]}): {text}",
                "text": line.strip(),
            })
        else:
            seen[text] = i
    return issues


def validate_single_h1(lines: list[str], is_inside_code) -> list[dict]:
    """A document must have exactly one H1.

    kb-pilot rule: H1 is the document title, not in the tree (the tree starts at H2),
    see kb-ingest Gotchas. Multiple H1s distort the structure; later blocks should be
    demoted to H2 during re-render.
    Note: `^#\\s+` only matches `# ` (`## `/`### ` are naturally excluded because the
    second char is non-space).
    """
    h1_lines = []
    for i, line in enumerate(lines, 1):
        if is_inside_code(i):
            continue
        h = _heading(line)
        if h and h[0] == 1:
            h1_lines.append((i, line.strip()))
    issues = []
    if len(h1_lines) > 1:
        first_line = h1_lines[0][0]
        for i, text in h1_lines[1:]:
            issues.append({
                "type": "multiple_h1",
                "line": i,
                "detail": (
                    f"multiple H1 headings (first at line {first_line}): {text} "
                    "(kb-pilot requires exactly one H1)"
                ),
                "text": text,
            })
    return issues


def validate_missing_h1(lines: list[str], is_inside_code) -> list[dict]:
    """A document must have exactly one H1 — the other half of `validate_single_h1`.

    `validate_single_h1` only fires above one H1, so a document with *none* used to
    pass validation with zero issues while still breaking the rule kb-polish states
    as hard ("exactly one H1"). The failure is silent and it lands downstream:
    kb-ingest falls back to the file stem for `title`, which quietly degrades
    routing without a single line anywhere saying so.

    kb-pilot's reason for the rule is in kb-ingest: H1 is the document title and
    never enters the tree, so the tree starts at H2.
    """
    for i, line in enumerate(lines, 1):
        if is_inside_code(i):
            continue
        h = _heading(line)
        if h and h[0] == 1:
            return []
    return [{
        "type": "missing_h1",
        "line": 0,
        "detail": "no H1 heading in the document (kb-pilot requires exactly one; H1 is the title)",
        "text": "",
    }]


def validate_headings_present(lines: list[str], is_inside_code) -> list[dict]:
    """The tree must not be empty: kb-ingest needs at least one H2+ heading.

    This is the check that closes a cross-skill blind spot. A document written in
    setext style (`Title` underlined with `===`) or one with no ATX headings at all
    used to report zero issues here, then fail at ingest with "no headings below
    H1" — kb-polish's Step 4 acceptance loop ("re-run Step 2 until zero issues")
    had already waved it through. Reporting it here means the same fact surfaces at
    the stage that can still fix it.

    Only levels 2+ count, because H1 is the title and never enters the tree.
    """
    for i, line in enumerate(lines, 1):
        if is_inside_code(i):
            continue
        h = _heading(line)
        if h and h[0] >= 2:
            return []
    return [{
        "type": "no_headings",
        "line": 0,
        "detail": "no H2+ headings; kb-ingest would build an empty tree (H1 is the title, not a node)",
        "text": "",
    }]


def validate_tables(lines: list[str], is_inside_code) -> list[dict]:
    issues = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if is_inside_code(i + 1) or not line.strip().startswith("|"):
            i += 1
            continue
        # find the contiguous table block
        block = []
        j = i
        while j < len(lines) and lines[j].strip().startswith("|"):
            block.append((j + 1, lines[j]))
            j += 1
        if len(block) >= 2:
            header_cols = _count_cols(block[0][1])
            # the second line should be the separator row
            sep_cols = _count_cols(block[1][1]) if len(block) > 1 else 0
            if sep_cols != header_cols:
                issues.append({
                    "type": "table_separator_mismatch",
                    "line": block[1][0],
                    "detail": f"header {header_cols} cols vs separator row {sep_cols} cols",
                })
            for row_line, row in block[2:]:
                cols = _count_cols(row)
                if cols != header_cols:
                    issues.append({
                        "type": "table_col_mismatch",
                        "line": row_line,
                        "detail": f"header {header_cols} cols vs data row {cols} cols",
                        "text": row.strip()[:80],
                    })
        i = j
    return issues


def _count_cols(row: str) -> int:
    # count columns split by non-escaped pipes
    # Known boundary: callers only reach this for lines whose first non-space char
    # is "|", so pipe-less (raw pipe-text) or other table dialects are not counted.
    return len(re.findall(r"(?<!\\)\|", row.strip())) - 1


def validate_codeblock_lang(lines: list[str], regions) -> list[dict]:
    issues = []
    # only check whether each code block's opening fence has a language tag
    for start, _end in regions:
        stripped = lines[start - 1].strip()
        if stripped.startswith("```") and len(stripped) == 3:
            issues.append({
                "type": "codeblock_no_lang",
                "line": start,
                "detail": "code block missing a language tag (e.g. ```python)",
            })
    return issues


def validate_image_paths(lines: list[str], is_inside_code, base_dir: Path) -> list[dict]:
    issues = []
    for i, line in enumerate(lines, 1):
        if is_inside_code(i):
            continue
        for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", line):
            raw_path = m.group(1).strip()
            if raw_path.startswith(("http://", "https://", "data:")):
                continue
            # drop any trailing title part
            path_part = raw_path.split(" ")[0]
            if not path_part:
                continue
            resolved = (base_dir / path_part).resolve() if not Path(path_part).is_absolute() else Path(path_part)
            if not resolved.exists():
                issues.append({
                    "type": "image_missing",
                    "line": i,
                    "detail": f"image reference path does not exist: {path_part}",
                })
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="mechanical Markdown structure validation (deterministic skeleton check; semantics left to the LLM).",
        epilog="""Examples:
  python validate_structure.py raw.md

Checks: heading jumps / duplicate headings / multiple H1 / missing H1 / no H2+
headings / table cols / code-block language / image paths

`missing_h1` and `no_headings` exist because a document can otherwise pass with
zero issues and still fail at ingest: kb-polish requires exactly one H1, and
kb-ingest builds an empty tree from a document with no H2+ headings. Both were
silent before, and silence at validation time is the failure that reaches the user.

Heading rules are borrowed from kb-ingest when it sits next to this skill. If it
does not, the heading checks are skipped and the output's `skipped` list says so —
the script still runs and reports the table/code/image checks.

Output: JSON to stdout; progress to stderr. The issue list states mechanical
facts; judging severity is the LLM's job.

Exit codes:
  0  validation completed — read "issues" in the JSON (findings are a result,
     not an error; a clean document and a broken one both exit 0)
  1  bad args, or the file does not exist""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="path to the Markdown file")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"[validate] file not found: {input_path}", file=sys.stderr)
        return 1

    lines = input_path.read_text(encoding="utf-8-sig").splitlines()
    skeleton = _load_skeleton()
    if skeleton is not None:
        regions = skeleton.find_code_fence_regions(lines)
        is_inside_code = skeleton.make_fence_checker(regions)
        issues = []
        issues += validate_heading_continuity(lines, is_inside_code)
        issues += validate_duplicate_headings(lines, is_inside_code)
        issues += validate_single_h1(lines, is_inside_code)
        issues += validate_missing_h1(lines, is_inside_code)
        issues += validate_headings_present(lines, is_inside_code)
        skipped = []
    else:
        regions = []
        is_inside_code = lambda _n: False
        issues = []
        skipped = [
            "kb-ingest's build_tree.py not found next to this skill; "
            "heading checks skipped (table/code/image checks still ran)"
        ]
    issues += validate_tables(lines, is_inside_code)
    issues += validate_codeblock_lang(lines, regions)
    issues += validate_image_paths(lines, is_inside_code, input_path.parent)

    result = {
        "ok": True,
        "input": str(input_path),
        "issue_count": len(issues),
        "issues": issues,
        "skipped": skipped,
    }

    # progress to stderr, structured result to stdout (the LLM parses stdout)
    print(f"[validate] found {len(issues)} issues", file=sys.stderr)
    for iss in issues:
        print(
            f"[validate] L{iss['line']} [{iss['type']}] {iss['detail']}",
            file=sys.stderr,
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
