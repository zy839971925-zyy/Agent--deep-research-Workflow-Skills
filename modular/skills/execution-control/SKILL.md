---
name: execution-control
description: Use when work creates durable artifacts or external side effects, delegates execution, needs authorization, or must preserve state/checkpoint/recovery semantics.
---

# Execution Control

This is a **Modular Reasoning Workflow Skill**. It preserves the governing semantics of Reasoning Workflow but is intentionally scoped to one Family. Use only the references needed for the current gap; do not bulk-load the folder.

User instructions and hard safety/authorization constraints take precedence. This Skill is a strategy and invariant layer, not a mandatory long checklist. If another Family clearly owns the next gap and that sibling Skill is installed, route to it rather than duplicating its method here.

Activate only when work persists beyond an answer: external side effects, durable artifacts, delegated execution, Swarm, checkpoint/resume, authorization, or controlled state.


## Progressive references
- [`runtime-and-delegation`](references/runtime-and-delegation.md) — Load only when the active gap matches one of: execution, delegation, swarm, schedule, worker, capability, failure-diagnosis, replanning.
- [`synchronization-and-recovery`](references/synchronization-and-recovery.md) — Load only when the active gap matches one of: checkpoint, resume, recovery, replay, side-effect, checkpoint-alignment.
- [`state-model-and-invariants`](references/state-model-and-invariants.md) — Load only when the active gap matches one of: state, canonical-state, invariants, durable.
- [`semantic-state-contract`](references/semantic-state-contract.md) — Load only when the active gap matches one of: semantic-state, lifecycle, effective-state.
- [`traceability-and-integrity`](references/traceability-and-integrity.md) — Load only when the active gap matches one of: traceability, integrity, event, lineage.
- [`domain-patterns`](references/domain-patterns.md) — Load only when the active gap matches one of: domain-pattern, implementation-pattern.

## Modular boundary

Return findings, decisions, evidence, uncertainty, and state effects to the parent task. Do not treat agreement between sibling Skills or agents as independent empirical evidence.
