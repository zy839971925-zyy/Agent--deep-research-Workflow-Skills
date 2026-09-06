# Problem framing and effort

**Trigger:** Ambiguous, multi-objective, consequential, or poorly scoped tasks; any task where the wrong question would produce a misleading answer or action.

**Reads:** user request, supplied context, constraints, intended use, known success conditions.

**Updates:** epistemic task, objective, scope, answer conditions, pivotal questions, effort vector, lane selection.

**May invalidate:** premature research plans, proxy questions, over/under-scoped execution.

**Exit:** the actual question/outcome and proportionate effort are clear enough to proceed.

**Related:** [reasoning structure and decomposition](reasoning-structure-and-decomposition.md), [inquiry and research](inquiry-and-research.md), [human context and interpretation](human-context-and-interpretation.md), [state model and invariants](state-model-and-invariants.md).

**Return:** [root workflow](../SKILL.md) → Identify task / Calibrate effort.

Use this to decide what problem is actually being solved and how much cognitive machinery it deserves. Return the framing to the main workflow; do not turn this into visible ceremony unless it helps the user.

## Start from the epistemic task or outcome

“Answering a question” is a complete task, not a degraded form of project execution. First identify what kind of knowing or judgment the user is asking for: fact, explanation, causal mechanism, verification, comparison, diagnosis, forecast, interpretation, evaluation, recommendation, or direct reasoning. Only then decide whether creation/action is also part of the objective.

A prompt's nouns are not automatically the research structure. Identify the intended use: understand, interpret, persuade, create, choose, diagnose, forecast, verify, implement, or audit. Ask which unanswered questions can actually change that outcome.

For complex work, prefer a few **answer-bearing questions** over a generic topic checklist. Useful examples are questions whose different answers would reverse a recommendation, invalidate a design, change an explanation, or alter the evidence required.

A compact internal contract may include:

`objective | output/success | scope/time | constraints/authorization | pivotal questions | exclusions`

Infer routine missing detail. Ask only when a materially different answer, action, or safety boundary depends on information that cannot reasonably be inferred.


## Find the essence before forcing a category

When a task is unfamiliar or poorly framed, do not begin by assigning it to the nearest familiar taxonomy. Start from concrete observations/constraints, identify recurring patterns and consequential relationships, then infer the mechanism or essence that best explains why the problem behaves as it does. Use categories only when they improve compression, comparison, or routing after that understanding exists.

A useful check is: `If I removed the category labels, would I still understand what variables and mechanisms make this problem work?`

## Cognitive operators

Tasks can combine operators; do not force one label.

- **Interpret:** infer meaning from language, behavior, context, symbols, or artifacts.
- **Explain:** build a mechanism or coherent account of why/how.
- **Retrieve:** locate a fact, record, file, source, or observation.
- **Verify:** test whether a specific claim is supported and current.
- **Diagnose:** locate a fault or cause using discriminating observations.
- **Compare:** align alternatives on dimensions that matter to the user.
- **Decide:** recommend under goals, trade-offs, uncertainty, and reversibility.
- **Forecast:** reason from current state to conditional future states.
- **Create:** produce writing, code, design, media, plans, or artifacts.
- **Execute:** carry out an authorized action rather than merely describe it.
- **Audit:** attack an existing conclusion, artifact, methodology, or evidence chain.
- **Research/inquire:** discover the problem space, identify evidence needs, test alternatives, and reduce answer- or frame-uncertainty.

Operators compose. For example, “write an article” can be `create + explain + research` if factual dependencies matter, while “what did this sentence imply?” may be `interpret + compare explanations` with no external retrieval.

## Calibrate five kinds of effort

Treat effort as a vector rather than one scalar. A task can need deep reasoning but almost no change governance, or simple reasoning with strict governance because the action is high consequence.

### Reasoning breadth

Increase when multiple interpretations, stakeholders, mechanisms, jurisdictions, boundary conditions, or indirect effects can change the outcome.

### Evidence depth

Increase when facts are current, disputed, private, dispersed, difficult to observe, quantitative, or consequential. Reduce when the user's supplied material already determines the answer.

### Challenge depth

Increase for causal claims, accusations, personality/motive inference, forecasts, high-stakes choices, conflicting sources, and conclusions resting on a few assumptions.

### Verification depth

Increase when mistakes are costly or hard to reverse, when exact numbers/dates/versions matter, or when an artifact must actually work rather than merely look plausible.

### Governance depth

Increase when work changes persistent state, affects other people or systems, is difficult to reverse, crosses interfaces, requires authorization, or needs later monitoring. Governance depth controls traceability, change records, review independence, approval/readiness gates, rollout/rollback discipline, and effectiveness checks. Pure analysis or ephemeral drafts usually need little or none.

User-specified depth controls all relevant dimensions. “Maximum” means expand the useful epistemic frontier, not repeat searches or expose private reasoning.

## Escalation and de-escalation

Escalate when new evidence reveals hidden complexity, a pivotal contradiction, entity/version ambiguity, a strong causal leap, weak-signal/high-impact information, repeated search failure, or a consequential second-order relationship.

De-escalate when direct evidence settles the pivotal issue, remaining uncertainty cannot change the user's outcome, another route would only duplicate the same provenance, or execution now creates more value than additional analysis.

Do not equate long output with deep work. A deeply investigated task can still have a concise answer.

[← Return to root workflow](../SKILL.md)
