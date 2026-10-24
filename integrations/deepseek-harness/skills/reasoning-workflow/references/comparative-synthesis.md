# Comparative evidence synthesis

**Trigger:** Several empirical studies, technical reports, models, or benchmarks are being compared and their apparent differences may reflect mismatched versions, populations, conditions, methods, or metrics.

**Do not load for:** A simple comparison with directly commensurable facts, or a question that only needs one source.

## Extract before comparing

Create a compact comparison card for each study or result. Capture only fields that affect interpretation:

| Field | Record |
| --- | --- |
| Identity and time | Exact paper/report, version/model, date, publication or correction status |
| Target and sample | Population, task, dataset, inclusion/exclusion, setting, and denominator |
| Design | Research design, intervention/comparator, protocol, time horizon, and relevant controls |
| System conditions | Model/checkpoint, prompt, tools, context, compute/budget, hardware, and evaluator where applicable |
| Outcome | Metric definition, unit, aggregation, effect/estimate, uncertainty interval or reported variance |
| Validity limits | Selection, confounding, measurement, benchmark contamination, missing data, external validity |
| Provenance | Primary source, reused data, sponsor/affiliations/conflicts, linked reports or source family |

Do not fill missing fields by guessing. Mark them unknown and decide whether the omission could change the comparison.

## Establish comparability

First state the estimand or question the comparison is meant to answer. Align task, population, version, protocol, metric, denominator, time window, and resource budget. A shared label such as “accuracy,” “efficacy,” or “benchmark score” is not enough if its operational definition differs.

- If the core target and measurement are sufficiently aligned, compare the results and retain their uncertainty.
- If only some conditions align, compare within those strata and name the boundary.
- If results answer different questions, present them side by side without ranking or pooling.
- Do not calculate a pooled effect or declare a winner unless the data and design justify that operation.

## Reconcile disagreements

When results disagree, test scope, model or intervention version, sampling, evaluator, prompt/tool budget, measurement, denominator, uncertainty, source lineage, and conflicts of interest before treating the disagreement as a true contradiction. Preserve negative findings and failed replications. Distinct sources that reuse one dataset or evaluation pipeline are not independent replication.

For model or benchmark comparisons, record whether the system had the same tools, search corpus, context, token/compute budget, and stopping rules. A performance difference under unequal conditions does not isolate a model effect.

## Use the card to improve the research frontier

After extracting the cards, identify which mismatch or missing datum could actually change the answer. If one can, name the exact source, table, appendix, or reproduction that could resolve it and pursue that next. Otherwise bound the comparison and stop. The card is an internal aid, not a mandatory table in every user-facing response.

[← Return to Deep Research](../families/deep-research.md)
