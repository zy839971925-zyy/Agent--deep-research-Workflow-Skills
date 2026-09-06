# Reasoning Workflow

Package release: **V5 — Semantic Enforcement Release**

This README is for humans and successor Agents who need to understand, audit, extend, or hand off the package. It is intentionally **not required by the runtime routing path**. The runtime entry is `SKILL.md`.

## V5 semantic enforcement

V5 freezes the two-Lane cognitive architecture and moves the main engineering effort into formal semantics. The governing rule is **Declared state is input. Effective state is computed.** Typed schemas define record-local meaning; a shared edge policy defines dependency/reference semantics; validators compute transitive stale/recompute states, explain closure blockers, reconcile delivery claims with canonical state, and validate event/raw lineage.

The acceptance hierarchy is: **type validity → graph validity → effective-state computation → closure semantics → integrity → decision/measurement structure → behavioral evaluation**. Validators certify structural admissibility, not epistemic truth.

New specialist references cover [semantic state contract](references/semantic-state-contract.md), [decision and recommendation quality](references/decision-and-recommendation.md), and [measurement and operationalization](references/measurement-and-operationalization.md). Machine semantics are centralized in `schemas/edge-policy.json` plus the Draft 2020-12 schemas; `scripts/semantic_core.py` is the shared execution engine.

## What this Skill is

`reasoning-workflow` is a general governing process layer for substantive work. It is designed to answer two independent questions well:

1. **Did the Agent actually understand and reason about the problem correctly?**
2. **If the task became persistent work, did the reasoning/research/decision/execution remain synchronized, traceable, complete, recoverable, and verifiable?**

It is not a project-management framework with a lightweight Q&A mode. Question answering, interpretation, diagnosis, explanation, verification, comparison, forecasting, and judgment are first-class complete tasks.

It is also not a replacement for specialist Skills. It governs how specialist work is framed, integrated, checked, and closed.

## Core architecture

```text
                         USER INTENT
                              │
                   EPISTEMIC TASK / OUTCOME
                              │
                    REVISABLE PROBLEM MODEL
                              │
               ┌──────────────┴──────────────┐
               │                             │
               ▼                             ▼
     QUESTION / REASONING LANE       ACTION / PROJECT LANE
               │                             │
 understand → essence/model          cognitive lane first
 → premises → decompose              → risk / change control
 → relationships                     → execute / re-observe
 → competing explanations            → verify / validate
 → uncertainty                       → reconcile / effectiveness
 → research/challenge                → close / reopen
 → recompose/answer
               │                             │
               └──────────────┬──────────────┘
                              ▼
                        USER OUTCOME
```

The Action lane extends the cognitive lane. It never replaces problem understanding with procedural control.

## The Question / Reasoning Lane

The Question lane exists to protect the original purpose of this project: an Agent should not jump directly from prompt wording to an answer or a search query.

It first identifies the **epistemic task**. Examples include:

- fact confirmation;
- causal explanation;
- mechanism analysis;
- truth/rumor verification;
- comparison;
- diagnosis;
- interpretation of a statement/person/context;
- forecasting;
- judgment or decision;
- forming a reasoned viewpoint.

It then builds a revisable model that distinguishes:

`fact / observation / premise / assumption / hypothesis / inference / judgment / recommendation / unknown`

### Premise management

A premise is any proposition a material reasoning step depends on. A premise can be an observation, definition, user constraint, retrieved fact, assumption, or earlier inference.

When an upstream premise changes, dependent reasoning must not silently remain current.

Example:

```text
P2 changed
  ↓
I3 inference           stale
C2 conclusion          stale
D4 decision            stale
A1 artifact            stale
V3 verification        rerun required
```

This is why premise/dependency tracking connects the Question lane to the Runtime layer.

### Decomposition and recomposition

Decomposition is a reasoning tool, not a ritual framework.

A useful decomposition tries to preserve:

- low unnecessary overlap;
- coverage of answer-bearing dependencies;
- coherent analytic levels;
- visible dependencies between branches.

The critical test is **recomposition**:

> If every subquestion were answered perfectly, would those answers be sufficient to answer the parent question?

If not, the decomposition is missing a bridge, mixing levels, or solving the wrong problem.

The workflow therefore avoids treating MECE, taxonomies, or issue trees as automatic truth. When the problem is not already well structured, a safer sequence is:

```text
concrete observations
        ↓
recurring pattern
        ↓
consequential relationship
        ↓
mechanism / essence
        ↓
abstraction / taxonomy
```

Classification compresses understanding after useful structure exists; it should not substitute for mechanism analysis.

### Induction, abduction, deduction

The workflow can combine three reasoning operators:

```text
induction:  observations → tentative pattern/generalization
abduction:  observations → plausible explanation(s)
deduction:  premises/hypothesis → implications/predictions
```

For diagnosis or explanation, a useful loop is:

```text
observation
   ↓
abduction
   ↓
competing hypotheses
   ↓
deduction of discriminating predictions
   ↓
evidence
   ↓
induction / model revision
```

The first plausible explanation is not promoted to fact simply because it is coherent.

### Relationships are typed

The workflow does not treat every link as generic “relatedness.” Important relationships can be distinguished as:

`causes`  
`correlates_with`  
`depends_on`  
`enables`  
`constrains`  
`mediates`  
`moderates`  
`precedes`  
`is_part_of`  
`is_example_of`  
`is_alternative_to`

Complex problems can also require feedback, delay, thresholds, adaptation, expectations, path dependence, common causes, confounding, selection, reverse causality, substitutes, complements, and external forces.

A relationship is pursued only when resolving it can change the answer, prediction, judgment, decision, design, or action.

## Inquiry / research is model-driven

Research is not automatic web search.

The workflow asks:

1. What is missing?
2. Why would this unknown change the answer?
3. What observation would support, distinguish, or falsify the current explanations?
4. Which evidence surface is closest to that observation?

Research questions are derived from the problem model, premises, hypotheses, and relationship structure. Search strings are downstream implementation details.

The workflow distinguishes:

- **answer uncertainty** — the question is well formed but the answer is unknown;
- **frame uncertainty** — the current problem space itself may be incomplete or wrong.

Frame-uncertain work uses:

`ORIENT → EXPAND → MAP → FOCUS`

before deep narrowing.

## Evidence quality

Evidence is not ranked only by institutional prestige.

A material source is evaluated for **position to know**:

- Did it have access to the event/system/data?
- Could its method observe the proposition?
- Does time/entity/version/population match?
- Is it direct knowledge, measurement, inference, hearsay, or copied reporting?
- What incentives or selection effects matter?
- Is apparent corroboration actually one provenance chain?

Official sources are often strongest for official policy or official statements. Operators/users may be better positioned to report lived implementation. Neither automatically proves hidden mechanisms or population-wide prevalence.

Evidence should also have **discriminating value**. Ten redundant sources are often weaker than one observation that separates two live hypotheses.

## Uncertainty is structured

When uncertainty is material, the workflow tries to locate its cause:

- missing evidence;
- source conflict;
- measurement uncertainty;
- definition/scope mismatch;
- premise/model uncertainty;
- causal uncertainty;
- future behavioral or external uncertainty.

The goal is not to eliminate every uncertainty. It is to reduce the uncertainties that can still change the user's answer or action, and explicitly bound the rest.

## Challenge and falsification

For a material conclusion, normal reasoning asks:

- What would make the answer change?
- Which premise would collapse the conclusion if false?
- What counterexample or contrary observation exists?
- What competing explanation also fits the observations?
- What evidence best distinguishes them?

Challenge is not reserved for high-risk project audits.

## Research stopping

The workflow does not stop because it reached a source/search quota.

A branch stops when another feasible inquiry has low expected **answer gain** relative to cost, or cannot materially change the parent answer.

Needle-in-a-haystack discovery may justify a few independent search trajectories. Multi-claim research usually benefits more from evidence-gap decomposition. Model agreement is never treated as empirical independence.

## System invariants

Every substantive task should preserve these qualities proportionately:

1. **Traceable** — important reasoning and work can be traced to its basis.
2. **Readable** — current state and rationale are understandable to a human/successor Agent.
3. **Synchronized** — upstream changes invalidate/update dependents.
4. **Original-preserving** — raw/source material is distinct from descendants.
5. **Complete** — original question/requirements and blockers have explicit disposition.
6. **Consistent** — canonical state, answer, runtime observations, and artifacts reconcile.
7. **Durable/recoverable** — long work can checkpoint/resume when runtime allows it.
8. **Fast/proportionate** — the workflow stays lightweight when the task is simple.

These are invariants, not mandatory artifacts.

## Effort vector

The workflow separately calibrates:

- reasoning breadth;
- evidence depth;
- challenge depth;
- verification depth;
- governance depth.

`Light / Standard / Deep / Max` are convenient presets. They are not fixed protocols or token budgets.

## Durable work architecture

For tasks that actually need persistence, the logical model is:

```text
PRESERVED HISTORY
raw inputs + observations + state-changing events
                  │
                  ▼
CANONICAL CURRENT-STATE PROJECTION
objective / requirements / questions / premises / evidence /
hypotheses / uncertainty / decisions / risks / actions /
artifacts / verification / effectiveness
                  │
         ┌────────┼────────┐
         ▼        ▼        ▼
       report    code     slides / UI / other views
```

Historical records answer **what happened and why**. The canonical projection answers **what is current now**.

The package does not promise transactional durability where the host environment cannot provide it.

## State and dependency propagation

Durable state can represent typed dependencies such as:

`depends_on`  
`derived_from`  
`supports`  
`contradicts`  
`premise_refs`  
`implements`  
`produces`  
`represents`  
`verifies`  
`monitors`  
`supersedes`  
`invalidates`

When a dependency/premise becomes stale, a current-like dependent cannot remain silently current.

## Raw versus derived material

Transformations create descendants, not silent replacements.

```text
RAW-001 original.jpg
  ├── DER-001 crop
  ├── DER-002 enhancement
  │      └── OCR-001
  └── OBS-004 visual observation
          └── INF-003 interpretation
```

When feasible/useful, records can preserve locator, retrieval/observation time, source version, visibility, and content hash/fingerprint.

## Completeness and question integrity

There are two different closure problems:

### Epistemic closure

Is another feasible inquiry likely to materially improve the answer?

### Delivery/action closure

Have the requested requirements, artifacts, blockers, verification, reconciliation, and effectiveness states been dispositioned?

For Question-lane work there is also a **question integrity** check:

- Did the answer drift into a nearby easier question?
- If decomposed, does recomposition actually answer the parent question?
- Are material premises still current?
- Are fact, inference, judgment, and recommendation appropriately distinguished?

## Specialist Skills

`reasoning-workflow` is an orchestration/governing layer.

It should compose with specialist capabilities:

```text
reasoning-workflow + product-design
reasoning-workflow + data-analysis / spreadsheet
reasoning-workflow + PDF / document tooling
reasoning-workflow + coding / repository tools
```

The specialist owns domain-specific execution. `reasoning-workflow` owns framing, inquiry quality, integration, state/traceability policy, verification, reconciliation, and closure.

## Package structure

```text
reasoning-workflow/
├── README.md
├── SKILL.md
├── agents/openai.yaml
├── assets/icon.svg
├── references/
│   ├── reasoning-structure-and-decomposition.md
│   ├── inquiry-and-research.md
│   ├── problem-framing-and-effort.md
│   ├── hypotheses-and-bias-control.md
│   ├── relationships-and-systems.md
│   ├── evidence-and-provenance.md
│   ├── retrieval-and-observation.md
│   ├── human-context-and-interpretation.md
│   ├── time-scenarios-and-forecasting.md
│   ├── multimodal-and-data.md
│   ├── state-model-and-invariants.md
│   ├── synchronization-and-recovery.md
│   ├── runtime-and-delegation.md
│   ├── traceability-and-integrity.md
│   ├── change-governance-and-effectiveness.md
│   ├── synthesis-execution-and-verification.md
│   ├── formal-review-and-audit.md
│   ├── domain-patterns.md
│   └── worked-examples.md
├── schemas/
├── scripts/
└── tests/
```

## Reference module contract

Each runtime reference uses a compact contract:

- `Trigger`
- `Reads`
- `Updates`
- `May invalidate`
- `Must verify` where applicable
- `Exit`
- `Related`
- `Return`

References link back to the root workflow. `SKILL.md` remains the total runtime router.

## Validators and regression cases

The deterministic scripts validate structure and invariants, not semantic truth:

`validate_skill.py` / `validate_links.py` use only the standard library. Semantic Draft 2020-12 validation uses `jsonschema>=4.18,<5` (declared in `scripts/requirements.txt`); if unavailable, semantic validators fail explicitly rather than silently falling back to a weaker rule set.

- `validate_skill.py`
- `validate_links.py`
- `validate_state.py`
- `validate_delivery.py`
- `validate_events.py`
- `validate_raw.py`
- `evaluate_run.py` (observable behavioral run artifacts only; never hidden chain-of-thought)

The existing 24 behavioral cases under `tests/cases/` remain the regression specification set. V5 does not expand the case count merely to add prose coverage; instead each case now has an `observables` contract and `evaluate_run.py` can score externally produced run artifacts against expected/forbidden events, final-state fields, and required finding codes. The package still does not claim that these cases have been executed against every model/runtime.

A behavioral run artifact records only observable process events, for example `lane_selected`, `orientation_started`, `effective_state_recomputed`, `stale_propagated`, `closure_attempted`, `verification_completed`, or `work_reopened`, plus public final state/findings/output references. It must never require hidden chain-of-thought. Case events can use exact fields or `_any_of` matchers.

Important epistemic regression cases include open inquiry, decomposition/recomposition, premise invalidation, question drift, alternative explanation, uncertainty typing, source position-to-know, and research stopping.

## Direct ZIP use

When the ZIP is attached rather than formally installed, instruct the Agent to read `reasoning-workflow/SKILL.md` and apply it as the governing workflow for subsequent substantive tasks in the conversation.

The ZIP cannot grant unavailable tools or persistence.

## Design boundary

The package deliberately does **not** require every task to create durable state, a project dossier, a research report, a risk matrix, or web searches.

A one-sentence interpretation may use:

`understand → model → answer → check`

An open research problem may use:

`understand → orient → decompose/recompose → model → research → challenge → synthesize → verify`

A durable consequential change may use both the complete cognitive lane and the runtime/change-control machinery.

The central design rule is:

> **Do not let workflow machinery replace thinking; do not let good thinking disappear when work becomes long, mutable, or operational.**
