# Contributing

Reasoning Workflow is intentionally kept as a small public workflow package rather than a dump of its private development harness.

The canonical Portable edition lives in [`skills/reasoning-workflow/`](skills/reasoning-workflow/). The [`modular/`](modular/) tree is a lightweight, human-browsable decomposition of the same semantics for hosts that prefer several focused Skills.

When proposing a change:

- start from a concrete failure mode, missing capability, or materially better simplification;
- preserve the six existing Skill Families unless there is strong evidence that a new boundary is necessary;
- prefer semantic invariants and conditional strategies over fixed step counts, source quotas, agent counts, or mandatory ceremonies;
- add Python or schema files only when deterministic runtime enforcement is genuinely useful — not merely to document an idea;
- keep Portable and Modular meaningfully aligned when shared semantics change;
- keep `README.md` and `README.zh-CN.md` synchronized for user-facing behavior;
- do not add private traces, chain-of-thought, credentials, proprietary eval sets, internal test harnesses, or generated build artifacts to the public repository.

A public pull request should be understandable from the changed workflow files themselves. If a change requires validation evidence, summarize the observable failure mode and the validation result in the pull request rather than committing a private engineering harness into the repository.

The public repository is versionless in product branding. Machine-format revisions may exist where interoperability requires them, but do not turn internal revisions into separate public product names.
