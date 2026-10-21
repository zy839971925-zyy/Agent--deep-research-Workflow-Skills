# Reasoning Workflow change log

## 2.1.1 — 2026-10-21

- Fix scoped review fingerprints to traverse singular/plural canonical references and transitive dependency cycles safely; missing/duplicate refs fail closed.
- Apply material delivery obligations across all lanes. Add an honest partial-handoff manifest that cannot claim full task completion.
- Enforce forbidden parallel nodes using actual dependency/wait ordering, regardless of optional concurrency groups; preserve independent legal parallel work.
- Make the Ultra method a required routed resource, and reject edited/stale routes or missing method files without silent depth reduction.
- Resolve promotion evidence by role, kind, lesson scope/fingerprint, current/pass status and file hash; require independence evidence for dual review. Tier1-only normal retrieval/advisory maintenance remain unchanged.
- Add optional `prepare_task.py` for profile → route → required/deferred resources, and 30 deterministic boundary tests. Final combined run: 69 passing tests / 38 actual CLI invocations. No model-compliance or external executor claim.
- Retain the 2.1 baseline test report and original regression suite; see the current test report and Chinese release guide.

## Historical 2.1 change log

# 2.1 implementation changes

This is a separately built upgrade, not a change to the audited original. Existing research methods, canonical work-state, reasoning families, verification records and learning promotion gates are retained. No third-party skill code was copied.

## Model-facing behavior

- Replaced the long root entry with a short result-oriented working loop and on-demand task strategies.
- Made explicit depth, scope, format, prohibitions and Stop/Cancel priority visible at the entry point.
- Separated depth from autonomy/persistence; general tasks need no compulsory project record, table, plan or delegation.
- Added practical artifact/code, coordination, continuity and external-action guidance without creating a plugin market, distributed bus, new state engine or mandatory fixed worker tree.
- Preserved research framing, ecology, missingness, source lineage, discriminating observations and affected-branch invalidation.

## Routing and resources

- Explicit Ultra requests apply from every depth and take precedence over automatic downgrade. An optional persistent requested-depth field carries explicit steering. API and CLI share normalization; strict bridge/resource selection reject inconsistent unnormalized profiles rather than accepting weaker review.
- Delegation and orthogonal-verification needs enable the necessary control families in Question and Action paths.
- Required controls remain reachable for Light/high-consequence and high-governance tasks. Typical-depth filtering and small reading budgets cannot silently remove a mandatory family. Ordinary short Light tasks still avoid reference-loading ceremony.
- Root/schema/index paths are derived from script locations rather than caller working directory at corrected entry points.

## Input, lineage and delivery

- Reject malformed raw/learning envelopes; validate explicitly supplied empty runtime objects.
- Bind content hash to supported algorithm and require known derived lineage.
- Check acceptance artifact references and manifest/canonical artifact identity, path, role and basis. Do not force all artifacts to current global state version.
- Reject manifest downgrades of canonical current/required material artifacts; digest checks are selected from canonical obligations, not an untrusted manifest flag. Keep a legal historical optional-artifact control.
- Add an opt-in strict workflow bridge: current profile/route, successful review strength, scoped canonical target fingerprint, canonical verification bindings, current-file manifest and actual SHA-256 bytes. A valid failed review is not a successful review.
- Separate strict structural validity from authenticated evidence and verified orthogonality. Strong orthogonal delivery requires both layer-target bindings and an exact trusted-host receipt; absent integration blocks strong credit. No identity/authentication platform is implemented.
- Preserve `passed` as a legacy record-validity alias while exposing `record_valid` and `verification_passed` separately.

## Runtime and host boundaries

- Proposal schema 1.1 specifies conservative whole-collection replacement arrays. Validate actual keys, declared write scope and allowed scope together; detect conflicts from actual replacements.
- Classification requires a trusted host submission verifier; public static CLI fails closed rather than guessing merge permission.
- Supply a helper for current ledger, executor, attempt, contract, lease and authorization callback checks; document atomic CAS/cancellation fence and durable dedup as host obligations, not implemented guarantees.
- Block terminal recovery, stale/unknown versions and unsafe external replay; idempotency requires host-bound key verification.
- Detect cycles on the joint plan/schedule waiting graph in serial, parallel and hybrid modes.
- Do not allow local isolation labels to bypass external resource lock conflicts. Missing replay safety on consequential/irreversible nodes is an error.

## Learning

- Share schema, semantic and validation-evidence admission between validation and retrieval.
- Prevent intrinsic/empty feedback from becoming validated merely by flipping a boolean.
- Require trusted resolution of validation evidence rather than accepting self-reported labels.
- Restrict ordinary retrieval to Tier1; explicit maintenance reading of Tier2/3 is advisory and grants no canonical-write authority.

## Evidence limits

The shipped regression suite runs real code, schemas and CLIs on synthetic inputs. No real host scheduler/executor, outside account, model adherence evaluation or quality/cost benchmark has been implemented or measured. Authentic authorization, review authorship, context-exposure receipts, semantic support and atomic commit remain trusted-host responsibilities. Strict file identity does not prove file correctness.
