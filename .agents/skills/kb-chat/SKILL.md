---
name: kb-chat
description: >-
  Use when the user asks a question that should be answered from the knowledge base,
  wants to compare content across documents, or corrects a previous answer. Triggers
  on questions about ingested content and on corrections like "that's wrong",
  "should be", "correct this" — even when the user doesn't name the underlying system.
config:
  repo_url: ""
  kb_path: knowledge_repo
---

# kb-chat — Answer like a human flipping through a book

The LLM is the routing engine, not a keyword matcher. It locates documents and sections by semantically understanding title/summary/keywords, reads the source, and answers with citations. Every answer must be grounded in the source text; if not found, say "not mentioned in the documents".

Path calculation: manifest entry `path: docs/api/auth.md` → tree.json at `.kb/index/docs/api/auth/`, source file at `{kb_path}/docs/api/auth.md`.

## QA workflow

Like a human flipping through a book: look up the TOC to locate the section, read the source, answer with citations. The LLM decides how deep to go at each step based on question difficulty.

Progress:
- [ ] **1. Routing preferences** — Read `.kb/memory/route_preferences.json` (if present) as a weak prior. Only honor preferences the user explicitly expressed; never infer from conversation history
- [ ] **2. Document routing** — Read `.kb/manifest.json`, locate the most relevant document via **semantic matching** of domain/title/summary/tags
  - If Top 1 is clearly better → select it
  - If multiple documents are hard to distinguish → list candidates and let the user choose; do not guess
  - If no document can be located → list Top 2–3 candidates (title + summary) and let the user choose; do not guess
- [ ] **3. Section localization** — Read the hit document's `tree.json`, locate the most precise section via **semantic matching** of node title/summary/keywords. Recurse into children until specific enough
- [ ] **4. Content extraction** — Read the line range [start_line, end_line] of the hit section from the source file
  - If the answer may span nodes, proactively expand the read range (adjacent nodes or lines)
  - If a child node is insufficient, fall back to the parent's range for fuller context
  - Record the line range read, for citation
  - For cross-document comparison: run Steps 2–4 independently per document; cite each source separately; do not mix routing or localization results
- [ ] **5. Correction loading** — Read `.kb/memory/corrections/{doc_id}.jsonl` (if present) and attach to context. The LLM judges relevance:
  - Duplicate records (same correct_answer) = multi-user consensus; boosts confidence; do not dedupe
  - conflicted status = conflicting answers; show all versions side by side; do not adjudicate
- [ ] **6. Generate answer** — Based on extracted source text, using the template below. If the user explicitly expresses a domain preference, write it to route_preferences.json

## Answer format template

```markdown
[Direct conclusion, one sentence]

[Elaboration, quoting key fragments from the source]

Source: {doc_id} {ch_id} {path}#L{start}-L{end}
```

- When a correction contradicts the source: state "source says X, correction says Y"
- When the documents contain no relevant info: say only "not mentioned in the documents"; do not fabricate
- For cross-document comparison: cite both document sources separately

## Correction flow

When the user says "that's wrong", "should be", "correct this":

- [ ] 1. Locate the doc_id and ch_id of the current question
- [ ] 2. Append a record to `.kb/memory/corrections/{doc_id}.jsonl`:
  ```json
  {"question": "the question", "correct_answer": "user's corrected answer", "ch_id": "ch_x", "session_id": "xxx", "timestamp": "ISO timestamp", "status": "active"}
  ```
- [ ] 3. When different users give different answers to the same question, mark status as conflicted
- [ ] 4. Commit to Git: `git add .kb/memory/ && git commit && git push`

## Gotchas

- **Never fabricate from training data** — If not found, say "not mentioned in the documents"; never answer from model memory
- **No keyword hard-matching** — Routing relies on semantic understanding of title/summary/keywords, not term frequency or literal matching
- **path field is critical** — The manifest entry's path is the source file path relative to the repo root; the source is read from there. tree.json lives under the `.kb/index/` mirrored directory
- **Correction conflicts** — conflicted records must show all versions; never adjudicate unilaterally
- **Correction duplicates** — Same answer across different session_ids is a consensus signal; do not dedupe
- **Cross-document comparison** — Run routing and localization independently per document; do not mix
- **Routing preferences** — Store only preferences the user explicitly expressed; never infer from conversation history
- **Scale boundary** — When a single repo exceeds a few hundred documents, split by team or domain into separate Git repos; no physical sharding
- **{kb_path} placeholder** — Replace with the actual knowledge base path at runtime; defaults to `knowledge_repo`
