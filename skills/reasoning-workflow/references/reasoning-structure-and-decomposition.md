# Reasoning structure and decomposition

**Trigger:** Multi-part, ambiguous, logically dense, explanatory, diagnostic, comparative, or planning questions where structure materially affects answer quality.

**Reads:** original user question, epistemic task, working model, constraints, current premises, open uncertainty.

**Updates:** parent question, subquestions, dependency structure, premise map, reasoning operators, recomposition state, question-drift check.

**May invalidate:** earlier decomposition, inferred scope, duplicate branches, conclusions that rely on a missing or changed premise.

**Must verify:** subquestions are at compatible levels where intended; material dependencies are covered; recomposition can answer the parent problem.

**Exit:** the structure is sufficient to reason/act without unnecessary overlap or missing answer-bearing dependencies.

**Related:** [problem framing and effort](problem-framing-and-effort.md), [inquiry and research](inquiry-and-research.md), [hypotheses and bias control](hypotheses-and-bias-control.md), [relationships and systems](relationships-and-systems.md).

**Return:** [root workflow](../SKILL.md) → Decompose / recompose.

## Start from the epistemic task

Before decomposing, state what kind of answer would resolve the parent question: fact, explanation, diagnosis, verification, comparison, forecast, judgment, decision, or recommendation. Decomposition should serve that answer type rather than create a generic topic outline.

## Decomposition quality

Use decomposition to expose answer-bearing uncertainty, dependencies, mechanisms, or separable work. Avoid decomposing merely because a framework is familiar.

Check:

- **low overlap:** subquestions should not repeatedly require the same reasoning without a deliberate shared dependency;
- **coverage:** include dependencies that can change the parent answer, not every interesting adjacent topic;
- **level stability:** avoid mixing causes, symptoms, stakeholders, outcomes, evidence sources, and execution steps as peer categories unless that is the intended analytic dimension;
- **dependency visibility:** when one branch requires another, record that dependency rather than treating them as independent;
- **recomposition:** if every subquestion were answered perfectly, would those answers be sufficient to answer the parent question?

If recomposition fails, add the missing bridge or revise the decomposition.

## Do not let taxonomy replace understanding

When the problem is not already well-structured, prefer:

`concrete observations → recurring pattern → consequential relationship → mechanism/essence → abstraction/taxonomy`

A category system is useful when it compresses a model that already explains the observations. It is harmful when it hides uncertainty behind labels.

## Premise-aware reasoning

A premise is any proposition on which a material inference depends, whether observed, retrieved, assumed, defined, or stipulated by the user. For important reasoning, preserve enough structure to answer:

`Which premises support this inference?`

If a premise changes or becomes stale, dependent inferences, judgments, recommendations, and artifacts must be reconsidered.

Do not confuse:

- a premise with a fact;
- an assumption with a verified observation;
- a hypothesis with a conclusion;
- a recommendation with an empirical proposition.

## Induction, abduction, deduction

Use the operators according to the task:

- **induction:** infer a tentative pattern or regularity from observations;
- **abduction:** propose plausible explanations for observations;
- **deduction:** derive implications that would follow if premises/hypotheses were true.

For diagnosis/explanation, a productive loop is:

`observation → abduction → competing hypotheses → deduction of discriminating predictions → evidence → induction/revision`

The operators may be implicit on simple tasks. Do not expose a ceremonial logic transcript.

## Recomposition before closure

After solving subquestions, reconstruct the parent answer explicitly enough to catch:

- missing bridges;
- inconsistent definitions;
- incompatible time horizons or populations;
- local branch answers that do not jointly imply the final conclusion;
- unresolved trade-offs hidden by decomposition;
- question drift from the original user request.

A well-answered collection of subquestions is not automatically a well-answered parent question.

## Adaptive granularity

Start with the coarsest structure that still exposes material dependencies. Refine only the branch whose internal uncertainty currently blocks the parent answer or action.

Use:

`coarse map → identify blocking branch → locally refine → reason / observe → recompose`

Do not create equal-depth trees for appearance. One branch may remain a single node while another needs several levels of mechanism, evidence, or execution detail.

## Reasoning stagnation

More reasoning is not useful when it keeps reproducing the same model. Treat a branch as stagnant when additional thought is not changing the problem representation, live hypotheses, pivotal uncertainty, material relationships, decision boundary, or next evidence need.

When stagnation is material, change the **operator**, not just the wording: reframe, reverse the causal direction, inspect a boundary case, derive a discriminating prediction, seek direct observation, use another specialist method, or retire the branch. Ultra may spend much more budget, but it should not spend that budget repeating an unchanged reasoning trajectory.

[← Return to root workflow](../SKILL.md)
