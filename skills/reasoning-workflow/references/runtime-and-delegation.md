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

A branch packet should be compact:

`branch question | material findings | evidence locators | provenance | counterevidence | uncertainty | failed routes | new leads | state/items affected | materiality to parent`

Do not ask subagents to write interdependent chapters in parallel when shared definitions or evidence state would drift. Multiple agents are not independent empirical sources.

## Specialist Skills

This Skill is the process/orchestration layer. Use specialist Skills when they own a better domain method or artifact capability. Preserve one governing objective and completion state while allowing the specialist to control implementation details.

Do not duplicate or override specialist instructions without a task-relevant reason. If two Skills conflict, higher-priority user/system instructions govern; otherwise prefer explicit ownership boundaries and reconcile outputs through the canonical state.

## Failures and retries

Retry only when a parameter change, alternate tool/surface, transient failure, new evidence, or different route creates a concrete prospect of success. Do not repeat unchanged failures. Record the consequence for the user outcome and state, not noisy tool logs.

When a capability is unavailable, leave a bounded gap or blocked item instead of inventing completion.

[← Return to root workflow](../SKILL.md)
