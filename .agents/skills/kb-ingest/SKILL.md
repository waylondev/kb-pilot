---
name: kb-ingest
description: >-
  Use when the user wants to add a Markdown document to the knowledge base, ingest
  a whole directory of .md files, or initialize the knowledge base from a Git repo.
  Triggers on "ingest this doc", "add to knowledge base", "import these markdown
  files", "set up the knowledge base from this repo" — even when the user doesn't
  name the underlying system. Markdown only; PDF/Word/HTML conversion is the user's job.
compatibility: Requires Python 3.10+ and Git
metadata:
  repo_url: ""
  kb_path: knowledge_repo
---

# kb-ingest — Ingest Markdown documents into the knowledge base

Original files stay in place. Metadata lives under `.kb/` in a mirrored path layout. Git is the source of truth. Path mapping: `docs/api/auth.md` → `.kb/index/docs/api/auth/`. Each `tree.json` is both the document record (doc_id, title, domain, source_path, summary, ingested_at) and the heading skeleton.

## Input / Output

```yaml
Input:
- repo_url: string          # Git URL to clone/pull; empty for local {kb_path}
- kb_path: string           # Knowledge base root, relative to project root (default: knowledge_repo)
- source_rel_path?: string  # Markdown file path inside {kb_path}; omit for batch/repo init

Output:
- tree.json: document record + heading skeleton with LLM-filled summary/keywords
- manifest.json: updated global routing table
```

## Failure handling

- Source file missing → stop and ask the user to check the path
- No usable headings or invalid Markdown syntax → return to Step 2 and ask the user to fix the document
- `tree.json` validation reports issues → inspect source headings, regenerate, then re-fill
- Git unavailable → report clearly and note that committing is the user's responsibility

## Available scripts

Deterministic subtasks use scripts; semantic tasks must be done by the LLM — scripts never touch semantics, the LLM never touches structure parsing. Both scripts support `--help`, emit JSON to stdout, and progress to stderr. **Both output minified JSON by default** (to save tokens when the LLM reads it in kb-chat); pass `--pretty` whenever you need a human-readable copy, e.g. before editing by hand.

- **`scripts/build_tree.py`** — Parses Markdown heading hierarchy into a tree.json (document record + heading skeleton; summary/keywords left empty for LLM to fill) and runs deterministic structure validation
- **`scripts/build_manifest.py`** — Scans all tree.json under `.kb/index/` and aggregates them into `.kb/manifest.json`

Script paths follow the standard skill convention: `scripts/...` is relative to **this skill's directory root** (the agent runs commands from there), so no absolute paths are needed for the scripts. Knowledge-base file paths, however, are resolved against the project root — so resolve `{kb_path}` to an absolute path (`{abs_kb}`) before running, and use `{abs_kb}/...` in the commands below.

## Ingest workflow

Progress:
- [ ] **1. Prepare repo** — If `{kb_path}` does not exist, `git clone {repo_url} {kb_path}`; otherwise `git pull`. Ensure `.kb/index/` exists
- [ ] **2. Locate source** — Confirm `{kb_path}/{source_rel_path}` exists; check that headings use valid `#`–`######` syntax. If the document has no usable headings, ask the user to fix the document and retry
- [ ] **3. Assign doc_id** — Omit `--doc-id` in Step 4; build_tree.py auto-infers it by scanning **all** tree.json under `.kb/index/` (`doc_{max_seq+1:03d}`), and **keeps the id stable on re-ingest** by reading the existing tree.json at the output path. Only pass `--doc-id` when you must force a specific id. Never count by hand
- [ ] **4. Generate tree.json** — Run (omit `--doc-id`; it is inferred automatically):
  ```bash
  python scripts/build_tree.py {abs_kb}/{source_rel_path} \
    {abs_kb}/.kb/index/{source_rel_dir}/tree.json \
    --title "{title}" --domain "{domain}" \
    --source-path {source_rel_path}
  ```
  `{abs_kb}` = absolute path to the knowledge base root (resolve `{kb_path}` from the project root). `{source_rel_dir}` = source_rel_path with `.md` stripped (e.g. `docs/api/auth.md` → `docs/api/auth`). `{source_rel_path}` stays relative to the kb root — that is what the manifest stores and kb-chat reads. `{domain}` is user-specified or inferred from the top-level directory
- [ ] **5. Validate skeleton** — Check the script reported `validation_issues: 0` (an empty tree — no H2+ headings — is itself an issue). Then review `validation_warnings`: currently (a) a heading that skips a level (e.g. H2 → H4), or (b) a tree whose top-level node is not an H2. Both are structurally allowed and nest correctly, but they usually signal a missing heading level in the source. Whether to act is the LLM's judgment: present the warning, and only ask the user whether to insert the missing level if you can't decide for the user — e.g. the fix is clearly a separate concern, or the source's intent is ambiguous. Do not interrupt for every warning
- [ ] **6. LLM fills summary and keywords, then self-verifies** — Read each section's full content, then autonomously distill a concise summary and keywords. Also write a one-sentence document-level summary into the top-level `summary` field. Then re-read each filled entry against its source: does the summary capture the section's actual point? Would these keywords help a future question route here? The LLM decides how many rounds — stop when every node's filling holds up against its source. **User sees**: a one-line summary of each filled section, e.g. "→ filled ch_1 'Overview': <brief summary>; keywords: [auth, login]"
- [ ] **7. Update manifest.json** — Run `scripts/build_manifest.py {abs_kb}` to aggregate all documents
- [ ] **8. Hand off to user** — `.kb/` is now updated but **not committed**: committing is the user's (or CI's) responsibility. Leave the working tree untouched — do not run any git command. Report back the doc_id, source path, and tree.json node count

## Batch ingest

When the user says "ingest entire directory", "scan all md files", or "initialize from a Git repo":

- [ ] 1. `git clone {repo_url} {kb_path}` (if not present)
- [ ] 2. Recursively scan `{kb_path}` for all `.md` files, excluding `.kb/` and `.git/`
- [ ] 3. For each file without a tree.json in its mirrored `.kb/index/` directory, run ingest workflow from Step 3 (assign doc_id, generate tree.json, fill and verify)
- [ ] 4. Finally run `scripts/build_manifest.py {abs_kb}` once
- [ ] 5. Remind the user to commit — `.kb/` and any new source files are updated but uncommitted; committing is the user's (or CI's) call. Do not run any git command

## Rebuild on change

When a source file is heavily modified, detect drift via `source_sha256` in tree.json:

- [ ] 1. Compare `source_sha256` in tree.json against the source file's current SHA256
- [ ] 2. If equal → skip; if not → re-run ingest workflow Step 4 (the script preserves existing summary/keywords and the document-level summary where structure still matches)
- [ ] 3. If structure changed, re-run Step 6 (old summary/keywords may not match new sections; re-fill and re-verify)
- [ ] 4. Run Step 7 to update the manifest; remind the user to commit (Step 8)

## Gotchas

- **source_path field** — Passed via `--source-path`; a typo makes the document unanswerable, because build_manifest.py uses it for the manifest's path field and kb-chat uses it to read the source
- **Heading hierarchy** — H1 is the document title and does not enter the tree; the tree starts at H2. Headings that skip a level (e.g. H2 → H4) are allowed — they nest under the nearest shallower heading with precise line anchors — and so is a tree whose top-level node is not an H2; but build_tree.py reports both as `validation_warnings`, because they usually signal a missing level. Source files without H2+ headings produce an empty tree (a `validation_issues` error)
- **Minified JSON** — tree.json and manifest.json are minified by default to save tokens; use `--pretty` when you need to read or edit them by hand
