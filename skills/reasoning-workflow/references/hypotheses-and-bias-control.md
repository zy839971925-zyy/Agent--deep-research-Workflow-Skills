# Premises, hypotheses, uncertainty, and bias control

**Trigger:** Ambiguous causes/meaning, causal claims, diagnosis, forecasting, contested interpretation, adversarial settings, important judgments, or conclusions vulnerable to anchoring.

**Reads:** working model, observations, premises/assumptions, current leading explanation, pivotal uncertainty.

**Updates:** premise map, alternative hypotheses, uncertainty type, discriminating observations, reversal conditions, confidence/bounds.

**May invalidate:** inferences, causal explanations, forecasts, judgments, decisions, recommendations, dependent artifacts.

**Must verify:** material conclusions do not rely silently on stale/unsupported premises; plausible alternatives are tested proportionately.

**Exit:** consequential premises are supported/bounded, material alternatives are tested proportionately or preserved as unresolved, and reversal conditions are known where useful.

**Related:** [reasoning structure and decomposition](reasoning-structure-and-decomposition.md), [inquiry and research](inquiry-and-research.md), [relationships and systems](relationships-and-systems.md), [evidence and provenance](evidence-and-provenance.md).

**Return:** [root workflow](../SKILL.md) → Premises / challenge / uncertainty.

## Premises are dependencies, not decorations

A **premise** is a proposition a reasoning step materially depends on. It may be:

- observed/retrieved evidence;
- a definition or scope choice;
- a user-stipulated constraint;
- an assumption accepted provisionally;
- an earlier inference reused downstream.

For consequential reasoning, preserve enough dependency structure to know what would become stale if a premise changed.

A compact record can be:

`premise | kind | support | used_by | uncertainty | stale? | reversal consequence`

Do not label a premise “fact” merely because later reasoning needs it.

## Working hypotheses are navigation tools

A hypothesis is a candidate explanation/model used to organize inquiry. It is not a conclusion and should not determine what evidence is allowed to count.

Ask what must be true for the current answer, plan, forecast, or diagnosis to hold. Identify premises that are both consequential and weakly tested. Seek direct evidence, discriminating evidence, or construct an answer that remains useful under uncertainty.

## Competing explanations

When the same observation can arise from more than one mechanism, ask:

- what else could explain it;
- which observations each explanation predicts;
- where their predictions differ;
- which feasible observation has the highest discriminating value;
- what existing evidence is inconsistent with each explanation.

Evidence that fits every explanation is usually weak for choosing among them. If several survive, preserve the ambiguity instead of blending them into false certainty.

## Induction, abduction, and deduction

Use them as complementary processes:

- **induction:** observations → tentative pattern/generalization;
- **abduction:** observations → plausible explanation(s);
- **deduction:** premises/hypothesis → testable implications.

A useful cycle for explanation/diagnosis is:

`observation → abduction → hypotheses → deduction → discriminating predictions → evidence → induction/revision`

Do not confuse an abductive “best explanation so far” with deductive proof.

## Structure uncertainty by source

When uncertainty matters, identify where it comes from rather than hiding it behind generic hedging:

- **missing evidence** — relevant observations are unavailable or not yet sought;
- **source conflict** — evidence sources make materially incompatible claims;
- **measurement uncertainty** — observations contain noise, error, sampling, OCR, model, or instrument limits;
- **definition/scope mismatch** — sources or branches use different populations, metrics, entities, versions, jurisdictions, or meanings;
- **premise/model uncertainty** — reasoning depends on assumptions or a simplified model that may be wrong;
- **causal uncertainty** — association/sequence is known but mechanism or direction is unresolved;
- **future behavioral/external uncertainty** — later choices, adaptation, policy, shocks, or strategic responses are not yet observable.

Then ask whether reducing that uncertainty would materially change the answer. Some uncertainty should be preserved, not cosmetically eliminated.

## Reversal and failure conditions

For a material conclusion, know what could overturn it:

`conclusion | decisive premises | strongest counterevidence | reversal evidence | residual uncertainty`

Ask:

- What evidence would make me change my answer?
- Which premise, if false, collapses the conclusion?
- Is there a counterexample or contrary observation?
- What new fact would reopen this branch?

This is ordinary reasoning hygiene, not only a high-risk audit step.

## Bias controls

Watch for:

- anchoring on the first narrative, category, or search result;
- confirmation search and motivated source selection;
- premature taxonomy before mechanism understanding;
- availability bias from vivid recent examples;
- attribution errors when situational explanations exist;
- hindsight contamination in historical analysis;
- confusing correlation, sequence, or plausibility with causation;
- base-rate neglect when a striking anecdote dominates broader evidence;
- false precision from numerical-looking heuristics;
- model consensus mistaken for independent evidence.

Do not respond by generating endless alternatives. The remedy is better premises, discriminating evidence, and explicit uncertainty.

[← Return to root workflow](../SKILL.md)
