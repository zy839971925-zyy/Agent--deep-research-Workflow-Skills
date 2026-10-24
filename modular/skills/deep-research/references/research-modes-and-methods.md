# Research modes and methods

**Trigger:** A material investigation is about real-world conditions, a technical/architecture decision, or a problem that mixes both; especially before committing to a build.

**Reads:** the user’s outcome and decision, current repository/runtime when available, existing evidence, scope, constraints, stakeholder needs, and unresolved answer-bearing questions.

**Updates:** research lens, evidence strategy, decision scenarios, trade-offs, assumptions, and next discriminating observation.

**May invalidate:** the initial frame, source strategy, architecture preference, forecast, or build recommendation.

**Exit:** the question has a suitable evidence path; key trade-offs and limits are visible; remaining user-only unknowns pass the [clarification gate](../../reasoning-core/references/clarification-gate.md).

**Related:** [inquiry and research](inquiry-and-research.md), [information target navigation](information-target-navigation.md), [measurement and operationalization](../../decision-analysis/references/measurement-and-operationalization.md), [domain patterns](../../execution-control/references/domain-patterns.md), [decision and recommendation](../../decision-analysis/references/decision-and-recommendation.md).

**Return:** [Deep Research](../SKILL.md) → inquiry and answer.

## Verify the research surface before depending on it

A product feature is not a session capability. Before promising or designing around a host's Deep Research mode, search, connector, agent pool, file reader, or visual UI, inspect what this runtime actually exposes and what permissions apply. Classify it as `available here`, `unavailable here`, or `not verified`. If only a lighter feature is present, either use it as a clearly named fallback or state what remains unavailable; never claim the host's Deep Research mode, connector, subagents, or interactive UI ran unless the runtime confirms it. Official product documentation can establish advertised scope and limits, not this account's entitlement or this session's successful execution. A connected source or advertised connector is not evidence that this run read it: use the current run’s visible source/activity record; if that record is unavailable, report actual use as unverified.

## Choose a lens by the evidence problem

“Research” can mean investigating the world, deciding how to build a system, or both. Choose by what must be known—not by whether the prompt contains words like “market,” “AI,” or “architecture.” Use only the parts that can change the answer. A mixed question may need linked lenses; do not force it into one.

## Real-world and empirical questions

First classify the claim being investigated: descriptive (what/how much), causal (what changed what), mechanistic (how/why), predictive (what may happen), or normative/evaluative (what should count as good or acceptable). These are not interchangeable: a source that describes prevalence does not establish a cause, and a forecast does not settle a value judgment.

- Define the population/entity, place, period, comparison, and outcome that the answer refers to. Keep denominator, selection, missingness, and measurement visible where they could change the conclusion.
- Match evidence to the proposition. Prefer records that could directly observe the claimed result or mechanism. For causal claims, inspect identification/design and plausible confounding; for prevalence, examine coverage and denominator; for forecasts, look for a relevant reference class and update conditions; for values, attribute objectives to the people or institutions that hold them rather than deriving them from descriptive evidence.
- Separate discovery from confirmation when the evidence permits it. Exploratory reading or analysis may reveal a neglected category or generate a hypothesis; do not treat the same exploratory pattern as independent confirmation. Seek a different source route, pre-specified comparison, held-out material, or direct check for the decisive claim. If that is unavailable, say so rather than implying replication.
- Use a brief premortem only for a consequential plan or forecast: imagine a plausible failure and generate candidate mechanisms/signposts, then test them against evidence. Vividness is not probability, and a premortem is not proof that all risks were found.

For data-heavy empirical work, describe before explaining: inspect definitions, distributions, denominators, outliers, subgroup variation, and missingness before proposing a mechanism. Treat patterns surfaced through flexible exploration as leads; seek a separate confirmatory check when the conclusion depends on them. Undisclosed analytic flexibility can inflate false-positive risk under studied conditions, but this does not make exploratory work invalid or require preregistration for every task.

When the real-world evidence depends on interviews or surveys, check who was sampled and who did not respond, the exact question wording and context, and plausible recall or social-desirability effects. Use contrasting or negative cases to challenge an emerging explanation. Qualitative interviews can reveal mechanisms and categories, but do not treat them as population prevalence estimates unless the sampling and measurement design supports that inference. In product-need research, keep stated preferences, observed behavior, and estimated population prevalence distinct; a small set of interviews can generate hypotheses, not market-share estimates.

When drawing on a named expert or practitioner, use the method as a candidate lens, not as evidence by reputation. Check whether the domain has stable learnable regularities and the practitioner received timely, informative feedback; if those conditions are unknown, do not assume their intuition transfers. When the heuristic matters to the conclusion, make it testable: identify the cue, expected signal, and action it suggests, then check that prediction against relevant records or outcomes rather than adopting the heuristic as proof.

For domain-specific evidence, use [domain patterns](../../execution-control/references/domain-patterns.md); when metrics or proxies carry the claim, use [measurement and operationalization](../../decision-analysis/references/measurement-and-operationalization.md). Do not repeat their checklists here.

## Technical and architecture research before a build

Use this path when the answer could change what should be built, how components should fit, or which design risk to retire first. Research informs a decision; it does not itself authorize implementation.

1. **Inspect the actual starting point.** Read the relevant repository, version, existing interfaces, tests, dependencies, deployment constraints, and user-provided requirements before recommending a generic architecture. State what was inaccessible; do not infer that an uninspected file or service is absent.
2. **Start from outcomes and architecture drivers.** Translate user or business goals into a small set of concrete quality-attribute scenarios. A scenario should say who or what produces a stimulus, under what operating conditions, what system response is expected, and how that response would be judged. Use measurable thresholds only when supported or elicited; otherwise preserve the missing threshold as an uncertainty.
3. **Compare materially different approaches.** For each live alternative, show which scenarios it supports, where it fails, and the important interaction between attributes such as latency, availability, security, privacy, changeability, cost, and operability. Do not add every quality attribute by rote. Identify risks, sensitivity points, and trade-off points; say which assumption or future observation would reverse the preference.
4. **Choose evidence that can discriminate.** Inspect authoritative platform/API documentation for external constraints; use repository and runtime evidence for local behavior; calculate comparable costs; and run a small reversible prototype, benchmark, or test when it can resolve a pivotal technical uncertainty more directly than more prose or web search. Keep results tied to exact versions and conditions.
5. **Recommend a build sequence, not just a diagram.** Separate established constraints from assumptions, identify the lowest-cost informative probe or reversible first slice, state dependencies and failure/rollback considerations, and keep the recommendation conditional where user priorities remain unresolved. For a durable or costly-to-reverse architecture choice, provide a compact decision record: problem/drivers, options considered, chosen direction and rationale, decisive evidence, assumptions/open risks, consequences, and a trigger for reopening the choice. This is report content, not permission to edit the repository or implement the design. Skip formal decision records for routine, reversible choices.

This is a lightweight, scenario-driven use of architecture evaluation—not a demand to conduct a full formal ATAM workshop for every software question. The SEI’s ATAM work is useful because it starts from business drivers, analyzes candidate architecture against quality-attribute scenarios, and exposes risks and sensitivity/trade-off points. Tailor the analysis to the actual project and stakeholder evidence.

## Hybrid research

When a question combines a real-world outcome with a proposed system—such as whether a feature is useful and how to implement it—link two chains rather than collapsing them:

`real-world need / affected population / evidence of value → required system behavior / quality scenarios → candidate design / local feasibility → testable next step`

Evidence that users want an outcome does not establish that a proposed architecture can deliver it; technical feasibility does not establish that the outcome matters. Keep the dependency between those claims explicit.

## Human methods are tools, not authority

Use documented methods because they change an evidence action, not because a famous person used them. The outside view/reference-class method is relevant to project durations, costs, and success rates that are vulnerable to inside-view planning; it requires a genuinely comparable reference class and is not a substitute for project-specific constraints. A premortem is a way to surface failure hypotheses, not a calibrated risk estimate. Exploratory/confirmatory separation helps prevent a discovered pattern from being mistaken for independent support; it does not make a second source independent when both inherit the same data.

Do not assume that a ritual “consider the opposite” prompt or a bias lecture reliably removes confirmation bias: a registered report found little evidence for those interventions on its tested outcomes, and effects should not be generalized beyond that study. Use the prompt only to generate a specific competing explanation and a discriminating check; assess the evidence, not the performance of a debiasing ritual. Likewise, uncertainty routing research motivates separating user-intent ambiguity from world-side evidence gaps, but benchmark results on simulated or constrained tasks do not establish universal thresholds or production gains.

Do not imitate a thinker’s persona, treat heuristics as universal laws, or inflate domain-specific findings into guarantees about AI performance. Feynman’s “cargo cult science” lecture gives a practical integrity test for consequential claims: surface the relevant facts, possible alternative causes, and details that could weaken the interpretation—not just the observations that inspired or support it. Apply this selectively to evidence that could change the answer; it is not a mandate to dump every irrelevant caveat.

## Method sources and scope

- Kazman, Klein, Barbacci, Longstaff, Lipson & Carriere (1998), [The Architecture Tradeoff Analysis Method](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/), CMU/SEI-98-TR-008: software architecture evaluation against competing quality attributes and their trade-offs.
- Kahneman & Lovallo (1993), [Timid Choices and Bold Forecasts](https://doi.org/10.1287/mnsc.39.1.17), *Management Science* 39(1): 17–31: an outside-view argument about planning and risk forecasts, not a universal predictive formula.
- Klein (2007), [Performing a Project Premortem](https://hbr.org/2007/09/performing-a-project-premortem), *Harvard Business Review*: practical technique for surfacing reservations and plausible failure causes in project planning.
- Mitchell, Russo & Pennington (1989), [Back to the Future: Temporal Perspective in the Explanation of Events](https://doi.org/10.1002/bdm.3960020103), *Journal of Behavioral Decision Making* 2(1):25–38: experiments on temporal perspective and explanations; its results do not by themselves establish that premortems improve project outcomes.
- Hoaglin (2003), [John W. Tukey and Data Analysis](https://doi.org/10.1214/ss/1076102418), *Statistical Science* 18(3):311–318: reviews Tukey’s exploratory/confirmatory distinction; useful as a methodological separation, not evidence that any particular AI research workflow improves.
- Kahneman & Klein (2009), [Conditions for intuitive expertise](https://pubmed.ncbi.nlm.nih.gov/19739881/), *American Psychologist* 64(6):515–526: reliable intuition depends on learnable regularities and adequate feedback; the review does not validate every expert heuristic or transfer it to unrelated domains.
- Simmons, Nelson & Simonsohn (2011), [False-Positive Psychology](https://doi.org/10.1177/0956797611417632), *Psychological Science* 22(11):1359–1366: demonstrates false-positive risks from undisclosed analytic flexibility under the paper’s studied setups; it is a caution for confirmation, not a prohibition on exploration.
- American Association for Public Opinion Research, [Standard Definitions](https://aapor.org/standards-and-ethics/standard-definitions/) and [Best Practices for Survey Research](https://aapor.org/standards-and-ethics/best-practices/): distinguish coverage, measurement and nonresponse error; recommend transparent reporting of sample, population, question wording, and survey methods. Response rate alone does not establish the magnitude of nonresponse bias.
- Feynman (1974), [Cargo Cult Science](https://calteches.library.caltech.edu/51/2/CargoCult.htm): argues for reporting relevant alternative causes, contrary facts, and details that may invalidate an interpretation; use as an integrity principle, not as a claim that the speech validates any particular workflow.
- Su & Cardie (2026), [Knowing but Not Showing: LLMs Recognize Ambiguity but Rarely Ask Clarifying Questions](https://arxiv.org/html/2605.25284): on AmbigQA-derived question-answering settings, retrieved context improved answerability but often further reduced clarification; this motivates explicit observable clarify/no-clarify tests, not a universal claim about every task or model.
- Li et al. (2026), [Clarify the User or Verify the World?](https://arxiv.org/pdf/2609.32255): proposes ACT/CLARIFY/VERIFY routing and reports results on τ-bench; it motivates source-aware uncertainty routing, not production thresholds or general performance guarantees.
- Ge et al. (2026), [Ask Before You Optimize](https://arxiv.org/abs/2609.05258): OR-Clarify/InterOPT studies formulation-critical gaps in simulated optimization tasks, measuring slot recovery and interaction cost. Its findings do not imply that every underspecified request should trigger an interview.
- Whitt et al. (2023), [Weakening the ideological immune system](https://doi.org/10.1080/23743603.2023.2196755): a registered report comparing debiasing interventions found little evidence for “consider the opposite” on its studied outcomes; use alternatives to design tests, not as a guaranteed debiasing protocol.
- NASA, [Stakeholder Expectations Definition](https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/): distinguishes needs, goals, measurable results-oriented objectives, and requirements; useful for eliciting outcomes before designing a system, not a demand to formalize every small project.
- Google Cloud, [Architecture Decision Records](https://docs.cloud.google.com/architecture/architecture-decision-records): describes ADRs as a lightweight way to retain decision drivers, options and rationale for significant choices; use selectively where future maintainers need the reasoning.

[← Return to root workflow](../SKILL.md)
