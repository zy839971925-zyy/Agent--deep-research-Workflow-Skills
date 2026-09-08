# Semantic state contract

**Trigger:** Structured or durable state is materialized, machine validation is requested, closure/readiness is being computed, or state from multiple agents/artifacts must be reconciled.

**Reads:** typed canonical state, edge policy, materiality, temporal scope, declared record states, event/raw ledgers.

**Updates:** effective record states, explainable findings, closure/readiness reports, stale/recompute provenance.

**May invalidate:** epistemic closure, delivery readiness, current artifact status, downstream reasoning, verification, effectiveness.

**Exit:** declared state has been interpreted under one shared semantic contract and all blocking findings are explicit.

**Related:** [state model and invariants](state-model-and-invariants.md), [synchronization and recovery](synchronization-and-recovery.md), [traceability and integrity](traceability-and-integrity.md).

**Return:** [root workflow](../SKILL.md) → Durable state / closure.

## Governing principle

**Declared state is input. Effective state is computed.**

A record may declare itself `current`, `answered`, `passed`, or `closed`. That declaration is not authoritative if upstream dependencies, supersession, invalidation, temporal scope, or closure rules imply otherwise.

Likewise:

- `declared_status` is stored on records;
- `effective_status` is computed by the semantic validator;
- `declared_delivery_ready` is a manifest claim;
- `computed_delivery_ready` is validator output;
- work may declare `closed`, but Question-lane closure uses `computed_epistemic_closed`.

Validators certify **structural admissibility, not epistemic truth**. They can prove that records are typed, references resolve, dependency semantics are internally coherent, stale state is not silently reused, and closure rules are satisfied. They cannot prove that a real-world premise is true or that a recommendation is wise.

## Materiality

Every epistemically or operationally relevant record can carry:

`material | supporting | incidental`

The question is not “is this detail interesting?” but:

> If this record were wrong, unknown, stale, or omitted, could it materially change the core answer, judgment, action, safety, or required delivery?

Only material unresolved/stale items normally block closure. Supporting/incidental items can remain bounded with a finding when they do not change the user's outcome.

## Temporal semantics

Do not collapse temporal meaning into one `stale` boolean.

- **invalid:** the record itself is unusable under the contract.
- **stale:** the record may once have been valid but is no longer current for this task/context.
- **superseded:** a newer authoritative version replaces it for the relevant scope.
- **historical:** it remains valid for a past time/scope even if not current for the present task.

Useful fields include `valid_for`, `observed_at`, `effective_at`, and `current_for_task`. Historical validity and present applicability are distinct.

## Record lifecycle families

Different record types have different declared status spaces. Do not reuse one ambiguous universal status enum.

- **Question:** `open | answered | bounded | deferred | invalidated`
- **Answer:** `draft | current | bounded | stale | invalidated | superseded`
- **Premise/Assumption:** `current | challenged | stale | invalidated | superseded | historical`
- **Hypothesis:** `candidate | leading | weakened | rejected | superseded`
- **Uncertainty:** `open | resolved | bounded | irreducible | deferred | invalidated`
- **Inference/Judgment/Recommendation/Decision:** `draft | current | challenged | stale | invalidated | superseded`
- **Artifact:** `draft | current | stale | superseded | historical`
- **Verification:** `pending | passed | failed | stale | blocked`
- **Effectiveness:** `pending | effective | ineffective | inconclusive | stale`

The canonical JSON Schema is the local-shape authority. Cross-record effective-state semantics are implemented by the shared semantic engine.

## Typed reference integrity

Build a registry:

`record_id → {record_type, collection, record, declared_status, effective_status}`

References are valid only when all relevant conditions hold:

1. the target exists;
2. the target has a compatible record type;
3. the target's effective state is compatible with the use;
4. the reference direction matches the edge contract.

For example, `premise_refs` may resolve only to Premise/Assumption records; `question_refs` only to Questions; `verification_refs` only to Verification records.

## Edge policy and cycle semantics

Keep edge semantics centralized rather than scattering them across ad-hoc conditionals. The Portable edition includes a machine-readable edge policy and validators; a Modular host may use its own equivalent enforcement as long as the same semantics are preserved.

Typical families:

- logical dependency / lineage / supersession: cycles normally invalid;
- causal/feedback relationships: cycles allowed;
- support networks: cycles allowed structurally but may warrant circular-support warnings;
- explicit invalidation: invalidation cycles are normally errors.

`hard` propagation means downstream current-like records become effectively stale/invalid. `recompute` means downstream support/conflict/measurement should be recomputed before material closure. `none/contextual` means no automatic stale propagation; another semantic rule decides.

## Explainable enforcement

Every computed blocking result must explain why. Prefer chains such as:

`P-2 invalidated → INF-3 effectively stale → JDG-4 effectively stale`

Closure reports should enumerate blockers rather than return only a boolean. Findings use:

- **ERROR:** blocks the relevant closure/readiness gate;
- **WARNING:** requires disposition or review but may not block;
- **INFO:** diagnostic context.

[← Return to root workflow](../SKILL.md)
