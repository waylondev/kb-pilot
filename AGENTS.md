# AGENTS — Design principles for LLM-driven knowledge base

> Scripts constrain the skeleton; the LLM fills the content. Trust the LLM's intelligence — it is the second engineer, not a keyword matcher.

## Core belief

The LLM is sufficiently intelligent. It only needs **a precise table of contents and the full source text** — the same two things a human uses in a library. No vectors, no chunks, no graphs, no extraction algorithms. The LLM reads, understands, and answers like a human flipping through a book.

## Skeleton vs. Flesh

| Layer | Who builds it | What it contains | Why |
|-------|--------------|-----------------|-----|
| **Skeleton** (deterministic) | Scripts | Heading hierarchy, line numbers, doc_id, SHA256 | Machines are good at counting lines and parsing structure |
| **Flesh** (semantic) | LLM | Summary, keywords, routing, localization, answers | Only the LLM understands meaning; scripts would destroy accuracy |

The boundary is absolute: **scripts never touch semantics; the LLM never touches structure parsing.** If you find yourself writing a regex to extract keywords or a rule to match summaries, stop — that is the LLM's job.

## What to do

- **Let the LLM navigate autonomously** — It picks the document, dives into the section, expands the read range as needed. Provide anchors (line numbers, TOC), not rules
- **Let the LLM organize answers freely** — The only hard requirement is traceable citations. Format, length, and style are the LLM's call
- **Let the LLM distill summaries** — After reading each section, the LLM writes what it understood. No templates, no extraction algorithms
- **Keep scripts minimal** — Parse structure, aggregate metadata, compute hashes. That is all
- **When uncertain, consult the user** — The LLM asks rather than guesses, just like a librarian
- **Let the LLM reflect on its own answer** — Before delivering, it re-checks every claim against the source and decides for itself how many rounds it needs. No fixed round count, no score threshold — the stop condition is "I can stand behind every claim". This is not a constraint; it is the LLM using its own judgment, like a human double-checking notes before answering

## What not to do

- **No vector embeddings** — The LLM does not need cosine similarity; it understands meaning directly
- **No chunk splitting** — Full source text with line-level TOC is more precise than any chunk
- **No entity graphs / knowledge graphs** — The heading tree is the only graph needed
- **No keyword extraction algorithms** — TF-IDF, RAKE, TextRank all miss what the LLM catches
- **No rigid decision trees for routing** — "If score > 0.8 then select" is not how a human browses a library
- **No answer templates beyond citation** — The LLM knows how to write a good answer
- **No format conversion** — PDF/Word/HTML → Markdown is the user's job, not the system's. The optional `kb-polish` skill is a user-side convenience (AnyDoc + LLM re-render → Markdown), never a required system stage
- **No sharding / physical splitting** — One repo = one cognitive boundary; split by team or domain, not by code
- **No auxiliary structures beyond tree.json + manifest.json** — Aliases, infoboxes, inverted indexes, multi-level routing tables all add complexity without value

## SKILL design principles

SKILLs **must** follow the official [Agent Skills](https://agentskills.io) guides. Do not improvise — read the guides, then implement. Key points adapted to this project:

- **Frontmatter uses only official fields** — `name`, `description`, `compatibility`, `metadata`, `license`, `allowed-tools`. No custom fields like `config`. Project tunables (`repo_url`, `kb_path`) go in `metadata`
- **Add what the agent lacks, omit what it knows** — Only write what the LLM wouldn't figure out on its own
- **Match specificity to fragility** — Be prescriptive for fragile operations (path mapping, doc_id); give freedom where multiple approaches are valid
- **Favor procedures over declarations** — Teach *how to approach*, not *what to produce*
- **Checklists, not decision trees** — Steps are progress markers, not if-else branches
- **Validation loops** — Validate after fragile operations (kb-ingest Step 5 + Step 6, kb-chat Step 5)
- **Bundling reusable scripts** — Deterministic logic lives in `scripts/`; the LLM handles semantics

## Script design principles

- **Self-contained with PEP 723 inline dependencies** — Declare external deps (e.g. `# /// script\n# dependencies = ["requests"]\n# ///`) so scripts run without separate install steps
- **Borrow, do not duplicate** — When two skills need the same deterministic routine, one owns it and the other borrows it, deriving the path from its own location rather than hard-coding a sibling's address (kb-chat → `check_source.py`, kb-polish → `build_tree.py`). Two copies of a subtle routine drift silently, and the drift surfaces as output that validates clean in one skill and parses wrong in the other. Borrowing always points optional → core, so the core never depends on an optional skill
- **A skill carries no corpus vocabulary** — Scripts ship format-shaped logic (an amount, a percentage, a heading) and nothing that belongs to the documents being processed. Corpus-specific knowledge arrives as a parameter (`check_drift.py --extra-pattern`), so a shared skill stays ignorant of whose documents it is running on
- **Declared dependencies live in one place** — An entry script declares its own with a PEP 723 block. A plugin that needs a third-party package declares it on the plugin class instead (see `verifiers/base.py`), so `extract_verify.py --list` stays accurate when a format is added and the entry script's dependency list stays the single place to update
- **argparse CLI with `--help`** — Examples and exit codes in the epilog. Exit codes are declared **per script** and are not uniform across the two skill families: the core scripts use `2` for an expected failure (missing file, unusable index), while `extract_verify.py` uses `2` for a missing dependency and `1` for a runtime failure. Read the epilog rather than assuming
- **stdout = JSON result, stderr = progress** — Machine-parseable output, human-readable logs
- **Single responsibility** — One script does one deterministic thing
- **Preserve the fillings a rebuild would otherwise blank, and report what was kept** — Summary/keywords are carried over where the structure still matches, because regenerating them means re-reading the whole document. Record fields like `title` and `domain` are *not* carried over: they are single semantic values, so there is no cost argument for inheriting one, and keeping it would mean the script asserting that last time's classification still holds. For those the script reports what it dropped (`previous_title`, `previous_domain`) instead. Silence is the failure mode either way: an edit that changes only a number or a sentence preserves every heading, so every filling is inherited while quietly going stale. The script states the facts (how much was reused, whether the source moved); judging staleness — and re-deriving what was dropped — is the LLM's job
- **Parse real Markdown, not a toy subset** — Fenced code blocks are part of the format, and a `#` inside one is a comment, not a heading. A parser that skips this invents phantom sections and truncates line ranges while still reporting zero validation errors, because the mangled ranges remain internally consistent. Validate against the failures that are *silent*, not just the ones that crash

## Official references

When creating or modifying SKILLs, **read these first** — do not write SKILLs from scratch based on guesswork:

| Guide | What it covers | URL |
|-------|---------------|-----|
| Quickstart | `SKILL.md` basic structure, discovery / activation / execution | https://agentskills.io/skill-creation/quickstart |
| Best practices | Spending context wisely, calibrating control, patterns for effective instructions | https://agentskills.io/skill-creation/best-practices |
| Optimizing descriptions | How to write the `description` field so the SKILL triggers on the right prompts | https://agentskills.io/skill-creation/optimizing-descriptions |
| Specification | Complete format reference for `SKILL.md` (frontmatter fields, progressive disclosure, file layout) | https://agentskills.io/specification |
| Using scripts in skills | When to bundle scripts, CLI interfaces, stdout / stderr conventions | https://agentskills.io/skill-creation/using-scripts |
| Example skills | Real-world SKILLs on GitHub for reference | https://github.com/anthropics/skills |

## File map

```
kb-pilot/
├── .agents/skills/
│   ├── kb-ingest/
│   │   ├── SKILL.md               # ingest workflow (8 steps: clone → tree → LLM fill → manifest → hand off; git commit is the user's job)
│   │   └── scripts/
│   │       ├── build_tree.py      # Markdown → tree.json (document record + skeleton, deterministic)
│   │       ├── build_manifest.py  # tree.json × N → manifest.json (deterministic)
│   │       └── check_source.py    # source SHA256 vs tree.json's recorded checksum → drift (read-only)
│   ├── kb-chat/                   # QA workflow (5 steps: route → localize → read → answer → self-verify)
│   │   └── SKILL.md               # Step 3 calls kb-ingest's check_source.py; kb-chat ships no scripts
│   └── kb-polish/                 # OPTIONAL, non-core: source document → Markdown
│       ├── SKILL.md               # (AnyDoc + LLM re-render, 5 steps). A user-side convenience only —
│       ├── references/            # not a required system stage; the user may convert any way they want.
│       │                          # workflow.md (full flow) + rules.md (boundaries & scoring)
│       └── scripts/               # convert_document / validate_structure / extract_verify / check_drift
│           └── verifiers/         # per-format deterministic verify-source plugins (one file per format)
└── tests/
    ├── test_core.py               # core-path regressions — kb-ingest's three scripts
    └── test_polish.py             # kb-polish — the stdlib-only scripts + the verifier registry
```

**Tests live in `tests/` and nowhere else.** No second test directory, no evaluation
harness parked under `examples/` or anywhere else. A corpus run may need generated
files; those are gitignored under `tests/`, never given a directory of their own.

kb-polish converts PDF, Word (`.docx`/`.docm`), Excel (`.xlsx`/`.xlsm`), PowerPoint
(`.pptx`/`.pptm`/`.ppsx`/`.ppsm`), EPUB, CSV, RTF and OpenDocument (`.odt`/`.ods`/`.odp`).
It does no OCR: a pure scan is kept by embedding every page as an image.

## Data model

Two metadata files, and no others — no aliases, no inverted indexes, no routing tables
beyond the manifest. This section is the authoritative description of both; the README
and the SKILLs point here rather than keeping their own copy.

Both are minified by default (fewer tokens when the LLM reads them); `--pretty` writes a
readable, hand-editable copy.

- **`tree.json`** (one per document) — the document record plus the heading skeleton:
  - record fields: `doc_id`, `title`, `domain`, `source_path`, `summary`, `ingested_at`, `source_sha256`, `total_lines`
  - skeleton: one node per `##`–`######` heading, each carrying `id`, `level`, `title`, `start_line`, `end_line`, `children` and the LLM-filled `summary` / `keywords`
  - H1 is the document title and does not appear as a node — the tree starts at H2
  - text between the H1 and the first H2 is the document intro: it belongs to **no node**, so a fact stated only there is not reachable through the TOC. kb-chat Step 3 covers this by reading from the top of the file when the question may concern it
- **`manifest.json`** (one per knowledge base) — a JSON **array** of routing entries, one per document: `doc_id`, `title`, `domain`, `summary`, `tags`, `updated_at`, `path`

**`tags` come from top-level sections only.** Sub-section keywords stay in tree.json for
localization, which keeps the manifest small and routing focused. A topic buried in a
sub-section may therefore be absent from `tags` — which is why kb-chat walks the section
tree instead of relying on tags alone.

## Tests

All tests live in `tests/` — neither a test file nor an evaluation harness goes anywhere else in the repo.

```
tests/
├── test_core.py     # core path: kb-ingest's three scripts — stdlib unittest, zero dependencies
└── test_polish.py   # kb-polish: validate_structure / check_drift + the verifier format registry
                     #   run: python tests/test_core.py && python tests/test_polish.py
```

The suite targets failures that are *silent* rather than loud. A parser that crashes gets noticed on the first run; one that invents a section, truncates a line range, or carries a stale summary forward does not — so those are what get pinned down.

Each test writes to a self-cleaning `tempfile.TemporaryDirectory` (system temp), so nothing under `tests/` is modified by a run — the only files shipped are the two test modules.

Run `test_core.py` after any change to a core script, `test_polish.py` after any change to a kb-polish script or to the verifier registry.

`test_polish.py` covers the parts of kb-polish that run on the standard library alone: the mechanical structure checks and the drift spot-check, plus which format maps to which plugin. What it does not cover is per-format conversion quality — that needs `firecrawl-anydoc` / `pymupdf` / `striprtf` and a corpus of real documents. When you do run that, put the runner in `tests/` with the rest of the suite and keep the generated corpus and per-document outputs gitignored; do not let it grow a second home.

## Optimization directions

When improving this system, ask: **"Am I adding structure the LLM needs, or am I adding rules the LLM doesn't need?"**

- **Good optimization**: Better heading parser, faster manifest aggregation, clearer SKILL steps, smarter line-range anchoring
- **Bad optimization**: Vector search fallback, chunk-level retrieval, keyword scoring, multi-stage routing pipeline, answer post-processing filters

The system is deliberately minimal. Every addition must justify itself against the core belief: the LLM is smart enough.
