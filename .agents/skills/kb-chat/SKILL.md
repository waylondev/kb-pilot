---
name: kb-chat
description: >-
  Use when the user asks a question that should be answered from the knowledge base
  or wants to compare content across documents. Triggers on questions about ingested
  content — even when the user doesn't name the underlying system.
license: MIT
compatibility: Requires Git and an initialized knowledge base (run kb-ingest first)
allowed-tools: Bash(python:*) Read
metadata:
  repo_url: ""
  kb_path: knowledge_repo
---

# kb-chat — Answer questions from the knowledge base

Path calculation: manifest entry `path: docs/api/auth.md` → tree.json at `.kb/index/docs/api/auth/`, source file at `{kb_path}/docs/api/auth.md`.

Path resolution: `{kb_path}` comes from this skill's `metadata` and is relative to the project root — resolve it to an absolute path (`{abs_kb}`) before running anything.

The one script this workflow borrows lives in the **kb-ingest** skill, which sits next to
this one. With `{skills_dir}` = this SKILL.md's parent directory (`.agents/skills/`), it is
`{skills_dir}/kb-ingest/scripts/…` — resolve that to `{abs_ingest}`. kb-chat deliberately
does **not** declare where kb-ingest lives: the two skills are independent, and a path
written in this file would go stale the moment either one moves. Derive it from your own
location instead.

## Input / Output

```yaml
Input:
- question: string           # user question
- domain_preference?: string # optional; user-specified domain as a routing hint

Output:
- answer: string             # grounded in source. Citations are inline, not a separate field: after each
                             # claim, append a clickable [path#L{start}-L{end}](path#L{start}-L{end}),
                             # e.g. "...returns a JWT token.[docs/api/auth.md#L42-L58](docs/api/auth.md#L42-L58)".
                             # End with a "Source:" footer listing the distinct citations.
```

## Data it reads

Both files are minified JSON — parse them, do not read them as prose.

- **`.kb/manifest.json`** — a JSON **array** of document entries (not an object):

  ```json
  [{"doc_id":"doc_001","title":"API Auth","domain":"api","summary":"...",
    "tags":["auth","jwt"],"updated_at":"2026-08-28T...","path":"docs/api/auth.md"}]
  ```

  `tags` come from **top-level sections only**; sub-section keywords stay in tree.json for localization, which keeps the manifest small and routing focused. A topic buried in a sub-section may therefore not appear in `tags` — fall back to the section walk in Step 2 rather than concluding the document is unrelated.

- **`.kb/index/{path without .md}/tree.json`** — the document record plus the heading skeleton:

  ```json
  {"doc_id":"doc_001","title":"API Auth","domain":"api","source_path":"docs/api/auth.md",
   "summary":"...","ingested_at":"...","source_sha256":"...","total_lines":120,
   "nodes":[{"id":"ch_1","level":2,"title":"Overview","summary":"...","keywords":[],
             "start_line":16,"end_line":40,"children":[]}]}
  ```

## Available script

One deterministic check backs Step 3. It ships with the **kb-ingest** skill rather than this one (`{abs_ingest}/scripts/check_source.py`), and it is read-only, so kb-chat can run it without writing anything:

- **`check_source.py {source_file} {tree_json}`** — compares the source's current SHA256 against the `source_sha256` recorded in tree.json and reports `drifted`. Exit code 0 means "check completed" — a drift is a result in the JSON, not an error.

## Workflow

> **Transparency**: Each step surfaces a short, user-visible signal so the user can follow the flow — where it routed, what it read, and what it verified. Keep these to one line each; they are progress markers, not report artifacts. The answer is the only long-form output.

Progress:
- [ ] **1. Document routing** — Read `.kb/manifest.json`. If `domain_preference` is provided, use it as a strong routing hint. Match domain/title/summary/tags semantically and produce a **ranked candidate list** (most relevant first), not a single pick. Then decide by count: none → answer "not mentioned in the documents" (never guess); one clearly relevant → proceed; several → start with the most relevant, and read further candidates if the question spans documents (comparison, relation, conflict) or the first pass comes up short. Do not interrupt the user just because several candidates exist — escalate only when reading still leaves you unable to decide (candidates conflict, or the question needs a hint). No numeric scores or thresholds; relevance is an ordering, not a score. **User sees**: the chosen document(s), e.g. "→ routed to docs/api/auth.md" (or "→ not in the knowledge base")
- [ ] **2. Section localization** — Read the hit document's `tree.json`, locate the most precise section via **semantic matching** of node title/summary/keywords. Recurse into children until specific enough. **User sees**: the section path, e.g. "→ section: Authentication flow » JWT issuance"
- [ ] **3. Content extraction** — Before reading, check the source has not drifted: run `python {abs_ingest}/scripts/check_source.py {abs_kb}/docs/api/auth.md {abs_kb}/.kb/index/docs/api/auth/tree.json` and read `drifted` from its JSON. If true, the source was edited after ingestion — warn the user that citations may be stale and offer to re-ingest before continuing. Compare the checksum, not the line count: an edit that changes a number or rewords a sentence keeps the line count identical while making every citation into that section silently wrong. Use start_line/end_line as navigation anchors; read the source starting from there. The LLM decides how much to read — expand to parent, siblings, or the full document as judgment dictates. Note that content between the H1 title and the first section heading is the document intro: if the question may concern it (overview, scope, intro facts), read from the top of the file. Record the exact line ranges read — they become the per-claim citations in Step 4. **User sees**: the ranges read, e.g. "→ read docs/api/auth.md#L16-L40"
- [ ] **4. Generate answer** — Organize the answer autonomously based on extracted source text. After each claim, attach a citation link `[path#L{start}-L{end}](path#L{start}-L{end})` backed by the exact range that supports it — `path` is the manifest path (relative to the kb root), so the link resolves against the current directory and clicks open. End with a `Source:` footer listing the distinct citations. **User sees**: the answer with inline citations and the Source footer
- [ ] **5. Self-verify** — Before delivering, re-read your own answer against the source: does every claim carry a citation, and do the cited ranges actually support it? Pay special attention to numeric claims (amounts, dates, ratios) — re-check each digit against the cited lines. Did you actually answer the question? The LLM decides how many rounds — a simple fact may need one glance, complex cross-document reasoning may need several. If a gap is found, go back to Step 3 and re-read, then re-verify. Stop when you can stand behind every claim; if the source still doesn't support it after re-reading, say "not mentioned in the documents". **User sees**: a one-line verdict, e.g. "→ verified: every claim grounded in the cited lines"

## Failure handling

- `.kb/manifest.json` missing → report "knowledge base not initialized; run kb-ingest first"
- No relevant document after routing → say only "not mentioned in the documents"
- Several candidates but reading still can't disambiguate (they conflict, or the question needs a hint) → list the candidates and ask the user to choose
- Source citation missing or line range wrong → re-read the source and verify before answering

## Gotchas

- **path field is critical** — The manifest entry's path is the source file path relative to the repo root; the source is read from there. tree.json lives under the `.kb/index/` mirrored directory. A mismatch makes the document unanswerable
- **tree.json and manifest.json are minified** — Read them as JSON, not prose; use `--pretty` (`{abs_ingest}/scripts/build_tree.py` / `{abs_ingest}/scripts/build_manifest.py`) if you need a readable copy
- **Drift is a checksum question, not a line-count one** — Comparing the source's current line count against `total_lines` feels equivalent and is not. The most common edits — fix a number, reword a clause, change a date — preserve the line count exactly, so the comparison reports "unchanged" while the cited lines now say something else. `check_source.py` compares the SHA256 and catches it
- **Citation links are relative by design** — The `#L{start}-L{end}` suffix is the standard GitHub line-range anchor; the path is the manifest `path` (relative to the kb root), so citations stay machine-independent, read the same as on GitHub, and click open from the current directory. Never embed absolute machine paths
- **Cross-document comparison** — Run routing and localization independently per document
