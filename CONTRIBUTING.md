# Contributing

Contributions should preserve the project's core distinction between **epistemic quality** and **runtime integrity**.

Before adding new methodology, ask whether the behavior can already be expressed through the existing Question / Reasoning Lane, Action / Project Lane, references, semantic contract, or validators. The project favors semantic enforcement over adding more process prose.

A useful change should normally include one or more of:

- a concrete failure mode;
- a schema or semantic-contract change;
- a validator rule;
- a regression specification or validator unit test;
- a documentation update explaining changed behavior.

Do not record private chain-of-thought in tests or behavioral traces. Prefer observable events, typed state, findings, artifacts, and final outputs.

Before proposing a change, run:

```bash
cd skills/reasoning-workflow
python -m pip install -r scripts/requirements.txt
python scripts/validate_skill.py .
python scripts/validate_links.py .
python scripts/validate_workflow.py .
python -m unittest discover -s tests -p 'test_*.py' -v
```
