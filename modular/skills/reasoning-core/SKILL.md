---
name: reasoning-core
description: Use when a task needs problem framing, representation choice, decomposition, relationships, causal chains, hypotheses, or careful interpretation.
---

# Reasoning Core

This is a **Modular Reasoning Workflow Skill**. It preserves the governing semantics of Reasoning Workflow but is intentionally scoped to one Family. Use only the references needed for the current gap; do not bulk-load the folder.

User instructions and hard safety/authorization constraints take precedence. This Skill is a strategy and invariant layer, not a mandatory long checklist. If another Family clearly owns the next gap and that sibling Skill is installed, route to it rather than duplicating its method here.

Always available for substantive tasks. Start light; load only the references needed by the current problem-model gap.


## Progressive references
- [`problem-framing-and-effort`](references/problem-framing-and-effort.md) — Load only when the active gap matches one of: framing, depth, autonomy, clarification, task-profile, representation.
- [`reasoning-structure-and-decomposition`](references/reasoning-structure-and-decomposition.md) — Load only when the active gap matches one of: decomposition, recomposition, structure, granularity, reasoning-stagnation.
- [`relationships-and-systems`](references/relationships-and-systems.md) — Load only when the active gap matches one of: causal-chain, systems, relationships, feedback, mechanism.
- [`hypotheses-and-bias-control`](references/hypotheses-and-bias-control.md) — Load only when the active gap matches one of: hypotheses, competing-explanations, bias, falsification.
- [`human-context-and-interpretation`](references/human-context-and-interpretation.md) — Load only when the active gap matches one of: human-context, interpretation, statement.
- [`worked-examples`](references/worked-examples.md) — Load only when the active gap matches one of: examples, workflow-example.

- [`model-adaptation`](references/model-adaptation.md) — Load when GPT-5.6+ model/runtime behavior, compute allocation, delegation, or compaction materially affects the route.

## Modular boundary

Return findings, decisions, evidence, uncertainty, and state effects to the parent task. Do not treat agreement between sibling Skills or agents as independent empirical evidence.
