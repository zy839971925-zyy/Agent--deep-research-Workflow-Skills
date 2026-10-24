# Measurement and operationalization

**Trigger:** An abstract construct is being judged through metrics, benchmarks, proxies, KPIs, survey items, model scores, measurements, or effectiveness indicators.

**Reads:** target construct, user objective/decision, candidate measures, data-generating process, uncertainty, alternative measures.

**Updates:** measurement records, proxy/construct mapping, validity limits, decision relevance, measurement uncertainty.

**May invalidate:** evidence interpretation, judgment, recommendation, KPI design, effectiveness conclusion, benchmark comparison.

**Must verify:** what is actually measured, construct validity, measurement uncertainty, temporal/population fit, proxy failure modes, and whether the construct matters to the decision.

**Exit:** the measure is either justified for its intended construct/decision use or explicitly bounded as a proxy with known divergence risk.

**Related:** [multimodal and data](multimodal-and-data.md), [decision and recommendation quality](decision-and-recommendation.md), [evidence and provenance](evidence-and-provenance.md).

**Return:** [root workflow](../SKILL.md) → Model / evidence / decision.

## Keep semantic layers distinct

`measurement validity ≠ decision relevance`

A metric can accurately measure a construct that is only weakly relevant to the user's real objective. Conversely, a decision-relevant construct may have only imperfect proxies.

Examples:

- market size can be measured well but does not by itself operationalize “worth entering”;
- benchmark score can measure benchmark performance without representing the user's production task;
- sales growth can measure sales without proving net value or causal effectiveness.

## Operationalization questions

Before leaning on a proxy, ask:

1. What construct does the user actually care about?
2. What observable quantity is being used as the operational measure?
3. Why should the measure track the construct in this population/time/context?
4. Where can measure and construct diverge?
5. What alternative measure should disagree if the operationalization is wrong?
6. Even if valid, how much does this construct affect the final decision?

## Measurement record

Durable work can store:

`id | construct | operational_measure | method/source | validity_status | uncertainty | valid_for | objective_refs | decision_relevance | alternative_measure_refs | premise_refs`

Use measurements as evidence only within their validated scope. Do not upgrade a convenient proxy into the construct itself.

## Measurement chains

For high-consequence metrics, benchmarks, graders, surveys, or proxies, trace enough of the measurement chain to know where validity can fail:

`construct → observable signal → collection/selection → transformation → metric/rubric → interpretation → decision`

A benchmark or judge is not outside the workflow; it is another measurement system. If a material audit, recommendation, or learning promotion depends on its score, validate the measurement's scope and failure modes before treating the score as ground truth.

[← Return to root workflow](../SKILL.md)
