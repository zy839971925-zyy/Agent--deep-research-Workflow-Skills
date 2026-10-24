# Reasoning Workflow — upgrade and migration

## 3.0.0 → 3.0.1

- Replace the complete Portable directory with the 3.0.1 package; keep references, tests, schemas, and scripts together. No schema migration is required.
- This is an evaluation-fixture maintenance release: it adds a content-bound historical checkpoint artifact, mixed-view interview evidence, and sparse-search/no-web controls. It does not claim a workflow behavior change or real-model improvement.

## 2.2.0 → 3.0.0

- Replace the complete Portable directory with the complete 3.0.0 directory; retain a backup. Keep references, tests, schemas, and scripts together.
- New triggered references distinguish empirical real-world research, pre-build architecture evaluation, and hybrid outcome-to-system questions. Existing Ultra methods remain; do not load every reference for every task.
- Ambiguity now routes through a specific evidence-first clarification gate. Check context, accessible project materials, external facts, and safe derivations before asking; ask only for unresolved user-owned information that can materially change the result. This never substitutes for action approval.
- Resume behavior explicitly searches authorized workspace indexes for moved or versioned artifacts and reconnects next actions to current acceptance conditions. It does not promise persistence a host lacks.
- V3 functional scenarios and fixtures are added as a manual behavior-evaluation protocol only. No real-model evaluation or improvement is claimed. The 3.0.0 package is included in the repository; no separate GitHub Release asset was published.


## 2.1.1 → 2.2.0 (local candidate)

- Replace the complete Portable Skill directory with the complete 2.2.0 directory; keep a backup for rollback. Do not mix a new entry point with old references or scripts.
- Research guidance adds a compact frontier, gap-driven citation tracing, targeted post-draft gap search, and optional cross-study/model/benchmark comparison. Load these only when triggered.
- Active model guidance targets GPT-6+ and current frontier models by observed capability, not GPT-5.6 compatibility or model-name stereotypes. Host profiles distinguish Codex, Claude Code, and app chat. Search, agents, connectors, and UI remain separate host/account settings; serial Ultra is the fallback without agents.
- Standalone Modular Deep Research now includes its information-target navigation reference and comparative synthesis. Modular remains instruction-only; it does not gain Portable's router, runtime scripts, or cross-Family state.
- Regenerate recorded routes against the current package as before. This release does not install tools, connect accounts, or grant authority. Model-compliance and research-quality evaluation remain unevaluated.
- The local archive is generated deterministically. Tests do not rewrite tracked receipts by default. Run archive parity and checksums before distributing.

## Historical 2.1 → 2.1.1 compatibility

## 2.1 → 2.1.1 compatibility

See [中文修复与升级说明](docs/RELEASE_2.1.1.zh-CN.md). Keep the 2.1 directory/records; load this separate directory through the same `SKILL.md` entry. There is no automatic migration or execution.

- Regenerate routes from the current normalized profile: routes now include `required_reference_ids`; resource selection rejects stale or edited routes.
- Re-review affected recorded targets with the new `fingerprint` function. Old hashes may change because singular/transitive dependencies are now included; do not relabel old reviews as current.
- Explicit material obligations are enforced in Question, Action and Mixed lanes. Use the optional partial handoff fields instead of falsely claiming full readiness. Omitted `delivery_kind` keeps complete-delivery behavior.
- `parallel_policy=forbidden` requires actual ordering, not missing or different group labels. Use serial mode or acyclic `starts_after`/dependency constraints; otherwise replan.
- Host evidence resolvers for promoted Tier2/3 records must implement `resolver(ref, role=..., record=...)`; boolean-only legacy callbacks fail closed for promotion, not for ordinary Tier1 evidence. See the [host adapter](references/host-adapter.md#learning-evidence-admission).

## Install without replacing the original

Keep this directory as a separate version. Make `SKILL.md` the model-facing entry; keep `references/`, `families/`, `schemas/` and `scripts/` next to it. The original audited directory is not modified by this release. No install script, account connection, global Python change or automatic canonical migration is performed.

The model can use the short entry alone for simple tasks. Only load a strategy/reference when a real task gap triggers it. Existing detailed research references remain available. General task coverage now includes research, artifacts/code, coordination, cross-session continuity and external-action boundaries. This does not install tools or confer access to outside systems.

## Operator commands

The examples assume a shell opened in this package. `uv` creates an isolated dependency environment; it does not modify managed Python. Python with `jsonschema==4.23.0` already installed also works. The scripts resolve their schemas/index relative to `__file__`, so absolute script paths work from another working directory.

```sh
uv run --no-project --with jsonschema==4.23.0 python tests/run_all.py
uv run --no-project --with jsonschema==4.23.0 python scripts/prepare_task.py tests/fixtures/standard_profile.json --signal ultra_requested
```

For strict recorded delivery, supply your actual current profile, deterministic route, work-state, manifest and review bundle:

```sh
uv run --no-project --with jsonschema==4.23.0 python scripts/validate_workflow.py \
  --profile profile.json --route route.json --state state.json \
  --manifest manifest.json --reviews reviews.json --root ./artifacts
```

This last command is a template, not a delivered example state. It is opt-in for substantial recorded work, not a requirement to build JSON for every short answer. `validate_workflow.py --help` and the relevant schema define its interface. The test suite contains a complete synthetic passing bridge and controlled failing variants.

## Compatibility and migration

| Area | 2.1 rule | Operator action |
|---|---|---|
| Model entry | Short active SKILL; old entry retained only as `docs/LEGACY_ENTRY.md` | Start with the new root; do not load both entries as competing instructions. |
| Explicit depth | Optional `requested_depth` persists steering; `ultra_requested` wins over automatic downgrade | Record explicit steering in profiles when using the recorded API. `route_task()` and the routing CLI apply the same normalization/version increment. The strict bridge/resource selector reject an unnormalized profile (`PROFILE_RECHECK_REQUIRED`); use the CLI's resulting `task_profile` plus route. Depth never grants autonomy. |
| Required controls | Delegation and orthogonal checks route in Question as well as Action; required families cannot be hard-filtered by typical depth/read budget | Expect a minimum family control set or explicit unsupported failure, not silent omission. Stage full reference reading as needed. |
| Raw input | Only a record list or an object containing `records` is accepted; `{}` or typo envelopes fail | Convert legacy envelopes deliberately. `[]` remains a valid explicit empty collection. |
| Raw identity | Nonempty content hashes require a supported algorithm; known derived records require nonempty parent references | Recompute authentic hashes; link real parents. Do not invent missing ancestry. Untraceable material stays unknown and gets no full-lineage credit. |
| Runtime optional objects | An explicitly supplied empty ledger/schedule is invalid, not omitted | Omit an optional argument when absent; do not use `{}` as a placeholder. |
| Worker wire format | Worker proposal schema **1.1**; `proposed_state_patch` maps allowed canonical collection names to full replacement arrays | Convert old freeform patches with a reviewed adapter. No implicit deep merge, header edits or JSON Pointer shortcut. This is a breaking proposal-format change. |
| Worker admission | Actual patch keys must equal declared write set and fit the node; overlapping collection replacements conflict | Split/serialize work or resolve centrally. Labels do not prove leaf-level independence. A trusted submission callback and atomic host commit are required. |
| Resume | Terminal, unknown/misaligned lifecycle and unsafe external outcomes do not yield automatic rerun permission | Reconcile against current host state. Reopen only via an authorized new attempt. Preserve old receipts. |
| Schedule | `depends_on ∪ starts_after` must be acyclic in all modes | Remove self/cyclic waiting edges; valid plan-only checks are not sufficient. |
| Resource locks | External resource conflicts are not removed by workspace/transactional labels | Host must provide actual lock/isolation mechanisms; local labels alone do not. |
| Delivery | Acceptance references must exist with correct type; canonical and manifest artifact identity/path/role/basis agree | Repair the actual binding. Do **not** rewrite all old bases to the global current version: unaffected older artifacts may remain valid. |
| File bytes | Manifest supports optional `content_sha256`; strict bridge requires it to match canonical metadata and real bytes | Hash the delivered bytes and bind review scope to the canonical artifact; never replace an artifact after review without rechecking. Canonical current/material status, not the manifest `declared_current` flag, selects mandatory checks; downgrading that flag is rejected. Legitimately historical/noncurrent optional files need not pretend to be current. |
| Review | `passed` remains the legacy record-validity alias; `record_valid` and `verification_passed` are separate | Consumers must not use record-valid exit 0 as business review success. The strict bridge additionally checks mode, target scope/fingerprint and canonical binding. |
| Strong review credit | `dual_orthogonal` requires nonempty layer-bound verification refs and a trusted host review callback; no self-reported enum/ref earns strong credit | Standalone strict CLI blocks this requirement without integration. Read `structural_valid`, `evidence_authenticated` and `orthogonality_verified` separately. Ordinary record checking stays available. |
| Learning | Validation and retrieval share schema/semantic/evidence admission; validated/promoted labels alone no longer suffice | Supply a trusted validation evidence resolver/index or keep records candidate/unadmitted. See host adapter. No auto-fabrication of evidence for old records. |
| Maintenance isolation | Runtime retrieval defaults to Tier1; Tier2/3 require explicit maintenance reading | `--maintenance` returns advisory material, not permission to modify canonical rules. Existing promotion gates remain. |

Existing schema versions are preserved where additions are optional or checks enforce existing contracts. Worker proposal 1.1 is explicitly breaking. The review bundle is a new version 1.0 sidecar. Legacy invalid records may now fail intentionally; do not silently coerce them into valid history.

## Host integration checklist

Read [host-adapter.md](references/host-adapter.md) before using any returned classification as execution/merge permission. The package has no actual scheduler, external-action executor, persistent deduplication store, authenticated principal service, atomic compare-and-swap, cancellation fence or provider receipt verifier.

A host must authenticate executor/attempt, obtain current ledger/lease/authority, validate candidate whole state, and atomically commit with cancellation and version checks. The provided Python helper checks supplied context but cannot authenticate it or close a time-of-check/commit race. Public proposal CLI is fail-closed until host admission; there is no worker-controlled override. Capability snapshots remain preflight information, not final authorization. Real sends/payments/signatures stay under native platform gates.

Review records/evidence must come from trusted reviewed storage. Fingerprints/digests establish identity, not correctness, independent authorship, source reliability or genuine fresh context. Unknown exposure cannot claim fresh-context credit. The bridge explicitly reports `host_execution_verified=false`.

## What has and has not been tested

The release has a deterministic real-code regression suite using synthetic data, real schemas and original-style CLI entry points. Read `tests/results/summary.json`, `cli_receipts.json` and `TEST_REPORT.md`. It exercises legal controls and previous failure shapes, plus review/delivery composition.

No model adherence study, real-world research-quality evaluation, cost/latency benchmark or external business action was run. The task strategy examples are behavioral guidance, not measured performance. A shorter entry is not proof that every model follows it. Before deploying broadly, run paired same-model/same-tools tasks spanning short questions, research, documents, code, coordination and long projects; retain held-out cases, quality failures and costs separately.
