---
name: kb-correct
description: >-
  Use when the user corrects a previous answer that came from the knowledge base.
  Triggers on "that's wrong", "should be", "correct this", "update the answer" —
  even when the user doesn't name the underlying system.
compatibility: Requires Git
metadata:
  repo_url: ""
  kb_path: knowledge_repo
---

# kb-correct — Persist a correction to the knowledge base

When the user disagrees with an answer, record the corrected answer as append-only evidence under `.kb/memory/corrections/`. Future kb-chat answers will load these records and either surface the correction or show it side-by-side with the source.

## Input / Output

```yaml
Input:
- question: string       # the original question
- correct_answer: string # the user's corrected answer
- doc_id: string         # document that provided the original answer
- ch_id?: string         # optional; chapter/section id, if known
- session_id: string     # current conversation id

Output:
- appended record in .kb/memory/corrections/{doc_id}.jsonl
- git commit + push
```

## Correction workflow

Progress:
- [ ] **1. Identify target** — Locate the doc_id (and ch_id, if available) of the answer being corrected. Use the current conversation context first; if unclear, ask the user to confirm
- [ ] **2. Append record** — Append a JSON line to `.kb/memory/corrections/{doc_id}.jsonl`:
  ```json
  {"question": "the question", "correct_answer": "user's corrected answer", "ch_id": "ch_x", "session_id": "xxx", "timestamp": "ISO timestamp", "status": "active"}
  ```
- [ ] **3. Detect conflicts** — If earlier records for the same question have a different `correct_answer`, mark the new record status as `conflicted`; otherwise keep `active`
- [ ] **4. Commit to Git** — `git add .kb/memory/ && git commit -m "kb: correct {doc_id}" && git push`
- [ ] **5. Report to user** — doc_id, ch_id, and whether the correction conflicts with existing records

## Failure handling

- Missing doc_id → ask the user which answer they are correcting
- `.kb/` directory missing → report "knowledge base not initialized; run kb-ingest first"
- Git unavailable → report clearly and do not leave uncommitted corrections

## Gotchas

- **Append-only** — Never edit or delete existing correction records; duplicates signal consensus, conflicts are shown side-by-side
