# AGENTS — Design principles for LLM-driven knowledge base

> Scripts constrain the skeleton; the LLM fills the content. Trust the LLM's intelligence — it is the second engineer, not a keyword matcher.

## Core belief

The LLM is sufficiently intelligent. It only needs **a precise table of contents and the full source text** — the same two things a human uses in a library. No vectors, no chunks, no graphs, no extraction algorithms. The LLM reads, understands, and answers like a human flipping through a book.

## Skeleton vs. Flesh

| Layer | Who builds it | What it contains | Why |
|-------|--------------|-----------------|-----|
| **Skeleton** (deterministic) | Scripts | Heading hierarchy, line numbers, doc_id, SHA256 | Machines are good at counting lines and parsing structure |
| **Flesh** (semantic) | LLM | Summary, keywords, routing, localization, answers | Only the LLM understands meaning; scripts would destroy accuracy |

The boundary is absolute: **scripts never touch semantics; the LLM never touches structure parsing.** If you find yourself writing a regex to extract keywords or a rule to match summaries, stop — that is the LLM's job.

## What to do

- **Let the LLM navigate autonomously** — It picks the document, dives into the section, expands the read range as needed. Provide anchors (line numbers, TOC), not rules
- **Let the LLM organize answers freely** — The only hard requirement is traceable citations. Format, length, and style are the LLM's call
- **Let the LLM distill summaries** — After reading each section, the LLM writes what it understood. No templates, no extraction algorithms
- **Let the LLM judge corrections** — It decides whether a correction is relevant, whether duplicates signal consensus, whether conflicts need side-by-side display
- **Keep scripts minimal** — Parse structure, aggregate metadata, compute hashes. That is all
- **When uncertain, consult the user** — The LLM asks rather than guesses, just like a librarian

## What not to do

- **No vector embeddings** — The LLM does not need cosine similarity; it understands meaning directly
- **No chunk splitting** — Full source text with line-level TOC is more precise than any chunk
- **No entity graphs / knowledge graphs** — The heading tree is the only graph needed
- **No keyword extraction algorithms** — TF-IDF, RAKE, TextRank all miss what the LLM catches
- **No rigid decision trees for routing** — "If score > 0.8 then select" is not how a human browses a library
- **No answer templates beyond citation** — The LLM knows how to write a good answer
- **No format conversion** — PDF/Word/HTML → Markdown is the user's job, not the system's
- **No sharding / physical splitting** — One repo = one cognitive boundary; split by team or domain, not by code
- **No auxiliary structures beyond tree.json + manifest.json** — Aliases, infoboxes, inverted indexes, multi-level routing tables all add complexity without value

## SKILL design principles

1. **Description focuses on user intent** — Triggers are natural phrases ("ingest this doc", "what's the difference"), not project names or implementation terms
2. **Checklist, not decision tree** — Steps are progress markers, not if-else branches. The LLM decides how to execute each step
3. **Gotchas are positive guidance** — "Answers must be grounded in source text" is better than "Never fabricate"
4. **Progressive disclosure** — Core logic in SKILL.md; script details in `--help`. Do not dump everything into the SKILL
5. **Config block declares tunables** — `repo_url`, `kb_path` are in frontmatter, not hardcoded in steps

## Script design principles

1. **argparse CLI with `--help`** — Examples and exit codes in the epilog
2. **stdout = JSON result, stderr = progress** — Machine-parseable output, human-readable logs
3. **Single responsibility** — `build_tree.py` parses headings; `build_manifest.py` aggregates entries. No god scripts
4. **Exit codes are meaningful** — 0 success, 1 unexpected, 2 file-not-found, 3 dependency-missing
5. **Preserve LLM work on rebuild** — When source changes, keep existing summary/keywords where structure still matches
6. **No magic numbers without comments** — Every constant gets a one-line explanation

## File map

```
.agents/
├── AGENTS.md                      # this file — design principles for all agents
└── skills/
    ├── kb-ingest/
    │   ├── SKILL.md               # ingest workflow (10 steps: clone → tree → LLM fill → manifest → commit)
    │   └── scripts/
    │       ├── build_tree.py      # Markdown → tree.json skeleton (deterministic)
    │       └── build_manifest.py  # metadata.yaml × N → manifest.json (deterministic)
    └── kb-chat/
        └── SKILL.md               # QA workflow (6 steps: route → localize → read → correct → answer)
```

## Optimization directions

When improving this system, ask: **"Am I adding structure the LLM needs, or am I adding rules the LLM doesn't need?"**

- **Good optimization**: Better heading parser, faster manifest aggregation, clearer SKILL steps, smarter line-range anchoring
- **Bad optimization**: Vector search fallback, chunk-level retrieval, keyword scoring, multi-stage routing pipeline, answer post-processing filters

The system is deliberately minimal. Every addition must justify itself against the core belief: the LLM is smart enough.
