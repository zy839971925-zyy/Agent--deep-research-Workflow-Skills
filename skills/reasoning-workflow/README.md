# Reasoning Workflow 3.0.1 — Portable edition

A general-purpose reasoning and execution workflow with a strong Deep Research path. Start with [SKILL.md](SKILL.md); load references only for active gaps.

The Portable edition includes the governing entry, six on-demand Families, references, schemas, optional Python helpers, synthetic tests, migration notes, and host-adaptation guidance. Keep the complete directory together so relative links and helper paths resolve.

- [3.0.1 release notes](docs/RELEASE_3.0.1.md): evaluation-fixture updates and what they do—and do not—validate.
- [Research modes and methods](references/research-modes-and-methods.md): real-world, pre-build architecture, and hybrid investigations.
- [Clarification gate](references/clarification-gate.md): check context and evidence before asking for user-owned details.
- [V3 functional scenarios](evals/v3-functional-scenarios.md): observable evaluation protocol; not model-evaluated.
- [Host profiles](references/harness-profiles.md): Codex, Claude Code, ChatGPT, Claude app chat, and Grok installation/fallback boundaries.
- [Model adaptation](references/model-adaptation.md): capability-first strategy for GPT-6+ and current frontier models; no behavior guarantees from model names.
- [Comparative synthesis](references/comparative-synthesis.md): optional method for studies, model evaluations, and benchmarks.
- [Usage and migration](UPGRADE.md): setup, compatibility, and host requirements.
- [Host adapter contract](references/host-adapter.md): trusted execution, authorization, evidence admission, and recovery responsibilities.
- [Change log](CHANGELOG.md) · [Test report](TEST_REPORT.md): version history and actual deterministic checks, not model-compliance claims.

The [Modular edition](../../modular/README.md) separates six instruction-only Families for hosts with their own routing. It omits Portable’s deterministic routing/runtime helpers and cross-Family state.

Run non-mutating package regression tests from the repository root:

```sh
python skills/reasoning-workflow/tests/run_all.py
```

Optional output goes only to an explicitly selected disposable directory via `--output-dir`. Static checks and deterministic release-building are described in the release notes. No Skill installation connects accounts, enables tools, or grants authority.

Historical project-intent material in `meta/` and `docs/LEGACY_ENTRY.md` is retained for provenance; it is not the active entry or current host-install guide.
