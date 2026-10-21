# Main-branch integration of 2.1.1

This repository combines the complete 2.1.1 package with public contracts already present on main at `7d4b31f37aa95fac1b05003b626b9fccea60abaa`. It is not a blind directory replacement. The earlier standalone archive remains unchanged outside this repository; the archive in `dist/` is rebuilt from this integrated source and therefore has a different checksum.

## Preserved repository controls

- Profile-content and routing-index fingerprints still invalidate stale routes. Both routing CLIs accept the same custom index. Mandatory Ultra references remain mandatory; phase budgets accommodate all required families and the Ultra overlay.
- Completed prerequisites require a verified node ledger. Malformed ledgers produce schema findings before deeper processing. External resource locks cannot be escaped by declaring local or transactional isolation; local read/write conflicts require genuinely distinct isolated workspaces.
- Material current artifacts require paths. The stronger 2.1.1 delivery contract also binds manifest path, role, and state version to canonical artifact identity.
- Disagreeing review verdicts require explicit reconciliation handling. A consistent failed review is a valid failure record, not a passed verification.
- The optional `harness_bridge.py` and its public tool-boundary tests remain. No host integration is activated merely by copying this directory.

The five 2.1.1 repairs, one-step preparation, partial-delivery boundary, and role-aware promotion-evidence checks are retained.

## Test compatibility

The original 39-test regression script is retained unchanged. The 30-test patch suite remains; its missing-Ultra-method test now constructs its route against the intentionally modified index so that it tests resource absence rather than the earlier stale-index rejection. In the repository suite, artifact fixtures now provide matching canonical identity and learning fixtures provide schema-valid provenance plus a trusted synthetic resolver. The false-current assertion checks the more specific 2.1.1 downgrade error. These changes do not waive unresolved delivery or learning evidence requirements.

Local integrated results: 34 repository tests passed; 69 package tests passed, including 38 real Python CLI invocations. The existing GitHub Actions workflow runs the 34 repository tests; package tests are also reproducible locally with `tests/run_all.py`. These are synthetic deterministic checks, not model compliance measurements or real external-executor integration tests.

## Distribution and evidence

`dist/reasoning-workflow-2.1.1.zip` contains the complete `reasoning-workflow/` directory. Its `SHA256SUMS` is regenerated after integration, test receipt normalization, and documentation updates. Cache files, credentials, private handoff material, and machine-local absolute paths are excluded. The repository-level `dist/SHA256SUMS` covers the archive itself. Normalized receipts replace ephemeral machine paths while retaining commands, outputs, and exit codes; they are records, not identity or authorization certificates.

`meta/README*.md`, the baseline-source comparison, and the standalone release notes are historical records. The root bilingual READMEs are the current installation and usage documentation. The shared reference copies in Modular are synchronized without duplicating runtime helpers.
