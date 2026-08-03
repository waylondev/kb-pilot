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

# kb-ingest — Ingest Markdown documents into the knowledge base

Original files stay in place. Metadata lives under `.kb/` in a mirrored path layout. Git is the source of truth. Path mapping: `docs/api/auth.md` → `.kb/index/docs/api/auth/`.

## Input / Output

```yaml
Input:
- repo_url: string          # Git URL to clone/pull; empty for local {kb_path}
- kb_path: string           # Knowledge base root, relative to project root (default: knowledge_repo)
- source_rel_path?: string  # Markdown file path inside {kb_path}; omit for batch/repo init

Output:
- metadata.yaml: document record (doc_id, title, domain, source_path, summary, ingested_at)
- tree.json: heading hierarchy with LLM-filled summary/keywords
- manifest.json: updated global routing table
```

## Failure handling

- Source file missing → stop and ask the user to check the path
- No usable headings or invalid Markdown syntax → return to Step 2 and ask the user to fix the document
- `tree.json` validation fails → inspect source headings, regenerate, then re-fill
- Git unavailable → report clearly and do not leave `.kb/` uncommitted

## Available scripts

Deterministic subtasks use scripts; semantic tasks must be done by the LLM — scripts never touch semantics, the LLM never touches structure parsing. Both scripts support `--help`, emit JSON to stdout, and progress to stderr.

- **`scripts/build_tree.py`** — Parses Markdown heading hierarchy to produce a tree.json skeleton (summary/keywords left empty for LLM to fill)
- **`scripts/build_manifest.py`** — Scans all metadata.yaml files and aggregates them into .kb/manifest.json

## Ingest workflow

Progress:
- [ ] **1. Prepare repo** — If `{kb_path}` does not exist, `git clone {repo_url} {kb_path}`; otherwise `git pull`. Ensure `.kb/index/` and `.kb/memory/corrections/` exist
- [ ] **2. Locate source** — Confirm `{kb_path}/{source_rel_path}` exists; check that headings use valid `#`–`######` syntax. If the document has no usable headings, ask the user to fix the document and retry
- [ ] **3. Assign doc_id and create metadata.yaml** — Scan all metadata.yaml under `.kb/index/`, take max sequence + 1 (e.g. `doc_007`). Never rely on memory. Then create `.kb/index/{source_rel_dir}/metadata.yaml`:
  ```yaml
  doc_id: {doc_id}
  title: "{title from H1}"
  domain: "{user-specified or inferred from top-level directory}"
  source_path: {source_rel_path}
  summary: ""  # filled by the LLM later
  ingested_at: "{ISO timestamp}"
  ```
- [ ] **4. Generate tree.json skeleton** — Run:
  ```bash
  python scripts/build_tree.py {kb_path}/{source_rel_path} \
    {kb_path}/.kb/index/{source_rel_dir}/tree.json \
    --doc-id {doc_id} --title "{title}"
  ```
  `{source_rel_dir}` = source_rel_path with `.md` stripped (e.g. `docs/api/auth.md` → `docs/api/auth`)
- [ ] **5. Validate skeleton** — Check tree.json: node count > 0, top-level nodes have children where expected, start_line/end_line are sane. On failure, go back to Step 2 and inspect heading hierarchy
- [ ] **6. LLM fills summary and keywords, then self-verifies** — Read each section's full content, then autonomously distill a concise summary and keywords. Also write a one-sentence document-level summary into the `summary` field of metadata.yaml. Then re-read each filled entry against its source: does the summary capture the section's actual point? Would these keywords help a future question route here? The LLM decides how many rounds — stop when every node's filling holds up against its source
- [ ] **7. Update manifest.json** — Run `scripts/build_manifest.py {kb_path}` to aggregate all documents
- [ ] **8. Commit to Git** — `git add .kb/` and any new source files, `git commit -m "kb: ingest {doc_id} - {title}"`, `git push`
- [ ] **9. Report to user** — doc_id, source path, tree.json node count

## Batch ingest

When the user says "ingest entire directory", "scan all md files", or "initialize from a Git repo":

- [ ] 1. `git clone {repo_url} {kb_path}` (if not present)
- [ ] 2. Recursively scan `{kb_path}` for all `.md` files, excluding `.kb/` and `.git/`
- [ ] 3. For each file without a metadata.yaml, run ingest workflow from Step 3 (assign doc_id and create metadata.yaml, generate tree.json, fill and verify)
- [ ] 4. Finally run `scripts/build_manifest.py {kb_path}` once
- [ ] 5. Single Git commit + push

## Rebuild on change

When a source file is heavily modified, detect drift via `source_sha256` in tree.json:

- [ ] 1. Compare `source_sha256` in tree.json against the source file's current SHA256
- [ ] 2. If equal → skip; if not → re-run ingest workflow Step 4 (the script preserves existing summary/keywords where possible)
- [ ] 3. If structure changed, re-run Step 6 (old summary/keywords may not match new sections; re-fill and re-verify)
- [ ] 4. Run Step 7 to update manifest, Step 8 to commit

## Gotchas

- **doc_id sequence** — Always scan metadata.yaml files under `.kb/index/` to confirm the max sequence; do not rely on memory
- **source_path field** — A typo in source_path makes the document unanswerable, because build_manifest.py uses it for the manifest's path field and kb-chat uses it to read the source
- **Heading hierarchy** — H1 is the document title and does not enter the tree; the tree starts at H2. Source files without H2 headings will produce an empty tree.json
