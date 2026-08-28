#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
check_drift.py — content-drift spot check (re-render output vs verify ground truth).

Deterministic layer: extract the set of numeric/amount tokens from the verify ground
truth (verify_text.txt, produced by extract_verify.py), and check whether the re-render
output (final.md) contains all of them, locating lost or rewritten content.
This is the mechanical backstop of the Step 4 validation loop; semantic cross-checks
remain the LLM's job.

Usage:
    python check_drift.py verify_text.txt final.md
    python check_drift.py verify_text.txt final.md --stdout-json
    python check_drift.py verify_text.txt final_1.md final_2.md   # combine multiple outputs

Output (stdout):
    {"ok": true, "truth_chars": N, "target_chars": N,
     "missing_tokens": [...], "missing_count": N, ...}

Exit codes:
    0  success (missing may be 0 or >0 — the drift result is in the JSON; the LLM/caller judges)
    1  bad args or file not found
"""

import argparse
import json
import re
import sys
from pathlib import Path

# numeric/amount patterns (aligned with common document content: HKD/USD/CNY amounts, percentages, years, days, monthly interest)
TOKEN_PATTERNS = [
    r"HK\$\s?[\d,]+(?:\.\d+)?",
    r"US\$\s?[\d,]+(?:\.\d+)?",
    r"人民幣\s?[\d,]+(?:\.\d+)?元",
    r"[\d]+(?:\.\d+)?%",
    r"月息\s?[\d.]+%",
    r"(?<!\d)[\d.]+\s*年",
    r"(?<!\d)\d+\s*天",
]


def extract_tokens(text: str) -> set:
    """Extract all numeric/amount tokens from the text."""
    toks = set()
    for pat in TOKEN_PATTERNS:
        for m in re.finditer(pat, text):
            toks.add(m.group(0).replace(" ", ""))
    return toks


def main() -> int:
    parser = argparse.ArgumentParser(
        description="content-drift spot check: do all ground-truth numeric tokens appear in the re-render output?",
        epilog="""示例:
  python check_drift.py verify_text.txt final.md
  python check_drift.py verify_text.txt final_1.md final_2.md --stdout-json

Rule: a token present in the truth but missing from the output is a content-loss or
rewrite signal (e.g. HK$6,000 not appearing). The caller (LLM/user) judges whether the
missing list is drift or an intentional removal (e.g. footer amounts).""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("truth", help="verify ground-truth file (extract_verify.py's verify_text.txt)")
    parser.add_argument("targets", nargs="+", help="re-render outputs (final.md or final_1.md final_2.md...)")
    parser.add_argument("--stdout-json", action="store_true", help="output result as JSON on stdout")
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

    truth_tokens = extract_tokens(truth_text)
    target_tokens = extract_tokens(target_text)
    missing = sorted(truth_tokens - target_tokens)

    result = {
        "ok": len(missing) == 0,
        "truth_chars": len(truth_text),
        "target_chars": len(target_text),
        "truth_token_count": len(truth_tokens),
        "target_token_count": len(target_tokens),
        "missing_count": len(missing),
        "missing_tokens": missing,
        "note": "missing tokens need human judgment: could be drift, or an intentional removal in the output (e.g. footer amounts)",
    }

    if args.stdout_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[check_drift] truth tokens {len(truth_tokens)}, missing {len(missing)}", file=sys.stderr)
        for m in missing:
            print(f"[check_drift]  MISSING: {m}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
