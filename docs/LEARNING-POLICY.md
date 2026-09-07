# Reasoning Workflow — Learning / Self-Evolution Policy

## Principle

Self-learning is controlled experience reuse, not automatic self-editing.

## Inputs

The Learning Plane may consume:

- successful runs with verified outcomes;
- failed runs;
- recovery trajectories;
- inefficient-but-successful trajectories;
- user corrections;
- deterministic/evaluator findings;
- benchmark results;
- CAPA records;
- regression failures.

## Candidate creation

A candidate must preserve provenance, applicability conditions, anti-conditions, supporting examples and counterexamples. Same-model intrinsic reflection without new evidence may create a candidate only.

## Tier 1 — Experience Memory

Validated strategy, recovery, and optimization lessons may be retrieved selectively. Runtime retrieval is limited to a small relevant subset chosen from the Task Profile and current gap. Track `learning_used`, `learning_helped`, and `learning_harmed`.

Stale/deprecated lessons are excluded. Harmful or low-value lessons are downgraded or deprecated rather than permanently accumulated.

## Tier 2 — Routing / Reference Heuristics

Routing heuristics may change depth, recheck triggers, or reference selection only after held-out routing/context evaluation and negative controls show improvement without unacceptable regression.

## Tier 3 — Canonical Workflow Change

Any change to `SKILL.md`, schemas, lifecycle/edge policy, authorization, closure, validators, or runtime invariants requires:

```text
candidate
→ minimal failing regression
→ shadow / offline evaluation
→ baseline comparison
→ independent review
→ promote / reject
→ rollback available
```

No single run can directly promote a canonical change.

## CAPA integration

Material workflow failures enter:

```text
failure
→ containment
→ root cause
→ corrective action
→ regression
→ verification
→ effectiveness check
→ preventive / generalization
→ closure
```

Only after effectiveness is observed should a generalized learning candidate be created.

## Root-cause classes

- problem misframing;
- wrong depth;
- wrong routing;
- context overload;
- missing context;
- evidence/provenance failure;
- instruction conflict;
- model capability limit;
- tool/runtime failure;
- validator gap;
- execution-plan error;
- schedule/delegation error;
- checkpoint/recovery error;
- success pattern / inefficiency.

## Promotion governance

Critical invariants, authorization rules, semantic lifecycle and closure changes require the highest review level. Every canonical change needs a rollback reference.
