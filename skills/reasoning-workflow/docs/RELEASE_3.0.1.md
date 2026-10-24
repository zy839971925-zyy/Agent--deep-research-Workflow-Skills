# Release 3.0.1

This maintenance release strengthens the evaluation fixtures and regression checks; it does not add a new research rule or claim better model performance.

- Replace the placeholder stale-checkpoint digest with a real archived v1 artifact and verify its SHA-256 against the current v2 draft.
- Add mixed qualitative interview excerpts so tests can distinguish need discovery from population prevalence, observed adoption, and learning efficacy.
- Add a controlled sparse-search recovery case and a no-web arithmetic control.
- Keep all such scenarios marked protocol-only until they are run and independently scored on models.

The deterministic test suite validates fixture integrity and repository contracts. It does not establish that a model will follow the scenarios or that research quality improved.
