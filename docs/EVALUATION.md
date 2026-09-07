# Evaluation

## Reproducible checks

From `skills/reasoning-workflow/`:

```sh
python -m pip install -r scripts/requirements.txt
python scripts/validate_skill.py .
python scripts/validate_links.py .
python scripts/validate_workflow.py .
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/build_distributions.py --source . --out-dir ../../dist
python scripts/validate_distribution.py ../../dist/reasoning-workflow-portable.zip ../../dist/reasoning-workflow-modular.zip
```

The current discovered suite passes **58/58 tests**. Structure, links,
workflow metadata, and Portable/Modular shared semantic consistency checks pass.
These deterministic checks cover routing, context disclosure, adherence,
learning, research contracts, runtime, recovery, and delivery.

## Behavioral evaluation boundaries

Deterministic checks do not establish real-agent performance. These remain unvalidated:

- real-model Task Profile classification accuracy;
- Skill trigger and Family/reference routing precision and recall across models;
- matched Deep Research quality non-inferiority;
- actual token, latency, and tool-call savings;
- measured dual-review error reduction;
- long-horizon learning effectiveness and harmful-memory rates;
- complete external Deep Research benchmark execution;
- behavioral equivalence across runtimes.

Evaluation definitions: [evals/deep-research](../skills/reasoning-workflow/evals/deep-research/).
Future comparisons must freeze baselines and acceptance margins before inspecting results.
Efficiency gains cannot excuse material loss in question fidelity, evidence quality,
causal coverage, or synthesis.
