# Runtime and delegation

**Trigger:** Tool-rich, cross-surface, private, delegated, sandboxed, capability-limited, or long-running tasks.

**Reads:** objective, required evidence/actions, available tools/surfaces, authorization, private-data constraints, current state.

**Updates:** capability plan, delegation branches, private/public routing, failure/blocked state.

**May invalidate:** plans that assumed unavailable capability or unauthorized access.

**Exit:** the task uses only capabilities actually available and authorized; delegated work has been integrated into the root state.

**Related:** [state model and invariants](state-model-and-invariants.md), [inquiry and research](inquiry-and-research.md), [evidence and provenance](evidence-and-provenance.md), [synchronization and recovery](synchronization-and-recovery.md).

**Return:** [root workflow](../SKILL.md) → Action / Project Lane or Inquiry loop.

## Capability preflight

Distinguish model capability, product/harness capability, connected tools, storage persistence, and user authorization. Web, files, private connectors, local repository, shell/code execution, media inspection, computer use, subagents, scheduling, and durable storage can vary by environment.

Do not assume a capability because another ChatGPT/Codex surface supports it. If the most direct surface is unavailable, use the best available route and narrow confidence or deliverable where necessary.

An attached ZIP supplies instructions but does not automatically install a persistent Skill or grant external tools.

## Private evidence routing

Classify material evidence where useful as public, user-provided, workspace/local-private, or confidential/restricted. Access for analysis does not imply authorization to publish or send the same content to a public search/tool.

When private evidence must be combined with public research, minimize disclosure. Generalize public queries, remove unnecessary identifiers, or perform joins locally when possible. Preserve the source visibility in provenance state.

## Delegation

Delegate only separable work that benefits from parallelism, independent discovery, another language/jurisdiction, reproduction, specialist method, or adversarial search. Root synthesis retains definitions, provenance deduplication, cross-branch conflict resolution, and final judgment.

### Hire by bottleneck

Do not start from an agent count. Start from the current bottleneck. A worker is justified when the parent is materially waiting on a branch such as research, verification, specialist execution, independent reproduction, or repeated rework that a scoped owner can resolve more effectively than the coordinator.

If the handoff cost, shared-state coupling, or reconciliation burden is likely to exceed the benefit, keep the work serial. More agents can reduce diversity or slow convergence when they share the same assumptions and evidence.

### Worker contract before handoff

Give a worker a compact contract, not an ambiguous role persona:

`job | allowed inputs/sources | judgment boundary | acceptance criteria | output contract | forbidden actions | uncertainty to preserve`

The contract should make clear what the worker owns and what remains a controller decision. Do not grant canonical-state authority, publishing authority, deletion authority, spending authority, or other external permission merely because the worker owns a branch.

### Handoff packet

Return state-bearing evidence rather than a long conversational transcript. A useful handoff packet is:

`task | status | material output | evidence/source locators | decisions made within scope | unresolved uncertainty | failed routes | state/items affected | next owner or next safe action`

When a shared workspace exists, use it as an internal bus for durable evidence, drafts, decisions, and handoffs; chat summaries are views of that state, not the authoritative state itself. This reduces copy-paste drift between workers.

Do not ask subagents to write interdependent chapters in parallel when shared definitions or evidence state would drift. Multiple agents are not independent empirical sources.

## Specialist Skills

This Skill is the process/orchestration layer. Use specialist Skills when they own a better domain method or artifact capability. Preserve one governing objective and completion state while allowing the specialist to control implementation details.

Do not duplicate or override specialist instructions without a task-relevant reason. If two Skills conflict, higher-priority user/system instructions govern; otherwise prefer explicit ownership boundaries and reconcile outputs through the canonical state.

## GPT-5.6+ runtime adaptation

For GPT-5.6 and later, adapt to actual runtime capabilities rather than hard-coding model versions. Use persisted reasoning when stable, compact when context becomes noisy, delegate when independent exploration or specialist work improves coverage, and move deterministic filtering or aggregation into code where available. Do not force fixed agent counts or uniform maximum reasoning effort across mechanical phases.

## Failures, triggers, and retries

When the runtime supports event-driven triggers, prefer a narrow event or state-change signal over constant polling. Poll only when no reliable trigger exists and the expected information value justifies the cost.

Retry only when a parameter change, alternate tool/surface, transient failure, new evidence, or different route creates a concrete prospect of success. Do not repeat unchanged failures. Record the consequence for the user outcome and state, not noisy tool logs.

When a capability is unavailable, leave a bounded gap or blocked item instead of inventing completion.

## Diagnose the failure before replanning

For material failure, distinguish where the chain broke before changing the plan:

`goal understanding → observation → interpretation → state carry → plan → tool selection → tool execution → dependency resolution → replan → verification → closure`

A later capability should not be blamed when the required state was never observed, was misread, or was lost upstream. Record the smallest useful failure class; do not create a heavy ontology for routine errors.

## Replan only at the affected level

Not every failed action invalidates the plan.

- **local execution failure:** repair parameters, retry with changed conditions, or use an alternate tool;
- **plan assumption invalidated:** reopen and replan the affected branch;
- **objective, constraint, or frame changed:** rebuild the relevant higher-level plan/model.

Trigger broad replanning from model-changing evidence, not from every transient tool error. Preserve unaffected plan semantics and completed work.

[← Return to root workflow](../SKILL.md)
