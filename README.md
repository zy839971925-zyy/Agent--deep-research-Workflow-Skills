<div align="center">
<img src="skills/reasoning-workflow/assets/icon.svg" width="88" height="88" alt="Reasoning Workflow" />

# Reasoning Workflow

Understand the problem. Choose the next useful move. Verify the outcome.

English · [简体中文](README.zh-CN.md)

[Start here](skills/reasoning-workflow/SKILL.md) · [Download 2.1.1](dist/reasoning-workflow-2.1.1.zip) · [Upgrade notes](skills/reasoning-workflow/docs/RELEASE_2.1.1.zh-CN.md)
</div>

## Purpose

Reasoning Workflow is a general-purpose reasoning and execution framework for AI agents, with Deep Research as a particular strength. It helps a model identify the real outcome, locate the uncertainty or bottleneck that matters, choose an appropriate method, and distinguish a useful intermediate result from completed work.

The aim has not changed: research follows the structure of the problem, not just the wording of the prompt. The next move might be a calculation, a source check, a specialist Skill, an authorized action, a focused question—or simply answering now. More process is not automatically better.

There is no fixed SOP, source quota, Agent roster, or mandatory long plan. Simple tasks stay simple. Detailed references, schemas, persistent state, and delegation are loaded only when they help the current task. Depth never expands permission.

## What it helps with

- Research: framing, competing hypotheses, primary evidence, source/claim fit, missingness, counterexamples, and pivotal verification.
- Decisions: alternatives, constraints, trade-offs, sensitivity, and recommendations that explain when the choice changes.
- Artifacts and code: usable outputs, explicit acceptance conditions, tests, and delivery checks.
- Longer work: dependencies, canonical state, controlled delegation, interruption recovery, and honest partial handoffs.
- External actions: separating preparation, authorization, execution receipts, and outcome verification.

Six on-demand families support these tasks: Core Reasoning, Deep Research, Decision Analysis, Execution Control, Audit & Verification, and Workflow Learning. Learning belongs to an explicit maintenance context; it does not silently rewrite the Skill during ordinary work.

This is not a replacement for a capable model, domain expertise, tools, permissions, or a trusted host. It is not a prompt for revealing hidden chain-of-thought. It does not make arbitrary agents reliable merely by being installed.

## Install the complete Skill

The current canonical edition is [`skills/reasoning-workflow/`](skills/reasoning-workflow/). Its model-facing entry is [`SKILL.md`](skills/reasoning-workflow/SKILL.md).

1. Clone this repository, or download and extract the complete [2.1.1 package](dist/reasoning-workflow-2.1.1.zip).
2. Place the entire `reasoning-workflow` directory in the Skill directory recognized by your host. A typical Codex user installation is `~/.agents/skills/reasoning-workflow/`; use your host's documented location when it differs.
3. Enable/select the Skill through the host. Ask the model to start with `SKILL.md` and read linked material only as needed. Do not paste the whole reference library into every context.
4. Python helpers are optional. To use them, install Python 3.10+ and the dependencies below; the hosted CI uses Python 3.12. Host capabilities and tool authorization must be configured separately.

Do not copy only `SKILL.md`: its references, schemas, scripts, and templates depend on the rest of the directory. Installing it neither connects accounts nor intercepts tool calls.

Example clone and isolated Python setup, from a shell:

```sh
git clone https://github.com/zy839971925-zyy/Agent--deep-research-Workflow-Skills.git
cd Agent--deep-research-Workflow-Skills
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r skills/reasoning-workflow/scripts/requirements.txt
```

The [Modular edition](modular/README.md) remains available for hosts that prefer six focused Skills. Shared reference content is synchronized; the Python routing/runtime helpers live in the canonical edition, not in each modular Skill. Use canonical when you need the complete 2.1.1 behavior.

## Quick start

A normal request needs no JSON profile:

> Use Reasoning Workflow. Compare the practical options for this problem, resolve the uncertainties that could change the recommendation, and give me a usable result. Keep the effort proportionate; do not take external actions without authorization.

For deterministic routing, try the supplied synthetic profile from the repository root:

```sh
python skills/reasoning-workflow/scripts/prepare_task.py \
  skills/reasoning-workflow/tests/fixtures/standard_profile.json

python skills/reasoning-workflow/scripts/prepare_task.py \
  skills/reasoning-workflow/tests/fixtures/standard_profile.json \
  --signal ultra_requested
```

`prepare_task.py` normalizes the profile, constructs the route, selects this phase's references, checks required local files, and exposes deferred gap references. Its expected output includes `status="prepared"`, `task_executed=false`, and `authority_granted=false`. It prepares a task; it does not run a model, read references on the model's behalf, or execute external tools. A simple Light task may select no references.

## Depth, Ultra, and capability limits

Light → Standard → Deep → Max → Ultra adjusts effort to uncertainty, consequence, and the value of further work. Research depth, verification, autonomy, and persistence are separate dimensions—not one global “do more” switch.

Ultra allocates more room for reframing, relationship discovery, alternative explanations, orthogonal evidence routes, boundary analysis, and selective pivotal checks. It does not mean longer answers, fixed numbers of searches, automatic parallelism, or unlimited agents. The router makes the Ultra method reference mandatory even without an `ultra` gap tag; reference budgets expand to fit mandatory controls.

A missing tool, independent reviewer, file, or trusted host integration must be reported as a concrete limit. Continue useful independent work where possible, but do not silently downgrade and claim complete Ultra execution. See [Ultra research](skills/reasoning-workflow/references/ultra-research.md) and [model adaptation](skills/reasoning-workflow/references/model-adaptation.md).

## Execution and partial results

Guidance and local validators are not a running external executor. The optional [harness integration](skills/reasoning-workflow/references/harness-integration.md) must be called by a trusted host to enforce tool boundaries. The [host adapter contract](skills/reasoning-workflow/references/host-adapter.md) describes identity, live authorization, evidence admission, and recovery responsibilities. A worker-supplied JSON label or file hash is not proof of any of those facts.

For incomplete work, a delivery manifest may declare `delivery_kind="partial"`, remaining work, and unresolved obligation references. It must not declare the root task closed or delivery-ready. `computed_partial_ready=true` means an acceptable intermediate handoff, not completion; it does not itself save a checkpoint, schedule follow-up, or retry an external action. Missing material requirements still block complete delivery in Question, Action, and Mixed lanes.

## What changed in 2.1.1

- Review fingerprints track relationship endpoints and transitive dependencies, invalidating stale review credit.
- Material delivery obligations apply across lanes; blocked work cannot masquerade as completed Question work.
- Forbidden parallelism cannot be bypassed by omitting or changing a concurrency-group label; actual ordering matters.
- Explicit Ultra loads the required method or reports the missing resource instead of silently omitting it.
- Tier 2/3 promotion checks typed, applicable, passing evidence rather than accepting nonempty reference strings.
- One-step preparation and explicit partial handoffs improve continuity without adding a mandatory state engine.

The main-branch integration also preserves its existing profile/index fingerprints, custom-index CLI, verified prerequisite ledger, external resource-lock isolation, artifact-path requirements, and review-disagreement checks. Test fixtures were updated only where the stricter canonical artifact/evidence interfaces require it. Details: [integration notes](skills/reasoning-workflow/docs/MAIN_INTEGRATION.md), [change log](skills/reasoning-workflow/CHANGELOG.md), and [upgrade guide](skills/reasoning-workflow/UPGRADE.md).

Keep a backup before upgrading. Rebuild old routes from the current normalized profile/index. Changed target fingerprints require a real new review, not merely a replacement hash. Legacy manifests without `delivery_kind` still mean complete delivery. Tier 2/3 resolvers need the role-aware evidence interface. Do not “migrate” by dropping unresolved obligations.

## Reproduce the checks

After installing the Python dependencies above, run from the repository root:

```sh
python -m unittest discover -s tests -v
python skills/reasoning-workflow/tests/run_all.py
python -m pip install markdown==3.7
python skills/reasoning-workflow/tests/check_package.py
```

The main-branch integration passed 34 public host-contract tests plus the package's 69 tests (39 baseline + 30 patch tests, including 38 actual CLI invocations). Package structure, local links, schemas, and archive checks are recorded separately. Test runs regenerate local receipt files; check a downloaded archive's checksum before running them. Distribution checksums are in [`dist/SHA256SUMS`](dist/SHA256SUMS).

These are deterministic code, synthetic contract, and cross-module tests—not 103 model trials. No multi-model blind evaluation or real payment, external executor, persistent recovery, or rollback integration has been certified. The six cross-task cases are evaluation protocols, not measured model success rates. No claim is made that every model will follow the Skill or that reasoning quality, latency, or cost has already improved.

## Repository and credits

- [`skills/reasoning-workflow/`](skills/reasoning-workflow/): complete canonical Skill, source, references, synthetic tests, and migration notes.
- [`modular/`](modular/): six focused instruction-only Skills with shared references.
- [`tests/`](tests/): public synthetic host and repository integration contracts.
- [`dist/`](dist/): complete installable archive and its checksum; no separate GitHub release is required.
- [`CONTRIBUTING.md`](CONTRIBUTING.md), [`PRIVACY.md`](PRIVACY.md), [`TERMS.md`](TERMS.md): contribution and project policies.

Created and maintained by [折鸢 / zy839971925-zyy](https://github.com/zy839971925-zyy), under the [MIT License](LICENSE). The project grows from problem-driven Deep Research into a general execution framework while retaining that original emphasis on framing, proportionate effort, evidence, and actual closure. Historical project introductions are retained in [`meta/`](skills/reasoning-workflow/meta/) for provenance, not as active installation instructions.
