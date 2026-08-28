# kb-polish processing boundaries & scoring criteria

## 1. Processing boundaries

| Dimension | May change | Must preserve |
|---|---|---|
| Heading-level structure | ✅ fill skipped levels, optimize meaning | ❌ do not reorder sections |
| Heading wording | ✅ remove ambiguity, optimize meaning | ❌ do not change core terms |
| Body content | ❌ keep identical to the source, no edits | ✅ preserve the source verbatim |
| Table format | ✅ convert to standard Markdown/HTML tables | ✅ preserve the raw data |
| Images | ❌ do not convert to text descriptions | ✅ keep the original image, shown on the web |
| **Logical relationships** | ❌ no reordering of sections, no splitting clauses, no changing ownership | ✅ preserve section order / table row-column correspondence / list nesting / clause numbers & ownership / conditional statements |
| **Multiple H1 blocks** | ✅ demote & merge into one H1 by default (rest H1→H2, internal levels shifted); split only when fully independent | ✅ each block's content fully preserved with levels shifted, no content lost; redundant headers/cross-page duplicates deleted |

> Logical relationships are the bottom line of Step 4 re-render: structure may be normalized (fill levels, unify tables, fix indentation), but the **logical relations between content** (what belongs to what, what comes before what, conditional dependencies, number nesting) must never change.
>
> **Single H1**: kb-pilot treats H1 as the document title (not in the tree; the tree starts at H2). Standard Markdown allows multiple H1s, but multiple H1 blocks in one input file are usually related (e.g. a credit-card PDF = notices/statements + product summary), so **merge into one final by default** (the main title keeps H1, the rest demote to H2 with internal levels shifted); split only when the blocks are fully independent and unrelated. Repeated H1s from headers/page breaks are cleaned and merged directly.

## 2. Format scoring criteria

### 2.1 Heading-level continuity (30 pts)
| Criterion | Score |
|---|---|
| `# → ## → ###` fully continuous, no jumps | 10 |
| Headings have clear meaning, no duplicates | 10 |
| Heading levels match the document logic | 10 |

**Deductions:**
- one jump: −3
- one duplicate heading: −2
- vague heading meaning (e.g. "Instructions"): −2

### 2.2 Table structural integrity (20 pts)
| Criterion | Score |
|---|---|
| Header present and correct | 10 |
| Consistent column counts, aligned data | 10 |

**Deductions:**
- missing header: −5
- inconsistent column counts: −3
- misaligned data: −2

### 2.3 Heading-meaning clarity (20 pts)
| Criterion | Score |
|---|---|
| Each heading independently conveys its topic | 20 |

**Deductions:**
- too generic (e.g. "Overview", "Introduction"): −3
- ambiguous heading: −2
- heading does not match content: −5

### 2.4 List format consistency (10 pts)
| Criterion | Score |
|---|---|
| Unified list markers (all `-` or all `1.`) | 5 |
| Reasonable indentation levels | 5 |

### 2.5 Code blocks & special elements (10 pts)
| Criterion | Score |
|---|---|
| Code blocks annotated with a language | 5 |
| Image reference paths correct | 5 |

### 2.6 Content truncation & mojibake (10 pts)
| Criterion | Score |
|---|---|
| No mojibake characters | 5 |
| Paragraphs complete, no truncation | 5 |

## 3. Content verification scoring (Step 3 extraction cross-check)

### 3.1 Text content completeness (35 pts)
| Criterion | Score |
|---|---|
| Source text fully appears in the Markdown | 35 |

**Deductions:**
- each missing piece of content: −5
- each scrambled piece of content: −3

### 3.2 Table data accuracy (30 pts)
| Criterion | Score |
|---|---|
| Table values match the source | 15 |
| Row/column relations match the source | 15 |

### 3.3 Heading & structure consistency (20 pts)
| Criterion | Score |
|---|---|
| Section order matches the source | 10 |
| Heading levels match the source | 10 |

### 3.4 Special elements preserved (15 pts)
| Criterion | Score |
|---|---|
| Images correctly preserved | 5 |
| Code blocks correctly preserved | 5 |
| Footnotes correctly preserved | 5 |

## 4. Core principles

1. **Content correctness first, format compliance second.** Verify content accuracy before adjusting format.
2. **Structure controllable, content lossless.** Only adjust document structure; never alter body content.
3. **Content verification is based on a deterministic source and cannot be skipped.** A text-only LLM cannot judge whether content matches the source; extract the source with PyMuPDF text layer / OOXML / ODF / EPUB plaintext and cross-check (seconds, deterministic). **No scans/images (no OCR)** — that is probabilistic recognition with high cost, outside this skill's scope.
4. **Human confirmation is the final backstop.** No automated flow fully replaces a human.
