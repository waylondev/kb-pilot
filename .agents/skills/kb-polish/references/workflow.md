# kb-polish detailed workflow

## 1. AnyDoc coarse conversion (Step 1)

### Goal

Convert the source document into a first-draft Markdown and extract all embedded files.

### Actions

Call the bundled script (deterministic conversion + asset extraction in one step):

```bash
# Install dependencies (one-time)
pip install firecrawl-anydoc

# Convert + extract (markdown + images/ + attachments/); result as JSON on stdout
python scripts/convert_document.py {input_file} -o {output_dir}
```

Internally the script uses the AnyDoc Python API (`anydoc.to_markdown(path)` for conversion, `anydoc.to_document(bytes)` for asset extraction). No hand-written parsing. Source: `scripts/convert_document.py`.

### Outputs

* `raw.md`: first-draft Markdown

* `images/`: extracted image files

* `attachments/`: extracted embedded files (PDF, Excel, etc.)

### Boundaries (field-tested on 2026-08-28 full-format matrix)

* AnyDoc supports Excel (.xlsx/.xls/.xlsm/.xlsb/.ods), Word (.docx/.doc/.docm/.odt/.rtf), PowerPoint (.pptx/.ppt/.pptm/.odp), EPUB (.epub), CSV (.csv), PDF (.pdf), but **does not support OCR**; pure scans (no text layer) are **kept by embedding every page as an image** (no OCR — see the scan branch in Step 4)

* AnyDoc **does not support .html/.md/.txt/.tsv** (raises `UnsupportedError` / unrecognized extension): html/md/txt are already text, ingest directly; **.tsv must be renamed to .csv** before conversion (content is identical)

* **AnyDoc handles .odp very weakly** (field-tested: only the title text survives; body/tables lost): convert ODP to .pptx first

* **RTF Chinese is garbled by AnyDoc conversion** (UTF-8 decoded as Latin-1, field-tested); the verify source (striprtf) extracts correctly — **rely on Step 3/4 rebuilding from the ground truth**; this is the typical value case for double cross-checking

* **PDFs using CID fonts (no ToUnicode CMap) are misjudged as "needs OCR"**: real scans take the image-embedding branch; if a text-layer PDF reports needs OCR it usually lacks ToUnicode — ask the user to re-export with an embedded font

* **PDF images need the PyMuPDF fallback**: AnyDoc's `to_document()` does not support PDF (PDF converts via `to_markdown` directly, so no `assets`), and PDF markdown carries no `![` references. kb-polish extracts PDF embedded images in Step 3 via PyMuPDF's block-level `get_text("dict")` view — image blocks appear **exactly where the source lays them out**, emitting `[image: <name>]` placeholders (and their bytes) in place. A geometry-matched `doc.extract_image()` fallback covers blocks whose decoded bytes are missing. Same convention as docx/pptx/epub

* **EPUB heading levels get flattened** (`<h1>`/`<h2>` all become `#`, producing duplicate H1s, field-tested): Step 2's `multiple_h1`/`duplicate_heading` catches it; Step 4 applies the single-H1 rule

* AnyDoc does not recursively convert nested files (e.g. an Excel attachment inside Word), but `to_document().assets` **can extract OLE embedded attachments** (field-tested: a .xlsx inside .docx lands in `attachments/`); handle that attachment separately, do not merge it into the body Markdown

* In the converted Markdown, images appear as alt text; **image reference placement (`![](./images/xxx.png)`) is the LLM's job in Step 4**

> **Batch use**: this workflow is per-file by design — no batch script. For many documents the LLM drives each file through Steps 1-5 one at a time (like kb-ingest's batch walk: repeat per file, isolated outputs). Scripts stay single-responsibility; the LLM handles repetition.

## 2. Structure validation (Step 2)

### Goal

Assess the structural quality of the first-draft Markdown and decide how deep the Step 3 content cross-check should be. Step 3's deterministic extraction runs for every document regardless.

### Actions

First run the mechanical structure check (deterministic skeleton):

```bash
python scripts/validate_structure.py {output_dir}/raw.md
```

The script outputs an `issues` list (heading jumps, duplicate headings, inconsistent table column counts, code blocks without a language tag, missing image paths). Severity is not scored — the LLM judges it from the issue list.

**LLM responsibility (scripts do no semantic judgment):**

* Weigh the issues against the document type (table/number-heavy, long, multi-format) and decide whether Step 3 does a full or a light cross-check

### Cross-check depth

Step 3's deterministic extraction (`extract_verify.py`, seconds) runs **for every document, unconditionally** — it is cheap and it is what gives Step 4 a ground truth. How deep the LLM cross-checks is its own judgment: weigh the issue list against the document type. A well-headed document can still have mangled tables or numbers, so table/number-heavy documents warrant a full cross-check whatever the issue list says.

> Rationale: structure and content accuracy are independent — AnyDoc can mangle tables/numbers even in a well-headed document. Extraction is cheap and unconditional (Step 3); only the depth of the LLM's comparison is its own call.

### Outputs

* Issue list (specific locations and problems)

* The LLM's recommendation on whether Step 3 does a full vs. light cross-check

## 3. Content verification (Step 3)

### Goal

Extract the deterministic ground-truth source (unconditional — runs for every document, whatever the Step 2 issue list says) and cross-check `raw.md` against it to validate content accuracy.

### Cross-check depth

The extraction in this step always runs. Whether the LLM does a **full cross-check** of `verify_text.txt` against `raw.md` or a light spot-check is its judgment from the Step 2 issue list and the document type. Rule of thumb: table/number-heavy documents (PDF/Excel/Word/PPT) and documents with many issues warrant a full cross-check; a clean document warrants a light one. A user asking for verification always gets a full one.

> **Boundary: no OCR, scans are kept as images.** A document with no text layer (scans / image-only PDF) has no deterministic text source, and OCR is probabilistic and costly — kb-polish does not OCR. Instead Step 3 renders every page to `images/page_N.png` and Step 4 keeps them as `![page N](./images/page_N.png)` with a "scanned / image-only (no text layer)" note, so the asset survives for viewing while its content stays unreadable to the LLM.

### Actions

Run `extract_verify.py -o {outdir} --save-text` (unconditional) to produce the deterministic source `verify_text.txt`, then the LLM compares it with `raw.md`, focusing on:

* Misaligned table data (digits, amounts, whether the card type and fee correspond 1:1)

* Text split / reordered by AnyDoc

* Missing content

```bash
# Extract the source text (auto-detects format → dispatches to plugin); save verify_text.txt for the LLM
python scripts/extract_verify.py {input} -o {outdir} --save-text
python scripts/extract_verify.py --list                            # list supported formats & plugins
```

**Plugins are split by format** (`scripts/verifiers/`, one file per format), all independent of AnyDoc's implementation, and **strictly aligned with AnyDoc-supported formats** (per the official format list, excluding html/md/txt — those do not go through this skill's conversion):

| Format                  | Plugin  | Extraction                      | Dependency |
| ----------------------- | ------- | ------------------------------- | ---------- |
| .pdf                    | pdf.py  | PyMuPDF text layer              | pymupdf    |
| .docx/.docm             | docx.py | zipfile+xml                     | stdlib     |
| .pptx/.pptm/.ppsx/.ppsm | pptx.py | zipfile+xml                     | stdlib     |
| .xlsx/.xlsm             | xlsx.py | zipfile+xml                     | stdlib     |
| .odt/.ods/.odp          | odt.py  | zipfile+xml                     | stdlib     |
| .epub                   | epub.py | zipfile+xml                     | stdlib     |
| .rtf                    | rtf.py  | striprtf control-word stripping | striprtf   |
| .csv                    | csv.py  | csv stdlib                      | stdlib     |

> Note: formats AnyDoc supports but that currently lack a lightweight verify plugin — legacy binary .doc/.ppt (no lightweight library; convert with LibreOffice first), .xls/.xlsb (xlrd/pyxlsb available; add as needed). Verification may be skipped or the user informed explicitly.

These plugins output a **raw source independent of AnyDoc** (OOXML/ODF/EPUB zip+XML plaintext, PDF engine text layer); the LLM can check each item against `raw.md` to spot misalignments.

### Verification checklist

The LLM checks these against `verify_text.txt` — completeness, accuracy, and structure consistency, with no scores attached:

* Text content completeness — does the source text fully appear in the Markdown

* Table data accuracy — table values and row/column relations match the source

* Heading & structure consistency — section order and heading levels match the source

* Special elements preserved — image refs, code blocks, footnotes correctly preserved

### Flow

1. Run `extract_verify.py -o {outdir} --save-text` to produce the deterministic source
2. If extraction is empty with a "text layer is empty" warning: it is a scan — keep the rendered page images (`images/page_N.png`) and build a final.md whose body is only the `![page N](./images/page_N.png)` references plus a one-line "scanned / image-only (no text layer), no OCR" note; do not invent page content
3. Compare the extraction against `raw.md` segments
4. Check only the points in the Step 2 issue list; output fix suggestions

### Outputs

* Corrected Markdown (fix content errors only, do not change the structure)

* Verification report (list which errors were fixed)

* Keep questionable content for Step 5 human confirmation

## 4. LLM re-render (Step 4) — standard Markdown from the verified ground truth

### Goal

On top of Step 3 verification, the LLM uses the **deterministic source as the content ground truth** and **re-renders** `raw.md` into complete, standards-compliant Markdown for kb-pilot ingestion. This is "rebuild", not "patch": emit clean, complete, logically coherent standard Markdown in one pass. **Two hard rules: ① preserve the original content, ② do not change logical relationships.**

### Re-render source priority (where content comes from)

| Layer                                                                         | Source            | Note                                                                               |
| ----------------------------------------------------------------------------- | ----------------- | ---------------------------------------------------------------------------------- |
| Content text (body / table data / list text)                                  | `verify_text.txt` | **the only content ground truth**; fixes raw\.md's split/reordered/misaligned text |
| Structural skeleton (heading levels / section organization / image positions) | `raw.md`          | AnyDoc's inferred structure + Step 2 issue-list corrections                        |

On conflict: content text obeys the ground truth; structure obeys the corrected skeleton.

### Content hard rules (violation = redo)

1. **Zero content change**: do not add content not in the source, do not delete source content, do not rewrite numbers, amounts, terms, or proper nouns (keep original traditional/simplified and spelling), do not polish wording
2. **No filling from memory**: when the ground truth is missing (e.g. an empty table cell, a missing text-layer page), keep the slot and mark "original is empty here" — never guess
3. **Logical relationships unchanged**: check the checklist below item by item after re-rendering
4. **Exactly one H1; multiple H1s demote & merge by default**: kb-pilot treats H1 as the document title (not in the tree; the tree starts at H2). Multiple H1 blocks in one input file are usually related (e.g. a credit-card PDF = notices/statements + product summary), so **keep one final by default: the main title stays H1, the rest demote to H2 with their internal levels shifted (H2→H3, H3→H4)**. Split into multiple finals only when the blocks are completely independent and unrelated (e.g. multiple unrelated documents stitched into one PDF). The LLM decides (excluding header misreads and cross-page duplicate titles — those are simply deleted as redundant)

### Logical-relationship checklist (self-check each item after re-render)

* [ ] Section order matches the source (including the order and nesting of clause numbers 1.2.3)

* [ ] Table rows/columns map 1:1; values keep their column-head ownership; merged-cell relations preserved

* [ ] List nesting and ownership unchanged (indentation, numbering continuity)

* [ ] Heading-to-content ownership unchanged (each paragraph stays under its heading)

* [ ] Conditional/logical statements not split or reordered (e.g. "if … then …" clauses, cross-paragraph qualifiers)

* [ ] Footnote/reference/cross-reference relations unchanged

### Normalization rules (applied uniformly during re-render)

| Item                             | Rule                                                                                                                                                                                                                                                                                                              |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Single H1**                    | Each final.md has exactly one H1 (kb-ingest: H1 is the title, not in the tree). Multiple H1 blocks **demote & merge by default**: the main title stays H1, the rest become H2 with internal levels shifted (H2→H3, H3→H4); redundant headers/cross-page duplicates are deleted. Split only when fully independent |
| Heading-level completion         | Fill skipped levels (# → ### becomes # → ## → ###)                                                                                                                                                                                                                                                                |
| Heading-meaning optimization     | Vague headings made specific (Instructions → Configuration parameter instructions)                                                                                                                                                                                                                                |
| Duplicate heading disambiguation | Add a semantic prefix to duplicates (Notes → Module A notes)                                                                                                                                                                                                                                                      |
| Table format unification         | Simple tables as Markdown tables, complex tables as HTML tables                                                                                                                                                                                                                                                   |
| List indentation fixes           | Fix unreasonable indentation levels                                                                                                                                                                                                                                                                               |
| Image reference fixes            | Ensure correct paths, uniform `![](./images/xxx.png)`                                                                                                                                                                                                                                                             |

### Common cleanup items (PDF-to-Markdown specific)

* Headers/footers (page numbers, bank names, doc numbers) must not remain as body text or headings

* Cross-page repeated document titles merge into one

* Headers misread as headings (e.g. an org name) demote to body text or delete

* Bold markers (`**`) keep only real emphasis from the source, not conversion noise

### Validation loop (must re-run after editing)

1. Re-run Step 2 validation on every re-render output (default single `final.md`; `final_1.md`, `final_2.md`, … on the split exception): `python scripts/validate_structure.py final.md`
2. If the issue list is not empty: fix and re-run until zero (output must have **exactly one H1**, no `multiple_h1`)
3. Content-drift spot check (mechanical backstop): `python scripts/check_drift.py verify_text.txt final.md` — compares the numeric/amount token sets; **no missing tokens = no numeric drift detected** (it only verifies numbers, so it cannot prove "zero content change" — prose drift is the LLM's judgment). A missing token must be judged as drift vs an intentional removal (e.g. footer amounts)
4. Only after no mechanical issues and no numeric drift, proceed to Step 5 human confirmation

## 5. Human confirmation (Step 5)

### Goal

The user confirms the final Markdown.

### Confirmation strategy

| Stage                     | Strategy                                                        |
| ------------------------- | --------------------------------------------------------------- |
| First use                 | Full confirmation (page-by-page for every document)             |
| After building confidence | Sampling (20%–30% spot check)                                   |
| High trust                | Confirm only key documents; trust verification for routine ones |

### Confirmation points

1. Body content matches the source
2. Heading levels are reasonable
3. Table data is correct
4. Image references are correct
5. No structural problems

If human confirmation fails: record the problems and re-run Step 3 or Step 4 for targeted fixes.

## 6. Outputs

### Output files

```
{output_dir}/
├── raw.md              # AnyDoc first draft
├── final.md            # LLM re-render (single H1, ingestible; final_1/2/…N.md on the split exception)
├── verify_text.txt     # deterministic verify source (content ground truth for re-render)
├── verify_result.json  # extract_verify.py result (stats + source preview + images list)
├── images/             # extracted images
└── attachments/        # extracted embedded files
```

### Ingestion

kb-polish only produces Markdown — it does not ingest. Place `final.md` (or the split `final_N.md` files) into `{kb_path}` alongside your other Markdown sources, then run the **kb-ingest** skill to add it to the index.

## 7. Error handling

| Situation                                                 | Handling                                                                                                                                                                                     |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AnyDoc conversion fails                                   | Tell the user to check whether the file format is supported                                                                                                                                  |
| Verification finds misalignment that cannot be auto-fixed | Mark the region and request human intervention                                                                                                                                               |
| Human confirmation fails                                  | Record the problems; re-run Step 3 verification or Step 4 re-render for targeted fixes                                                                                                       |
| Scan (empty text layer)                                   | **Keep as images**: render pages to `images/page_N.png`, final.md body = `![page N](./images/page_N.png)` references + "image-only (no text layer), no OCR" note; LLM must not guess content |
| Unsupported special format                                | Ask the user to prepare a Markdown version manually                                                                                                                                          |

<br />
