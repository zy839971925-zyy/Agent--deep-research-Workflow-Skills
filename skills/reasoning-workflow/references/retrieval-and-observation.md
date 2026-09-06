# Retrieval and observation

**Trigger:** The current task cannot be answered reliably from supplied information/direct reasoning alone.

**Reads:** specific information need, uncertainty source, available evidence surfaces, entity/version/time scope.

**Updates:** observations, retrieved material, failed routes, source locators, new vocabulary/leads.

**May invalidate:** assumptions about available evidence, entity identity, current version, or problem framing.

**Exit:** the needed observation is obtained/bounded or further retrieval has low expected answer gain.

**Related:** [inquiry and research](inquiry-and-research.md), [evidence and provenance](evidence-and-provenance.md), [runtime and delegation](runtime-and-delegation.md).

**Return:** [root workflow](../SKILL.md) → Need evidence / Inquiry loop.

Use when the task needs information beyond what is already given. Retrieval follows an information need; it is not a default display of diligence.

## Choose the evidence surface first

Ask where the uncertainty is most directly observable. Possible surfaces include:

- conversation context and user-provided materials;
- connected/private workspace sources;
- local repository, git history, source code, configuration, logs, tests, and runtime state;
- structured data, spreadsheets, databases, registries, filings, or official records;
- public web, current documentation, academic literature, archives, and specialist reporting;
- social/community sources, issue trackers, forums, user reports, interviews, and field observations;
- experiments or computation when authorized and supported.

Prefer direct observation over commentary about observation. Public web is one surface, not the default for every task.

## Discovery versus verification

For discovery, vary concepts, aliases, terminology, language, adjacent disciplines, source ecosystems, entities, references, citations, and historical paths. Learn vocabulary from encountered sources rather than endlessly rephrasing the prompt.

For verification, narrow to exact entity, identity, version, date, jurisdiction, population, metric, configuration, or quoted assertion. Resolve entity/version before merging evidence.

## Inspect underlying material

Search snippets, generated summaries, abstracts, and reposts are routing aids. Read the underlying source and the context required for the inference. Inspect methods, footnotes, tables, figures, code, or version history when the claim depends on them.

For code, distinguish documentation claims, inspected implementation, and observed execution. Reading code is not running it. For human statements, distinguish original recording/text from transcript, paraphrase, or secondary report.

## When a route fails

Repeated results may reflect vocabulary mismatch, indexing limits, syndication, a faulty premise, inaccessible primary material, or the wrong evidence surface. Change the relevant dimension rather than issuing cosmetic query rewrites.

A failed URL is not evidence that a publication or feature does not exist. Seek authorized mirrors, repositories, archives, primary substitutes, or local copies where appropriate.

## Independent trajectories versus gap decomposition

For a complex multi-claim task, decompose by missing evidence and let the root synthesis maintain shared state.

For a high-value needle-in-a-haystack fact where search path dependence is the main failure mode, try a small number of genuinely independent discovery trajectories: different starting clues, source ecosystems, languages, entities, or historical directions. Compare the evidence found; model agreement is not empirical corroboration.

## Stop repetition

Track enough search history to recognize route duplication. Stop unchanged retries with no concrete prospect of new evidence. A search round is valuable only if it changes the working model, closes a material gap, reveals a new route, or strengthens verification.

[← Return to root workflow](../SKILL.md)
