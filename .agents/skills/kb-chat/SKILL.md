---
name: kb-chat
description: >-
  Use when the user asks a question that should be answered from the knowledge base
  or wants to compare content across documents. Triggers on questions about ingested
  content — even when the user doesn't name the underlying system.
compatibility: Requires Git and an initialized knowledge base (run kb-ingest first)
metadata:
  repo_url: ""
  kb_path: knowledge_repo
---

# kb-chat — Answer questions from the knowledge base

Path calculation: manifest entry `path: docs/api/auth.md` → tree.json at `.kb/index/docs/api/auth/`, source file at `{kb_path}/docs/api/auth.md`.

## Input / Output

```yaml
Input:
- question: string           # user question
- domain_preference?: string # optional; user-specified domain as a routing hint

Output:
- answer: string             # grounded in source, with traceable citations
- citations: Source: {doc_id} {ch_id} {path}#L{start}-L{end}
```

## Workflow

Progress:
- [ ] **1. Document routing** — Read `.kb/manifest.json` (and `.kb/memory/route_preferences.json` if present, as a weak prior). If `domain_preference` is provided, use it as a strong routing hint. Locate the most relevant document via **semantic matching** of domain/title/summary/tags. When uncertain, list a few candidates and let the user choose
- [ ] **2. Section localization** — Read the hit document's `tree.json`, locate the most precise section via **semantic matching** of node title/summary/keywords. Recurse into children until specific enough
- [ ] **3. Content extraction** — Use start_line/end_line as navigation anchors; read the source starting from there. The LLM decides how much to read — expand to parent, siblings, or the full document as judgment dictates. Record the actual lines read for citation
- [ ] **4. Correction loading** — Read `.kb/memory/corrections/{doc_id}.jsonl` (if present) and attach to context. The LLM judges relevance: duplicate records (same correct_answer) signal multi-user consensus and boost confidence; conflicted records show all versions side by side
- [ ] **5. Generate answer** — Organize the answer autonomously based on extracted source text. If the user expresses a domain preference, write it to `.kb/memory/route_preferences.json`
- [ ] **6. Self-verify** — Before delivering, re-read your own answer against the source: every claim grounded in the cited lines? Did you actually answer the question? The LLM decides how many rounds — a simple fact may need one glance, complex cross-document reasoning may need several. If a gap is found, go back to Step 3 and re-read, then re-verify. Stop when you can stand behind every claim; if the source still doesn't support it after re-reading, say "not mentioned in the documents"

## Failure handling

- `.kb/manifest.json` missing → report "knowledge base not initialized; run kb-ingest first"
- No relevant document after routing → say only "not mentioned in the documents"
- Ambiguous routing between multiple documents → list candidates and ask the user to choose
- Source citation missing or line range wrong → re-read the source and verify before answering

## Gotchas

- **path field is critical** — The manifest entry's path is the source file path relative to the repo root; the source is read from there. tree.json lives under the `.kb/index/` mirrored directory. A mismatch makes the document unanswerable
- **Cross-document comparison** — Run routing and localization independently per document
