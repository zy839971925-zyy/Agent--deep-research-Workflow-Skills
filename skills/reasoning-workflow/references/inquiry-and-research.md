# Inquiry and research

**Trigger:** Open-ended, unfamiliar, frame-uncertain, contested, multi-source, current, relationship-heavy, or explicitly Deep/Max/Ultra questions.

**Reads:** user objective, current working model, known/given information, pivotal uncertainties, available evidence surfaces.

**Updates:** problem frame, coverage map, questions, hypotheses, evidence gaps, provenance map, relationships, confidence, stopping state.

**May invalidate:** earlier framing, assumptions, hypotheses, inferences, decisions, recommendations.

**Exit:** the problem frame is adequate for the task; answer-bearing uncertainties are supported, contested, or bounded; another feasible route has low expected answer gain.

**Related:** [problem framing and effort](problem-framing-and-effort.md), [retrieval and observation](retrieval-and-observation.md), [evidence and provenance](evidence-and-provenance.md), [relationships and systems](relationships-and-systems.md), [hypotheses and bias control](hypotheses-and-bias-control.md).

**Return:** [root workflow](../SKILL.md) → Question / Reasoning Lane.

## Research is not synonymous with search

Research is the controlled reduction of uncertainty about the user's actual question. Search, source reading, experiments, files, code/runtime observations, calculations, interviews, archives, and direct reasoning are possible evidence operations; none is mandatory merely to display diligence.

Begin from the working model and ask what would actually change the answer.

## First distinguish frame uncertainty from answer uncertainty

### Answer uncertainty

The proposition is well specified but the answer is unknown. Example: whether a particular regulation is currently in force for a named jurisdiction and date.

Use focused identification, exact-source retrieval, version/date resolution, corroboration where warranted, and targeted verification.

### Frame uncertainty

The problem model itself may omit an important definition, entity, mechanism, stakeholder, adjacent field, comparison class, time boundary, or source ecosystem. Example: whether an emerging business model is viable when even the relevant substitutes, value chain, and revenue bottleneck are not yet clear.

Do not immediately optimize retrieval around the user's nouns. Orient before narrowing.

## Orientation before commitment

When frame uncertainty is material, explore enough of the terrain to learn:

- canonical terminology, aliases, translations, and contested definitions;
- entity/identity/version distinctions;
- relevant chronology and governing time boundaries;
- major schools of explanation or stakeholder perspectives;
- likely primary records, datasets, communities, repositories, institutions, or archives;
- adjacent domains that may contain a mechanism or useful analogy;
- obvious disagreements and unexplained anomalies;
- upstream/downstream relationships that might change the problem frame.

Orientation is not a generic “search every category” checklist. Each route must have a reason: discovering vocabulary, revealing a hidden variable, locating a source ecosystem, or testing whether the initial frame is incomplete.

After orientation, compress the problem into a few **answer-bearing questions** rather than a topic inventory.

## Build a coverage model, not a source quota

For complex work, maintain a small coverage model such as:

`question | why it matters | current answer | uncertainty source | evidence needed | route/status`

Coverage is about the propositions needed to answer the task, not how many websites were visited. Add a branch when it can change the answer. Remove or pause branches that are merely interesting.

## Research questions come from the model

Do not translate the user prompt directly into search keywords. Derive research questions from the working model, premises, competing hypotheses, relationships, and uncertainty. Each meaningful retrieval should have an intended epistemic job: discover the frame, establish a premise, distinguish alternatives, test a mechanism, resolve a version/entity, estimate magnitude, or falsify a conclusion.

Before a retrieval, be able to answer internally: `what is missing? why does it matter? what result would change the model?`

## Answer gain before source count

Prefer the next route that can change the answer, boundary, confidence, decision, or pivotal uncertainty. Do not chase the largest unknown if different answers would not affect the user's outcome. Treat information gain as useful only when it produces answer gain.

Do not assign fake numerical scores. A qualitative priority is enough: pivotal / useful / bounded / low-value.

## Research from discriminating questions

For a material uncertainty:

1. state the competing plausible answers or the relevant range of possibilities;
2. ask what observation would differ between them;
3. choose the evidence surface most able to observe that difference;
4. retrieve/observe the underlying material;
5. update the claim, hypothesis, relationship, and provenance state;
6. identify what is now the highest-value unresolved gap.

Evidence that merely repeats what every hypothesis predicts has low information value even if it comes from prestigious sources.

## Reasoning-aware retrieval intent

For important retrieval, keep the evidence need beside the query: global question, pivotal claim or gap, current state, live alternatives, desired observation, and the discriminating role. The search string is a lossy projection of this intent. If the interface accepts only keywords, still preserve the intent in the working model.

## Discover beyond literal keywords

Do not rely on prompt-keyword matching. Change the research route when useful through:

- synonyms, historical names, local-language terms, model/version names;
- causes, symptoms, effects, mechanisms, components, substitutes, complements;
- authors, organizations, datasets, citations, bibliographies, issue trackers, filings, archives;
- adjacent professions or disciplines that observe the same mechanism under another label;
- counterparties, affected users, competitors, regulators, suppliers, implementers, critics;
- exact phrases, identifiers, dates, errors, code symbols, product numbers, legal citations.

A new route should target a different information need or failure mode, not merely paraphrase the previous query.

## Unknown-unknown probe

Before strong closure on a frame-uncertain task, ask once:

> What important category of cause, evidence, stakeholder, time period, adjacent system, or terminology could be absent from the current model and still change the conclusion?

If a plausible candidate exists, sample it. Do not expand indefinitely: the branch must have a credible path to changing the answer.

## Hypothesis competition and abductive reasoning

When several causes can produce the same observation, do not ask only “why did this happen?” Ask:

- what else could produce it;
- what each explanation uniquely or disproportionately predicts;
- which existing observation is inconsistent with each explanation;
- what feasible next observation would best discriminate them.

Keep unresolved alternatives alive when the evidence does not distinguish them. Do not convert ambiguity into a blended narrative.

## Research state for long investigations

For long or delegated work, retain a compact state:

`objective | scope | answer-bearing questions | current best answer | decisive evidence | counterevidence | provenance clusters | assumptions | frame gaps | answer gaps | failed routes | new leads | next best action`

Materialize it into durable state only when the runtime/task justifies persistence. For state semantics, use [state model and invariants](state-model-and-invariants.md).

## Multi-agent strategy

When subagents exist, use them to expand genuine search-path diversity or fill separable evidence gaps. Two useful patterns differ:

- **Needle discovery:** a small number of genuinely independent search trajectories when the main failure mode is path dependence.
- **Complex multi-claim research:** decompose by evidence gap, source ecosystem, jurisdiction/language, adversarial route, or reproduction task.

A branch should return evidence and uncertainty, not a polished mini-report. Model agreement is not independent empirical corroboration.

## Marginal information gain and stopping

Do not use search count, source count, elapsed time, or report length as a proxy for completeness. Continue while a feasible next observation has meaningful expected answer gain.

Stop a branch when:

- it cannot materially change the answer;
- its evidence is inapplicable to the entity/version/time/population;
- it only repeats the same provenance or vocabulary;
- no feasible observation can discriminate the alternatives;
- the expected answer gain is low relative to the cost.

For important unresolved claims, try a genuinely different route before declaring convergence when one is available.

[← Return to root workflow](../SKILL.md)
