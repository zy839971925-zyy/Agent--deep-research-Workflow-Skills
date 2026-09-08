<div align="center">

<img src="./skills/reasoning-workflow/assets/icon.svg" width="88" height="88" alt="Reasoning Workflow" />

# Reasoning Workflow

### Understand the problem before you search, decide, or act

A general-purpose governing Skill for reasoning, Deep Research, decisions, controlled execution, verification, and evidence-gated workflow learning.

**English** · [简体中文](./README.zh-CN.md)

[Start in 30 seconds](#start-in-30-seconds) · [Choose an edition](#choose-an-edition) · [How to use it](#how-to-use-it) · [Depth](#depth-light-to-ultra) · [Architecture](#how-the-workflow-thinks) · [Repository](#repository-map)

**[Browse Portable / canonical Skill](./skills/reasoning-workflow/)** · **[Browse Modular edition](./modular/)** · [Read `SKILL.md`](./skills/reasoning-workflow/SKILL.md)

</div>

---

## Why this exists

Powerful agents can search, write, code, call tools, delegate work, and operate for a long time. The hard part is increasingly not *whether* an agent can do something, but whether it is solving the right problem, using the right evidence, allocating enough—but not excessive—effort, preserving state correctly, and knowing when a result is actually complete.

Reasoning Workflow governs that layer.

It helps an agent answer questions such as:

- What is the real task or desired outcome?
- Is the problem well framed, or is the current framing itself uncertain?
- Which premise, causal edge, constraint, or missing observation actually carries the answer?
- Should the next move be reasoning, retrieval, a calculation, a specialist Skill, a user question, a worker, or no further work at all?
- What evidence would distinguish competing explanations?
- Is a recommendation robust, or does it flip under a small change in assumptions or user preferences?
- Is a failed action a local tool error, a planning failure, an observation failure, or evidence that the whole frame changed?
- Does a second reviewer provide genuinely independent verification, or merely repeat the same failure mode?
- What must be true before the task can be closed?

The goal is **not to make every task longer**. The goal is to make effort proportional to uncertainty, consequence, and actual decision value.

> **Research follows the structure of the problem, not merely the wording of the prompt.**

---

## What it is — and what it is not

Reasoning Workflow is a governing Skill above specialist capabilities. It can coordinate a coding Skill, browser, data-analysis Skill, design Skill, local tools, connectors, subagents, or other domain methods without trying to replace them.

It is **not**:

- a prompt collection;
- a fixed chain-of-thought template;
- a mandatory long checklist;
- a “search N sources” recipe;
- a fixed multi-agent hierarchy;
- a reason to ask the user more questions than necessary;
- a replacement for permissions, safety controls, domain expertise, or specialist Skills;
- proof that an answer is correct merely because the workflow was invoked.

The design favors **semantic invariants + adaptive strategy**. Strong models should have room to choose, reorder, repeat, compress, or skip strategies when the current task state justifies it.

---

## Start in 30 seconds

### One command for supported coding agents

If you use the open `skills` CLI, the fastest cross-agent install is:

```bash
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills --skill reasoning-workflow
```

The CLI can target supported agents such as Codex and Claude Code. Add `-g` for a user-wide install, or use `--list` first to inspect the Skills exposed by this repository.

```bash
# Inspect before installing
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills --list

# Example: install Portable globally for Codex
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills \
  --skill reasoning-workflow --agent codex -g
```

This is a community/open-ecosystem installer, not a requirement. Manual and host-native installation remain supported below.

### ChatGPT Skills

If your ChatGPT workspace supports uploaded Skills:

1. Open **Plugins → Skills**.
2. Choose **Create → Upload from your computer**.
3. Upload the Portable Skill folder/package built from [`skills/reasoning-workflow/`](./skills/reasoning-workflow/).
4. After installation, ask ChatGPT to use **Reasoning Workflow** on a task.

If you package the folder yourself, keep `SKILL.md` at the root of the uploaded Skill package together with its `references/`, `families/`, `schemas/`, `scripts/`, `agents/`, and `assets/` directories.

### Codex

The Portable edition follows the Agent Skills structure. A direct GitHub-folder install can be requested with Codex's skill installer:

```text
$skill-installer install https://github.com/zy839971925-zyy/Agent--deep-research-Workflow-Skills/tree/main/skills/reasoning-workflow
```

Or copy the folder into a standard Codex/Agent Skills location such as:

```text
.agents/skills/reasoning-workflow/
```

This repository also includes [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) for plugin-style discovery.

### Claude Code

Copy the Portable Skill folder to either a project-level or user-level Skills directory:

```text
# Project
.claude/skills/reasoning-workflow/

# User-wide
~/.claude/skills/reasoning-workflow/
```

The named directory should contain `SKILL.md`; do not place `SKILL.md` loose directly under `skills/`.

### Other Agent Skills-compatible clients

Use the same self-contained folder:

```text
skills/reasoning-workflow/
└── SKILL.md
```

The public [Agent Skills specification](https://agentskills.io/) defines `SKILL.md` as the required entry point and allows optional scripts, references, and assets. Host-specific discovery locations vary, so use the directory that your client documents.

---

## Choose an edition

The repository exposes both editions as normal folders. There are no opaque distribution ZIPs in `main`, so GitHub users can inspect everything before installing it.

| Edition | Location | Best for | Runtime model |
| --- | --- | --- | --- |
| **Portable / canonical** | [`skills/reasoning-workflow/`](./skills/reasoning-workflow/) | Most users; ChatGPT/Codex/Claude; one governing Skill | Full depth gate, cross-Family routing, schemas and optional deterministic helpers |
| **Modular** | [`modular/skills/`](./modular/skills/) | Advanced hosts that compose several independent Skills | Six lightweight semantic Skills; no duplicated Python/schema runtime |

### Portable is the default

Portable is the full governing workflow. It contains:

- `SKILL.md` — universal entry point;
- six Family indexes;
- progressively loaded references;
- machine-readable schemas for task/state/runtime contracts;
- a small set of runtime Python helpers for deterministic routing and validation;
- host metadata and the project icon.

It intentionally **does not** contain development-only tests, eval fixtures, build reports, generated distributions, or internal engineering artifacts.

### Modular is intentionally lighter

The Modular edition exposes six independent semantic Skills without duplicating Portable's schemas or Python runtime into every Family:

- [`reasoning-core`](./modular/skills/reasoning-core/)
- [`deep-research`](./modular/skills/deep-research/)
- [`decision-analysis`](./modular/skills/decision-analysis/)
- [`execution-control`](./modular/skills/execution-control/)
- [`audit-verification`](./modular/skills/audit-verification/)
- [`workflow-learning`](./modular/skills/workflow-learning/)

Each contains only its own instructions and Family references. If you need Reasoning Workflow's bundled deterministic router, semantic state validators, or full cross-Family governing loop, install Portable instead.

You can also install only the Modular capability you want with the `skills` CLI:

```bash
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills --skill deep-research
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills --skill decision-analysis
```

---

## How to use it

You normally do **not** need a giant prompt. Give the agent the real goal, important constraints, and any depth preference that matters.

### General use

```text
Use Reasoning Workflow for this task.

Goal: [what I actually need]
Constraints: [scope, deadline, permissions, sources, risk boundaries]
Deliverable: [answer, recommendation, code change, report, artifact, etc.]

Choose proportionate depth. Do not turn a simple task into a project.
```

### Deep Research

```text
Use Reasoning Workflow at Deep depth to investigate this question: [question].

Build the research around the decisive premises, relationships, and causal links rather than literal keywords.
Distinguish frame uncertainty from answer uncertainty.
Prefer evidence routes that could actually change the answer.
Keep competing explanations alive until evidence discriminates between them.
Give me the best-supported conclusion, boundary conditions, and remaining material uncertainty.
```

### Ultra Research

```text
Use Reasoning Workflow at Ultra depth for: [question].

Spend the extra budget broadly before converging:
reframe the problem when useful, search for hidden relationships and omitted variables,
explore materially different hypotheses and evidence ecosystems,
and reset the research path if it becomes homogeneous or anchored.

Do not spend most of the extra budget repeatedly verifying the same claim.
Verify the pivotal claims strongly, then give me the calibrated answer and what could still change it.
```

### Decision / recommendation

```text
Use Reasoning Workflow to decide what I should do.

Goal: [goal]
Known options: [A, B, ...]
Constraints: [constraints]
Preferences: [what I care about, if known]

Check whether the option set is incomplete.
Separate factual uncertainty from model, preference, and option uncertainty.
Show the decisive trade-offs, robustness region, and conditions that would switch the recommendation.
Only ask me a question if the answer could materially improve the decision.
```

### Causal or systems analysis

```text
Use Reasoning Workflow to explain why [outcome] is happening.

Do not jump from sequence or correlation to causation.
Model only relationships that could materially change the explanation:
upstream causes, mediators, feedback, incentives, substitutes, delays,
confounders, reverse causality, thresholds, and competing mechanisms.
```

### Controlled execution

```text
Use Reasoning Workflow to implement [change].

Authorized scope: [scope]
Preserve: [invariants]
Do not change: [forbidden areas]

Use delegation only when a real bottleneck benefits from it.
Keep evidence-bearing handoffs compact.
Diagnose failures before replanning.
Verify the final effective state, not just the last successful tool call.
```

### Keep it light

```text
Use Reasoning Workflow, but keep this Light unless the task reveals a material hidden complication.
```

Reasoning Workflow may **de-escalate** as well as escalate. Invoking the workflow does not mean invoking Ultra.

---

## Depth: Light to Ultra

Depth controls **epistemic ambition and total budget**, not a fixed number of searches, agents, steps, references, or model tokens.

| Depth | Best for | Typical behavior |
| --- | --- | --- |
| **Light** | Stable, direct, well-specified work | Minimal framing, direct answer/action, relevant check only |
| **Standard** | Bounded analysis, writing, implementation | Normal reasoning and verification; limited supporting context |
| **Deep** | Material uncertainty, causal questions, contested evidence | Explicit problem model, competing explanations, stronger evidence and challenge |
| **Max** | Maximum useful depth within the current trajectory | Push the current framing/research path to its useful limit; strong material verification |
| **Ultra** | Problems where the trajectory itself may be narrow, path-dependent, incomplete, or structurally uncertain | Much larger budget for reframing, hidden relationships, alternative hypotheses, cross-domain/evidence routes, missingness/boundaries, and stronger synthesis |

### Max vs Ultra

- **Max:** *How far can this strong trajectory be pushed?*
- **Ultra:** *What might this entire trajectory be missing?*

Ultra is not “Max + more sources.” It is a higher-budget **diverge → prune → investigate → rebuild if needed → converge** mode.

> **Ultra expands aggressively, prunes intelligently, and verifies selectively.**

Ultra does not automatically mean a fixed agent count, a giant up-front plan, every model call at maximum reasoning effort, exhaustive search, or reviewer voting.

---

## How the workflow thinks

The universal reasoning spine is a dependency graph, not a fixed SOP:

```text
real task / desired outcome
        ↓
problem representation and frame
        ↓
pivotal premises, constraints, relationships, mechanisms
        ↓
uncertainty and competing explanations
        ↓
evidence needs / observations / reasoning operations
        ↓
model update
        ↓
answer or decision
        ↓
action when authorized
        ↓
observation + verification
        ↓
reopen upstream state when reality disagrees
```

### Representation before decomposition

A perfectly decomposed wrong problem is still wrong. When several materially different representations remain plausible, the workflow can keep them alive briefly and only refine the branch whose uncertainty blocks progress.

### Search follows evidence need

```text
problem graph
→ uncertain premise / causal edge
→ evidence need
→ intended observation
→ best evidence surface
→ observation
→ model update
→ next answer-bearing uncertainty
```

The query is only a projection of the evidence need. It is not the research plan.

### Reasoning depth is not repetition

If additional thinking stops changing the problem model, live hypotheses, pivotal uncertainty, or answer boundary, the workflow changes representation, reasoning operator, evidence route, or abstraction level instead of repeating the same reasoning for longer.

---

## The six Families

The Families are routes through one governing system, not six mandatory phases.

| Family | Owns | Typical trigger |
| --- | --- | --- |
| **Core Reasoning** | framing, problem representation, decomposition, relationships, hypotheses, interpretation | every substantive task, starting light |
| **Deep Research** | orientation, evidence needs, retrieval, provenance, causal/systemic uncertainty, forecasting, Ultra | material evidence or frame uncertainty |
| **Decision Analysis** | alternative generation, trade-offs, preferences, robustness, opportunity cost, recommendation | choice or prioritization |
| **Execution Control** | plans, authorization, delegation, state, checkpoint/recovery, replay safety | durable work or side effects |
| **Audit / Verification** | contract checks, independent review, evaluator validity, effectiveness | material verification or closure risk |
| **Workflow Learning** | CAPA, experience reuse, negative-transfer control, eval-gated promotion | maintenance plane only |

A normal Q&A task may use only Core Reasoning and a light verification check. A research task may add Deep Research. A durable repository change may activate Execution Control. Workflow Learning does not bulk-load into ordinary user work.

---

## Three gates that should not be confused

One useful control pattern is to keep three different questions separate:

1. **Source gate** — is this source, observation, file, dataset, or private input appropriate for the question?
2. **Evidence gate** — does the inspected material actually support the claim, scope, mechanism, or decision dependency?
3. **Action gate** — is the external action authorized, in scope, and sufficiently controlled or reversible?

These are not a mandatory three-step workflow. They become relevant at different points. A trustworthy source can still fail to support a claim, and strong evidence never manufactures permission to act.

---

## Delegation: hire by bottleneck, not by agent count

Reasoning Workflow does not assume that “more agents = better.” Parallel work is useful only when the branch is separable enough and the expected benefit exceeds coordination cost.

A worker is justified when the parent task is materially waiting on something such as:

- independent research or another evidence ecosystem;
- a specialist method or language/jurisdiction;
- reproduction or adversarial verification;
- a scoped execution branch;
- repeated rework that benefits from a dedicated owner.

Before handoff, define a compact worker contract:

```text
job
allowed inputs / sources
judgment boundary
acceptance criteria
output contract
forbidden actions
uncertainty to preserve
```

Return an evidence-bearing handoff instead of a transcript dump:

```text
task | status | material output | evidence/source locators
| decisions made within scope | unresolved uncertainty
| failed routes | state/items affected | next owner / next safe action
```

When a shared workspace exists, durable evidence/state should be the internal bus; chat summaries are views of the state, not the state itself.

---

## Progressive context disclosure

Repository size, installed Skill size, and model context size are three different things.

The intended loading path is:

```text
metadata
→ SKILL.md
→ Task Profile
→ active Family
→ current unresolved gap
→ normally 1–3 relevant references
→ release / replace context when the gap changes
```

`Related` links are navigation, not auto-load instructions.

The Portable Skill currently contains dozens of small files because responsibilities are separated cleanly. That does **not** mean the model reads all of them. Most schemas and Python helpers should be executed or consulted only when their machine contract is active.

---

## Why there are Python files and schemas

The public Skill does not ship a development test/eval harness. The Python and JSON files in Portable remain because they are part of the **runtime workflow itself**, not test infrastructure.

The runtime helpers cover:

- deterministic Task Profile / Family routing;
- progressive reference selection;
- semantic state and typed dependency validation;
- execution plan/schedule/checkpoint/worker validation;
- delivery/event/raw-lineage integrity;
- dual-verification record checks;
- maintenance-plane learning gates and selective retrieval.

They are optional in the sense that a host without local script execution can still follow the semantic workflow. In that environment, the agent must not claim machine enforcement occurred.

The only Python dependency is declared in [`scripts/requirements.txt`](./skills/reasoning-workflow/scripts/requirements.txt): `jsonschema` for schema validation.

---

## Model adaptation

The workflow is optimized for GPT-5.6-class and later reasoning agents, while remaining capability-based rather than branching on every model name.

It asks what the runtime can actually do:

- preserve useful reasoning across turns;
- compact long context;
- run independent workers;
- vary reasoning effort dynamically;
- move mechanical filtering/aggregation into deterministic code;
- provide reliable tool use and state persistence.

Strong models receive more outcome-focused constraints and fewer unnecessary procedural instructions. A weaker or less reliable runtime may receive more local scaffolding. **Workflow structure itself is adaptive.**

Ultra depth does not mean every model call uses maximum compute. Spend expensive reasoning where it can reveal new structure, resolve decisive uncertainty, or synthesize difficult evidence; use cheaper/deterministic operations for mechanical work when possible.

---

## Controlled learning

Normal user tasks do not rewrite Reasoning Workflow.

Reusable rules are **earned, not merely written**. A successful-looking strategy from one run remains a candidate until evidence supports generalization.

The maintenance plane distinguishes:

- clean success → strategy lesson;
- failure → recovery → success → recovery lesson;
- success with unnecessary cost/retries/context → optimization lesson.

A retrieved lesson is challenged for applicability and negative transfer before use. Canonical changes require stronger evidence than self-reflection alone.

---

## Repository map

The public repository contains the open-source workflow itself, the runtime files that directly support it, and the small amount of documentation/metadata needed to discover, install, understand, and reuse it.

```text
.
├── README.md
├── README.zh-CN.md
├── LICENSE
├── CONTRIBUTING.md
├── PRIVACY.md
├── TERMS.md
├── .codex-plugin/
│   └── plugin.json
│
├── skills/
│   └── reasoning-workflow/          # Portable + canonical edition
│       ├── SKILL.md                 # governing entry point
│       ├── routing-index.json       # progressive routing metadata
│       ├── families/                # 6 Family indexes
│       ├── references/              # progressively loaded reasoning modules
│       ├── schemas/                 # runtime semantic contracts
│       ├── scripts/                 # runtime routing / validation helpers only
│       ├── agents/                  # OpenAI host metadata
│       └── assets/                  # icon
│
└── modular/
    ├── README.md
    └── skills/                      # lightweight independent Family Skills
        ├── reasoning-core/
        ├── deep-research/
        ├── decision-analysis/
        ├── execution-control/
        ├── audit-verification/
        └── workflow-learning/
```

### Public-repository boundary

The repository intentionally excludes development-only material that is not required to understand, install, or run Reasoning Workflow: private test/eval harnesses, benchmark fixtures, generated distribution archives, build reports, distribution tooling, and contracts with no runtime consumer.

That keeps the public surface focused on the workflow rather than on the author's engineering workspace.

### Why do the remaining files exist?

They fall into four clear groups:

| Group | Why it remains |
| --- | --- |
| `SKILL.md`, Families, references | the actual reasoning/workflow knowledge |
| schemas + runtime scripts | optional deterministic enforcement for state/routing/execution/verification |
| Modular Skills | independently browsable/installable semantic composition |
| README/license/plugin metadata | discovery, installation, licensing, host integration |

The two editions intentionally duplicate a small amount of semantic prose so both remain inspectable and installable from GitHub, while the deterministic runtime exists only once in Portable.

---

## Design principles

- **Search is downstream of reasoning.**
- **Universal entry does not mean universal full execution.**
- **Rigor is not ceremony.**
- **Representation precedes decomposition when framing is unstable.**
- **Reasoning depth is not repetition.**
- **Source count is not evidence independence.**
- **Reviewer count is not verification independence.**
- **Declared state is input; effective state is computed.**
- **Plan semantics are invariant under scheduling.**
- **Delegate by bottleneck, not by agent quota.**
- **Handoffs carry evidence/state, not transcript volume.**
- **Strong evidence does not grant action authority.**
- **Verification credit belongs only to the exact state/content verified.**
- **Learning is controlled experience reuse, not automatic self-editing.**
- **A polished answer is not proof that the workflow was followed.**
- **For Ultra: expand aggressively, prune intelligently, verify selectively.**

---

## Compatibility and references

Reasoning Workflow follows the open Agent Skills pattern: a `SKILL.md` entrypoint with optional references, scripts, and assets. Useful public references include:

- [Agent Skills specification](https://agentskills.io/)
- [OpenAI Plugins repository](https://github.com/openai/plugins)
- [Anthropic Skills repository](https://github.com/anthropics/skills)
- [Claude Code Skills documentation](https://code.claude.com/docs/en/skills)

The project deliberately uses progressive disclosure: keep the entrypoint high-signal and move conditional detail into focused references.

---

## Validation status

Deterministic checks cover routing, semantic propagation, authorization, recovery, delivery closure, review records, and controlled learning; development tests run outside the installable public tree

Real-model Task Profile classification, Skill trigger precision/recall, cross-model routing, matched Deep Research quality, token/latency savings, dual-review error reduction, long-horizon learning, and external Deep Research benchmarks remain unvalidated

Passing code checks does not establish real-agent behavioral performance

---

## Limitations

Reasoning Workflow improves process discipline; it does not provide magical guarantees.

- A model can still misunderstand instructions.
- A source can still be wrong.
- A reviewer can share the same blind spot as the solver.
- A schema can validate internal consistency without proving real-world truth.
- Tool/runtime capability varies by host.
- Model and product behavior can change over time.

For consequential work, the correct standard is still proportionate evidence, independent verification where materially useful, explicit permissions, and human/domain review where required.

---

## Contributing

The canonical implementation is [`skills/reasoning-workflow/`](./skills/reasoning-workflow/). The Modular edition is a lightweight projection of the same semantics.

When proposing a change, prefer solving a concrete failure mode with the smallest semantic change possible. Do not add a new Family, schema, workflow phase, mandatory checklist, agent count, search quota, or review layer unless the improvement clearly justifies the complexity.

See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## License

Released under [MIT License](./LICENSE).

Reasoning Workflow is intentionally versionless in public branding. The repository evolves in place; machine/plugin/schema revision fields may still exist where compatibility requires them.
