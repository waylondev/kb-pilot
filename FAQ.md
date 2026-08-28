# FAQ

## General

### Q: What's the difference between kb-pilot and LLM Wiki?

LLM Wiki is a **"compiler" model** — the LLM reads, reconstructs, and rewrites source documents into a structured set of Markdown Wiki pages. Queries read the compiled output, not the original text. Information loss occurs during compilation.

kb-pilot is an **"index" model** — no compilation, no reconstruction, no modification of the source. `tree.json` records heading hierarchy, line numbers, and index metadata — never the source text itself. Queries read the **original source** via line-number anchors, so the source text itself is not rewritten during indexing.

**One reads compiled content; the other reads the original source.**

---

### Q: Isn't this just a directory?

Yes, but the difference is that this directory is **executable, traceable, and correctable**:

- **Executable**: The system navigates by the directory and extracts the original source — not a static page for humans
- **Traceable**: Answers cite `docs/api/auth.md#L16` — line-level reference
- **Correctable**: `manifest.json` and `tree.json` are JSON — regenerate with `--pretty`, fix directly, and Git tracks every change

Not a static directory for humans, but the skeleton the system uses to retrieve.

---

## Scope & Trade-offs

### Q: What kind of knowledge base is kb-pilot designed for?

kb-pilot is a **focused choice**, not a universal RAG replacement. It is designed for **small to mid-sized, well-structured Markdown corpora** — tens to hundreds of documents within one team, product, or domain — where answers must be traceable to exact source lines and the source is worth reading precisely.

Choose it when:

- Documents have clear heading hierarchy (`#`, `##`, `###`) and stable source files
- The corpus is maintained like a Git repo, with humans responsible for document quality
- Answers must cite exact source lines and be auditable
- The repository maps to one team, product, policy area, or technical domain

Choose a conventional RAG system for large or unstructured corpora, web-scale or real-time search, millisecond latency, or resilience to messy documents. See the README's "Scope" and "When RAG is the better fit" sections for the full boundary.

---

### Q: What are kb-pilot's known boundaries?

kb-pilot's "trust the LLM, no vectors, no graphs" design comes with honest trade-offs. These define *when* kb-pilot needs human review — they are properties of the design, not bugs to be fixed:

- **Routing recall depends on summaries** — a question reaches a document only if the LLM routes to it via title/summary/keywords. If a summary happens not to mention the answer's keywords, the document may be missed. Note that `manifest.json` `tags` are collected from **top-level sections only**, so a topic confined to a sub-section may not appear in the routing entry at all. That is an index problem, not a source problem (see "What if the answer is wrong because a summary or keyword is misleading?").
- **Conflicts are found when both sides are read** — if two documents disagree, kb-pilot can surface the conflict, but only when routing happens to land on both documents. There is no entity index or contradiction detector.
- **Enumeration is the LLM's judgment** — for "list all X" questions, exhaustiveness depends on the LLM's patience to keep reading. There is no structural guarantee it scans the whole relevant domain.
- **"Not mentioned" is a global claim** — deciding the corpus doesn't cover a topic requires scanning it; stop early, and "not found" can be mistaken for "doesn't exist".
- **Self-verification checks what was answered** — Step 5 re-checks every claim against its cited lines, but it does not audit omitted facts or unrelated details in the answer.
- **Version selection needs the current date** — choosing between dated document versions relies on "today's date" being available in context; the system has no built-in version timeline.

These are exactly why line-level citations exist: when an answer matters, a human can click through and verify it in seconds.

---

### Q: What does the README mean by "version awareness"?

It refers to the `source_sha256` checksum in each `tree.json` (see "Version awareness (drift protection)" under Step 4 of the README's end-to-end workflow), and it does two things:

- **Detects drift before reading** — kb-chat compares the source's current checksum against the recorded one and warns if they differ, because citations may then point at text that has since changed. This compares checksums, not line counts: an edit that changes a number or rewords a sentence keeps the line count identical while silently making a citation wrong.
- **Re-anchors on re-ingest** — re-ingesting recomputes line anchors against the corrected text, so citations land on the new lines.

What it does **not** do is decide whether an existing LLM-written summary is still accurate. `build_tree.py` preserves previous summaries by matching `(level, title)`, so an edit that leaves the headings intact carries every old summary forward — including ones that edit invalidated. The script reports `source_changed` and how many fillings were reused; judging whether they are now stale, and re-verifying them, is the LLM's job. That is the boundary between the two layers: scripts state facts about the skeleton, the LLM decides what the text means.

`title` and `domain` follow the opposite rule: they are **not** inherited, and are re-derived on every ingest. Both sit on the semantic side of the line — `domain` is a routing hint that exists only in the index, the source carries no trace of it — and both are a single value, so there is no cost argument for keeping the old one the way there is for a document's worth of summaries. Leaving them out drops the previous value, which the script announces on stderr and reports as `previous_title` / `previous_domain`. Pass the flags on every re-ingest; that is how the classification gets reconsidered rather than assumed.

It also does **not** mean kb-pilot automatically selects between different document versions (e.g., an old and a new contract). Selecting "what applies now" depends on the LLM noticing version markers in the source and on the current date being provided in context — see "known boundaries" above.

---

## Corrections

### Q: How do I correct a wrong answer?

There is no separate correction layer — **the source is the single source of truth**.

1. Locate the wrong lines in the source Markdown and fix the fact there.
2. Re-ingest the document (kb-ingest) so `tree.json` line numbers and the checksum stay in sync with the corrected text.
3. Commit and push. Team members pick up the fix with `git pull`.

Every correction stays anchored in the original text and in Git history, instead of accumulating a parallel patch file that can drift from the source.

---

### Q: What if the answer is wrong because a summary or keyword is misleading?

That's an index problem, not a source problem:

1. Regenerate the document's tree with `--pretty`.
2. Edit the summary/keywords in `tree.json`.
3. Rebuild the manifest (minified by default) and commit.

The index is JSON regenerated by scripts; Git tracks the change.

---

## Comparisons

### Q: How is the TOC different from a vector DB's "domain field filter"?

A vector DB's domain field filter does **coarse-grained** filtering (e.g., "only finance documents"), but after filtering, it still relies on vector recall. kb-pilot's TOC provides **line-level anchors into the source**, so the LLM can navigate to a specific document section and verify against the original text.

**Fundamental difference: vector DB is "filter and recall"; TOC is "navigate and read the source."**

---

### Q: What's the difference between parent-child chunking and kb-pilot's TOC?

Parent-child chunking is a patch **within** the vector retrieval framework — small chunks for recall, parent chunks for context compensation. But the root issue remains: you're still chunking, still relying on vector recall.

kb-pilot's TOC **doesn't chunk the source**. It reads relevant source sections via line numbers, rather than stitching together pre-split fragments.

**Parent-child chunking is "tagging shredded fragments"; kb-pilot's TOC is "indexing source structure and reading source sections."**

---

### Q: Why not just use grep/ripgrep?

grep/ripgrep work well for structured documents — **if the user knows exactly what to search for**.

kb-pilot's differentiator: the user doesn't need to hit the exact keyword. The LLM routes to the document and section via semantic matching, then verifies against line-numbered source text. **One is "I know what to search for"; the other is "the LLM figures out what to read for me."**

---

## Cost & Scale

### Q: Doesn't reading full source consume more tokens? Isn't it expensive?

Yes, that's the direct tradeoff. A few points to consider:

1. **Less volume than full-repo reading**: The TOC narrows the reading scope to likely relevant sections. Traditional RAG may use fewer tokens per chunk, but may need multiple retrieval rounds to assemble an answer.

2. **What you get**: More complete local context, precise citations, and source-grounded self-verification. If you only need "rough answers," this approach may not be cost-effective. But if you need **accurate citations and traceable conclusions**, the extra reading cost can be worthwhile.

**It's a tradeoff: cost for accuracy.** Choose based on your scenario — kb-pilot isn't for every use case.

---

### Q: What about large document volumes? Won't the LLM be overwhelmed by the manifest?

This is kb-pilot's design scope — **tens to hundreds of documents**, for team knowledge bases, technical docs, project specifications, and other well-structured Markdown corpora where answers must be traceable to exact source lines. Not a general-purpose search engine for millions of documents.

Beyond that, split by domain:
- Engineering team knowledge base → one Git repo
- Finance team knowledge base → another Git repo

**One knowledge base = one Git repo = one cognitive boundary** — this is a design decision, not a technical limitation.

---

### Q: What if the repository grows beyond a few hundred Markdown files?

This is where kb-pilot's intended boundary starts to matter. The design target is tens to hundreds of documents in one coherent team or domain, not an ever-growing universal corpus.

If the repository grows beyond that boundary, split it by ownership or subject area. The project principle is "one knowledge base = one Git repo = one cognitive boundary," so scale is handled by clearer repo boundaries rather than adding vector search or sharding layers.

---

### Q: What if a single document is very long?

Long documents are acceptable when they have clear heading hierarchy. `tree.json` uses headings and line ranges as navigation anchors, so a long manual with well-formed sections is easier to use than many tiny files with vague names.

If one heading contains several unrelated topics, fix the Markdown structure first. kb-pilot deliberately avoids automatic chunk splitting because arbitrary chunks make citations and source review harder to trust.

---

## Input Formats

### Q: What about images, PDFs, Excel files?

The rule: **the system does not perform format conversion.**

AGENTS.md states: **"No format conversion — PDF/Word/HTML → Markdown is the user's job, not the system's."**

PDFs, images, Excel files must be converted to Markdown before ingestion — but you choose how. This isn't a technical limitation — it's a design choice: conversion accuracy must remain your responsibility. You can convert any way you like (manually, an external tool, or the optional **kb-polish** skill, which runs AnyDoc + a deterministic verify cross-check and an LLM re-render, then asks you to confirm). The recommended workflow is AI-assisted conversion + human review.

**If a document references an image (e.g., "see Figure 5"), the extracted source snippet includes the reference text and surrounding Markdown context. The system does not interpret image contents unless that content is represented in Markdown.**

---

### Q: Is the Markdown format requirement high maintenance?

No. Markdown is the lightest-weight format — you only need **basic heading hierarchy** (`#`, `##`, `###`), not complex schemas.

AI can convert PDF/Word to Markdown; humans just need to verify key information — not write from scratch.

---

## Maintenance

### Q: What happens when source documents change?

Re-ingest the changed Markdown files so `tree.json` and `manifest.json` reflect the current headings, line ranges, and checksums. The deterministic scripts rebuild structure; the LLM rechecks summaries and keywords where the source meaning or section layout has changed.

There is no separate correction layer. If a fact was corrected by editing the source, re-ingest the document so line anchors and the checksum track the corrected text. The current source always wins.

---

### Q: What if the source Markdown has poor headings?

The source should be fixed before ingestion. kb-pilot depends on headings as the table of contents; if a document has vague headings, missing H2 sections, or several topics under one heading, routing and citation quality will suffer.

This is intentional. The system treats document structure as part of knowledge quality, not as something to hide behind embeddings or post-processing.

---

### Q: What if two documents conflict?

The answer should cite the conflicting source lines and explain the disagreement rather than forcing a single merged conclusion. In a Git-based knowledge base, conflicting source documents are usually a documentation governance issue.

There is no separate correction layer — when the authoritative policy or fact changes, update the source Markdown and re-ingest. The goal is not to make conflicts disappear, but to make them visible and traceable.

---

## Design

### Q: Can two LLMs doing cross-validation replace human judgment?

Two LLMs can filter out some errors, but fundamentally it's still **"LLM evaluating LLM"** — if both models share similar biases or blind spots, they can be wrong together.

**The core question remains: who validates the knowledge?**

kb-pilot's approach: **keep the human in the loop**. Indexes are JSON — regenerate with `--pretty`, fix them directly, and Git tracks every change. Humans only need to intervene when there's a conflict, rather than pre-validating every answer.

---

### Q: What's the difference between kb-pilot and PageIndex?

Both follow the same core flow: build tree → LLM navigates → locate node → extract source.

Differences:

| | kb-pilot | PageIndex |
|---|---|---|
| Index format | JSON, readable & editable | Opaque, not editable |
| Git-native | ✅ | ❌ |
| Source is the correction | ✅ | ❌ |
| Human-editable index | ✅ | ❌ |
| Self-verification | ✅ | ❌ |

**kb-pilot is lighter, more transparent, more maintainable.**

---

### Q: What's kb-pilot's advantage in one sentence?

**Replace chunk-level vector recall with TOC-guided source navigation; let the LLM handle semantic understanding; use Git as the collaboration backbone.** Designed for mid-scale (tens to hundreds of documents), structured knowledge bases that require accurate citations, traceable conclusions, and low infrastructure overhead.

---

## See also

- [README.md](./README.md) — Project overview and quick start
- [AGENTS.md](./AGENTS.md) — Design principles
