---
name: kb-ingest
description: >-
  Use when the user wants to add a Markdown document to the knowledge base, ingest
  a whole directory of .md files, or initialize the knowledge base from a Git repo.
  Triggers on "ingest this doc", "add to knowledge base", "import these markdown
  files", "set up the knowledge base from this repo" — even when the user doesn't
  name the underlying system. Markdown only; PDF/Word/HTML conversion is the user's job.
compatibility: Requires Python 3.10+, Git, and PyYAML
metadata:
  repo_url: ""
  kb_path: knowledge_repo
---

# kb-ingest — Build a table of contents for a document

Original files stay in place. Metadata lives under `.kb/` in a mirrored path layout. Git is the source of truth. Path mapping: `docs/api/auth.md` → `.kb/index/docs/api/auth/`.

## Available scripts

Deterministic subtasks use scripts; semantic tasks must be done by the LLM. Both scripts support `--help`, emit JSON to stdout, and progress to stderr.

- **`scripts/build_tree.py`** — Parses Markdown heading hierarchy to produce a tree.json skeleton (summary/keywords left empty for LLM to fill)
- **`scripts/build_manifest.py`** — Scans all metadata.yaml files and aggregates them into .kb/manifest.json

## Ingest workflow

Progress:
- [ ] **1. Prepare repo** — If `{kb_path}` does not exist, `git clone {repo_url} {kb_path}`; otherwise `git pull`. Ensure `.kb/index/` and `.kb/memory/corrections/` exist
- [ ] **2. Locate source** — Confirm `{kb_path}/{source_rel_path}` exists; check heading hierarchy (`#`–`######`) is complete. If missing, ask the user to fix the document and retry
- [ ] **3. Assign doc_id** — Scan all metadata.yaml under `.kb/index/`, take max sequence + 1 (e.g. `doc_007`). Never rely on memory
- [ ] **4. Create metadata.yaml** — In `.kb/index/{source_rel_dir}/`:
  ```yaml
  doc_id: {doc_id}
  title: "{title from H1}"
  domain: "{user-specified or inferred from top-level directory}"
  source_path: {source_rel_path}
  summary: ""  # filled by LLM in Step 7
  ingested_at: "{ISO timestamp}"
  ```
- [ ] **5. Generate tree.json skeleton** — Run:
  ```bash
  python scripts/build_tree.py {kb_path}/{source_rel_path} \
    {kb_path}/.kb/index/{source_rel_dir}/tree.json \
    --doc-id {doc_id} --title "{title}"
  ```
  `{source_rel_dir}` = source_rel_path with `.md` stripped (e.g. `docs/api/auth.md` → `docs/api/auth`)
- [ ] **6. Validate skeleton** — Check tree.json: node count > 0, top-level nodes have children where expected, start_line/end_line are sane. On failure, go back to Step 2 and inspect heading hierarchy
- [ ] **7. LLM fills summary and keywords** — Read each section's full content, then autonomously distill a concise summary and keywords that capture its essence. Also write a one-sentence document-level summary into the `summary` field of metadata.yaml. Trust the LLM's understanding — no templates, no extraction rules, no keyword algorithms. (**Cannot be replaced by a rule-based script** — scripts cannot understand semantics, and would destroy routing accuracy)
- [ ] **8. Self-verify fillings** — Re-read each filled summary/keywords against its source section: does the summary capture the section's actual point? Would these keywords help a future question route here? The LLM decides how many rounds — a short section may need one glance, a complex one may need re-reading and refining. Stop when every node's filling holds up against its source
- [ ] **9. Update manifest.json** — Run `scripts/build_manifest.py {kb_path}` to aggregate all documents
- [ ] **10. Commit to Git** — `git add .kb/` and any new source files, `git commit -m "kb: ingest {doc_id} - {title}"`, `git push`
- [ ] **11. Report to user** — doc_id, source path, tree.json node count

## Batch ingest

When the user says "ingest entire directory", "scan all md files", or "initialize from a Git repo":

- [ ] 1. `git clone {repo_url} {kb_path}` (if not present)
- [ ] 2. Recursively scan `{kb_path}` for all `.md` files, excluding `.kb/` and `.git/`
- [ ] 3. For each file without a metadata.yaml, run ingest workflow from Step 4
- [ ] 4. Finally run `scripts/build_manifest.py {kb_path}` once
- [ ] 5. Single Git commit + push

## Rebuild on change

When a source file is heavily modified, detect drift via `source_sha256` in tree.json:

- [ ] 1. Compare `source_sha256` in tree.json against the source file's current SHA256
- [ ] 2. If equal → skip; if not → re-run ingest workflow Step 5 (the script preserves existing summary/keywords where possible)
- [ ] 3. If structure changed, re-run Step 7 and Step 8 (old summary/keywords may not match new sections; re-fill and re-verify)
- [ ] 4. Run Step 9 to update manifest, Step 10 to commit

## Gotchas

- **doc_id sequence** — Always scan metadata.yaml files under `.kb/index/` to confirm the max sequence; do not rely on memory
- **source_path field** — In metadata.yaml, source_path is relative to the repo root. build_manifest.py uses it to generate manifest's path field; kb-chat uses it to read the source. A typo here makes the document unanswerable
- **Heading hierarchy** — Source files must have a complete `#`–`######` hierarchy; this is the foundation of tree.json. H1 is the document title and does not enter the tree; the tree starts at H2
- **summary/keywords cannot be scripted** — Rule-based scripts cannot understand semantics and would break kb-chat's routing accuracy. Even if it looks like "just keyword extraction", the LLM must fill each node
- **Markdown only** — PDF/Word/HTML conversion is the user's responsibility
- **No vectors / chunks / graphs** — This is the core design boundary; the LLM only needs a TOC and the full source text
- **No metadata in user directories** — All metadata lives under `.kb/`; deleting it uninstalls cleanly
- **Concurrency** — When multiple users ingest simultaneously, file conflicts under `.kb/` are resolved by Git merge; no application-layer locking
- **Scale boundary** — When a single repo exceeds a few hundred documents, split by team or domain into separate Git repos; no physical sharding
- **{kb_path} placeholder** — Replace with the actual knowledge base path at runtime; defaults to `knowledge_repo`
