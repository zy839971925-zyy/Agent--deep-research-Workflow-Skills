# Reasoning Workflow 3.0.1 — Modular edition

The Modular edition splits the six workflow Families into independently installable instruction-only Agent Skills. Use it when the host already handles skill discovery/routing well, or when a task needs only a focused subset. The shared research method is versioned with Portable 3.0.1; Modular is not six complete replacements for the governing Portable Skill.

- `reasoning-core` — framing, representation, decomposition, relationships, hypotheses, interpretation
- `deep-research` — problem-driven research, retrieval, evidence/provenance, freshness, comparative synthesis, Ultra research
- `decision-analysis` — option completeness, trade-offs, preferences, robustness, recommendation
- `execution-control` — authorized execution, durable state, delegation, checkpoint/recovery
- `audit-verification` — verification, independent review, evaluator validity, effectiveness
- `workflow-learning` — maintenance-plane CAPA and evidence-gated learning

Each Skill contains its Family instructions and only the references it owns. The standalone Deep Research Skill includes its information-target navigation and research-mode references; Reasoning Core includes the clarification gate. Shared methods are mirrored where needed; the Python router, schemas, runtime helpers, and cross-Family state remain in Portable.

## Host installation

| Host | Suggested installation |
| --- | --- |
| Codex CLI / IDE | Place each selected full Skill folder under the recognized `.agents/skills/<skill-name>/` path. |
| Claude Code | Place each selected full Skill folder under `.claude/skills/<skill-name>/`; follow current activation rules. |
| ChatGPT, Claude app, Grok chat | Use native Skills if the actual product surface exposes them; otherwise use project/custom instructions and supply only needed references. |

See the canonical [host profiles](../skills/reasoning-workflow/references/harness-profiles.md) for account/configuration limits, serial Ultra behavior, and UI fallbacks. Load only currently exposed tools; serial research remains possible in ordinary chat. The [research-mode guide](../skills/reasoning-workflow/references/research-modes-and-methods.md) and [clarification gate](../skills/reasoning-workflow/references/clarification-gate.md) are available as references in their respective Skills. Do not assume a product exposes the canonical Python helpers, agents, search, MCP, Research mode, connectors, or interactive UI.

For the full Light-to-Ultra gate, deterministic routing, cross-Family state, and execution contracts, install the [Portable edition](../skills/reasoning-workflow/).

Install one focused Skill with the open `skills` CLI, for example:

```bash
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills --skill deep-research
```
