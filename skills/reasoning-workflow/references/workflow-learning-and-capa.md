# Workflow Learning and CAPA

[← Back to Workflow Learning family](../families/workflow-learning.md) · [Back to root workflow](../SKILL.md)

Use this module only in the maintenance plane, after a run or evaluation has produced external outcome evidence, deterministic findings, independent review, user correction, benchmark results, or another source of genuinely new information.

## Core boundary

Self-learning is not self-editing. A model criticizing its own answer without new evidence may create a **candidate insight**, but cannot validate or promote a canonical learning.

## CAPA failure loop

For material workflow nonconformity use:

`failure → containment → root cause → corrective action → regression → verification → effectiveness check → preventive/generalization → closure`

Classify root cause before changing instructions. Useful classes include problem misframing, wrong depth, wrong routing, context overload, missing context, evidence/provenance failure, instruction conflict, model capability limit, tool/runtime failure, validator gap, execution-plan error, schedule/delegation error, and checkpoint/recovery error.

Do not respond to every failure by adding prompt text. Correct the mechanism that allowed the failure.

## Learning tiers

### Tier 1 — Experience memory

Store only validated, portable strategy/recovery/optimization lessons. Retrieve a small number whose applicability conditions match the active Task Profile and current gap. Track whether use helped or harmed.

### Tier 2 — Routing/reference heuristic

A routing lesson may propose changes to depth or reference selection. Promotion requires held-out evaluation against the current baseline and negative controls.

### Tier 3 — Canonical workflow change

Changes to SKILL.md, schemas, policy, validators, closure, authorization or runtime invariants require:

`candidate → minimal regression fixture → offline/shadow eval → baseline comparison → independent review → promote/reject → rollback available`

Never promote a Tier 3 change from a single trajectory.

## Memory hygiene

Validated memory may be promoted, downgraded, deprecated or marked stale. Deprecated/stale lessons are not runtime-retrievable. Prefer compact transferable heuristics over transcript storage. Preserve provenance and counterexamples.

## Learning and CAPA integration

CAPA creates a learning candidate only after corrective action passes verification and an effectiveness observation supports generalization. A one-off fix is not automatically a reusable lesson.

## Runtime isolation

Learning Plane is not part of normal task context. Ordinary runs may retrieve only a small validated experience-memory subset selected from the active profile and gap. Canonical Skill edits remain maintenance operations.

---

**Routing rule:** Return to the governing router after this module. `Related ≠ automatic load`; do not recursively load references.
