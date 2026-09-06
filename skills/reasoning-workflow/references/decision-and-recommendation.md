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

## Typed decision records

Durable state can represent:

- `objective` with provenance and priority/weight only when justified;
- `constraint` with source and hard/soft type;
- `alternative` with feasibility state;
- `consequence` linking an alternative to an objective and relevant premises/measurements;
- `recommendation` with `objective_refs`, `alternative_refs`, `consequence_refs`, `assumption_refs`, and sensitivity/conditionality;
- `decision` with selected alternative, authority, rationale refs, and decision status.

[← Return to root workflow](../SKILL.md)
