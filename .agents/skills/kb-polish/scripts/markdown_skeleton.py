#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
markdown_skeleton.py — what counts as a heading, and what is inside a code fence.

This is kb-polish's own copy of the skeleton rules, so the skill stands alone and
publishes independently. kb-ingest's `build_tree` carries the same rules for the
same reason; the two copies are pinned behaviour-identical by the cross-skill
contract tests in tests/test_consistency.py, not by importing a sibling. If one
side changes, that test goes red and forces the other to follow.

Follows CommonMark:
- ATX heading: 1-6 `#`, at least one non-space char after them, trailing `#`
  sequence stripped from the title. `#heading` (no space) is a paragraph, not a
  heading.
- Fenced code block: ``` or ~~~ (3+ chars, up to 3 leading spaces); the closing
  fence must use the same character and be at least as long; a backtick fence's
  info string may not contain a backtick; an unterminated fence runs to EOF. A
  `# comment` inside a fence is code, not a heading.
"""

import bisect
import re

FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def heading(line: str):
    """Return (level, title) if `line` is an ATX heading, else None."""
    m = HEADING_RE.match(line)
    if not m:
        return None
    return len(m.group(1)), m.group(2).strip()


def find_code_fence_regions(lines: list) -> list:
    """Return fenced code regions as [(start, end), ...] with 1-based inclusive lines."""
    regions = []
    open_char = ""
    open_len = 0
    start = 0

    for i, line in enumerate(lines, 1):
        if open_char:
            m = FENCE_CLOSE_RE.match(line)
            if m and m.group(1)[0] == open_char and len(m.group(1)) >= open_len:
                regions.append((start, i))
                open_char, open_len, start = "", 0, 0
            continue

        m = FENCE_OPEN_RE.match(line)
        if not m:
            continue
        fence = m.group(1)
        # A backtick fence's info string may not contain a backtick (CommonMark)
        if fence[0] == "`" and "`" in m.group(2):
            continue
        open_char, open_len, start = fence[0], len(fence), i

    if open_char:
        regions.append((start, len(lines)))  # unterminated fence runs to EOF
    return regions


def make_fence_checker(regions: list):
    """Return an O(log n) predicate `is_inside_code(line_no)` for the given regions."""
    if not regions:
        return lambda line_no: False
    starts = [r[0] for r in regions]

    def is_inside_code(line_no: int) -> bool:
        idx = bisect.bisect_right(starts, line_no) - 1
        return idx >= 0 and line_no <= regions[idx][1]

    return is_inside_code
