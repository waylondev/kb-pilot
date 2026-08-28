# kb-polish processing boundaries & principles

## 1. Processing boundaries

| Dimension                 | May change                                                                                                       | Must preserve                                                                                                                   |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Heading-level structure   | ✅ fill skipped levels, optimize meaning                                                                          | ❌ do not reorder sections                                                                                                       |
| Heading wording           | ✅ remove ambiguity, optimize meaning                                                                             | ❌ do not change core terms                                                                                                      |
| Body content              | ❌ keep identical to the source, no edits                                                                         | ✅ preserve the source verbatim                                                                                                  |
| Table format              | ✅ convert to standard Markdown/HTML tables                                                                       | ✅ preserve the raw data                                                                                                         |
| Images                    | ❌ do not convert to text descriptions                                                                            | ✅ keep the original image, shown on the web                                                                                     |
| **Logical relationships** | ❌ no reordering of sections, no splitting clauses, no changing ownership                                         | ✅ preserve section order / table row-column correspondence / list nesting / clause numbers & ownership / conditional statements |
| **Multiple H1 blocks**    | ✅ demote & merge into one H1 by default (rest H1→H2, internal levels shifted); split only when fully independent | ✅ each block's content fully preserved with levels shifted, no content lost; redundant headers/cross-page duplicates deleted    |

> Logical relationships are the bottom line of Step 4 re-render: structure may be normalized (fill levels, unify tables, fix indentation), but the **logical relations between content** (what belongs to what, what comes before what, conditional dependencies, number nesting) must never change.
>
> **Single H1**: kb-pilot treats H1 as the document title (not in the tree; the tree starts at H2). Standard Markdown allows multiple H1s, but multiple H1 blocks in one input file are usually related (e.g. a credit-card PDF = notices/statements + product summary), so **merge into one final by default** (the main title keeps H1, the rest demote to H2 with internal levels shifted); split only when the blocks are fully independent and unrelated. Repeated H1s from headers/page breaks are cleaned and merged directly.

## 2. Core principles

1. **Content correctness first, format compliance second.** Verify content accuracy before adjusting format.
2. **Structure controllable, content lossless.** Only adjust document structure; never alter body content.
3. **Content verification is based on a deterministic source.** A text-only LLM cannot judge whether content matches the source; the deterministic extraction (PyMuPDF text layer / OOXML / ODF / EPUB plaintext, seconds) runs **by default for every document**, giving Step 4 a ground truth. How deep the LLM cross-checks is its own judgment from the issue list and the document type — the extraction itself is never skipped. **No OCR; scans are kept as page images** — OCR is probabilistic recognition with high cost and is outside this skill's scope; a scan (no text layer) is preserved by rendering each page to `images/page_N.png` and embedding `![page N](./images/page_N.png)`, with the content itself left unreadable (never guessed).
4. **Human confirmation is the final backstop.** No automated flow fully replaces a human.

<br />
