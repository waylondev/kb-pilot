---
name: kb-chat
description: >-
  Use when the user asks a question that should be answered from the knowledge base,
  wants to compare content across documents, or corrects a previous answer. Triggers
  on questions about ingested content and on corrections like "that's wrong",
  "should be", "correct this" — even when the user doesn't name the underlying system.
metadata:
  repo_url: ""
  kb_path: knowledge_repo
---

# kb-chat — Answer like a human flipping through a book

The LLM is the routing engine, not a keyword matcher. It locates documents and sections by semantically understanding title/summary/keywords, reads the source, and answers with citations. Every answer must be grounded in the source text; if not found, say "not mentioned in the documents".

Path calculation: manifest entry `path: docs/api/auth.md` → tree.json at `.kb/index/docs/api/auth/`, source file at `{kb_path}/docs/api/auth.md`.

## QA workflow

Like a human flipping through a book: look up the TOC to locate the section, read the source, answer with citations. The LLM navigates autonomously — pick the most relevant document, dive into the section, expand the read range when needed. When uncertain between documents, consult the user rather than guess.

Progress:
- [ ] **1. Routing preferences** — Read `.kb/memory/route_preferences.json` (if present) as a weak prior. Only honor preferences the user explicitly expressed
- [ ] **2. Document routing** — Read `.kb/manifest.json`, locate the most relevant document via **semantic matching** of domain/title/summary/tags. When uncertain, list a few candidates and let the user choose
- [ ] **3. Section localization** — Read the hit document's `tree.json`, locate the most precise section via **semantic matching** of node title/summary/keywords. Recurse into children until specific enough
- [ ] **4. Content extraction** — Use start_line/end_line as navigation anchors; read the source starting from there. The LLM decides how much to read — expand to parent, siblings, or the full document as judgment dictates. Record the actual lines read for citation
- [ ] **5. Correction loading** — Read `.kb/memory/corrections/{doc_id}.jsonl` (if present) and attach to context. The LLM judges relevance: duplicate records (same correct_answer) signal multi-user consensus and boost confidence; conflicted records show all versions side by side
- [ ] **6. Generate answer** — Organize the answer autonomously based on extracted source text. If the user explicitly expresses a domain preference, write it to route_preferences.json
- [ ] **7. Self-verify** — Before delivering, re-read your own answer against the source: every claim grounded in the cited lines? Did you actually answer the question? The LLM decides how many rounds — a simple fact may need one glance, complex cross-document reasoning may need several. If a gap is found, go back to Step 4 and re-read, then re-verify. Stop when you can stand behind every claim; if the source still doesn't support it after re-reading, say "not mentioned in the documents"

## Answer requirements

The LLM organizes the answer freely — the only hard requirement is **every claim carries a traceable citation**:

```
Source: {doc_id} {ch_id} {path}#L{start}-L{end}
```

- When a correction contradicts the source: state "source says X, correction says Y"
- When the documents contain no relevant info: say only "not mentioned in the documents"
- For cross-document comparison: cite each source separately

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

- **Answers must be grounded in source text** — If not found, say "not mentioned in the documents"
- **Routing is semantic, not lexical** — Match title/summary/keywords by meaning, not term frequency
- **path field is critical** — The manifest entry's path is the source file path relative to the repo root; the source is read from there. tree.json lives under the `.kb/index/` mirrored directory
- **Corrections are append-only** — Duplicate answers = consensus (keep them); conflicting answers = show all versions (let the user decide)
- **Cross-document comparison** — Run routing and localization independently per document
- **Routing preferences** — Store only preferences the user explicitly expressed
- **Scale boundary** — When a single repo exceeds a few hundred documents, split by team or domain into separate Git repos
- **{kb_path} placeholder** — Replace with the actual knowledge base path at runtime; defaults to `knowledge_repo`
