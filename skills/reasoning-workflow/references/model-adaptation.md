# Model adaptation for GPT-5.6 and later

**Trigger:** GPT-5.6+, GPT-6 Astra, Codex or another capable agent model is used for substantive reasoning, Deep/Max/Ultra research, tool-rich work, long-context work, or delegated execution.

**Reads:** model/runtime capabilities, available tools, user objective, Task Profile, active route, context pressure, tool results, verification need.

**Updates:** prompting style, planning horizon, context disclosure, delegation strategy, reasoning-effort allocation, compaction behavior, tool-use policy.

**May invalidate:** fixed long plans, repeated instructions, unnecessary reference loading, uniform high reasoning effort, hard-coded agent counts, or verification loops that do not improve the answer.

**Exit:** the workflow is adapted to the actual model/runtime without changing its semantic invariants.

**Related:** [problem framing and effort](problem-framing-and-effort.md), [inquiry and research](inquiry-and-research.md), [runtime and delegation](runtime-and-delegation.md), [synthesis and verification](synthesis-execution-and-verification.md), [ultra research](ultra-research.md).

**Return:** [root workflow](../SKILL.md) → Task Profile / routing.

## Principle

For GPT-5.6 and later, prefer outcome-focused instructions, semantic invariants, and adaptive strategy over rigid step-by-step scripts. Stronger models often perform better when the workflow states what must remain true and what success means, while leaving tactical planning flexible.

Do not remove structure. Move structure from mandatory visible procedure into constraints, state, routing, and verification.


## Strong-model behavior guardrails

For GPT-5.6 and later, keep instructions lean and non-duplicative. Stronger models infer routine gaps well, so specify outcome, hard constraints, epistemic invariants, and success criteria before prescribing tactics. When several Skills or instruction files are visible, eliminate conflicting guidance rather than adding another priority paragraph.

For GPT-6 Astra-class runtimes, account for four tendencies: it may ask for clarification where a reasonable assumption would suffice, it is more sensitive to Skill-file instructions, it may delegate less than desired unless parallel discovery is explicitly useful, and it may over-test small tasks. Bias toward autonomous follow-through when the user's intent is clear, request subagents by purpose rather than count, and keep verification proportional to consequence and uncertainty.

Treat model names as capability examples, not permanent branches. The adapter should survive newer GPT-5.6+ models by testing available capabilities first.

## Planning

Prefer long-horizon understanding with short-horizon execution:

```text
broad objective and success criteria
→ next useful research/action step
→ observe
→ update model
→ re-plan
```

Do not force a complete detailed plan when early evidence may change the frame. Use plans to maintain direction, not to lock the model into stale paths.

## Token and reasoning budget

Depth controls epistemic ambition, not constant per-call compute. Ultra may allow a much larger total token budget, but tokens should be spent where additional reasoning can discover new structure, relationships, explanations, evidence routes, or decisive uncertainty.

Avoid uniform maximum reasoning effort for every phase. Use high effort for framing, mechanism synthesis, causal judgment, adversarial comparison, and final pivotal-claim verification. Use cheaper or lower-effort routes for mechanical extraction, sorting, deduplication, formatting, and repetitive metadata work when the runtime supports it.

## Context and compaction

Use progressive context disclosure. Load the root, current profile, active family, and only the references needed for the current gap. A stronger model does not benefit from duplicated instructions or irrelevant reference bulk.

Preserve useful reasoning when the problem model remains stable. When a major reframe occurs, avoid blindly inheriting old reasoning that may anchor the new pass.

Compact only when context is becoming noisy, obsolete branches accumulate, or the problem model has stabilized after broad exploration. Preserve current problem model, pivotal claims, live hypotheses, decisive evidence, contradictions, bounded unknowns, retired routes, and next high-value gap. Drop duplicate source text, stale branches, same-provenance repetition, and process noise.

## Tool and programmatic work

Use model tokens for epistemic work. Use deterministic computation and tools for mechanical work: filtering, aggregation, sorting, deduplication, hash checking, test execution, metadata extraction, and reproducible calculations.

If the task provides many documents or records, do not push all raw material into the model context by default. Use tools to reduce them to candidate evidence units, then spend reasoning budget on interpretation and judgment.

## Delegation

When the runtime supports subagents, use them for separable work that improves coverage, speed, or independence: distinct framings, evidence ecosystems, jurisdictions/languages, reproduction tasks, adversarial search, or specialist methods.

Do not hard-code an agent count. Do not let subagents vote on truth. Branches return evidence, uncertainty, counterevidence, failed routes, and materiality to the parent. Root synthesis reconciles evidence and commits canonical conclusions.

If subagents are unavailable, emulate distinct passes serially when the benefit justifies the cost.

## Compatibility floor

Target GPT-5.6 and later without creating version-branch sprawl. Adapt to observed capabilities rather than named models where possible:

```text
multi-agent available?        → parallel independent discovery when useful
persisted reasoning available? → preserve stable reasoning; reset after major reframe
dynamic effort available?      → raise/lower compute by phase
programmatic tools available?  → move mechanical work out of model context
weak instruction following?    → use more procedural scaffolding
strong instruction following?  → reduce repetition and resolve conflicts
```

The semantic workflow remains the same. Only the strategy and compute allocation change.

## Scaffolding elasticity

Workflow structure is itself an adaptive resource. Use more procedural scaffolding only when the model/runtime is likely to miss required transitions, lose state, or violate important invariants. Use less when a stronger model reliably infers routine steps and extra instructions cause over-planning, duplicated work, or instruction conflict.

Adjust locally rather than creating model-specific forks:

```text
missed obligation        → add local scaffold / explicit success condition
over-planning            → remove step detail; keep invariant and outcome
context overload         → reduce references and examples
weak delegation          → state the purpose/independence condition more clearly
unnecessary delegation   → tighten materiality threshold
repeated verification    → narrow checks to pivotal claims / expensive failure modes
```

Do not infer that a newer model always needs less structure. Observe adherence and task performance; tune only the part that is failing.

[← Return to root workflow](../SKILL.md)
