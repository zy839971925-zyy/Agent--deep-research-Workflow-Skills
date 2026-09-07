# Reasoning Workflow — Architecture

Reasoning Workflow is a universal reasoning and Deep Research governing system. It keeps two first-class task-completion lanes and adds an allocation layer before expensive cognition or runtime machinery.

```text
Universal substantive-task entry
        ↓
Task Admission / Depth Gate
        ↓
Versioned Task Profile
        ↓
Deterministic Family route
        ↓
Progressive reference selection
        ↓
Universal Reasoning System
        ↓
Question / Reasoning Lane  OR  Action / Project Lane
        ↓
Depth-gated verification
        ↓
Closure

post-run only:
Trace / Eval / CAPA → Learning Plane → gated candidate promotion
```

## Separation of concerns

- **Model:** understands task semantics and forms the Task Profile.
- **Router:** maps a valid structured profile to Families and resources deterministically.
- **Reasoning system:** builds and updates the problem model, relationships, hypotheses, uncertainty, evidence needs, decisions and synthesis.
- **Machine runtime:** enforces typed state, lifecycle, Plan/Schedule, authorization, recovery, replay safety and closure.
- **Adherence engine:** checks state preconditions, transitions, observable events, tools/resource loads and validator findings.
- **Learning Plane:** learns from externally grounded outcomes but cannot self-edit canonical rules without evaluation gates.

## Two lanes remain authoritative

Depth routing is not a third lane. Swarm is scheduling. Learning is maintenance.

### Question / Reasoning Lane

```text
understand → model → reason/research → challenge → recompose → answer → verify
```

### Action / Project Lane

```text
reason → decide → plan → authorize → execute → re-observe → verify → reconcile → effectiveness → close/reopen
```

## Progressive disclosure

The repository may be large while active model context stays small. Schemas, validators and references remain available but enter model context only when the active Task Profile and unresolved gap justify them.

## Source of truth

`skills/reasoning-workflow/` is the canonical development source. Portable and Modular distributions are generated from it by `scripts/build_distributions.py` and checked with `SEMANTIC_MANIFEST.json`.
