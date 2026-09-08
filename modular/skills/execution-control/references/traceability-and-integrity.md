# Traceability and integrity

**Trigger:** Multiple requirements, durable state, multiple artifacts/representations, controlled changes, audit-sensitive work, delivery packages, or any task where omission/drift would materially matter.

**Reads:** requirements, questions/answers, premises, observations, evidence, hypotheses/uncertainty, inferences, judgments/recommendations, decisions, actions, artifacts, verification/effectiveness records, canonical state version.

**Updates:** typed trace links, requirement coverage, artifact representation contracts, delivery manifest, consistency findings, closure blockers.

**May invalidate:** delivery readiness, artifact-current status, verification, closure.

**Exit:** material records are traceable; requirements are dispositioned; required representations are reconciled; delivery blockers are explicit.

**Related:** [state model and invariants](state-model-and-invariants.md), [synchronization and recovery](synchronization-and-recovery.md), change governance and effectiveness (route to the relevant sibling Skill if needed), formal review and audit (route to the relevant sibling Skill if needed).

**Return:** [root workflow](../SKILL.md) → Reconcile / Completion.

## End-to-end typed traceability

A citation is not the same as full traceability. For durable material work, preserve enough typed links to answer both forward and backward questions:

- Why was this decision/action taken?
- Which evidence and premises support this conclusion?
- Which artifact implements this requirement?
- Which verification proves this requirement/artifact state?
- Which outputs become stale if an upstream requirement changes?

Useful record prefixes are illustrative, not mandatory:

```text
REQ requirement
Q   pivotal question
RAW preserved source/original
OBS observation
EVD evidence record
PRE premise/assumption
HYP hypothesis
UNC uncertainty
INF inference
JDG judgment
REC recommendation
DEC decision
RSK risk
ACT action
ART artifact
VER verification/validation
EFF effectiveness
```

Example:

`REQ-001 → Q-003 → OBS-012/RAW-005 → EVD-021 → PRE-004 → HYP-002 → INF-009 → JDG-003/REC-001 → DEC-004 → ACT-006 → ART-003 → VER-018 → EFF-002`

Not every task needs every type. Use only the granularity needed to prevent material ambiguity or drift.


## Question integrity

Traceability also applies to pure Question / Reasoning work. Preserve enough linkage to answer:

- What original question is this branch answering?
- Which premises/evidence support the final inference or judgment?
- Which uncertainty remains unresolved?
- If the question was decomposed, how do the branch answers recompose into the parent answer?
- Did research drift into an adjacent question?

For complex inquiry, an answer should be able to point back to its parent question and decisive support without requiring a project/change record.

## Raw and derived lineage

Preserve source material as distinct from descendants whenever technically feasible. A transformation creates a new record with `derived_from`, not a silent replacement.

For material source records, useful metadata can include:

`raw_id | source locator | observed/retrieved_at | original name | version hint | visibility | hash/fingerprint when feasible | transformations/descendants`

A hash supports identity/integrity checking; it does not prove the source is truthful. Do not claim immutable storage when the medium cannot enforce it.

## Requirement coverage is separate from research convergence

Before delivery closure, every explicit user requirement and material acceptance condition needs a disposition such as:

`satisfied | not applicable with reason | user-approved deferred | blocked with reason | superseded`

A requirement coverage entry should link to the artifact/action that satisfies it and the verification that checks it when verification is warranted.

A useful conceptual matrix:

`requirement | source | status | artifact/action | verification | notes`

Do not declare delivery complete with a silently missing requirement simply because the substantive analysis is excellent.

## Representation contracts and cross-artifact consistency

Different artifacts may intentionally represent different subsets of the canonical state. Record the role when drift matters:

`artifact | based_on state/version | represents IDs | role(full/summary/implementation/visual/etc.) | current/stale | verification refs`

A summary can omit details without conflict. A contradiction in a shared material value, decision, requirement, version, threshold, or result is a consistency anomaly.

Examples:

```text
canonical threshold = 0.8
code = 0.75          → conflict/blocker
manual = 0.8
```

```text
full report = risks A/B/C/D
slides = risks A/C
slides role = selected-summary → not automatically inconsistent
```

No material artifact may be declared current while it materially conflicts with authoritative state or another required representation without an explicit accepted divergence.

## Delivery manifest

For multi-artifact or handoff work, maintain a compact manifest containing:

- work/state version;
- requirement coverage summary;
- delivered artifacts and their representation roles;
- verification references/status;
- stale or superseded items excluded from delivery;
- unresolved blockers/deferred items;
- whether the package is delivery-ready.

The manifest is a closure aid, not a substitute for inspecting the artifacts. Its `declared_delivery_ready` value is not authoritative: the validator computes readiness by reconciling the manifest against canonical typed state and effective verification/artifact status.

## Integrity gate

Before `delivery_ready = true`, verify as warranted:

- every requirement has an explicit disposition;
- required artifacts exist and are the intended current versions;
- no blocking material stale item is represented as current;
- required verification/validation has passed or is explicitly pending/blocked;
- required cross-artifact representations are reconciled;
- unresolved risks/limitations are disclosed at the level relevant to the user's objective.

An epistemically complete answer can still fail this gate. A delivery can pass this gate while retaining explicitly bounded uncertainty that does not block the user's requested use.

[← Return to root workflow](../SKILL.md)
