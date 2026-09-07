# Architecture Migration

The current architecture preserves the Universal Reasoning Spine, the two first-class lanes, typed lifecycle/state semantics, Plan/Schedule separation, Worker proposal authority, Checkpoint/Recovery and Replay Safety.

The major transition is allocation and progressive routing:

1. Task Admission / Depth Gate is a formal Task Profile rather than prose only.
2. Task Profile revisions can re-route Skills/resources; depth may escalate or de-escalate.
3. References are progressively loaded through `routing-index.json` and Family indexes; `Related` never auto-loads.
4. Adherence uses state preconditions, valid transitions and observables rather than same-turn event presence alone.
5. Dual-layer verification is depth-gated and distinguishes fresh-context review from truly orthogonal review.
6. Workflow Learning is an isolated maintenance plane with CAPA and eval-gated promotion/rollback.
7. Portable and modular packages are generated from one canonical source and share machine semantics by hash.

No third reasoning lane is introduced. Swarm remains a scheduling strategy beneath Action / Project work.
