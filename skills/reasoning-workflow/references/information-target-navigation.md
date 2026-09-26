# Information target navigation

**Trigger:** A Deep/Max/Ultra investigation is stuck at prompt keywords, an unclear decomposition, repetitive search results, or uncertainty about where a decisive observation would appear.

**Reads:** the user's real question, current problem model, live explanations, available evidence surfaces, and failed routes.

**Updates:** the problem representation, answer-bearing dependencies, next information target, predicted observations, evidence route, and the model after observation.

**Exit:** a useful observation changes or bounds the answer, or the next target has too little answer gain to justify its cost. Return to [inquiry and research](inquiry-and-research.md) for synthesis.

## Navigate from the question to an observation

Treat a search string as the last, lossy projection of a research decision. Use this small loop only for a material gap:

`problem representation → answer-bearing dependency → information target → response field → observation method → model update`

1. **Represent the question.** Specify what the user would count as an answer: a fact, a causal explanation, a comparison, or a decision under constraints. If the framing is uncertain, consider a second materially different representation. Keep it only if it changes what would count as evidence. Orientation can discover the vocabulary or actors needed to build the model.
2. **Decompose at the dependency.** Ask which premise, mechanism, comparison, or boundary the answer depends on. Split a branch only when its parts require different observations; record how the parts will recompose into the original question. A list of nouns from the prompt is not a decomposition.
3. **Set an information target.** State a specific uncertainty and what possible result would change the answer, confidence, boundary, or next action. For rival explanations, seek an observation they predict differently. If all live explanations predict the same result, that result is not the next target.
4. **Find the response field.** Ask where those different predictions would leave an observable trace: a controlled comparison, raw record, runtime trace, dataset, version history, affected-user report, or another surface. Map the expected signal under each explanation, who produces the record, when it is recorded, what is missing, and whether two apparent sources share an origin. Choose a feasible field that exposes the difference with the fewest material confounders.
5. **Choose an observation method.** Inspect a supplied file, run a permitted experiment, follow citations, query a database, interview when authorized, or search the web. Only now translate the target and field into exact identifiers, measurements, time windows, terms, and source constraints for the available interface.
6. **Update the model.** Inspect the underlying material. Note whether it distinguishes the explanations, exposes a new variable, contradicts the frame, or merely repeats the same provenance. Follow a changed dependency to its downstream conclusions. Pick a new target, change fields, or stop with a bounded answer.

The response field is more precise than a category of websites: it describes **how the world would respond under each live explanation**, where that response could be seen, and why the observation would be interpretable. A missing search result has weak meaning when the record may never have been published or indexed.

## Small working card

Use this internally for a long branch; skip the card when the target is already clear. It need not become a schema or an output section.

```text
User question / useful answer:
Current representation and decisive dependency:
Live alternatives or range:
Information target — what result would change the answer?:
Response field — predicted traces, record origin, confounders:
Next observation / route (query only if search is the right method):
Observed difference → model update / next target / bounded stop:
```

## Example: a claim of longer battery life

Question: “Does the new battery chemistry last longer in practice?” The initial wording hides a comparison problem: *cycle retention under like-for-like use* differs from advertised calendar life or a device-level runtime gain.

| Step | Research decision |
| --- | --- |
| Dependency | Does the gain persist at the same temperature, charge limits, discharge rate, and end-of-life threshold? |
| Alternatives | Chemistry improves retention; or a gentler charging protocol explains the reported gain. |
| Information target | A matched cycle-life comparison: does the advantage survive the same protocol? A gain that vanishes would narrow the claim to the protocol. |
| Response field | Test methods and per-cycle capacity curves, ideally from an independent lab as well as the maker. Predict persistent separation under the chemistry explanation and reduced separation under the protocol explanation; inspect cell differences and censoring. |
| Observation method | Locate the exact cell/version and test protocol first. Then search within papers, lab datasets, or technical reports using the cell identifier plus `cycle retention`, temperature, charge window, and rate. |
| Update | If comparable curves are unavailable, report what the published tests establish and leave the like-for-like longevity claim unresolved. Rephrasing “battery lasts longer” into five web queries would not close this gap. |

The same navigation applies to code investigations: if “the agent got worse after an update” might reflect retrieval coverage or answer synthesis, a paired run's retrieved passages and cited answer spans are response fields. Search release notes only if the traces make a version change a live causal dependency.

## Path reset

When repeated queries return the same publisher, syndicated claims, or evidence that every hypothesis predicts, do not keep replacing synonyms. Change one upstream choice: the representation, the pivotal dependency, the target observation, or the response field. If no feasible field can distinguish the explanations, retain both and state the resulting limit instead of manufacturing certainty.

[← Return to root workflow](../SKILL.md)
