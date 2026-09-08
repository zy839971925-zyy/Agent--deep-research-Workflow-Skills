# Decision and recommendation quality

**Trigger:** The user asks what to choose, whether to act, which option is preferable, what risk to accept, or what recommendation follows from uncertain evidence.

**Reads:** user objectives/values, constraints, alternatives, consequence estimates, uncertainties, measurements, judgments, reversibility/opportunity costs.

**Updates:** objective/constraint/alternative/consequence records, decision model, sensitivity/robustness notes, recommendation, value-of-information judgment.

**May invalidate:** recommendation, decision, action plan, project scope, research priorities.

**Must verify:** user-stated versus inferred objectives, feasible option set, consequence assumptions, sensitivity to uncertain premises, and whether more information could change the decision.

**Exit:** the recommendation follows transparently from objectives, alternatives, consequences and uncertainty; unknown value weights are not silently invented.

**Related:** [measurement and operationalization](measurement-and-operationalization.md), [hypotheses and bias control](hypotheses-and-bias-control.md), [time, scenarios and forecasting](time-scenarios-and-forecasting.md).

**Return:** [root workflow](../SKILL.md) → Judgment / recommendation.

## Belief quality is not decision quality

A probability estimate or factual belief does not determine an action by itself. Decision quality also depends on objectives, downside/upside, constraints, reversibility, opportunity cost, and available alternatives.

Moderate belief confidence can still justify a strong decision when one option is cheap and reversible; high factual certainty can still leave a weak recommendation when values or trade-offs are unresolved.

## Objectives are not evidence-derived facts

Track objective provenance:

- **user_stated:** explicitly given by the user;
- **inferred:** plausibly inferred and labeled as such;
- **default_constraint:** safety, legality, feasibility, hard platform limits, or other governing constraint.

Do not invent a precise value function. When important value weights are unknown, prefer conditional recommendations:

`If X matters more → A; if Y matters more → B.`

## Build a decision-complete option set

Do not assume the alternatives named in the prompt are the full feasible set. Before optimizing among options, ask whether a materially different strategy, staged option, combination, deferral, experiment, or reversible probe could dominate the apparent choice.

Use proportionately:

`generate materially different feasible options → remove infeasible options → prune clearly dominated options → deeply compare the live set`

This is not a brainstorming quota. Stop generating alternatives when new options are variations that do not change the decision frontier.

## Separate uncertainty types

Keep at least these uncertainties conceptually distinct when they affect the choice:

- **state uncertainty:** what will happen in the world;
- **model uncertainty:** whether the consequence model or causal mechanism is right;
- **value uncertainty:** what the user actually values or how objectives trade off;
- **option uncertainty:** whether a materially better alternative has not yet entered the set.

More factual research does not resolve value uncertainty by itself. When value weights are genuinely unresolved, give conditional recommendations or ask only when the missing preference is decision-sensitive.

## Decision path

Use only as much structure as the decision warrants:

`objective → feasible alternatives → constraints → consequences → trade-offs → uncertainty → robustness/sensitivity → reversibility → opportunity cost → value of more information → recommendation`

Ask:

- Which alternatives are actually feasible?
- What consequences matter to each objective?
- Which consequence estimates depend on fragile premises?
- Does the recommendation change under plausible parameter/value changes?
- Is a staged/reversible option available?
- What is sacrificed by choosing this option now?
- Could one additional piece of information plausibly change the decision enough to justify its cost?

## Value of information

Do not research an uncertainty merely because it exists. More information is valuable when resolving it can improve the decision. If the same action is robust across plausible values, further research may have low decision value even when epistemic uncertainty remains.

## Robustness region and switch conditions

Sensitivity analysis should identify where the recommendation remains valid, not merely whether one parameter can move. When useful, describe a **robustness region** and the conditions that switch the recommendation:

```text
A remains preferred while conditions stay within R;
A/B are both reasonable near boundary B;
choose B once condition C crosses the decision threshold.
```

Prefer ranges, ordering, and switch conditions to invented precision.

## Clarification as value of information

A missing user preference or constraint does not automatically justify interruption. Ask when the expected improvement in the decision is material relative to the cost of interruption and the information cannot be safely inferred.

`missing information → could it change the chosen action? → by enough to matter? → ask / infer / proceed conditionally`

This is distinct from authorization: low clarification value can justify proceeding, but no amount of inference can manufacture permission for a consequential action.

## Probability discipline

Do not treat a model's verbalized numeric confidence as a calibrated probability merely because it is precise. Use probabilities as decision inputs only when they come from justified data, a defensible model, calibrated forecasting, or an explicitly hypothetical scenario. Otherwise prefer qualitative confidence, ranges, scenario conditions, and sensitivity.

## Typed decision records

Durable state can represent:

- `objective` with provenance and priority/weight only when justified;
- `constraint` with source and hard/soft type;
- `alternative` with feasibility state;
- `consequence` linking an alternative to an objective and relevant premises/measurements;
- `recommendation` with `objective_refs`, `alternative_refs`, `consequence_refs`, `assumption_refs`, and sensitivity/conditionality;
- `decision` with selected alternative, authority, rationale refs, and decision status.

[← Return to root workflow](../SKILL.md)
