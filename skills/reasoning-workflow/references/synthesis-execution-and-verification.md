# Synthesis, execution and verification

**Trigger:** Transition from analysis/research to the user-facing answer, artifact, recommendation, action, or acceptance check.

**Reads:** objective, evidence/inference/judgment, constraints, artifacts/actions, verification state, unresolved uncertainty.

**Updates:** final synthesis/deliverable, verification findings, bounded limitations, completion status.

**May invalidate:** delivery readiness if the result does not answer the real task or fails critical checks.

**Exit:** the requested outcome is produced at the warranted quality and verified proportionately.

**Related:** [traceability and integrity](traceability-and-integrity.md), [formal review and audit](formal-review-and-audit.md), [change governance and effectiveness](change-governance-and-effectiveness.md).

**Return:** [root workflow](../SKILL.md) → Synthesize/answer or Verify/Reconcile.

Use near the transition from analysis to the user's actual deliverable or action.

## Build the result around the parent goal

A direct answer can itself be the complete parent outcome. Do not force a question into project semantics simply because this workflow also supports durable execution. Lead with the answer, artifact, recommendation, diagnosis, implementation, or other requested outcome. Organize evidence by its role in solving the problem, not by search order or source identity.

Keep these layers conceptually distinct when material:

`observation/evidence → inference → judgment → recommendation/action`

A citation can support an observation or source assertion without proving a recommendation. A recommendation should expose the uncertain premises that could reverse it when those premises matter.

## Writing and creation

When the parent task is an article, message, report, design, script, presentation, codebase, or other artifact, research should improve the artifact rather than replace it with a research memo. Preserve user-specified genre, voice, audience, structure, and format.

Use external facts only when they serve the piece. Separate sourced facts from rhetorical framing or creative choices. For persuasive writing, do not manufacture certainty beyond the evidence.

## Diagnosis and implementation

Prefer direct observations from the actual system, file, code, logs, tests, or environment over generic explanations. When authorized to fix or build, carry evidence into implementation and verify the result rather than stopping at a diagnosis. If the work creates a material persistent change, use the change-governance lane before implementation and do not call the work closed merely because the immediate change was made.

## Editorial/evidence audit

Before delivery, ask:

- Does the answer address the user's actual objective rather than a proxy problem?
- Are important observations distinguishable from inference and assumption?
- Are entity, identity, version, time, jurisdiction, population, units, and definitions aligned?
- Are consequential claims supported by inspected material or explicitly bounded?
- Did compression erase qualifiers, negation, contradiction, or uncertainty?
- Is causal or psychological language stronger than the evidence?
- Did execution actually produce and check the requested result?
- For controlled change, does the actual state match the approved/baselined record, and were deviations captured?
- If effectiveness cannot yet be observed, is the change correctly left effectiveness-pending instead of falsely closed?
- Would another feasible action likely change the decision or answer materially?

## Deliver proportionately

Separate **epistemic stopping** from **delivery integrity**. Research can be complete while a requested artifact is still missing; conversely a delivery can be structurally complete while retaining explicitly bounded uncertainty that does not block its intended use.

Do not surface the entire research machinery unless the user asks for an audit trail. A simple task should still have a simple answer. A complex task may need structured evidence, scenarios, caveats, or appendices.

A bounded unresolved issue can still be a complete result if the uncertainty is stated at the level that matters. Do not fabricate resolution because a budget or tool limit was reached.


## Change completion semantics

Keep `implemented`, `verified`, `validated`, and `effective` distinct. Immediate verification answers whether the change was executed correctly; effectiveness requires sufficient subsequent evidence that the intended process is being followed and the intended result is sustained without unacceptable balancing effects.


## Question integrity and recomposition

For Question / Reasoning work, verify the answer against the original epistemic task before delivery. Check:

- **question drift:** did research solve a nearby easier question instead of the user's original one?
- **recomposition:** if the problem was decomposed, do the branch answers actually combine into the parent answer?
- **premise integrity:** are material premises current and appropriately supported/bounded?
- **role integrity:** are fact, inference, judgment, and recommendation still distinguishable where material?
- **uncertainty integrity:** are unresolved uncertainties attributed to their actual source rather than hidden by vague wording?

A polished synthesis that answers the wrong question is a failed result.


## Pivotal-claim synthesis

For Deep, Max, and Ultra research, synthesize in two passes when the answer depends on multiple material claims. First construct an epistemic synthesis: what is known, inferred, judged, recommended, contested, bounded, or unknown. Then write the user-facing answer.

Before strengthening a conclusion, inspect the weakest material dependency. A conclusion cannot be more certain than the pivotal premise, measurement, causal edge, source fit, or evidence route it depends on.

Final verification should focus on pivotal claims: does the cited source entail the claim, merely contextualize it, partially support it, or fail to support it? Does the entity/version/time/population/definition match? Is the wording stronger than the evidence permits?

[← Return to root workflow](../SKILL.md)
