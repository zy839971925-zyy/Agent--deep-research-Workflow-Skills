# Ultra research overlay

**Trigger:** Explicit Ultra research requests, or a Max research task that remains unable to converge because of material frame instability, retrieval-path stagnation, unresolved evidence ecology gaps, severe source conflict, or pivotal claim undercoverage.

**Reads:** root question, current Task Profile, current problem model, pivotal claims, live hypotheses, evidence gaps, provenance clusters, failed routes, known limits of available tools and context.

**Updates:** expanded problem-space map, fresh frame comparison, orthogonal research routes, evidence-ecology map, missingness and boundary notes, pivotal-claim support state, convergence state.

**May invalidate:** initial framing, decompositions, hypotheses, evidence priorities, overconfident synthesis, verification scope, and recommendations derived from a narrower research path.

**Must verify:** Ultra does not mean unlimited search, fixed agent count, fixed source quota, or full-report forensic citation checking. It must preserve answer relevance, proportionate closure, source provenance, and calibrated uncertainty.

**Exit:** the research space has been broadened enough to expose material alternative framings and evidence ecosystems; remaining uncertainty is bounded or unlikely to change the answer; pivotal claims are supported, contested, or explicitly left unresolved; the final answer is calibrated to the weakest material dependency.

**Related:** [inquiry and research](inquiry-and-research.md), [evidence and provenance](evidence-and-provenance.md), hypotheses and bias control (route to the relevant sibling Skill if needed), relationships and systems (route to the relevant sibling Skill if needed), synthesis and verification (route to the relevant sibling Skill if needed), model adaptation (route to the relevant sibling Skill if needed).

**Return:** [root workflow](../SKILL.md) → Deep Research / Audit-Verification.

## What Ultra means

Ultra is not Max with more rigid process. Max asks whether the current research trajectory has been pursued to the maximum useful depth. Ultra asks whether the trajectory itself may be too narrow, path-dependent, or blind to a different framing.

Ultra allows substantially more reasoning and research budget. The marginal budget should usually go first to useful breadth and explanatory depth: reframe the problem, discover hidden relationships, inspect adjacent systems, generate alternative mechanisms, cross domains, widen evidence ecosystems, and test whether the original research path was too narrow. Verification still matters, but concentrate it on pivotal claims, fragile dependencies, contradictions, and high-consequence conclusions instead of turning Ultra into a verification-heavy mode.

Budget is permission, not a quota. Do not burn tokens on duplicate searches, repeated summaries, or checking claims that cannot change the answer.

## Strategy library, not checklist

Use this overlay as a strategy library. Select, combine, reorder, repeat, or skip strategies according to the current problem state. Preserve these invariants:

- search follows an evidence need, not prompt keywords;
- conclusions stay connected to pivotal premises and evidence;
- alternatives stay live when evidence does not distinguish them;
- new evidence may invalidate upstream framing and downstream synthesis;
- source count does not equal source independence;
- unresolved material uncertainty remains visible;
- final synthesis must answer the original question, not the easiest nearby question.

## Budget allocation

Ultra raises the total budget ceiling; it does not create a quota that must be consumed. Spend additional tokens and tool calls where they can reveal new answer-bearing structure. A useful default bias is:

`reframe / expand → connect / hypothesize → investigate → prune → challenge → selectively verify → synthesize`

This is a strategic bias, not a fixed sequence. If the frame is already stable, spend less on reframe. If a pivotal claim is fragile, spend more on verification. If search paths are homogeneous, spend more on orthogonal discovery. Repeated confirmation with no change in the problem model has low marginal value.

## Ultra research pattern

A useful pattern is:

```text
initial Max research
→ provisional answer
→ pivotal claim map
→ fresh frame reconstruction
→ orthogonal discovery routes
→ evidence ecology and missingness audit
→ boundary / heterogeneity exploration
→ strongest live alternative when evidence-supported
→ targeted final research
→ epistemic synthesis
→ narrative synthesis
→ pivotal-claim verification
→ calibrated answer
```

This is not mandatory order. New discoveries can send the task back to framing, decomposition, evidence selection, or hypothesis generation.

## Fresh frame reconstruction

Run a fresh frame pass when early research may have anchored the model. Rebuild the problem from the original user objective with reduced dependence on the current leading answer. Compare the fresh model with the primary model.

Look for missing actors, definitions, incentives, mechanisms, confounders, adjacent fields, jurisdictions, languages, source ecosystems, time regimes, populations, thresholds, feedback loops, and second-order effects. Add only candidates that could materially change the answer.

A same-model fresh pass is useful for re-framing. It is not automatically independent verification.

## Reasoning-aware retrieval

A search query is a lossy projection of an evidence need. When the runtime permits, preserve the retrieval intent alongside the query:

```text
global question
current pivotal claim
current state
specific gap
live competing explanations
desired observation
discriminating role
query / route
```

The query should be the final projection, not the starting point. If the available interface accepts only keywords, generate keywords from the evidence need and keep the need in the internal working model.

## Divergence before convergence

Ultra should widen the problem space before narrowing it. Useful expansion routes include upstream causes, downstream effects, inside-out mechanisms, outside-in constraints, historical formation, temporal lag, scale effects, incentives, stakeholder perspectives, selection effects, measurement proxies, substitutes/complements, feedback, expectation effects, and cross-domain analogies.

Do not pursue every route. Prune by answer gain: keep branches that could alter the explanation, boundary, confidence, recommendation, or verification target.

## Evidence ecology

Map which evidence ecosystems the current answer relies on. Different URLs are not independent if they share an origin, method, incentive, or blind spot.

Prefer failure-mode diversity: if one class of evidence is wrong or incomplete, another route should be able to notice it through a different mechanism. Examples include official records, filings, independent tests, user/operator evidence, practitioner communities, issue trackers, datasets, archives, regulators, competitors, suppliers, and critics.

## Missingness audit

Near convergence, ask what evidence may be absent because it was never observed, recorded, published, indexed, retrieved, read correctly, or represented in synthesis. Missingness can come from unpublished failures, local-language material, paid databases, internal data, survivorship bias, small negative cases, or source ecosystems the agent cannot access.

Do not search indefinitely for invisible evidence. Use the audit to bound the conclusion and avoid treating absence of evidence as evidence of absence.

## Boundary and heterogeneity search

For broad claims, ask where the claim weakens, reverses, or stops applying: population, scale, time, region, version, institution, market regime, implementation context, incentive structure, or measurement method.

Prefer conclusions shaped like:

```text
A appears supported under conditions C1/C2;
evidence is mixed under C3;
A may weaken or reverse under C4;
remaining uncertainty is U.
```

Avoid flattening heterogeneous evidence into one overgeneralized answer.

## Strongest live alternative

Construct a strongest rival answer only when an evidence-supported alternative remains live and could materially change the conclusion. Do not manufacture false balance.

Compare the current answer and live rival by asking which evidence both explain, which evidence genuinely separates them, whether that discriminating evidence is reliable, and whether the winner depends on one fragile premise.

## Synthesis discipline

Separate epistemic synthesis from narrative synthesis. First determine what is known, inferred, judged, recommended, contested, or unknown. Then write the answer.

Before strengthening a conclusion, inspect the weakest material dependency. A conclusion cannot be stronger than the pivotal premise, measurement, causal edge, or evidence route it depends on.

Final verification should focus on pivotal claims, not every sentence. Check whether cited evidence entails, partially supports, contextualizes, or fails to support the claim; whether entity/version/time/population/definition match; and whether wording exceeds the evidence strength.

[← Return to root workflow](../SKILL.md)
