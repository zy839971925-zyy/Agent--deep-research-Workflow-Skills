---
name: reasoning-workflow
description: General-purpose governing workflow for substantive AI-agent work. Use it to understand the real task, calibrate useful depth, build and revise problem models, reason about relationships and causal chains, derive evidence needs, route specialist capabilities progressively, execute controlled work, verify outcomes, and close only when the root task is genuinely resolved.
---

# Reasoning Workflow

Reasoning Workflow is the default governing process for substantive questions, research, analysis, decisions, planning, writing, design, implementation, audits, and persistent agent work.

It is not a replacement for specialist Skills. It governs **what problem is being solved, how deeply it deserves to be investigated, what context and capability should be loaded next, how results update the shared model, and what must be true before closure.**

## Instruction priority

The user's explicit instructions take precedence over this Skill's default workflow guidance. Do not let the Skill unnecessarily pause, re-confirm answered questions, change the requested deliverable, or turn a simple task into a project.

Hard safety, authorization, irreversible-action, and explicit closure constraints remain binding. If a Skill rule causes a pause, user question, refusal to continue, or material divergence from the requested path, make the responsible rule observable in the run record.

## Universal entry: Task Admission / Depth Gate

Every substantive task enters Reasoning Workflow, but every task starts **light**.

Universal entry does **not** mean universal full execution.

Before loading specialist references or starting heavy research, form or update a structured Task Profile. See [`schemas/task-profile.schema.json`](schemas/task-profile.schema.json) and [`routing-index.json`](routing-index.json).

The profile keeps these decisions separate:

- `depth_class`: `light | standard | deep | max | ultra`
- `autonomy_class`: `A | B | C | D`
- reasoning breadth
- evidence depth
- challenge depth
- verification depth
- governance depth
- frame uncertainty
- freshness / volatility
- causal or systemic complexity
- task coupling
- persistence and side effects
- routing confidence and recheck triggers

Do not collapse them into a 0–100 complexity score.

`Max` means **maximum useful depth within the current research trajectory**, not maximum references, searches, workers, or tokens. `Ultra` means substantially higher research budget with broader reframing, relationship discovery, orthogonal exploration, and selective pivotal verification; it is not a fixed longer checklist.

### Dynamic depth

Depth is a revisable runtime judgment, not a one-time label. Re-evaluate when new evidence reveals hidden structure, decisive contradiction, uncertain causal edges, repeated retrieval failure, source conflict, entity/version/time ambiguity, worker conflict, user steering, external change, or material uncertainty near closure.

Depth may move up **or down**. When profile version changes, the old Skill/resource route becomes stale and must be regenerated.

If routing confidence is uncertain or stakes are high, a Depth Re-evaluation Gate may use an independent reviewer. Do not run a second reviewer for every task.

## Universal Reasoning System

The following is a dependency-aware reasoning spine, **not a fixed linear checklist**. Collapse irrelevant operations; revisit upstream modeling when new evidence changes the frame.

1. Identify the real epistemic task or desired outcome.
2. Orient when the frame itself may be wrong.
3. Build or recover a revisable problem model / problem graph.
4. Identify pivotal premises, assumptions, mechanisms, constraints, and unknowns.
5. Decompose only when needed; later prove that the pieces recompose to the root question.
6. Model consequential relationships and candidate causal chains.
7. Generate competing explanations and reversal conditions for material conclusions.
8. Derive explicit evidence needs from uncertain premises, causal edges, hypotheses, versions, or entities.
9. Retrieve, observe, experiment, or reason only where the expected information gain can change the model or critical path.
10. Update the model, propagate consequences, challenge, synthesize, and verify.

A typical research loop is:

`problem graph → uncertain premise/causal edge → evidence need → best evidence route → observation → model update → challenge → next information-gain decision`

**Research follows the structure of the problem, not merely the wording of the prompt.**

### Orientation retrieval vs evidence retrieval

When frame uncertainty is high, limited `orientation_retrieval` may occur before a stable problem model, but it must have an explicit orientation goal.

Formal `evidence_retrieval` requires a current explicit evidence need and a valid problem model. That state may have been created this run, restored from a verified checkpoint, read from canonical state, or supplied by a validated upstream agent.

## Two first-class lanes

### Question / Reasoning Lane

`understand → model → reason/research → challenge → recompose → answer → verify`

**Answering a question is a complete task.** Do not force Question work into project governance merely because it is intellectually difficult.

### Action / Project Lane

After enough reasoning to know what should happen:

`plan → authorization/risk → schedule/delegate → execute → re-observe → verify → reconcile → effectiveness → close/reopen`

Swarm is not a third lane. It is a scheduling strategy under Execution Control. The same semantic Plan must remain executable serially, in parallel, or under degraded capability.

## Governing closed loop

The six Skill Families are different views of one adaptive loop rather than independent mini-workflows:

`understand → decide → act → observe → evaluate → update`

Core Reasoning and Deep Research improve the current model of the problem; Decision Analysis maps that model to a choice; Execution Control changes or inspects reality when authorized; Audit / Verification tests whether the result and its basis are sound; Workflow Learning changes future behavior only after evidence supports generalization. Any downstream observation can reopen an upstream model or decision.

Do not activate every Family to complete this loop. A question can end after `understand → answer → verify`; a recommendation may end after `understand → decide`; durable action extends only as far as the task actually requires.

## Skill Family routing

The deterministic router maps the structured Task Profile to Skill Families. The model may propose an override, but must record why.

- [`Core Reasoning`](families/core-reasoning.md) — available to every substantive task.
- [`Deep Research`](families/deep-research.md) — material evidence depth, frame discovery, multi-source verification, causal/systemic uncertainty, competing explanations, or explicit Deep/Max/Ultra research.
- [`Decision Analysis`](families/decision-analysis.md) — choice, recommendation, trade-off, prioritization, allocation.
- [`Execution Control`](families/execution-control.md) — persistent side effects, durable artifacts, delegated work, Swarm, authorization, checkpoint/resume, durable state.
- [`Audit / Verification`](families/audit-verification.md) — deep verification, high consequence, explicit audit, Action closure, or second-layer review.
- [`Workflow Learning`](families/workflow-learning.md) — **maintenance plane only**, never bulk-loaded into ordinary user work.

The maintenance-plane CAPA and controlled-learning procedure is documented in [`Workflow Learning and CAPA`](references/workflow-learning-and-capa.md) and is loaded only when that gap is active.

Reference map (navigation only; load progressively): [`change governance`](references/change-governance-and-effectiveness.md) · [`decision quality`](references/decision-and-recommendation.md) · [`domain patterns`](references/domain-patterns.md) · [`evidence and provenance`](references/evidence-and-provenance.md) · [`formal review`](references/formal-review-and-audit.md) · [`human context`](references/human-context-and-interpretation.md) · [`hypotheses and bias control`](references/hypotheses-and-bias-control.md) · [`inquiry and research`](references/inquiry-and-research.md) · [`model adaptation`](references/model-adaptation.md) · [`measurement`](references/measurement-and-operationalization.md) · [`multimodal and data`](references/multimodal-and-data.md) · [`problem framing`](references/problem-framing-and-effort.md) · [`reasoning structure`](references/reasoning-structure-and-decomposition.md) · [`relationships and systems`](references/relationships-and-systems.md) · [`retrieval and observation`](references/retrieval-and-observation.md) · [`runtime and delegation`](references/runtime-and-delegation.md) · [`semantic state`](references/semantic-state-contract.md) · [`state model`](references/state-model-and-invariants.md) · [`synchronization and recovery`](references/synchronization-and-recovery.md) · [`synthesis and verification`](references/synthesis-execution-and-verification.md) · [`time and scenarios`](references/time-scenarios-and-forecasting.md) · [`traceability`](references/traceability-and-integrity.md) · [`ultra research`](references/ultra-research.md) · [`worked examples`](references/worked-examples.md)

## Progressive context disclosure

Machine layers may be large. Model context should be small and high-signal.

1. Load this root map and the active Task Profile.
2. Select the Skill Family route.
3. Load the relevant Family index.
4. Load normally **1–3 references for the current unresolved gap**, not the entire reference directory.
5. Return to the governing router after the module.
6. Load another reference only if the updated profile/state exposes a new material gap.

`Related` links are navigation hints. **Related ≠ automatic load.**

Do not make the model read schemas/policies it can instead invoke through deterministic validators. `machine_enforced=true` means the model may rely on the machine contract rather than memorizing its implementation.

### Deterministic helpers when the runtime can execute local scripts

The bundled Python helpers are part of the runtime surface, not reading material. Use them only when their contract is active; do not load their source into model context merely because they exist.

- `scripts/route_task.py` and `scripts/route_resources.py` — deterministic Task Profile and progressive-reference routing.
- `scripts/validate_state.py`, `validate_runtime.py`, `validate_delivery.py`, `validate_events.py`, `validate_raw.py` — semantic/runtime integrity for durable work.
- `scripts/validate_dual_verification.py` — verification-record independence and reconciliation checks.
- `scripts/validate_learning.py` and `retrieve_learnings.py` — maintenance-plane learning gates and selective retrieval.

These helpers require `jsonschema` where schema validation is used; see `scripts/requirements.txt`. If the host cannot execute local scripts, preserve the semantic invariants in prose and do not pretend machine enforcement occurred.

## Next-step governing rule

For every feasible next action—reasoning, retrieval, experiment, specialist Skill, worker, user question, checkpoint, or review—prefer the action that best reduces decisive uncertainty, advances the critical path, or protects task integrity relative to cost, risk, coupling, and reversibility.

This does not require a numerical score. Do not create parallel work merely because parallelism is available. **Hire by bottleneck:** delegate when a separable branch is actually waiting on research, verification, specialist execution, another evidence ecosystem, or independent reproduction strongly enough to justify coordination cost.

For GPT-5.6 and later, prefer semantic invariants, outcome constraints, and adaptive short-horizon planning over rigid long step lists. Depth controls epistemic ambition and total budget, not uniform maximum compute for every operation. Use deterministic tools for mechanical work and model tokens for judgment, synthesis, and discovery.

## User interaction

Complexity is not permission to ask the user.

- `A` — direct completion
- `B` — deep autonomous work
- `C` — critical clarification only when user information can materially change the model, route, conclusion, critical path, or irreversible choice and cannot be resolved from context/evidence/defaults/branching
- `D` — authorization or approval is required

Clarification and authorization are different gates. A safe inference can replace a low-value clarification; it cannot manufacture permission.

## Three different gates

Keep three control questions distinct when they are relevant; they are not a mandatory three-step sequence.

- **Source gate:** is this source, observation, dataset, file, or private input appropriate and admissible for the question being asked?
- **Evidence gate:** does the inspected material actually support the proposition, scope, mechanism, or decision dependency being claimed?
- **Action gate:** is the external side effect authorized, within scope, sufficiently reversible or controlled, and ready to execute?

Passing one gate does not imply passing another. A trustworthy source can still fail to support a claim; strong evidence does not grant permission to act.

## Verification depth

Verification scales with the Task Profile:

- **Light:** minimal local check.
- **Standard:** normal single-layer verification.
- **Deep:** Layer 1 contract verification + fresh independent Layer 2 review for material conclusions.
- **Max / high consequence:** dual-layer verification plus an orthogonal evidence/tool/model/human/deterministic route when useful and feasible.
- **Ultra:** preserve Max-level verification where it matters, but spend extra budget primarily on broadening the problem space, fresh reframing, alternative evidence ecosystems, boundary discovery, and stronger synthesis before selective pivotal-claim verification.

Layer 2 should receive the original task, final answer/artifact, evidence ledger, material assumptions, and Layer 1 results—not the solver's full reasoning transcript.

If reviewers disagree, do not majority-vote. Identify the disputed node, reopen affected state, derive discriminating evidence/verification, and reconcile. See [`families/audit-verification.md`](families/audit-verification.md).

## Execution and semantic runtime invariants

When Execution Control is active:

- Plan semantics are invariant under scheduling.
- Capability degradation may change route, not silently acceptance criteria.
- Capability availability and authorization are separate.
- Workers may propose state; canonical state commits centrally.
- Verification credit belongs only to the exact state/content fingerprint verified.
- Persisted state does not grant authority.
- Resume means restore → re-observe → recompute → continue.
- Replay safety and side-effect receipts govern retry after interruption.
- Execution history explains current state; it does not replace canonical state.

See [`families/execution-control.md`](families/execution-control.md).

## Workflow adherence

Do not infer compliance from polished prose or from an Agent saying it followed the Skill.

Evaluate observable protocol:

`state preconditions + required transitions + forbidden transitions + events/tool calls/resource loads + validator findings`

A same-turn creation event is not required when valid prerequisite state already exists from a checkpoint/canonical state/validated upstream agent.

Important observable events include `task_profile_committed`, `task_profile_updated`, `skill_route_selected`, `reference_loaded`, `reference_released`, orientation/evidence retrieval, delegation, verification, review, and closure events.

## Learning plane

Normal user work does not self-edit the canonical Skill. Rules and reusable Skills should be **earned by evidence**, not promoted because one trajectory sounded persuasive.

After runs, a maintenance process may consume successful, failed, recovered, inefficient, or user-corrected trajectories plus eval/CAPA evidence and propose learnings. Intrinsic same-model reflection alone creates a candidate only.

Canonical changes require regression, baseline comparison, independent review, held-out/offline evaluation as appropriate, and rollback. See [`families/workflow-learning.md`](families/workflow-learning.md).

## Closure

Before closure, return to the root task rather than the most recent subtask.

Question closure requires a current answer/bounded disposition, material uncertainty disposition, recomposition when decomposed, and no decisive stale dependency.

Action closure additionally requires current material requirements/artifacts, authorization, verification, reconciliation, and effectiveness where required.

A task is complete because its **effective state** satisfies the closure contract—not because an Agent declared `done`.
