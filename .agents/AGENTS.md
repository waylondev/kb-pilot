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
- **Let the LLM reflect on its own answer** — Before delivering, it re-checks every claim against the source and decides for itself how many rounds it needs. No fixed round count, no score threshold — the stop condition is "I can stand behind every claim". This is not a constraint; it is the LLM using its own judgment, like a human double-checking notes before answering

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

SKILLs **must** follow the official [Agent Skills](https://agentskills.io) guides. Do not improvise — read the guides, then implement. Key points adapted to this project:

- **Frontmatter uses only official fields** — `name`, `description`, `compatibility`, `metadata`, `license`, `allowed-tools`. No custom fields like `config`. Project tunables (`repo_url`, `kb_path`) go in `metadata`
- **Add what the agent lacks, omit what it knows** — Only write what the LLM wouldn't figure out on its own
- **Match specificity to fragility** — Be prescriptive for fragile operations (path mapping, doc_id); give freedom where multiple approaches are valid
- **Favor procedures over declarations** — Teach *how to approach*, not *what to produce*
- **Checklists, not decision trees** — Steps are progress markers, not if-else branches
- **Validation loops** — Validate after fragile operations (kb-ingest Step 6 + Step 8, kb-chat Step 7)
- **Bundling reusable scripts** — Deterministic logic lives in `scripts/`; the LLM handles semantics

## Script design principles

- **Self-contained with PEP 723 inline dependencies** — Declare external deps (e.g. `# /// script\n# dependencies = ["pyyaml"]\n# ///`) so scripts run without separate install steps
- **argparse CLI with `--help`** — Examples and exit codes in the epilog
- **stdout = JSON result, stderr = progress** — Machine-parseable output, human-readable logs
- **Single responsibility** — One script does one deterministic thing
- **Preserve LLM work on rebuild** — Keep existing summary/keywords where structure still matches

## Official references

When creating or modifying SKILLs, **read these first** — do not write SKILLs from scratch based on guesswork:

| Guide | What it covers | URL |
|-------|---------------|-----|
| Quickstart | `SKILL.md` basic structure, discovery / activation / execution | https://agentskills.io/skill-creation/quickstart |
| Best practices | Spending context wisely, calibrating control, patterns for effective instructions | https://agentskills.io/skill-creation/best-practices |
| Optimizing descriptions | How to write the `description` field so the SKILL triggers on the right prompts | https://agentskills.io/skill-creation/optimizing-descriptions |
| Specification | Complete format reference for `SKILL.md` (frontmatter fields, progressive disclosure, file layout) | https://agentskills.io/specification |
| Using scripts in skills | When to bundle scripts, CLI interfaces, stdout / stderr conventions | https://agentskills.io/skill-creation/using-scripts |
| Example skills | Real-world SKILLs on GitHub for reference | https://github.com/anthropics/skills |

## File map

```
.agents/
├── AGENTS.md                      # this file — design principles for all agents
└── skills/
    ├── kb-ingest/
    │   ├── SKILL.md               # ingest workflow (11 steps: clone → tree → LLM fill → self-verify → manifest → commit)
    │   └── scripts/
    │       ├── build_tree.py      # Markdown → tree.json skeleton (deterministic)
    │       └── build_manifest.py  # metadata.yaml × N → manifest.json (deterministic)
    ├── kb-chat/                   # QA workflow (7 steps: route → localize → read → answer → self-verify)
    │   └── SKILL.md
    └── kb-correct/                # correction persistence
        └── SKILL.md
```

## Optimization directions

When improving this system, ask: **"Am I adding structure the LLM needs, or am I adding rules the LLM doesn't need?"**

- **Good optimization**: Better heading parser, faster manifest aggregation, clearer SKILL steps, smarter line-range anchoring
- **Bad optimization**: Vector search fallback, chunk-level retrieval, keyword scoring, multi-stage routing pipeline, answer post-processing filters

The system is deliberately minimal. Every addition must justify itself against the core belief: the LLM is smart enough.
