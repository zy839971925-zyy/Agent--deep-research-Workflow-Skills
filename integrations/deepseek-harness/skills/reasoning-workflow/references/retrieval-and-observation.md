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

## Online search: turn the causal model into retrieval moves

A causal chain is a set of hypotheses to investigate, not a query template and not an established fact. Search should retrieve observations that can update a specific link, not merely pages that repeat the question's nouns.


When the search interface supports useful operators, treat them as optional controls, not as the strategy itself. For example, an exact phrase/title, a known `site:` domain, or a date/`filetype:` filter can locate a specific official document or PDF; use the syntax documented for that engine and inspect whether it worked. Add restrictive operators one at a time because they can hide relevant evidence. Search ranking and filtered results are never a completeness guarantee.

1. **Choose one answer-bearing gap.** Name the proposed edge or claim, its population/system and time scope, the live rival explanation, and the observation that would change the answer. Keep only variables that affect this gap; do not pack every node in a causal diagram into one long query.
2. **Orient, then target.** If terminology or evidence sources are unclear, begin with a broad orientation query or a relevant review/official overview. Read titles and underlying material to learn the field's construct names, measures, aliases, study designs, and source venues. Then make focused queries for the gap. In a bibliographic database, combine synonyms within a concept and combine only the essential concepts across sets; use both free text and the database's controlled vocabulary when available. On general web search, use the interface's actual syntax rather than assuming Boolean, phrase, wildcard, or exclusion operators behave consistently across engines.
3. **Vary the query's job, not just its wording.** Depending on the unresolved link, search separately for: (a) the effect or comparison, with the relevant population, exposure/intervention, comparator, outcome, and time; (b) the mechanism or mediator, including process, sequence, dose, and timing; (c) the strongest live alternative, such as confounding, selection, reverse causality, implementation failure, or null/negative results; and (d) a boundary that could change generalization. These are candidate query roles, not a quota; use only those that could change the answer. Avoid one overconstrained query that requires every link and all terminology to appear in the same result.
4. **Let useful results teach the next query.** Open the source, not just the result snippet. Extract its exact population names, measures, intervention labels, methods, authors, registry IDs, or cited source that can resolve a named gap. Change one search dimension at a time and record a concise, observable decision note: name the unresolved gap, what the prior results did or did not yield, and why one changed dimension (for example, a synonym, design, entity, language/source ecosystem, or reference route) should help. This is an action rationale, not a request for hidden chain-of-thought. If a known pivotal source is not found, search its exact title/author or identifier, then adjust the term or filter responsible; do not interpret a failed query as evidence the source does not exist.


Adapt to the yield rather than rewriting for its own sake: if results are too broad, add one discriminating population, date, jurisdiction, design, measure, or known source-family constraint; if too few appear, remove the most restrictive conjunct, expand aliases or adjacent terminology, try another language/source family, or verify the operator. If results keep returning the same source family, change the evidence route or query role instead of stacking filters. Record the same short decision note for why the next query changed; an empty result set still does not prove absence.
5. **Read and classify evidence at the claim/link level.** Verify exact entity, version, population, design, comparator, outcome definition, dates, and scope in the underlying material. Mark what it informs: descriptive pattern, proposed mechanism, causal effect, boundary, counterexample, or unresolved. A plausible mechanism or an association does not by itself establish that the whole chain is causal. For observational causal claims, inspect the design and assumptions; triangulate only genuinely different data/design routes, and look for available negative controls, falsification checks, or sensitivity analyses. When an answer depends on mediation (`X → M → Y`), check whether the evidence establishes temporal order (exposure before mediator before outcome) and inspect the design and assumptions needed to identify the mediator–outcome link, including relevant confounding. Pairwise associations alone do not establish mediation; without adequate support, call the mechanism plausible or unverified. A citation trail is a useful adjunct for undiscovered terminology and later critiques, not an independent confirmation or a substitute for searching other routes.
6. **Keep a proportionate search trace.** For sustained or reproducibility-sensitive work, record the information gap, service/database and interface, date, exact queries and material filters, useful sources found, vocabulary/route learned, and the short observable reason for any material query change. Keep the trace compact for ordinary tasks; exhaustive reviews need a fuller, reproducible strategy. Search ranking and snippets are not a census of the evidence, and no-result pages do not establish that evidence is absent.
7. **Stop on evidence gain, not query count.** Stop when the answer-bearing links have been examined through suitable source types, material alternatives and boundaries are supported, contradicted, or explicitly unresolved, and another route is unlikely to change the conclusion. If several queries only return the same source family or add no new observation, redirect to the missing evidence surface or state the access/coverage limit. Do not claim a comprehensive search unless the method and scope justify it.

### Example: search a proposed tutoring-to-outcome chain

Suppose the working hypothesis is `after-school tutoring → attendance/dose → targeted practice and feedback → mathematics achievement`. Prior achievement, family resources, motivation, and self-selection may also affect both participation and outcomes. Treat this as a provisional map, not a discovered fact. Rather than search only `does tutoring improve math?`, make targeted retrieval moves such as:

| Search role | Illustrative query | What it can help locate |
| --- | --- | --- |
| Effect/comparison | `after-school tutoring mathematics randomized evaluation achievement` | Comparative estimates and study designs; check the actual programme, population, comparator, and follow-up. |
| Mechanism/link | `tutoring attendance dosage targeted feedback mathematics outcomes` | Measures or observations of the proposed intermediate process and its timing. |
| Rival explanation | `tutoring mathematics selection bias prior achievement family resources` | Evidence about enrollment selection or competing causes of participation and outcomes. |
| Boundary/adverse evidence | `tutoring mathematics null effects implementation fidelity attrition` | Non-effects, implementation variation, dropout, or subgroup limits. |

These phrases are starting points; adapt them to the search engine/database and terminology found in relevant sources. Do not infer that the mediator caused the outcome merely because it correlates with both, or that a study supports the whole chain because its conclusion uses causal language.

### Search-method references

- Bates MJ. “The Design of Browsing and Berrypicking Techniques for the Online Search Interface.” *Online Review* (1989), 13(5):407–424. The berrypicking model treats search needs and queries as evolving as useful sources reveal new terms and routes: https://pages.gseis.ucla.edu/faculty/bates/articles/berrypicking.pdf
- Google Search Help, [Refine Google searches](https://support.google.com/websearch/answer/2466433?hl=en), documents Google-specific phrase, `site:`, date and file-type operators; these should not be assumed to work identically in other search tools. Google Scholar, [Search Help](https://scholar.google.com/intl/en/scholar/help.html?hl=en), describes title/author, “Cited by” and “Related articles” routes as discovery aids, not independent confirmation.
- Cochrane Handbook, Chapter 4, *Searching for and selecting studies*: iterative strategies, concept/synonym structure, free text and controlled vocabulary, and complementary citation searching. Its review-search recommendations are not a mandatory quota for every web lookup: https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04
- Bramer WM, de Jonge GB, Rethlefsen ML, Mast F, Kleijnen J. “A systematic approach to searching: an efficient and complete method to develop literature searches.” *Journal of the Medical Library Association* (2018), 106(4):531–541. DOI: https://doi.org/10.5195/jmla.2018.283
- Rethlefsen ML et al. “PRISMA-S: an extension to the PRISMA Statement for Reporting Literature Searches in Systematic Reviews.” *Systematic Reviews* (2021), 10:39. DOI: https://doi.org/10.1186/s13643-020-01542-z
- Hernán MA et al. “Causal Inference About the Effects of Interventions From Observational Studies in Medical Journals.” *JAMA* (2024). https://jamanetwork.com/journals/jama/fullarticle/2818746
- Cashin AG, McAuley JH, VanderWeele TJ, Lee H. “Understanding how health interventions or exposures produce their effects using mediation analysis.” *BMJ* (2023), 382:e071757. https://doi.org/10.1136/bmj-2022-071757. This is a health-research guide; apply its temporal-order and confounding cautions when a causal conclusion depends on mediation.

These sources support search-design and causal-appraisal practices within their stated scopes; they do not demonstrate that adding this guidance improves a language model's research performance.

## Inspect underlying material

Search snippets, generated summaries, abstracts, and reposts are routing aids. Read the underlying source and the context required for the inference. Inspect methods, footnotes, tables, figures, code, or version history when the claim depends on them.

For code, distinguish documentation claims, inspected implementation, and observed execution. Reading code is not running it. For human statements, distinguish original recording/text from transcript, paraphrase, or secondary report.

## When a route fails

Repeated results may reflect vocabulary mismatch, indexing limits, syndication, a faulty premise, inaccessible primary material, or the wrong evidence surface. Change the relevant dimension rather than issuing cosmetic query rewrites.

A failed URL is not evidence that a publication or feature does not exist. Seek authorized mirrors, repositories, archives, primary substitutes, or local copies where appropriate.

## Independent trajectories versus gap decomposition

For a complex multi-claim task, decompose by missing evidence and let the root synthesis maintain shared state.

For a high-value needle-in-a-haystack fact where search path dependence is the main failure mode, try a small number of genuinely independent discovery trajectories: different starting clues, source ecosystems, languages, entities, or historical directions. Compare the evidence found; model agreement is not empirical corroboration.

## Gap-driven citation tracing

When a pivotal claim remains unresolved and the underlying literature is accessible, use citation links to pursue a named gap: trace backward to the method or original result, then forward to independent replications, critiques, corrections, retractions, or later evidence. Inspect whether the citing work adds evidence or merely repeats a claim. Group papers and reports that share data, authorship, origin, or evaluation pipelines into provenance families.

Citation chaining is a targeted route, not a source quota or completeness guarantee. Stop when the next link is unlikely to change the answer, when repeated links return to the same source family, or when access limits leave the gap bounded.

## Stop repetition

Track enough search history to recognize route duplication. Stop unchanged retries with no concrete prospect of new evidence. A search round is valuable only if it changes the working model, closes a material gap, reveals a new route, or strengthens verification.

[← Return to root workflow](../SKILL.md)
