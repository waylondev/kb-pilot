#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
validate_structure.py — mechanical Markdown structure validation.

Deterministic layer: checks only mechanical "skeleton" issues (heading jumps, table
column counts, list indentation, etc.) and outputs a structured issue list for the LLM.
Semantic dimensions (heading-meaning clarity, truncation & mojibake) are the LLM's job;
this script does no semantic judgment.

Usage:
    python validate_structure.py raw.md
    python validate_structure.py raw.md --stdout-json

Output (stdout):
    {"ok": true, "issues": [...], "mechanical_scores": {...}}

Exit codes:
    0  success
    1  bad args or file not found
"""

import argparse
import json
import re
import sys
from pathlib import Path

# mechanical check dimensions (the skeleton part of workflow.md Step 2)
# semantic dimensions (heading-meaning clarity 20%, truncation & mojibake 10%) are the LLM's job

MAX_WEIGHT = {
    "heading_continuity": 30,  # heading-level continuity (mechanically checkable part)
    "table_integrity": 20,     # table structural integrity (mechanically checkable part)
    "list_consistency": 10,    # list format consistency
    "codeblock_lang": 10,      # code-block language annotation
    "image_path": 10,          # image reference path existence
}


def find_code_fence_regions(lines: list[str]) -> list[tuple[int, int]]:
    """Return code-fence line regions [(start, end), ...] (inclusive 1-based lines)."""
    regions = []
    in_fence = False
    start = 0
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_fence:
                in_fence = True
                start = i
            else:
                in_fence = False
                regions.append((start, i))
    if in_fence:
        regions.append((start, len(lines)))
    return regions


def is_inside_code(i: int, regions: list[tuple[int, int]]) -> bool:
    return any(start <= i <= end for start, end in regions)


def validate_heading_continuity(lines: list[str], regions) -> list[dict]:
    issues = []
    prev_level = None
    for i, line in enumerate(lines, 1):
        if is_inside_code(i, regions):
            continue
        m = re.match(r"^(#{1,6})\s+", line)
        if not m:
            continue
        level = len(m.group(1))
        if prev_level is not None and level > prev_level + 1:
            issues.append({
                "type": "heading_jump",
                "line": i,
                "detail": f"heading level jump: {prev_level} -> {level} (fill in the missing levels)",
                "text": line.strip(),
            })
        prev_level = level
    return issues


def validate_duplicate_headings(lines: list[str], regions) -> list[dict]:
    seen = {}
    issues = []
    for i, line in enumerate(lines, 1):
        if is_inside_code(i, regions):
            continue
        m = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if not m:
            continue
        text = m.group(2).strip()
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


def validate_single_h1(lines: list[str], regions) -> list[dict]:
    """A document must have exactly one H1.

    kb-pilot rule: H1 is the document title, not in the tree (the tree starts at H2),
    see kb-ingest Gotchas. Multiple H1s distort the structure; later blocks should be
    demoted to H2 during re-render.
    Note: `^#\\s+` only matches `# ` (`## `/`### ` are naturally excluded because the
    second char is non-space).
    """
    h1_lines = []
    for i, line in enumerate(lines, 1):
        if is_inside_code(i, regions):
            continue
        if re.match(r"^#\s+", line):
            h1_lines.append((i, line.strip()))
    issues = []
    if len(h1_lines) > 1:
        first_line = h1_lines[0][0]
        for i, text in h1_lines[1:]:
            issues.append({
                "type": "multiple_h1",
                "line": i,
                "detail": (
                    f"multiple H1 headings (first at line {first_line}): {text}. "
                    "kb-pilot requires a single H1 (document title); later blocks should be demoted to H2"
                ),
                "text": text,
            })
    return issues


def validate_tables(lines: list[str], regions) -> list[dict]:
    issues = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if is_inside_code(i + 1, regions) or not line.strip().startswith("|"):
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
    return len(re.findall(r"(?<!\\)\|", row.strip())) - 1


def validate_lists(lines: list[str], regions) -> list[dict]:
    issues = []
    markers = {}
    for i, line in enumerate(lines, 1):
        if is_inside_code(i, regions):
            continue
        stripped = line.strip()
        m = re.match(r"^([-*+])\s+", stripped)
        if m:
            markers.setdefault(m.group(1), []).append(i)
    if len(markers) > 1:
        summary = ", ".join(f"{k}({len(v)}x)" for k, v in markers.items())
        first_lines = [str(v[0]) for v in markers.values()]
        issues.append({
            "type": "list_marker_mixed",
            "line": int(first_lines[0]),
            "detail": f"mixed list markers: {summary} (recommend unifying to one)",
        })
    return issues


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


def validate_image_paths(lines: list[str], regions, base_dir: Path) -> list[dict]:
    issues = []
    for i, line in enumerate(lines, 1):
        if is_inside_code(i, regions):
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
  python validate_structure.py raw.md --stdout-json

Checks: heading jumps / duplicate headings / multiple H1 / table cols / list markers / code-block language / image paths""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="path to the Markdown file")
    parser.add_argument("--stdout-json", action="store_true", help="output result as JSON on stdout")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"[validate] file not found: {input_path}", file=sys.stderr)
        return 1

    lines = input_path.read_text(encoding="utf-8-sig").splitlines()
    regions = find_code_fence_regions(lines)

    issues = []
    issues += validate_heading_continuity(lines, regions)
    issues += validate_duplicate_headings(lines, regions)
    issues += validate_single_h1(lines, regions)
    issues += validate_tables(lines, regions)
    issues += validate_lists(lines, regions)
    issues += validate_codeblock_lang(lines, regions)
    issues += validate_image_paths(lines, regions, input_path.parent)

    # mechanical score: each dimension starts at 0 and is deducted per issue
    mechanical_scores = {}
    for dim, weight in MAX_WEIGHT.items():
        dim_issues = [x for x in issues if x["type"].startswith(_dim_prefix(dim))]
        mechanical_scores[dim] = max(0, weight - len(dim_issues) * _penalty_per_issue(dim))

    result = {
        "ok": True,
        "input": str(input_path),
        "issue_count": len(issues),
        "issues": issues,
        "mechanical_scores": mechanical_scores,
        "note": "mechanical score is indicative only; semantic dimensions (heading meaning / truncation / mojibake) need the LLM",
    }

    if args.stdout_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[validate] found {len(issues)} issues", file=sys.stderr)
        for iss in issues:
            print(
                f"[validate] L{iss['line']} [{iss['type']}] {iss['detail']}",
                file=sys.stderr,
            )

    return 0


def _dim_prefix(dim: str) -> str:
    return {
        "heading_continuity": "heading_",
        "table_integrity": "table_",
        "list_consistency": "list_",
        "codeblock_lang": "codeblock_",
        "image_path": "image_",
    }.get(dim, dim + "_")


def _penalty_per_issue(dim: str) -> int:
    # heading jumps matter more: -5 each; others -3
    return 5 if dim in ("heading_continuity", "table_integrity") else 3


if __name__ == "__main__":
    sys.exit(main())
