# Reasoning Workflow — Modular Edition

The Modular edition exposes the six Reasoning Workflow Families as independently installable Agent Skills. Use it when the host already handles Skill discovery/routing well, or when you want only a focused subset of the workflow.

- `reasoning-core` — framing, representation, decomposition, relationships, hypotheses, interpretation
- `deep-research` — problem-driven research, retrieval, evidence/provenance, forecasting, Ultra research
- `decision-analysis` — option completeness, trade-offs, preferences, robustness, recommendation
- `execution-control` — authorized execution, durable state, delegation, checkpoint/recovery
- `audit-verification` — verification, independent review, evaluator validity, effectiveness
- `workflow-learning` — maintenance-plane CAPA and evidence-gated learning

Each Skill contains its own Family instructions and progressively loaded references. The deterministic router, schemas, state validators, and other Python runtime helpers live only in the Portable/canonical edition instead of being duplicated across all six Skills.

For the strongest default behavior, use Portable at [`../skills/reasoning-workflow/`](../skills/reasoning-workflow/). Portable owns the universal Light → Ultra depth gate, deterministic routing, cross-Family state, and full governing loop.

To install only one Modular Skill with the open `skills` CLI, select it by name, for example:

```bash
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills --skill deep-research
```
