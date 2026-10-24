# Model adaptation for GPT-6+ and current frontier models

**Trigger:** A frontier model, model family, or host runtime materially changes the available reasoning effort, context, tools, parallelism, persistence, or presentation surface.

**Reads:** the user's objective and depth, actual model/runtime identity when exposed, available tools and limits, context pressure, current research state, and observed failure modes.

**Updates:** phase allocation, scaffold strength, context disclosure, delegation, serial fallback, and presentation strategy.

**May invalidate:** model-name assumptions, fixed long plans, uniform maximum effort, unnecessary repetition, or an instruction that presumes an unavailable host feature.

**Exit:** the workflow matches capabilities actually exposed by the current host while preserving the research and authorization invariants.

**Related:** [harness profiles](harness-profiles.md), [problem framing and effort](problem-framing-and-effort.md), [runtime and delegation](runtime-and-delegation.md), [Ultra research](ultra-research.md).

**Return:** [root workflow](../SKILL.md) → Task Profile / routing.

## Principle: capability-first, model-aware

Target GPT-6-generation and later systems, including current Claude 5.5/5.1-class models where available. These are target examples, not proof that a particular model or product exposes a capability or performs a task better. Do not preserve a GPT-5 compatibility target by default, create model-name branches, or infer behavior from a marketing label.

Adapt to the *observed model-plus-harness* pair. A model can reason about a tool it cannot call; a CLI may support agents while the API or consumer chat does not; a product may use a different model for its Research mode. A skill instruction cannot install a tool, grant access, enforce a permission boundary, guarantee persistence, or force an interactive UI.

Strong models benefit from clear outcomes, epistemic invariants, and room to choose tactics. Keep procedural structure where it protects a material transition, prevents a known failure, or makes work recoverable. Do not remove scaffolding merely because the model is newer, and do not add model-specific personality claims without direct, task-relevant evidence.

## Inspect the live capability surface

Before planning tool-dependent work, establish only what the current interface actually shows:

- search, webpage retrieval, citation display, file/PDF reading, code execution, data analysis, and connected sources;
- reasoning-effort controls, context limits or compaction behavior, and whether state can be saved outside the conversation;
- independent agents, their tool and permission scope, and whether they can run concurrently;
- charts, diagrams, artifacts, interactive elements, or host-provided widgets;
- account, plan, workspace, region, and administrator limits that are visible or documented.

Treat unknown features as unavailable for this run. Continue with supplied information and available methods; mark the exact consequential gap rather than describing a planned tool call as completed.

## Allocate effort by epistemic leverage

Use the strongest available reasoning for the work whose error would propagate: reconstructing a disputed frame, identifying decisive dependencies, designing a discriminating observation, reconciling independent evidence, assessing causal claims, and synthesizing limitations. Delegate or use cheaper processing for bounded extraction, metadata normalization, deduplication, formatting, or mechanical comparison only when the host actually supports it and the output remains inspectable.

Depth governs the breadth and persistence of inquiry, not uniform maximum compute. After a major reframe, rebuild from the user’s objective and retained evidence instead of carrying forward a provisional answer as settled. Use a provisional synthesis to expose evidence gaps, then deliberately search for those gaps—including a plausible adverse result—rather than merely confirming the draft.

## Context and recoverable state

Progressively load the entry point, active family, and only the references that address a live gap. More context is useful when it contains decision-bearing evidence or constraints, not simply because a model accepts a larger prompt.

For a long task, preserve a compact external or conversation-visible evidence packet when the host supports it: question and scope; current frame; pivotal claims; source locators and decisive passages; source-family/dependency notes; conflict and uncertainty; closed or failed routes; next discriminating target. Do not depend on hidden chain-of-thought, a subagent's unreturned context, or a promise that compaction preserves every tool result.

## Delegation and serial Ultra

Use agents only when the current harness exposes them and independent branches could materially improve coverage, speed, or error independence. Give each worker a self-contained question, scope, seed evidence, named gap, permitted sources/tools, and a compact evidence-return format. The root researcher evaluates source independence and resolves conflicts; agent consensus is not corroboration.

If agents are absent, run justified branches serially: complete one useful evidence route, update the research frontier, then select the next route. Preserve Ultra’s broader reframing and cross-checking; do not pretend work was parallel or lower the depth merely because the host has one conversation thread.

## Presentation surfaces

When the host supports an interactive chart, comparison, diagram, or artifact, prefer it only if the structure helps the user inspect relationships, trade-offs, or dense data. Keep simple factual answers in text. Use a clear text/table fallback when the UI is unavailable; do not imply that a skill can invoke an Apps SDK widget, artifact, or chart without a supported host capability.

## Tune from observed failures, not stereotypes

Change scaffolding locally when the workflow misses a real obligation, loses context, over-searches, over-plans, delegates unnecessarily, or repeats verification without changing the answer. Keep the semantic contract fixed: answer the real question; distinguish observation, inference, and unknown; preserve provenance and boundaries; use tools only as available and authorized; and do not claim unperformed work.

A newer model is not itself evidence of better research. Claims about quality, reliability, cost, or latency require task-relevant evaluation; official product documentation establishes feature availability, not measured performance gains.

[← Return to root workflow](../SKILL.md)
