# State model and invariants

**Trigger:** Long, multi-step, multi-artifact, delegated, interruptible, consequential, or persistent work where drift, handoff, or recovery matters.

**Reads:** objective, requirements, questions, premises, observations/evidence, hypotheses/uncertainty, inferences/judgments/recommendations, decisions, risks, actions, artifacts, verification/effectiveness state, runtime persistence capabilities.

**Updates:** canonical current-state projection, state version, readable status, historical event references, persistence profile.

**May invalidate:** any derived decision, action, artifact, test, or effectiveness criterion based on superseded state.

**Exit:** a proportionate current-state representation exists and the persistence level matches the actual task/runtime need.

**Related:** [synchronization and recovery](synchronization-and-recovery.md), [traceability and integrity](traceability-and-integrity.md), [runtime and delegation](runtime-and-delegation.md), change governance and effectiveness (route to the relevant sibling Skill if needed).

**Return:** [root workflow](../SKILL.md) → Action / Project Lane.

## Separate current truth from historical truth

For durable material work, preserve two logical layers:

1. **Historical authority:** source/raw records, observations, user steering, decisions, and state-changing events. Preserve rather than silently rewriting them whenever technically feasible.
2. **Operational authority:** one canonical current-state projection describing what is current now.

The current projection may change. The history explains how and why it changed.

Do not create multiple silent “truths” in UI state, working notes, saved files, agent summaries, and deliverables. Derived artifacts are views/representations of canonical state and should identify the state/version they were based on when material.

## Persistence profiles

Do not force a state directory onto every task.

### P0 — Ephemeral

Use for short questions, simple interpretations, small rewrites, or directly determined work. State remains in current context. Preserve the invariants semantically; create no state files merely for ceremony.

### P1 — Structured

Use for complex analysis or research that benefits from explicit compact state but is unlikely to require crash recovery or handoff. Maintain IDs/records conceptually or in a lightweight scratch artifact when the environment supports it.

### P2 — Durable

Use when work is long, interruptible, delegated, multi-artifact, has persistent side effects, or needs later effectiveness checking. Persist a canonical state projection and sufficient history/checkpoints in a task-scoped location supported by the runtime.

A logical durable layout may be:

```text
.reasoning-workflow/
├── work-state.json
├── events.jsonl
├── raw-manifest.json
├── delivery-manifest.json
└── checkpoints/
```

The path is illustrative. Respect workspace conventions and authorization; do not contaminate a user's repository or deliverables merely to satisfy this layout.

### P3 — Managed external state

When a system already provides transactional versions, revision IDs, ETags, database constraints, Git commits, workflow state, or idempotency controls, use those native mechanisms as the stronger authority rather than building a competing local truth.

## Canonical work state

A durable current-state projection should include only what prevents drift and enables continuation. Typical fields:

`work_id | schema_version | state_version | status | objective | scope | requirements | acceptance criteria | questions/answers | observations/evidence | premises/assumptions | hypotheses | uncertainties | relationships | inferences | judgments/recommendations | decisions | risks | actions | artifacts | verification | effectiveness | stale items | blocked items | last completed action | next safe action | updated_at`

Do not force every field onto every task. Omit inapplicable collections rather than inventing content.


## Premises and epistemic state

Durable work should not preserve only project requirements and actions. When reasoning dependencies matter, the canonical state may also represent premises, hypotheses, uncertainty, relationships, inferences, judgments, recommendations, and answers. This allows an upstream factual/premise change to propagate into downstream reasoning rather than only into implementation records.

A premise may point to an observation/evidence record or may be an explicit user definition/assumption. A downstream inference can reference that premise through `premise_refs` or `depends_on`. Stale premises should make material current-like dependents stale until they are re-evaluated or explicitly rebased.

## Semantic state contract

For machine-managed state, record-specific `declared_status` is only an input. The semantic engine computes `effective_status` from type rules, temporal scope, supersession/invalidation, and dependency propagation. Closure/readiness must use the computed state. See [semantic state contract](semantic-state-contract.md).

Materiality is explicit (`material | supporting | incidental`) so closure does not become formalistic. Only unresolved/stale items capable of changing the core answer, action, safety, or required delivery should normally block closure.

## Readability is an operational property

A successor should be able to answer quickly:

- What are we trying to achieve?
- What has the user explicitly required?
- What is current versus stale?
- What evidence and decisions are carrying the plan?
- What has already been changed?
- What is blocked or effectiveness-pending?
- What is the next safe action?

Machine state that is technically valid but incomprehensible to a human is not sufficient for this workflow.

## Historical events

For durable work, meaningful state changes may be represented as append-only events when the runtime supports it:

`event_id | seq | timestamp | actor | type | from_version | to_version | changed items | invalidated items | reason/source`

Useful event types include user constraint changes, evidence updates, decision changes, implementation commits, verification results, artifact generation, risk acceptance, rollback, effectiveness results, and reopen decisions.

Do not claim append-only or immutable guarantees that the storage medium cannot actually enforce. Preserve originals and prior versions as strongly as feasible.

## State version invariant

Every material current projection has one `state_version`. A derived artifact or verification record should identify the version or canonical IDs it represents when version drift could matter.

Do not mark two contradictory material states as simultaneously authoritative. Use explicit supersession, conflict, or stale status.

## Specialist-skill composition

This state belongs to the governing process, not to a specialist Skill. A product-design, spreadsheet, PDF, coding, or other Skill may update artifacts or domain-specific decisions, but the governing workflow retains the user objective, cross-domain requirements, traceability, staleness, and completion state.

[← Return to root workflow](../SKILL.md)
