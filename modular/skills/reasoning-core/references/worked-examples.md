# Worked examples

**Trigger:** A boundary case is unclear and an illustrative application can clarify how much machinery to use.

**Reads:** current task pattern and lane uncertainty.

**Updates:** none; examples guide interpretation only.

**May invalidate:** none directly; examples are not empirical validation.

**Exit:** the appropriate light/deep/question/action pattern is clear.

**Related:** [problem framing and effort](problem-framing-and-effort.md), inquiry and research (route to the relevant sibling Skill if needed).

**Return:** [root workflow](../SKILL.md).

These are invented usage patterns, not measured evaluations.

## A single sentence

User asks what “你开心就好” means. The workflow stays light: preserve the literal text, inspect supplied conversational context, generate only a few plausible pragmatic readings, avoid claiming a hidden motive, and state what context would distinguish them. No web search unless external context is actually needed.

## Writing an article

User asks for an article about an emerging technology. Identify audience, thesis, genre, and factual dependencies. Research current claims that carry the argument, not every sentence. Use the evidence to improve the article and deliver the article, not a separate research report unless requested.

## Debugging code

User reports a crash. Choose the closest evidence surface: code, version, logs, tests, runtime reproduction, then upstream documentation/issues if needed. Do not begin with broad web search merely because the workflow includes research.

## Product decision

User asks which product to buy. Identify their use, constraints, current options, switching cost, and decision-sensitive differences. Verify changing specs/prices/availability, incorporate field evidence with model/version context, and recommend with the assumptions that could reverse the choice.

## Rumor verification

A social post claims a product line is discontinued. First support the claim that the post exists, trace the earliest provenance, then seek independent signals with different error mechanisms: official catalog changes, distributor status, supply observations, or direct company response. Repetition of the same rumor is one provenance cluster.

## Complex forecast

User asks how a policy may affect an industry. Escalate: current governing text, implementation capacity, affected actors, incentives, buffers, outside-in forces, second-order effects, competing mechanisms, scenarios, and observable signposts. Preserve point-in-time information and avoid pretending a scenario is a probability estimate.

## Trivial stable question

User asks for a simple transformation already determined by supplied text. The workflow recognizes that external evidence has near-zero value and proceeds directly. “Always-on” means the reasoning habit is applied, not that the web must be searched.


## Persistent change versus ordinary creation

**User:** “Rewrite this paragraph to sound clearer.”

Use the ordinary workflow. The supplied paragraph is the evidence surface; governance depth is near zero. Deliver the rewrite and check it against the requested tone. No change dossier is needed unless this paragraph is a controlled artifact in a larger project.

**User:** “Update this production workflow so approvals are faster.”

Activate controlled change governance. Baseline the current workflow, define the proposed delta and success criteria, sweep impact/risk families including compliance, human handoffs, error detection and downstream effects, obtain relevant stakeholder review when available, define process/outcome/balancing measures and rollback, implement only after readiness, then distinguish immediate verification from a later effectiveness check of actual adoption and sustained outcome.

## Open-ended question with frame uncertainty

User asks whether an emerging industry is worth entering. Do not jump straight to market-size keywords. First orient on definitions, value chain, substitutes, who captures margin, distribution power, technology constraints, policy exposure, adjacent industries, and disagreement in the source ecosystem. Convert the terrain into a few answer-bearing questions, then research the evidence that can discriminate business-model hypotheses. This is a complete Question / Reasoning Lane task even if no project is executed.

## Steering and stale propagation

User first asks for a plan under constraint A, then changes the material constraint to B. Preserve unrelated evidence, record that B supersedes A, mark dependent assumptions/decisions/artifacts/tests stale, reopen only affected branches, then regenerate and reverify what actually depends on the changed constraint. Do not restart everything or silently keep A active.

## Complete analysis but incomplete delivery

A complex report is excellent but the user also required a ZIP, source files, and validation output. Epistemic research may be complete, but the Action / Project Lane must fail the delivery integrity gate until each requested artifact is satisfied, explicitly deferred/blocked with reason, or superseded by the user.

[← Return to root workflow](../SKILL.md)
