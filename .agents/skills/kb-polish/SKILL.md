---
name: kb-polish
description: Convert source documents into high-quality Markdown conforming to the kb-pilot spec — PDF, Word (docx/docm), Excel (xlsx/xlsm), PowerPoint (pptx/pptm/ppsx/ppsm), EPUB, CSV, RTF and OpenDocument (odt/ods/odp). Runs AnyDoc coarse conversion, structure validation & scoring, content verification (deterministic extraction cross-check), and normalization. Does NOT OCR; pure scans (no text layer) are kept by embedding every page as an image. Use when the user needs a document converted to Markdown, PDF-to-MD, Word-to-MD, ODT-to-MD, RTF-to-MD, pre-ingestion preprocessing (kb-ingest), or conversion-quality verification.
license: MIT
compatibility: Requires Python 3.10+; dependencies firecrawl-anydoc (AnyDoc conversion), pymupdf (PDF verify source), striprtf (RTF verify source); scripts need a Bash/python environment. validate_structure.py borrows the Markdown skeleton parser from the kb-ingest skill, so the two must be installed together.
allowed-tools: Bash(python:* pip:*) Read Write
metadata:
  version: "1.3.2"
---
# kb-polish Skill
> Convert source documents into high-quality Markdown that meets kb-pilot ingestion standards.

## Quick guide (5 steps, run in order; complete each before the next)

- [ ] 1. **AnyDoc coarse conversion**: `python scripts/convert_document.py {input} -o {outdir}` — produces `raw.md` and extracts embedded assets (`images/`, `attachments/`)
- [ ] 2. **Structure validation & scoring**: `python scripts/validate_structure.py {outdir}/raw.md` — mechanical checks (heading jumps/duplicates, table column counts, lists, code blocks, image paths); semantic dimensions are assessed by the LLM using the issue list
- [ ] 3. **Content verification**: `python scripts/extract_verify.py {input} -o {outdir} --save-text` dispatches to format plugins to extract a **deterministic source text** (`verify_text.txt`, text layer / OOXML plaintext, seconds; runs by default, whatever the Step 2 score). For PDF it **also extracts embedded images into `{outdir}/images/`** and emits `[image: <name>]` placeholders (the docx/pptx/epub convention), since AnyDoc does not expose PDF assets. The LLM cross-checks the source against `raw.md` — full comparison when the Step 2 score is low or the doc is table/number-heavy, otherwise a light spot-check. **Scans (no text layer): every page is rendered to `images/page_N.png` and embedded as `![page N](./images/page_N.png)`** so the asset survives for viewing — kb-polish still does no OCR, so tell the user the pages are images only (the LLM cannot read their content)
- [ ] 4. **LLM re-render**: treat `verify_text.txt` as the **content ground truth** and `raw.md` as the structural skeleton, then organize into standard Markdown (see output template). **Hard rules: preserve original content and do not change logical relationships** (section order / table rows & columns / list nesting / clause ownership); **exactly one H1** — multiple H1 blocks are demoted & merged by default (the main title keeps H1, the rest become H2 with levels shifted down); split only when blocks are fully independent. After re-rendering, re-run Step 2 to confirm zero issues, and run `scripts/check_drift.py` to confirm **no numeric token is lost** (a numbers-only check — it proves no numeric drift, not zero content change). If the documents use figures the built-in patterns do not recognise (a local currency word, a statutory period, a product code), pass them with `--extra-pattern` — repeatable. The script ships **format-shaped patterns only** (an amount, a percentage); a corpus's vocabulary belongs on the command line, never baked into a shared skill
- [ ] 5. **Human confirmation**: after the user confirms, hand off to `kb-ingest`

## Output structure template (standard skeleton for final.md)

```markdown
# [Single document title]              ← only one # in the whole file (kb-pilot: H1 is the title, not part of the tree)
## [Section]                           ← tree starts at H2
### [Subsection, optional]             ← continuous levels, no jumps
| Header | Col | ... |                ← rows/columns map 1:1 to the source
|---|---|---|
| data | ... | ... |                  ← values/wording preserved verbatim
## [Next section]
```

> Constraints: body text is preserved verbatim (including traditional characters / original spelling / terms); no polishing, no completion, no reordering of logic; strip headers/footers; demote & merge multiple H1 by default.

> Scripts only do deterministic work (conversion, extraction, mechanical validation). Semantic judgments (heading meaning, truncation, image placement) are entirely the LLM's job, following the kb-pilot principle "scripts own the skeleton, the LLM owns the content".

## Gotchas (field-tested pitfalls, read first)

- **No OCR on scans — embed pages as images instead**: scans (no text layer) are not readable as text, but the document is not dropped. Step 3 renders every page to `images/page_N.png` and the re-render keeps them as `![page N](./images/page_N.png)` (with a "scanned / image-only, no text layer" note). The LLM must not guess page content — it is an image-only asset for viewing, not a text source
- **AnyDoc does not support .html/.md/.txt/.tsv**: raises `UnsupportedError` / unrecognized extension. html/md/txt are already text — ingest directly, do not run this skill; **.tsv must be renamed to .csv** first (content is identical)
- **AnyDoc handles .odp very weakly** (field-tested: only the title text is converted; body/tables are lost): convert ODP to .pptx first
- **Complex merged-cell tables get mangled by AnyDoc** (misaligned data, split text, reordered cells): such documents must go through Step 3 verification
- **RTF Chinese text is garbled by AnyDoc conversion** (UTF-8 decoded as Latin-1, field-tested); but the verify source (striprtf) extracts correctly — **rely on Step 3/4 rebuilding from the ground truth**; this is the typical value case for double cross-checking
- **PDFs using CID fonts (no ToUnicode CMap) are misjudged as "needs OCR"** by AnyDoc: real scans take the image-embedding branch; if a text-layer PDF reports needs OCR it is usually missing ToUnicode — ask the user to re-export with an embedded font
- **PDF images need the PyMuPDF fallback**: AnyDoc's `to_document()` does not support PDF (PDF converts via `to_markdown` directly, so no `assets`), and its PDF markdown carries no `![` references. kb-polish extracts PDF embedded images in Step 3 via PyMuPDF's block-level `get_text("dict")` view — image blocks appear **exactly where the source lays them out**, emitting `[image: <name>]` placeholders (and their bytes) in place, right in the flow. A geometry-matched `doc.extract_image()` fallback covers blocks whose decoded bytes are missing. Same convention as docx/pptx/epub
- **EPUB heading levels get flattened** (`<h1>`/`<h2>` are all turned into `#`, producing duplicate H1s, field-tested): Step 2's `multiple_h1`/`duplicate_heading` catches this; Step 4 handles the single-H1 rule
- **Headers/footers misread as headings** (page numbers, org names, doc numbers): Step 4 demotes them to body text or deletes them; repeated document titles across pages are merged
- **Empty PDF text layer = scan signal**: `extract_verify.py` warns, renders each page to `images/page_N.png`, and the re-render keeps them as `![page N](./images/page_N.png)` — image-only asset, no OCR, no invented text
- **Image placement**: inline images in all source formats appear in the verify source as `[image: <filename>]` placeholders (structural markers emitted by scripts, not body content); Step 4 converts them to `![](./images/<filename>)`. The files are landed in `images/` — by convert (docx/pptx/xlsx/odt/epub via AnyDoc `to_document`) or by verify (PDF via PyMuPDF). If raw.md has image alt text but the ground truth has no placeholder, trust the ground truth; do not insert images speculatively
- **Re-render is not rewriting**: Step 4 rebuilds Markdown from the verified ground truth, but content must change by zero — no polishing, no completion, no reordering (section order / table rows & columns / list nesting / clause ownership). When ground truth is missing, mark "original is empty here", never guess
- **Exactly one H1; multiple H1s demote & merge by default**: kb-pilot treats H1 as the document title (not in the tree; the tree starts at H2). Standard Markdown allows multiple H1s, but multiple H1 blocks in one input file are usually related (e.g. a credit-card PDF = notices/statements + product summary), so **merge into one final by default: keep the main title as H1, demote the rest to H2 with internal levels shifted**; delete redundant headers/cross-page duplicates. Only split when the blocks are fully independent. `validate_structure.py`'s `multiple_h1` guards against multiple H1s in a single file
- **Do not use scripts for semantic judgment**: `validate_structure.py` only checks mechanical structure; heading semantics / content truncation are for the LLM to assess — don't expect the script score to replace the LLM
- **Batch use needs no batch script**: this skill is single-file by design. For many documents, run these 5 steps **per file**, one document at a time, with isolated outputs — like kb-ingest's batch walk. The LLM drives the repetition; scripts stay single-responsibility

## Detailed docs (when to load)

- `references/workflow.md`: complete 5-step execution flow. **Read when reaching Step 2 scoring / Step 3 verification / Step 4 re-render**, includes verification details and the format mapping table
- `references/rules.md`: processing boundaries and scoring criteria. **Read before Step 4 re-render**, to avoid altering body content, misaligning tables, or changing logical relationships

## Scripts

- `scripts/convert_document.py`: AnyDoc conversion + embedded asset extraction (markdown + images/ + attachments/)
- `scripts/validate_structure.py`: mechanical Markdown structure validation (issue list + mechanical score, for the LLM to score). It does **not** carry its own Markdown parser — it borrows kb-ingest's `build_tree.py`, deriving the path from its own location, so "what counts as a heading" is decided in exactly one place
- `scripts/extract_verify.py`: verify-source extraction entry (dispatches to verifiers/ plugins by format; outputs source text for LLM cross-check)
- `scripts/check_drift.py`: content-drift spot check (numeric tokens in verify_text vs final.md; outputs the missing list; used in the Step 4 validation loop)
- `scripts/verifiers/`: format verification plugins, one file per format (pdf/docx/pptx/xlsx/odt/epub/rtf/csv), aligned with AnyDoc-supported formats
