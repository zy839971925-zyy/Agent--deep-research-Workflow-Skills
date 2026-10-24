# Clarification gate

**Trigger:** A material ambiguity or missing input may change the answer, research route, or recommendation; especially when the user asks the agent to clarify before proceeding.

**Reads:** current request and relevant conversation/task state; accessible supplied materials and repository evidence; verifiable external facts; safe derivations and reversible paths.

**Updates:** resolved assumptions, remaining user-owned uncertainty, the smallest useful question, or a conditional result that can proceed without an interruption.

**May invalidate:** premature questions, unsupported assumptions, over-broad interviews, and work blocked by facts the agent could have checked itself.

**Return:** [Problem framing and effort](problem-framing-and-effort.md) → [Reasoning Core](../SKILL.md).

A question is not a substitute for investigation. Before asking, run this short gate; no hidden chain-of-thought disclosure is required.

## Resolve the uncertainty at its source

1. **Name the dependency.** What concrete answer or recommendation could change depending on the missing information? If no material result changes, infer a routine detail, state a bounded assumption if useful, or proceed.
2. **Route it to the source that can resolve it.**
   - **Conversation/task state:** reread the relevant user statement, correction, saved requirement, or checkpoint; prefer the latest explicit instruction.
   - **Supplied material/project state:** inspect accessible files, repository, code, configuration, tests, and relevant history/index before asking the user to restate facts.
   - **Current host/tool capability:** inspect the actual runtime's exposed tools, permissions, and source access. Product documentation describes possible features, not whether they are available in this session. Record material capability as `available here`, `unavailable here`, or `not verified`; never claim to have used a feature from a skill instruction alone.
   - **External-world fact:** check a current authoritative source or the relevant authorized read tool. Do not ask the user for public facts the agent can look up.
   - **Derivable or routine:** calculate, or use only a genuinely conventional, clearly labelled reversible assumption/range/conditional branch.
   - **User-owned:** intent, values, priorities, private circumstances, desired trade-off, unavailable personal input, or a choice only the user can make. Do not infer these from public facts.
3. **Try a safe path.** Check whether a short, dependency-relevant investigation, calculation, bounded comparison, reversible preparation, or conditional answer can preserve progress without pretending the unknown is known. Do not use this step to take an action beyond authority.
4. **Challenge the need to interrupt.** Ask yourself operationally: would plausible answers materially change the result or a consequential action? Have you checked only the context, artifacts, capability, external fact, or derivation relevant to this dependency and likely to change the answer? Do not search every source category by default. Can independent work continue while the answer is pending? If the remaining decision is truly user-owned and cannot be safely conditioned, ask only the smallest input that resolves it. Otherwise proceed with an explicit assumption or conditional result.

## Preserve material uncertainty without creating a second tracker

For a consequential open dependency, keep its current interpretation(s), resolver, evidence or assumption, status (`verified`, `assumed`, `open`, `conflicted`, or `deferred`), and what observation would change that status in the existing task state. Track only material items. A correction or new evidence invalidates the conclusions that depend on it, not unrelated finished work. An answer to a clarification settles that choice only; it does not grant authority for a separate action.

## Ask narrowly, then continue

- Ask neutral, concrete questions. Explain the specific decision they change; avoid asking for a full brief when one constraint is pivotal.
- Bundle questions only when each is genuinely required for the same next step and the user can answer them together. Otherwise ask the highest-value question first, then stop when sufficient.
- Use an adaptive interview (“Grill Me”) only when requested or clearly useful for a genuinely open-ended objective. Ask one high-leverage question at a time, update the working frame after each answer, and stop once the result is decision-ready. Do not turn routine tasks into an interview.
- If useful independent work remains, complete it before or while waiting. Save the current state and exact dependency for continuation where the task is persistent.
- Clarification is not consent. Never infer authorization for sending, spending, signing, deleting, publishing, committing, or another consequential action from an answer to a scope question.

A short final check:

`What changes if the answer differs? → Who owns that fact? → Can context, project evidence, external research, or safe derivation resolve it? → If not, what is the one smallest user-only input?`

## Limits

This gate does not require endless searches or certainty. Stop when remaining uncertainty is immaterial, cannot be reduced through authorized sources, or can be represented honestly as a condition. If an essential external source is inaccessible, state the actual access limit; do not mislabel it as missing user input. Follow higher-priority safety, privacy, and authorization rules.
