# Synthetic partial-handoff checkpoint

## Root objective
Recommend an architecture for optional backup and cross-device restoration in the fictional offline-first schedule app. Do not implement or deploy.

## Acceptance conditions
- Compare local user-controlled export/import with provider-backed sync.
- Preserve the owner's explicit rule: no server-held plaintext.
- Account for recovery and conflict behavior using the currently available evidence.
- Name the remaining uncertainty, a reversible test, and an exit condition.
- Deliver one integrated root recommendation; this checkpoint is not completion.

## Work state
- Complete and independently verified: local export/import integrity analysis (see `../completed/local-export-analysis.md`).
- Partial, awaiting evidence: provider key-management and recovery branch.
- A provider-sync draft and two downstream sections depend on the assumption that the provider can hold recoverable plaintext; that premise is now invalid.
- Wait trigger: current provider key-management evidence becomes available. The latest user says it is now at `materials/provider-key-management-v2.md`.
- Next: inspect the version-2 evidence and dependency map; revise only impacted claims; integrate and verify the root recommendation.

No prior transcript or earlier tool output is available in this simulated resumed session.
