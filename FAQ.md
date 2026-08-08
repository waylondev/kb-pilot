# FAQ

## General

### Q: What's the difference between kb-pilot and LLM Wiki?

LLM Wiki is a **"compiler" model** — the LLM reads, reconstructs, and rewrites source documents into a structured set of Markdown Wiki pages. Queries read the compiled output, not the original text. Information loss occurs during compilation.

kb-pilot is an **"index" model** — no compilation, no reconstruction, no modification of the source. `tree.json` only records heading hierarchy and line numbers. Queries extract the **original source** via line numbers. **Zero loss.**

**One reads compiled content; the other reads the original source.**

---

### Q: Isn't this just a directory?

Yes, but the difference is that this directory is **executable, traceable, and correctable**:

- **Executable**: The system navigates by the directory and extracts the original source — not a static page for humans
- **Traceable**: Answers cite `docs/api/auth.md#L16` — line-level reference
- **Correctable**: `manifest.json` and `tree.json` are plain text — if something is wrong, fix it directly; Git tracks every change

Not a static directory for humans, but the skeleton the system uses to retrieve.

---

## Corrections

### Q: Will old correction records pollute newer versions of documents? (Version drift)

This is a theoretical concern. Current design handles it with:

1. **SHA256 checksum**: Each `tree.json` node includes `sha256`. When the source file changes, the new tree replaces the old one.

2. **LLM judges at read time**: When `kb-chat` loads corrections, the LLM reads the current source and determines whether an old correction still applies — if the source conflicts with the old record, it defers to the source.

3. **Human intervention**: Correction records are plain text JSONL — if outdated, manually delete or mark them. Git tracks the full history.

**The risk exists, but the design handles it by deferring to the LLM and human judgment at read time, rather than building complex version mapping tables.** If you need tighter version binding, `sha256` is already in `tree.json` — PRs welcome.

---

### Q: Corrections are append-only — won't they accumulate?

Yes. That's by design — **correction records are the audit log of knowledge evolution**.

- Multiple identical corrections → consensus signal, reinforcing confidence
- Conflicting corrections → shown side by side, no "fake harmony"
- Outdated records can be manually deleted or marked (plain text JSONL, trivial to edit)

---

## Comparisons

### Q: How is the TOC different from a vector DB's "domain field filter"?

A vector DB's domain field filter does **coarse-grained** filtering (e.g., "only finance documents"), but after filtering, it still relies on vector recall. kb-pilot's TOC provides **line-level deterministic positioning**, not probabilistic matching.

**Fundamental difference: vector DB is "filter and guess"; TOC is "direct locate."**

---

### Q: What's the difference between parent-child chunking and kb-pilot's TOC?

Parent-child chunking is a patch **within** the vector retrieval framework — small chunks for recall, parent chunks for context compensation. But the root issue remains: you're still chunking, still relying on vector recall.

kb-pilot's TOC **doesn't chunk the source**. It extracts complete original source via line numbers, not stitched-together fragments.

**Parent-child chunking is "tagging shredded fragments"; kb-pilot's TOC is "indexing the complete source."**

---

### Q: Why not just use grep/ripgrep?

grep/ripgrep work well for structured documents — **if the user knows exactly what to search for**.

kb-pilot's differentiator: the user doesn't need to hit the exact keyword. The LLM routes to the document and section via semantic matching, then uses the same line-level positioning. **One is "I know what to search for"; the other is "the LLM figures out what to read for me."**

---

## Cost & Scale

### Q: Doesn't reading full source consume more tokens? Isn't it expensive?

Yes, that's the direct tradeoff. A few points to consider:

1. **Less volume**: The TOC pinpoints only relevant sections — you don't scan everything. Traditional RAG may use fewer tokens per chunk, but may need multiple retrieval rounds to assemble an answer.

2. **What you get**: No lost context, precise citations, zero hallucination. If you only need "rough answers," this approach isn't cost-effective. But if you need **accurate citations and traceable conclusions**, the cost is necessary.

**It's a tradeoff: cost for accuracy.** Choose based on your scenario — kb-pilot isn't for every use case.

---

### Q: What about large document volumes? Won't the LLM be overwhelmed by the manifest?

This is kb-pilot's design scope — **tens to hundreds of documents**, for team knowledge bases, technical docs, project specifications. Not a general-purpose search engine for millions of documents.

Beyond that, split by domain:
- Engineering team knowledge base → one Git repo
- Finance team knowledge base → another Git repo

**One knowledge base = one Git repo = one cognitive boundary** — this is a design decision, not a technical limitation.

---

## Input Formats

### Q: What about images, PDFs, Excel files?

The rule: **the system does not perform format conversion.**

AGENTS.md states: **"No format conversion — PDF/Word/HTML → Markdown is the user's job, not the system's."**

PDFs, images, Excel files must be converted to Markdown before ingestion. This isn't a technical limitation — it's a design choice: the accuracy of conversion must be the user's responsibility. AI-assisted conversion + human review is the recommended workflow.

**If a document references an image (e.g., "see Figure 5"), the extracted source snippet includes the reference text, and the LLM perceives the context.**

---

### Q: Is the Markdown format requirement high maintenance?

No. Markdown is the lightest-weight format — you only need **basic heading hierarchy** (`#`, `##`, `###`), not complex schemas.

AI can convert PDF/Word to Markdown; humans just need to verify key information — not write from scratch.

---

## Design

### Q: Can two LLMs doing cross-validation replace human judgment?

Two LLMs can filter out some errors, but fundamentally it's still **"LLM evaluating LLM"** — if both models share similar biases or blind spots, they can be wrong together.

**The core question remains: who validates the knowledge?**

kb-pilot's approach: **keep the human in the loop**. Indexes are plain text JSON — fix them directly. Correction records are Git-tracked. Humans only need to intervene when there's a conflict, rather than pre-validating every answer.

---

### Q: What's the difference between kb-pilot and PageIndex?

Both follow the same core flow: build tree → LLM navigates → locate node → extract source.

Differences:

| | kb-pilot | PageIndex |
|---|---|---|
| Index format | Plain text JSON, readable & editable | Opaque, not editable |
| Git-native | ✅ | ❌ |
| Correction loop | ✅ | ❌ |
| Human-editable index | ✅ | ❌ |
| Self-verification | ✅ | ❌ |

**kb-pilot is lighter, more transparent, more maintainable.**

---

### Q: What's kb-pilot's advantage in one sentence?

**Replace probabilistic vector recall with deterministic line-level positioning; let the LLM handle all semantic understanding; use Git as the collaboration backbone.** Designed for mid-scale (tens to hundreds of documents), structured knowledge bases that require high accuracy, traceable citations, and low-cost deployment.

---

## See also

- [README.md](./README.md) — Project overview and quick start
- [AGENTS.md](./AGENTS.md) — Design principles