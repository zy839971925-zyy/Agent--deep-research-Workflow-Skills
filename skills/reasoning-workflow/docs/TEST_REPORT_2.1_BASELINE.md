# Reasoning Workflow 2.1 — test report

## Executed result

The final local regression run completed with **39 tests, 0 failures, 0 errors**,
including **31 real subprocess CLI invocations**, using Python 3.14.7 and
jsonschema 4.23.0 in an isolated uv environment. Test totals include legal
baselines and refusal controls; they are not counts of defects or agents.
The earlier independent audit ran the then-current 38-test revision; the final
39th test validates the six cross-task evaluation fixtures, not model behavior.

From this package directory, run:

```sh
PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with jsonschema==4.23.0 python tests/run_regression.py
```

The dependency is isolated; this command does not modify managed Python.
Machine-readable results: [summary.json](../tests/results/summary.json) and
[cli_receipts.json](../tests/results/cli_receipts.json). The runner executes copied workflow
entrypoints against synthetic fixtures, not mock substitutes for the CLI.

## Coverage and controls

- Explicit Ultra selection: direct API and CLI agree; user depth does not
  increase autonomy. Unnormalized profile/route pairs are rejected by the bridge.
- Delegation, orthogonal verification and Light high-risk/high-governance
  controls remain reachable without forcing all reasoning dimensions upward.
- Strict raw envelopes, supplied empty runtime objects, hash algorithms,
  derived lineage, acceptance references and artifact identity/content binding.
- Actual patch write sets/conflicts, trusted submission-context hooks,
  terminal-state recovery refusal, combined dependency/wait cycles,
  side-effect replay classification and external lock conflicts.
- Learning validation and retrieval share admission checks; intrinsic-only
  validation contradictions are refused; maintenance records are isolated.
- Working-directory independence and profile → review → canonical → delivery
  binding, including valid single/dual baselines and failed/stale review controls.

## Independent review findings closed

1. Manifest current downgrade: a current/material canonical artifact cannot be
   excluded from digest verification by setting manifest `declared_current=false`.
   The original tampered-file counterexample is rejected with
   `ART_CURRENT_DOWNGRADE`; the legitimate historical noncurrent control passes.
   Required/current obligations come from canonical state and delivery references.
2. Explicit-depth inconsistency: `requested_depth=ultra` with stored
   `depth_class=standard` cannot satisfy the strict bridge with a single review.
   It is rejected with `PROFILE_RECHECK_REQUIRED`; normalization and subsequent
   routing produce Ultra/dual. A profile without requested depth retains its
   normal behavior. Regression tests cover API, CLI and bridge consistency.

The separate read-only audit reported six targeted checks passing, including
legal Ultra/dual and ordinary single controls. Its inputs and review remain in
the sibling `upgrade_review` evidence directory, not part of this portable
package; the bundled regression suite contains equivalent maintained checks.

## Orthogonality and host boundary

The ordinary-input-evidence counterexample now exits 1 with
`ORTHOGONALITY_UNVERIFIED`: structure can be valid while delivery eligibility,
evidence authentication and orthogonality credit remain false. Strong credit
requires two bound layer verification records and a trusted host-code resolver
receipt, not arbitrary JSON or a self-reported basis. Tests of the callback use
a synthetic host control only. They are not real authentication, proof of
independent authorship or an empirical assessment of review independence.

The bridge explicitly separates `structural_valid`, `evidence_authenticated`,
`orthogonality_verified` and `host_execution_verified`. It does not implement a
host executor, platform authorization, real CAS transactions or remote cancel
fences. The host must implement those contracts before using them for effects.
Without required support, strong claims/actions must remain blocked.

## What has not been measured

- No real model-following, model-quality, cost or latency evaluation was run.
- The six [cross-task cases](../evals/cross_task_cases.json) are a validated
  experimental protocol, not successful model execution trajectories.
- No external business action, account access or real side-effect replay occurred.
- Schema validity, file hashes and structural checks do not certify factual truth.
- This release is an opt-in standalone copy; it does not install a host platform
  or replace the original workflow automatically.

See [migration and usage](../UPGRADE.md),
[host adapter](../references/host-adapter.md) and
[change log](../CHANGELOG.md).
