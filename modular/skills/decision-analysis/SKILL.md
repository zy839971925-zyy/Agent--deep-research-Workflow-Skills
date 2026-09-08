---
name: decision-analysis
description: Use when the deliverable is a choice, recommendation, prioritization, trade-off, resource allocation, or robustness-sensitive decision.
---

# Decision Analysis

This is a **Modular Reasoning Workflow Skill**. It preserves the governing semantics of Reasoning Workflow but is intentionally scoped to one Family. Use only the references needed for the current gap; do not bulk-load the folder.

User instructions and hard safety/authorization constraints take precedence. This Skill is a strategy and invariant layer, not a mandatory long checklist. If another Family clearly owns the next gap and that sibling Skill is installed, route to it rather than duplicating its method here.

Activate when the core deliverable is a choice, recommendation, trade-off, prioritization, or resource-allocation decision.


## Progressive references
- [`decision-and-recommendation`](references/decision-and-recommendation.md) — Load only when the active gap matches one of: decision, recommendation, tradeoff, choice, allocation, option-set, preference-uncertainty, robustness, clarification-voi.
- [`measurement-and-operationalization`](references/measurement-and-operationalization.md) — Load only when the active gap matches one of: measurement, metric, proxy, operationalization.

## Modular boundary

Return findings, decisions, evidence, uncertainty, and state effects to the parent task. Do not treat agreement between sibling Skills or agents as independent empirical evidence.
