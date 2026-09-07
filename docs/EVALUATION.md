# Reasoning Workflow — Evaluation Report

## Executive result

The deterministic routing/runtime architecture is implemented and regression-tested. The current environment did **not** provide an isolated multi-model Agent runner suitable for matched generation experiments, so the most important model-level claim remains:

> **Deep Research generation-quality non-inferiority is NOT YET EMPIRICALLY VALIDATED.**

Unit tests, routing fixtures, context counts and adherence validators are not presented as substitutes for live-agent quality evaluation.

## Frozen baseline

Before the depth-gated routing transition, the frozen baseline had:

- root `SKILL.md`: 303 lines / 20,991 characters;
- 22 references / 2,314 reference lines;
- 50 / 50 unit/regression tests passing;
- 24 behavioral specifications;
- 6 runtime fixtures;
- no first-class machine-readable Family/reference route;
- adherence driven more heavily by same-run event/sequence obligations.

## Current deterministic regression

Current suite: **79 / 79 PASS**.

Test groups include routing, context, adherence, learning, Deep Research contract, distribution, runtime semantics, state semantics, recovery and delivery validation.

## Routing evaluation

A deterministic profile-to-route matrix covers 18 Task Profiles: simple negative controls and Deep/Max research/action categories.

- expected Family routes: **18 / 18**;
- Light negative controls stay in Core Reasoning without Deep Research, Swarm, durable runtime, or dual review;
- Deep Research profiles add Deep Research and depth-appropriate verification;
- decision-grade research adds Decision Analysis;
- checkpoint/resume and serial-vs-Swarm cases add Execution Control without changing the reasoning lane.

This validates the **router implementation**, not real-model Task Profile classification accuracy.

## Static context comparison

These are character/line proxies, not measured production input tokens.

| Measure | Result |
| --- | ---: |
| Frozen root | 20,991 chars / 303 lines |
| Current portable root | 11,375 chars / 197 lines |
| Root character reduction | 45.8% |
| Frozen root + all references | 159,193 chars — artificial bulk-load upper bound |
| Portable routed context, 18-profile mean | 22,039 chars |
| Portable routed range | 12,670–35,272 chars |
| Modular routed context, mean | 11,539 chars |
| Modular routed range | 1,633–25,235 chars |
| Mean references selected per profile | 1.28 |

The bulk-load comparison is an upper bound only; it does not claim the frozen workflow actually loaded every reference on every task.

Light tasks with no unresolved structured gap select zero references beyond the root/family entry context.

## Reference Load Precision

Observable reference loading records `reference_id`, `family`, `load_reason`, `current_gap`, and `profile_version`. Live traces can additionally record `reference_used` / `reference_contributed` so unused-reference rates can be measured.

Static tests prove:

- unselected Family references are rejected;
- `Related` does not trigger cascade;
- per-phase reference limits are enforced;
- stale profile routes cannot continue after depth re-evaluation.

Real unused-reference rates are not yet empirically measured.

## Adherence evaluation

Deterministic protocol cases verify that:

- orientation retrieval can precede a stable problem model when an orientation goal exists;
- evidence retrieval without an evidence need is rejected;
- restored/canonical problem model + evidence need can satisfy prerequisites without same-turn creation events;
- Skill defaults cannot override explicit user instructions except separately governed safety/authorization constraints;
- reference loads must match active Family/route/profile;
- Worker execution needs valid Plan/node-contract state;
- high-authority side effects require authorization;
- depth-gated independent review is required before closure when requested by the route.

Real-model Skill trigger recall/precision, Family selection and end-to-end protocol behavior remain pending.

## Dual-layer verification

Machine checks include:

- dual mode requires Layer 2;
- reviewer context cannot be the solver context;
- full solver reasoning transcript is rejected as Layer-2 input by default;
- orthogonal mode requires an independence basis beyond fresh context;
- review conflict cannot close by majority vote and must reopen/reconcile disputed state;
- Light/Standard tasks are not forced through a second reviewer.

## Deep Research benchmark adaptation

`evals/deep-research/` defines adapters and metrics rather than copying external benchmark corpora. The evaluation design draws from FutureSearch Deep Research Bench, DeepResearch Bench, DeepResearch Bench II, and ReportBench.

Metrics remain separate rather than collapsing into one universal score: root-question fidelity, framing, frame discovery, causal coverage, evidence-need quality, citation accuracy, provenance/source independence, factual correctness, recall, analysis, synthesis, competing explanations, uncertainty calibration, drift, premature closure, efficiency, unnecessary search, context, reference loads, tool calls and runtime.

## What has not yet been run

- isolated matched model generations across frozen/current/minimal variants;
- cross-model or cross-runtime adherence;
- full benchmark report grading;
- live latency/token/tool-call quality trade-offs;
- measured dual-review error reduction;
- long-horizon learning effectiveness and harmful-memory rates.

Context reduction is therefore a **candidate optimization** that must be reversed or adjusted if future live Deep/Max evaluation shows material quality degradation.

## Non-inferiority policy

Concrete benchmark runs should freeze non-inferiority margins **before** viewing generation results. High-value Deep/Max dimensions should show no practically meaningful degradation versus the frozen baseline. Context or latency gains do not excuse material loss in root-question fidelity, factual/citation quality, causal coverage, analysis, or synthesis.
