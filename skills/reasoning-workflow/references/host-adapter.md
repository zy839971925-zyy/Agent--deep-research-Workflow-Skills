# Trusted host adapter

This package validates records and computes obligations. It is not a scheduler, payment provider, authentication broker, transaction engine or durable storage service. A model cannot enforce host guarantees by repeating these rules.

## Worker submission and cancellation

`validate_worker_proposal` performs static contract checking. The 2.1 patch format is an object mapping canonical collection names to complete replacement arrays; no JSON Pointer paths, top-level headers or implicit deep merge. Actual replacement keys must equal the declared write set and fit the node's allowed set. Two replacements of the same collection conflict, even if the workers believe they touch different records. This deliberately conservative wire format avoids misleading leaf-level conflict claims.

`classify_worker_proposals(..., submission_verifier=callback)` refuses admission without a trusted callback. The callback is supplied by host code, not loaded from worker JSON. `host_adapter.verify_submission_context` checks a current ledger against authenticated executor, active attempt, lifecycle, contract and a present, unexpired lease, and requires an authorization callback. It does not authenticate those supplied observations.

The host must do all of the following in the same commit boundary:
- Read current authoritative state, plan, attempt, lease and cancellation state.
- Authenticate the executor and resolve relevant authorization for the actual target/action.
- Revalidate schema, actual patch scope and all references/invariants on the candidate whole state.
- Commit with compare-and-swap or a transaction plus a cancellation fence. An earlier callback is not a lock.
- Deduplicate proposal IDs with durable receipts across batches. Return the prior receipt on repetition.

If the host lacks this interface, keep the proposal pending; never treat static CLI exit 0 as merge permission. The worker-proposal CLI deliberately reports `WORKER_HOST_CONTEXT_REQUIRED` until a real host performs the commit. There is no unsafe JSON flag to bypass it.

## Recovery and replay

Checkpoint integrity and plan/schedule binding are validated separately before `compute_resume_actions`. The helper checks current ledger terminal state and version alignment, but returns obligations, never execution permission. Failed/cancelled/completed nodes do not automatically rerun. Non-running or misaligned state requires reconciliation.

Idempotence must be bound to the same operation and a stable host-confirmed key; the helper only requests this check. Side-effect nodes without declared replay safety default unsafe. Consequential/irreversible nodes marked safe are rejected by the plan validator. Reliable safe replay requires host implementation, valid authority and current external-outcome evidence. Otherwise block unknown attempts. Local workspace/transactional labels cannot bypass shared resource lock conflicts.

## Review to delivery

Use the existing small CLIs for local record checking. For a substantial recorded deliverable use `validate_workflow.py` to connect profile → deterministic route → review mode/result → scoped target fingerprint → canonical verification → manifest → actual file bytes.

Inputs are the normalized current profile, its exact deterministic route, canonical work-state, manifest and `review-bundle.schema.json` sidecar. Each review uses the existing dual-verification record plus target references, a fingerprint, actual context exposure and, when claiming orthogonal review, evidence references. The existing dual CLI retains `passed` as a record-validity compatibility alias and now exposes `record_valid` and `verification_passed` separately. A valid failed record is not a passing review.

Generate `fingerprint(state, target_refs)` from `validate_workflow.py`. It includes target records and reachable singular/plural record dependencies (`from_ref`, `to_ref`, `*_ref`, `*_refs`, `depends_on`, `derived_from`, `supports`, `contradicts`, `represents`, `implements`), excluding traversal through verification_refs. Cycles terminate without discarding reachable nodes; unresolved dependencies or duplicate IDs reject the fingerprint. It binds only that scope, not a global state version: an unchanged artifact based on an older version can remain valid. Changes to the target/dependency records invalidate its review. A target's verification_refs field is itself part of the target bytes, so set final bindings before fingerprinting.

Material answers/artifacts/recommendations/decisions need passing reviews at least as strong as the current route, matching canonical verification IDs and target refs. The strict bridge rejects profiles whose explicit depth requires normalization; routing CLI returns the updated profile and version. Direct API routing applies the same normalization but does not mutate the caller's profile.

Canonical current/material status chooses required byte checks; a false manifest `declared_current` cannot suppress them. Historical optional files may remain noncurrent. Current files require matching manifest `content_sha256`, canonical artifact `metadata.content_sha256`, and actual SHA-256 bytes under `--root`. Canonical path and basis must agree with the manifest; basis need not equal the current global version.

These are mechanical checks, not semantic truth guarantees. The host must resolve evidence references, verify method/execution receipts and actual inherited context. A string reference is not proof of independence. The bridge separately outputs `structural_valid`, `evidence_authenticated`, and `orthogonality_verified`. Structural validity alone never grants orthogonal credit. `orthogonality_verified=null` means not requested; false means unverified when requested.

For `dual_orthogonal`, each layer must reference a different nonempty set of canonical passed verification records, bound to the same target scope/fingerprint. Raw input evidence cannot stand in for those executed checks. Even those bindings are not authentication. The API additionally requires `review_verifier(entry, state)`, a trusted host-code callback that verifies actual evidence provenance, execution/method receipts and the claimed different failure path. It returns `{verification_id, target_fingerprint, layer1_verification_refs, layer2_verification_refs, evidence_authenticated: true, orthogonality_verified: true}` for that exact review. Exceptions, absent callback, stale/mismatched receipts and false/unknown values grant no credit and block strict delivery when orthogonality is required. The package checks binding; the host must make and substantiate the truth assessment. A callback returning true unconditionally is not a production verifier.

The standalone CLI deliberately has no worker JSON flag or credential mechanism for this callback. Without host integration it reports the strong requirement unverified and exits 1, even if its records are structurally valid. Single/minimal ordinary structural checks remain available without claiming evidence authentication. Regression tests use an explicitly synthetic callback only to exercise interface behavior, not certify any real independent reviewer. Do not turn this adapter into a new identity platform or claim the Skill authenticates methods by itself. `packet_only` must be a trusted observation, not a worker's guess. Unknown exposure may not claim fresh-context credit; different models or tools do not automatically remove common-source failure. The bridge does not authenticate review authors or sign records; use only trusted, reviewed input storage. It reports `host_execution_verified=false` even when local checks pass.

## Partial handoff

Question, Action and Mixed lanes all honor explicit material requirements/acceptance and runtime obligations. A Question lane label cannot hide a blocked required deliverable.

A valid intermediate result may use the optional manifest fields `delivery_kind: "partial"`, `remaining_work` (nonempty), `remaining_obligation_refs` (all unresolved material requirement/acceptance IDs), and `declared_delivery_ready: false`. The canonical task must remain open/blocked rather than closed/ready. Existing byte, reference, status consistency and material-artifact checks still apply. `computed_partial_ready: true` means only that the intermediate handoff is structurally admissible; `computed_delivery_ready` and `computed_task_complete` remain false. Full closure is not waived and the remaining task is not automatically scheduled or executed.

## Capabilities

Capability snapshots are routing/preflight data, not final operation authorization. Existing allowed/denied/approval_required gates remain, but the host rechecks principal, actual action/target, constraints and freshness at use. Do not impose one universal TTL or accept freeform scope as authorization. Missing integration means blocked/unsupported for the affected operation, not permission to downgrade it silently.

## Learning evidence admission

`learning_core.admit_record` is shared by validation and retrieval. Schema validity is checked before semantic use. Validated/promoted records need non-intrinsic feedback and validation references, and the caller must supply a trusted resolver that actually resolves those references. Without that resolver they are not admitted. A candidate remains only a candidate.

For local tests/operators, both learning CLIs accept `--validation-evidence INDEX.json`. This trusted-host index maps a validation ref to `{path, sha256, verdict: "pass", kind}`; permitted kinds are `external_evaluation`, `human_feedback`, `deterministic_test`, `external_observation`. Paths must stay under the index directory and bytes must match SHA-256. The index is host-curated, not worker-supplied. Digest identity is not a semantic evaluation or proof of who issued an evaluation; the operator must inspect or authenticate its provenance. A forged index from an untrusted source grants no credit.

For promoted Tier2, `held_out_eval_refs` also requires role-aware evidence. Promoted Tier3 additionally verifies regression, baseline, dual-review and rollback evidence. Each gate index entry needs `roles` (matching gate role), `learning_ids` (including this lesson), `current: true`, `subject_sha256: learning_subject_fingerprint(record)`, and `verdict: "pass"`, plus the path/hash. Gate `kind` must match: regression → `deterministic_test`; held_out → `external_evaluation` or `deterministic_test`; baseline → `baseline_comparison`; dual_review → `independent_review` plus `independence_verified: true`; rollback → `rollback_plan`. The bound lesson fingerprint covers ID/tier/signature/lesson/conditions/proposed patches; changing these requires fresh gate evidence. The resolver API is `resolver(ref, role=role, record=record)`. Gate verdicts and current/independence labels remain host-authenticated responsibilities; this offline index cannot turn a worker's invented record into real evidence.

Ordinary retrieval defaults to Tier1 only. `--maintenance` also reads admitted Tier2/3 material as advisory evidence, never as instructions or canonical-application permission. Existing promoted gates (regression, held-out, baseline, dual review, rollback) still apply. No CLI writes the learning library or promotes a rule automatically.
