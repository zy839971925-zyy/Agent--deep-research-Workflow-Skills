# Reasoning Workflow 2.1.1

A lightweight general-purpose workflow with a strong Deep Research path.

Start with [SKILL.md](SKILL.md). It is the short model-facing entry, not a requirement to load the full package. Simple questions can be answered directly. Depth, autonomy, persistence and risk are separate choices; more thinking never expands permission.

- [2.1.1 中文说明](docs/RELEASE_2.1.1.zh-CN.md): 修复、功能完善、迁移和实测边界。
- [Task strategies](references/task-strategies.md): research, artifacts/code, coordination, continuity and external actions; combine only the strategies needed now.
- [Usage and migration](UPGRADE.md): setup, compatibility changes, commands and host requirements.
- [Host adapter](references/host-adapter.md): trusted submission context, recovery, review-to-delivery and learning evidence interfaces.
- [Change log](CHANGELOG.md): implemented fixes and limits.
- [Test report](TEST_REPORT.md): actual deterministic regression results, not model performance claims.

Run the local safe synthetic suite:

```sh
uv run --no-project --with jsonschema==4.23.0 python tests/run_all.py
```

It uses temporary local files and executes the shipped Python functions/CLIs. It makes no external account or business calls. This release does not replace the original directory, install third-party skills, connect accounts or migrate saved state automatically. Python dependencies use an isolated environment.

Use `schemas/` and recorded state only when a task actually needs them. `families/` and the detailed existing `references/` are on-demand material, not compulsory phases. `meta/README*.md` preserves the historical GitHub project intent, not the current install entry. `docs/LEGACY_ENTRY.md` is a historical entry for migration comparison, not the active instruction file.

An executable checker can validate structure, bindings, versions and bytes. It cannot certify semantic truth, model compliance, authentic external authorization or real-world success. The supplied host adapter deliberately distinguishes those responsibilities.
