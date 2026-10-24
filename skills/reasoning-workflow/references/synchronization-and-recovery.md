# Synchronization and recovery

**Trigger:** User steering, changing upstream inputs, multiple artifacts/views, concurrent/delegated work, external state changes, interruption, resume, retries, or persistent side effects.

**Reads:** canonical state, dependency links, state/event versions, artifact versions, current runtime/external observations, previous checkpoint.

**Updates:** stale/current/conflict state, invalidation propagation, checkpoints, resume position, idempotency/operation status.

**May invalidate:** premises, hypotheses, inferences, judgments, recommendations, decisions, risks, plans, artifacts, verification, effectiveness criteria, delivery readiness.

**Exit:** current state has been reconciled; stale dependencies are known; repeated side effects are prevented where feasible; a safe next action is identified.

**Related:** [state model and invariants](state-model-and-invariants.md), [traceability and integrity](traceability-and-integrity.md), [runtime and delegation](runtime-and-delegation.md).

**Return:** [root workflow](../SKILL.md) → Re-observe / Reconcile.

## Dependency-aware invalidation

Do not respond to every upstream change by restarting all work. Maintain typed dependency relationships where material, such as:

`depends_on | premise_refs | derived_from | supports | contradicts | implements | produces | represents | verifies | monitors | supersedes | invalidates`

When an upstream item changes, mark dependent items stale until they are re-evaluated. Preserve unrelated current work.

Example:

```text
Constraint C17 changes A → B
  ├── P3 premise-dependent inference stale
  ├── H3 hypothesis          stale
  ├── D4 decision            stale
  ├── R8 risk assessment     stale
  ├── ART2 artifact          stale
  └── T11 verification       rerun required

EVD7 unrelated evidence      remains current
```

A stale item is not automatically wrong; it is no longer justified as current by the latest upstream state.

## Steering protocol

When the user changes scope, constraints, entities, or downstream intent:

1. record the new authoritative instruction and what it supersedes;
2. identify the changed upstream nodes;
3. propagate staleness through material dependencies;
4. preserve unaffected evidence and completed work;
5. reopen only affected inquiry/action branches;
6. update the current-state version and next safe action;
7. regenerate/reverify stale deliverables only as needed.

Do not silently keep older user instructions active when the new instruction conflicts with them.

## Cross-view synchronization

Artifacts, UI views, code, documents, saved projects, and summaries can drift. A representation should declare what canonical IDs/state it represents when material.

On reconciliation, compare **meaning**, not just timestamps. Different representations may intentionally contain different detail. A summary may omit material that a full report contains without conflict; contradictory values, versions, decisions, or required requirements are conflicts.

## Conflict handling

When two updates cannot both be current:

- identify their authoritative sources and observation/version times;
- do not merge incompatible values by averaging or guesswork;
- preserve both historical records;
- choose or request the authoritative resolution according to user instruction, system ownership, or governing policy;
- mark downstream dependents stale until resolved.

When an external system provides revision IDs or optimistic-concurrency tokens, use them rather than overwriting a newer version blindly.

## Checkpoint discipline

For durable work, checkpoint after material state transitions such as:

- user scope/constraint change;
- major evidence update;
- consequential decision or risk disposition;
- mutation/side effect;
- verification or validation milestone;
- handoff or delegation merge;
- before a risky or hard-to-reverse operation;
- before a known interruption or context compaction.

A checkpoint should make the next action safe, not merely summarize prose. Preserve at least the current state version, last completed action, open/stale/blocked items, relevant artifact references, and `next_safe_action`.

## Resume protocol

Do not resume by merely reading the last paragraph of a conversation.

1. load the latest checkpoint/current-state projection;
2. validate its schema/required fields when machine state exists;
3. confirm referenced artifacts/resources still exist and identify their current versions;
4. re-observe volatile external/runtime state;
5. detect side effects that may already have committed;
6. propagate staleness caused by changes since checkpoint;
7. resolve conflicts before writing over newer state;
8. reconnect the next action to the original acceptance conditions and latest user steering;
9. resume from the next safe action.

### Resume across workflow or runtime revisions

A checkpoint describes the environment at the time it was written, not the environment now. Before continuing material work, compare the recorded workflow version, policy/semantic-contract identity, and repository revision (when repository content matters) with the currently loaded workflow and workspace. Re-check the actual host surface, tools/connectors, permissions, and external versions that could change the next action or the validity of prior evidence. Record only the identifiers and capability facts that matter; an omitted or unreadable value is unknown, not “unchanged.”

A mismatch does not make every prior result stale. Re-evaluate only routes, tests, claims, and artifacts that depend on the changed workflow, policy, code revision, capability, or source; preserve independent verified work. Do not carry forward a prior tool-use or test-success claim unless current-run evidence still supports it. If the current environment cannot be inspected, state that boundary and use a safe supported fallback or keep the dependent step blocked. A schema can check that a checkpoint contains version fields; only a trusted host can compare them with the actual current environment.

### When a referenced file or resource cannot be found

Do not treat a stale path, empty listing, or failed lookup as proof that the material never existed or is gone. Search the accessible workspace and relevant file/index/manifest by its stable ID, known name, type, content cues, and recorded version; inspect plausible candidates before choosing one. If multiple versions match, compare their contents, provenance, timestamps, and task state rather than trusting the filename alone. Do not silently substitute an older artifact, recreate a possibly current file, or claim a full search when access or results are partial. If no candidate is available after the relevant authorized search, preserve the missing-reference state, describe the searched scope/limitation, and ask for the smallest user-supplied artifact or locator only if the task cannot proceed without it.

### Resume focus check

After an interruption, handoff, merge, or checkpoint, re-read the root objective, current acceptance conditions, latest correction, completed work, and remaining obligations. For the next action, name the open requirement or answer-bearing uncertainty it advances. If it serves neither, it is probably scope drift: defer or discard it, while preserving any genuinely independent requested work. Reconnect useful branch results to the root answer, keep unresolved dependencies visible, and do not restart completed or unaffected work. This is a brief alignment check, not a new planning phase or a reason to repeat the entire investigation. Human interruption research can motivate concise resumption cues, but it is not direct evidence that a particular AI-agent checkpoint design improves model performance. Mark, Gudith & Klocke (2008), [“The Cost of Interrupted Work: More Speed and Stress”](https://ics.uci.edu/~gmark/chi08-mark.pdf), reports a controlled study of interrupted office tasks; applying its lesson to agent continuity is an engineering analogy, not a measured AI effect.

If the runtime cannot actually persist files or inspect external state, state the limitation and fall back to the strongest supported semantic checkpoint.

## Idempotency for side effects

A retry after interruption may repeat an action. For material side effects, use the target system's idempotency/version mechanism when available, or track a logical operation identity such as:

`operation_id | idempotency_key | attempt | started_at | committed_at | result_ref`

Before repeating a write/send/deploy/create action, check whether the logical operation has already committed. Do not promise exactly-once execution when the runtime/system cannot guarantee it.

## Atomicity and partial failure

Prefer operations that are atomic or safely reversible when feasible. When a multi-step change partially fails:

- record which steps actually committed;
- do not report the entire plan as completed;
- re-observe resulting state;
- decide whether to continue, compensate, roll back, or escalate;
- update downstream state based on what happened, not what was intended.

## Aligned checkpoint validity

A checkpoint is safely resumable only when the states that matter can be reconciled:

`cognitive/problem state ↔ canonical workflow state ↔ relevant workspace/external state`

Restoring an old reasoning context while the environment has already changed can be worse than starting fresh. On resume, compare the checkpoint's assumptions and artifact/operation fingerprints with current observable reality. If alignment cannot be established, preserve the checkpoint as history, mark affected nodes stale, and reconstruct the next safe state instead of pretending exact recovery.

[← Return to root workflow](../SKILL.md)
