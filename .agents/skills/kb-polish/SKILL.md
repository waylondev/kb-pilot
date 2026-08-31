---
name: kb-polish
description: >-
  Convert documents (PDF, Word docx/docm, Excel xlsx/xlsm, PowerPoint pptx/pptm/ppsx/ppsm,
  EPUB, CSV, RTF, OpenDocument odt/ods/odp) into Markdown for kb-pilot ingestion,
  by wrapping AnyDoc and extracting embedded objects into assets/. Does NOT OCR.
  Use when converting docs to Markdown, PDF-to-MD, Word-to-MD, or pre-ingestion prep.
license: MIT
compatibility: Requires Python 3.10+; dependency firecrawl-anydoc; scripts need a Bash/python environment. Standalone — no other skill is required at runtime.
allowed-tools: Bash(python:* pip:*) Read Write
---
# kb-polish Skill
> A thin AnyDoc convenience wrapper: convert a document to a first-draft Markdown and pull its embedded objects into `assets/`. The LLM then organizes that draft into the kb-pilot Markdown standard before `kb-ingest`.

This is a **convenience helper, not a required stage**. Per AGENTS.md, format conversion is the user's job; kb-polish simply makes it one command and hands the semantic organization to the LLM. No mechanical validation, no scoring, no drift-check — those are exactly the guardrails AGENTS.md tells us to omit. The only multis-step rule is "exactly one H1", which is the LLM's judgment, applied on read-in, not by a script.

## Steps

- [ ] 1. **Convert + extract assets**: `python scripts/convert_document.py {input} -o {outdir}` — writes `raw.md` and lands embedded objects into `images/` (images) and `attachments/` (other files). JSON result on stdout.
- [ ] 2. **LLM organizes into standard Markdown**: read `raw.md`, correct its layout into the kb-pilot form (see template). This is the LLM's semantic job — fix split/reordered/misaligned text, rebuild heading levels, restore table rows/columns, point image references at `images/`.
- [ ] 3. **Human confirmation**, then hand off to `kb-ingest`.

## Output template (what Step 2 produces)

```markdown
# [Single document title]              ← exactly one # in the whole file (kb-pilot: H1 is the title, not part of the tree)
## [Section]                           ← tree starts at H2
### [Subsection, optional]             ← continuous levels, no jumps
| Header | Col | ... |                ← rows/columns map 1:1 to the source
|---|---|---|
| data | ... | ... |                  ← values/wording preserved verbatim
## [Next section]
```

> Body text is preserved verbatim (traditional characters / original spelling / terms); no polishing, no completion, no reordering of logic. Strip headers/footers (page numbers, doc numbers, repeated titles). **Multiple H1s demote & merge by default** — the main title keeps H1, the rest become H2 with their internal levels shifted down; split only when blocks are fully independent.

## Gotchas (field-tested, read first)

- **No OCR.** A pure scan (no text layer) converts, but its content is not machine-readable — the LLM cannot read page images. Tell the user to supply a text-layer version; do not render-and-read or invent content.
- **AnyDoc does not support .html/.md/.txt/.tsv**: html/md/txt are already text — ingest directly, do not run this skill; **.tsv must be renamed to .csv** first (content is identical).
- **AnyDoc handles .odp very weakly** (field-tested: only the title survives; body/tables lost): convert ODP to .pptx first.
- **RTF and complex merged-cell tables convert poorly** (garbled Chinese / misaligned data). The LLM repairs these from context in Step 2; if a table or clause cannot be reconstructed confidently, flag it for Step 3 human confirmation rather than guess.
- **Single-H1**: it is the one layout rule kb-ingest requires (the tree starts at H2). Apply it as an LLM judgment, not mechanically.

## Scripts

- `scripts/convert_document.py`: AnyDoc conversion + embedded-asset extraction (deterministic; the only script — raw.md + images/ + attachments/)