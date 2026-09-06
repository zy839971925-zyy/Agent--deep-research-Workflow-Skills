# Change governance and effectiveness

**Trigger:** A task creates/modifies persistent consequential state, especially when changes affect people, systems, interfaces, compliance, or later outcomes.

**Reads:** baseline, proposed delta, requirements, evidence, risks, authorization, current state, acceptance/effectiveness needs.

**Updates:** change record, risk review ledger, controls/actions, readiness, implementation state, V&V, calibration, effectiveness/closure.

**May invalidate:** plans, artifacts, approvals, tests, closure if implementation deviates or effectiveness fails.

**Exit:** change is correctly left proposed/blocked/implemented/verified/effectiveness-pending/effective/reopened with evidence appropriate to its state.

**Related:** [state model and invariants](state-model-and-invariants.md), [traceability and integrity](traceability-and-integrity.md), [synchronization and recovery](synchronization-and-recovery.md).

**Return:** [root workflow](../SKILL.md) → Action / Project Lane.

Use when work creates or modifies persistent state: a file or controlled artifact, code/configuration, workflow, process, policy, data pipeline, operating practice, plan being put into effect, or other consequential implementation. The purpose is closed-loop control, not paperwork.

## Scale the lane

Governance depth should match consequence, persistence, reversibility, coupling, number of affected people, regulatory/security/safety exposure, and uncertainty.

- **Minimal:** small reversible edit; preserve before/after or diff and verify the requested result.
- **Controlled:** meaningful persistent change; use a compact change record, impact sweep, acceptance criteria, rollback, and post-change check.
- **Formal:** high-consequence, cross-system, regulated, hard-to-reverse, or operational change; use durable records, qualified cross-functional review, authorization/readiness gates, staged rollout where feasible, and scheduled effectiveness review.

Do not force formal change control onto analysis-only tasks, casual writing, or throwaway experiments unless the output itself is being adopted as a controlled work product.

## Establish a baseline and change record before implementation

For controlled/formal changes maintain a traceable, visually scannable record. Use the project's existing change-control format when one exists; otherwise a compact Markdown/table record is sufficient.

Useful fields:

`change id/status | objective/problem | baseline/version | proposed delta | rationale/technical basis | affected items/interfaces/stakeholders | owner/authority | assumptions/dependencies | risks/unknowns | actions/controls | acceptance/verification criteria | outcome/process/balancing measures | rollout/rollback/temporary expiry | implementation evidence | deviations | validation result | effectiveness due/result | residual risk | closure/reopen decision`

Prefer a before/after diff, dependency/impact map, or risk/action table when it makes the change easier to audit. Preserve the link from requirement/problem → decision → change → test/evidence → result.

A useful status model is:

`proposed → assessed → approved/ready → implementing → implemented → verified/validated → effectiveness pending → effective/closed`

A failed check moves the record back to investigation/assessment rather than being cosmetically closed.

## Systematic impact/risk sweep

For material changes, scan the relevant risk universe before deciding that an area is irrelevant. Do not omit a category solely because initial intuition says it is unrelated. Mark each family as `relevant`, `N/A — reason`, or `unknown — follow-up`.

Adapt the families to the domain, but normally consider:

- objective, requirements, scope, assumptions, and success criteria;
- functional behavior, quality, performance, reliability, compatibility, interfaces, dependencies, and data integrity;
- safety, security, privacy, legal/regulatory/compliance, and abuse/misuse where applicable;
- human factors, accessibility, usability, operator workload, training, handoffs, incentives, and actual-versus-written practice;
- operations, maintenance, support, observability, incident response, capacity, resources, schedule, and cost;
- affected users/stakeholders, communication, reputation, equity/distributional effects where material;
- reversibility, rollback, temporary-change expiry, migration, version coexistence, and recovery from partial failure;
- upstream/downstream and second-order effects, feedback, common-cause failures, correlated dependencies, and new failure modes;
- measurement quality: whether the proposed controls and success criteria can actually detect failure and improvement.

Use structured techniques only when they fit the problem: FMEA, HAZOP/SWIFT, fault tree, threat modeling, premortem, scenario analysis, dependency analysis, checklists, or experiments. A checklist is a coverage device, not proof that risk is understood.

## Team and review design

No single reviewer possesses every relevant perspective. For consequential changes, use actual cross-functional or independent review when available.

Useful coverage can include:

- someone who owns or deeply knows the affected process/system;
- someone responsible for implementation;
- an operator/end user or affected stakeholder who knows how work is actually performed;
- someone competent in the risk/review method;
- security/privacy/safety/legal/data/domain specialists when the sweep identifies those exposures;
- a fresh-eye reviewer for changes where framing lock-in is a meaningful risk.

The team size should follow the problem, not a quota. If actual independent reviewers or subagents are unavailable, perform a structured multi-perspective sweep but label it as non-independent; do not manufacture “team approval.”

Resolve review findings explicitly: `accepted/actioned | rejected with rationale | deferred with owner/date | unresolved/blocking`.

### Merge multi-reviewer findings deliberately

When several reviewers produce overlapping or conflicting findings, merge them into one risk review ledger rather than concatenating comments.

A useful record is:

`finding/risk id | description | causal mechanism | affected requirement/item | reviewers/origins | risk family | evidence | severity/priority | disagreement | disposition | owner | blocker?`

Merge obvious duplicates only when they describe the same underlying failure mechanism and affected state. Preserve distinct causes that merely share a symptom. Record dissent when qualified reviewers disagree; do not erase disagreement through majority vote. After merge, re-run the risk-family coverage sweep to identify categories no reviewer actually assessed. The governing owner/authority resolves blockers or accepts residual risk according to the task context.

## Turn assessment into controls and measurable outcomes

A risk finding is incomplete until it changes the plan, acceptance decision, or monitoring.

For each material action capture:

`risk/finding | preventive control | detection/monitoring | owner | evidence/output | due/trigger | verification method | residual risk | approval/disposition`

Define measures before implementation when possible:

- **Outcome measure:** did the intended result improve?
- **Process/adherence measure:** is the new way of working actually being followed reliably?
- **Balancing measure:** did improvement in one area create a new problem elsewhere?

Add thresholds, baseline, expected direction/magnitude when meaningful, data source, observation window, and stop/rollback triggers. Do not retrofit success criteria after seeing the result merely to declare success.

## Readiness gate before implementation or release

For controlled/formal changes, verify readiness before crossing the implementation boundary:

- approved scope and current baseline are known;
- critical risk actions required before release are complete;
- changed procedures, documentation, configurations, tests, and training are ready where applicable;
- monitoring and failure detection are in place;
- rollback/recovery or temporary-change expiry is workable when relevant;
- acceptance and effectiveness criteria are defined;
- authorization exists for the action the agent is about to perform.

A safety-, security-, privacy-, or integrity-critical unresolved item is a gate, not a caveat to hide after implementation.

## Implement with controlled exposure

Prefer small, staged, observable, reversible changes when this reduces risk without defeating the objective. For broad releases, progressive exposure, pilots, canaries, feature flags, or limited-scope trials can provide earlier evidence and smaller blast radius.

Record what was actually changed and any deviation from the approved plan. If implementation reveals hidden complexity that materially changes risk, stop or escalate governance before expanding scope.

Temporary changes need an owner, expiry/review date, and explicit restore/permanent-adoption decision; do not let “temporary” become an unreviewed permanent baseline.

## Separate verification, validation, and effectiveness

### Verification — did we do the change right?

Use inspection, tests, analysis, demonstration, diff/baseline comparison, or other objective evidence to confirm implementation matches the approved change and requirements.

### Validation — did we make the right change for the intended use?

Check the changed artifact/system/process in the intended context against the user's or stakeholder's real need, not only the specification.

### Calibration — what did reality teach us?

Compare predicted risks, mechanisms, thresholds, and outcomes with observations. Update assumptions, monitoring thresholds, test coverage, or the model when reality differs.

For material learning, preserve a compact calibration record:

`prediction/assumption | expected observation | actual observation | deviation | plausible reason | model update | control/process update | regression test/check added?`

Calibration is not complete if the new insight exists only in prose and cannot influence the next similar task. Feed durable lessons into the relevant state, control, checklist, test, or reference when the environment and authorization support it.

### Effectiveness — did the change work and stay working?

After enough time or exposure to observe the effect, check separately:

1. **implementation fidelity:** is the work/process actually being performed as designed?
2. **outcome:** did the intended result occur and persist?
3. **balancing/unintended effects:** did new harms, costs, failure modes, or risk migration appear?
4. **residual risk:** is remaining risk acceptable under the original objective?

Outcome improvement alone does not prove the change caused it. If causal attribution matters, use a stronger comparison, time-series, controlled rollout, counterfactual, or other justified design when feasible.

## Close, monitor, or reopen

Do not close a material change merely because code was merged, a document was published, training was delivered, or an action item was marked complete.

Close only when the warranted evidence exists that:

- the implemented state matches the controlled record;
- acceptance/validation criteria passed;
- documentation, procedures, ownership, and training are updated where relevant;
- effectiveness criteria passed, or the change remains explicitly `effectiveness pending` with an owner and due checkpoint;
- material unintended effects and residual risks are dispositioned;
- anomalies and deviations are resolved or knowingly accepted by the appropriate authority;
- the new baseline and lessons learned are captured.

If effectiveness fails, reopen the change/problem, revisit the causal model and controls, and decide whether to modify, roll back, replace, or escalate. The effectiveness check is part of the work, not an optional retrospective.

[← Return to root workflow](../SKILL.md)
