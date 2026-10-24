# Current candidate — version 3

Evidence note for the synthetic workflow evaluation. The user now requires user-controlled data export/import and rejects server-held plaintext. This note is a candidate, not a verified external platform guarantee.

Options for investigation:
1. Improve encrypted user-controlled export/import; strongest fit to local-first privacy, weaker unattended cross-device convenience.
2. Add provider-backed sync only if client-side encryption, key recovery, conflict handling, and deletion behavior can be demonstrated; unknown key management is a blocker, not a solved detail.
3. Defer cross-device sync and measure demand while hardening local backup/restore.

Outstanding evidence: inspect current platform documentation and repository tests; determine what minimal prototype can test restore integrity and conflict behavior. The recommendation must preserve the user's stated privacy boundary.
