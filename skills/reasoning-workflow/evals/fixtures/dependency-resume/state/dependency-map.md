# Synthetic dependency map

- P0: Server-held plaintext is acceptable. **Invalidated** by the latest user correction.
- P1: Provider can recover server-held plaintext keys. **Unverified in old draft; recheck against new material.**
- C1: Recommend provider-backed sync. Depends on P0, P1, and acceptable conflict handling.
- S1: “Provider sync is the preferred default.” Depends on C1.
- S2: “Provider can restore access without user-held keys.” Depends on P1.
- L1: Local export/import integrity test passed. Depends on the local export branch only; not affected by P0/P1.

Re-evaluate P0/P1, C1, S1 and S2. Preserve L1 unless new evidence directly bears on it.
