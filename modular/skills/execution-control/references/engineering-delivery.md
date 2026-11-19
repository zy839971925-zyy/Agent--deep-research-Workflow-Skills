# Engineering delivery through the normal entry point

Start at the request. If the user wants investigation, inspect and report. If they want a runnable change, trace one representative input from the normal entry through its state or data dependencies to the user's observable outcome. Prefer existing project conventions. Keep unrelated edits and incidental dependencies outside the change.

### Decide what must remain true

Read local instructions, callers, lockfiles, and existing checks relevant to the change. Identify the acceptance condition, a previous behavior or data format users rely on, and the most consequential failure. Reproduce a reported defect on a disposable copy if practical. If it cannot be reproduced, distinguish the observed symptom, suspected cause and test that could distinguish it. For unfamiliar tools, discover the appropriate specialist or check versioned documentation.

### Choose checks by failure mechanism

| Change | Useful witness | Failure worth exercising |
|---|---|---|
| Import, migration or state write | Existing data opens through the same client before and after the change | A partial write, repeated import or recovery leaves consistent state |
| CLI, API or adapter | Call the public entry with the caller's actual argument shape and inspect result and exit status | Invalid or legacy input reports the correct outcome across supported entry points |
| Distributed package | Build, unpack or install in an empty directory apart from the source repository, then exercise one normal task | A runtime asset, executable bit or relative dependency exists only in the checkout |
| UI or motion | Walk the actual interaction in both directions on the relevant viewport and inspect visible state | Cancellation, interruption, reduced motion or a changed return destination |
| Performance | Compare the same inputs and environment before/after; include units and variability | A faster microbenchmark leaves the user-visible bottleneck unchanged |

Use the smallest check that would fail on the old defect and pass on the change; preserve a meaningful unchanged control. Add a regression where the existing tests miss this behavior. Build or run broader checks when shared dependencies or release artifacts make them relevant. An expected failure caused by missing tooling is a verification gap; retain the command and scope for the report.

### Close the change

Read the diff against the request. Check generated copies and released artifacts where the project ships them. Re-run through the real entry after the final edit. Report what the user can use, what was observed, and material limits such as untested devices. If the implementation depends on unresolved product direction, narrow the change to agreed work or ask before starting expensive dependent implementation.
