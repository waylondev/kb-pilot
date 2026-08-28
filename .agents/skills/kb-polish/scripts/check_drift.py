#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
check_drift.py — content-drift spot check (re-render output vs verify ground truth).

Deterministic layer: extract the set of numeric tokens from the verify ground truth
(verify_text.txt, produced by extract_verify.py) and check whether the re-render
output (final.md) contains all of them, locating lost or rewritten content.
This is the mechanical backstop of the Step 4 validation loop; semantic cross-checks
remain the LLM's job.

Two tiers of tokens are checked, because their drift signal differs:
  structured  currency amounts, percentages, periods — a missing one is almost
              certainly real content loss
  numeric     any bare number — noisier, but it stops the check from silently
              passing on documents that contain no currency or percentages

Usage:
    python check_drift.py verify_text.txt final.md
    python check_drift.py verify_text.txt final_1.md final_2.md   # combine multiple outputs

Output (stdout):
    {"ok": true, "truth_chars": N, "target_chars": N,
     "missing_structured": [...], "missing_numeric": [...], "missing_count": N, ...}

Exit codes:
    0  success (missing may be 0 or >0 — the drift result is in the JSON; the LLM/caller judges)
    1  bad args or file not found
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Structured figures — currency amounts, percentages, periods. These carry enough
# shape that a missing one is almost certainly real content loss, so they are
# reported separately from bare numbers.
TOKEN_PATTERNS = [
    r"HK\$\s?[\d,]+(?:\.\d+)?",
    r"US\$\s?[\d,]+(?:\.\d+)?",
    r"[¥￥$]\s?[\d,]+(?:\.\d+)?",
    r"人民幣\s?[\d,]+(?:\.\d+)?元",
    r"[\d]+(?:\.\d+)?%",
    r"月息\s?[\d.]+%",
    r"(?<!\d)[\d.]+\s*年",
    r"(?<!\d)\d+\s*天",
]

# Bare numbers, so the check is not a no-op on documents that contain no currency
# or percentages. Without this, a technical or policy document matches nothing and
# the script reports zero drift no matter how much was lost. The lookbehind skips
# identifier-ish numbers (page_1, v2), which are noise rather than content.
GENERIC_NUMERIC = r"(?<![A-Za-z_])\d[\d,]*(?:\.\d+)?"


def extract_tokens(text: str, patterns=None) -> set:
    """Extract numeric tokens; defaults to structured figures plus bare numbers."""
    toks = set()
    for pat in (list(TOKEN_PATTERNS) + [GENERIC_NUMERIC] if patterns is None else patterns):
        for m in re.finditer(pat, text):
            toks.add(m.group(0).replace(" ", ""))
    return toks


def drop_subsumed(tokens: list) -> list:
    """Drop tokens wholly contained in another token.

    The currency patterns overlap by design, so a missing `HK$6,000` also yields
    `$6,000` from the generic-currency pattern. Reporting both is noise. Bare
    numbers are left alone, since there `20` and `2026` can be genuinely distinct.
    """
    return [t for t in tokens if not any(t != o and t in o for o in tokens)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="content-drift spot check: do all ground-truth numeric tokens appear in the re-render output?",
        epilog="""Examples:
  python check_drift.py verify_text.txt final.md
  python check_drift.py verify_text.txt final_1.md final_2.md

Rule: a token present in the truth but missing from the output is a content-loss or
rewrite signal (e.g. HK$6,000 not appearing). missing_structured is high-confidence;
missing_numeric is noisier and needs the document as context — a hit may be drift, an
intentional removal (footer amounts), or a reformat (6,000 -> 6000).

Passing proves no numeric drift, never that the content is unchanged — prose drift
is the LLM's judgment.

Output: JSON to stdout; progress to stderr.

Exit codes:
  0  check completed — missing_count may be 0 or >0; the drift result is in the
     JSON and judging it is the caller's job, not an exit code's
  1  bad args, or an input file does not exist""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("truth", help="verify ground-truth file (extract_verify.py's verify_text.txt)")
    parser.add_argument("targets", nargs="+", help="re-render outputs (final.md or final_1.md final_2.md...)")
    args = parser.parse_args()

    truth_path = Path(args.truth)
    if not truth_path.is_file():
        print(f"[check_drift] truth file not found: {truth_path}", file=sys.stderr)
        return 1
    for t in args.targets:
        if not Path(t).is_file():
            print(f"[check_drift] output file not found: {t}", file=sys.stderr)
            return 1

    truth_text = truth_path.read_text(encoding="utf-8")
    target_text = "".join(Path(t).read_text(encoding="utf-8") for t in args.targets)

    truth_structured = extract_tokens(truth_text, TOKEN_PATTERNS)
    target_structured = extract_tokens(target_text, TOKEN_PATTERNS)
    truth_numeric = extract_tokens(truth_text, [GENERIC_NUMERIC])
    target_numeric = extract_tokens(target_text, [GENERIC_NUMERIC])

    missing_structured = drop_subsumed(sorted(truth_structured - target_structured))
    missing_numeric = sorted(truth_numeric - target_numeric)

    result = {
        "ok": not missing_structured and not missing_numeric,
        "truth_chars": len(truth_text),
        "target_chars": len(target_text),
        "truth_token_count": len(truth_structured | truth_numeric),
        "target_token_count": len(target_structured | target_numeric),
        "missing_count": len(missing_structured) + len(missing_numeric),
        "missing_structured": missing_structured,
        "missing_numeric": missing_numeric,
        "coverage": (
            "structured figures + bare numbers"
            if truth_structured
            else "bare numbers only — the ground truth has no currency/percentage figures, "
                 "so structured checking adds nothing for this document"
        ),
        "note": (
            "missing_structured (currency/percent/period) is almost certainly real content loss. "
            "missing_numeric lists bare numbers and is noisier: a hit may be drift, an intentional "
            "removal (footer amounts), or a reformat (6,000 -> 6000) — judge against the document. "
            "Passing this check proves no numeric drift, never that the content is unchanged."
        ),
    }

    # progress to stderr, structured result to stdout (the LLM parses stdout)
    print(
        f"[check_drift] truth tokens {len(truth_structured | truth_numeric)}, "
        f"missing {len(missing_structured) + len(missing_numeric)} "
        f"(structured {len(missing_structured)})",
        file=sys.stderr,
    )
    for m in missing_structured:
        print(f"[check_drift]  MISSING (structured): {m}", file=sys.stderr)
    for m in missing_numeric:
        print(f"[check_drift]  MISSING (numeric): {m}", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
