# Current Architecture — Major File Changes

This document records the major files introduced or reshaped during the transition to depth-gated routing, progressive context, independent verification, and controlled learning. Public release numbering has been retired; Git history is the chronological source of truth.

## Added architecture layers

### Routing and task depth

- `routing-index.json`
- `schemas/task-profile.schema.json`
- `scripts/routing_core.py`
- `scripts/route_task.py`
- `scripts/route_resources.py`
- `families/core-reasoning.md`
- `families/deep-research.md`
- `families/decision-analysis.md`
- `families/execution-control.md`
- `families/audit-verification.md`
- `families/workflow-learning.md`

### Dual verification

- `schemas/dual-verification.schema.json`
- `scripts/validate_dual_verification.py`

### Controlled learning and CAPA

- `schemas/learning-record.schema.json`
- `schemas/capa-record.schema.json`
- `scripts/learning_core.py`
- `scripts/retrieve_learnings.py`
- `scripts/validate_learning.py`
- `references/workflow-learning-and-capa.md`

### Distribution and consistency

- `scripts/build_distributions.py`
- `scripts/validate_distribution.py`
- `SEMANTIC_MANIFEST.json`

### Evaluation structure

- `evals/deep-research/README.md`
- `evals/deep-research/metrics.json`
- `evals/deep-research/task-manifest.json`
- `tests/routing/`
- `tests/context/`
- `tests/adherence/`
- `tests/learning/`
- `tests/deep-research/`
- `tests/distribution/`

## Reshaped existing layers

The root `SKILL.md` is now a thinner governing map. Existing references remain the detailed reasoning/research/runtime knowledge base but are progressively routed rather than bulk-loaded.

The adherence evaluator now reasons from state preconditions, transitions, observables, resource loads, and validator findings rather than assuming same-turn event creation is always required.

Public product release numbers have been removed from human-facing names and filenames. Runtime integrity fields such as `schema_version`, `state_version`, `profile_version`, `plan_version`, and `schedule_version` remain because they are machine semantics, not branding.
