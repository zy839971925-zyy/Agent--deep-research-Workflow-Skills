# Multimodal and data evidence

**Trigger:** Claims depend on images, charts, tables, datasets, audio, video, OCR/transcription, or calculations.

**Reads:** original modality/data, metadata, task claim, transformation/calculation requirements.

**Updates:** observations, derived records, calculations, transformation lineage, limitations.

**May invalidate:** claims based on transcription/OCR/chart-reading/calculation errors or transformed material mistaken for original.

**Exit:** relevant modality/data has been inspected/processed with lineage and uncertainty preserved.

**Related:** [evidence and provenance](evidence-and-provenance.md), traceability and integrity (route to the relevant sibling Skill if needed), [retrieval and observation](retrieval-and-observation.md).

**Return:** [root workflow](../SKILL.md) → Evidence / Verification.

Use when conclusions depend on images, PDFs, charts, tables, spreadsheets, datasets, audio, video, OCR, metadata, or calculations.

## Observe the right modality

Extraction can lose layout, legends, footnotes, merged cells, visual emphasis, signs, units, or speaker/timing information. Inspect the original modality when those affect a material claim. If the modality cannot be inspected, narrow the claim instead of inventing details.

Retain useful locators: page/figure/table, slide, sheet/cell, image region, timestamp, file version, or code location. Distinguish original pixels/audio, OCR, transcripts, metadata, derived data, and secondary descriptions.

## Tables and charts

Check units, axes, log scales, denominators, frequency, sample scope, missing values, footnotes, revisions, and comparison periods. OCR may swap signs, decimals, labels, or columns. Prefer underlying data for exact quantities; label visual estimates.

A chart association does not establish causation. A generated illustration is not measurement evidence.

## Calculations and data transformations

Separate source inputs, transformations, assumptions, and derived results. For consequential numbers, retain reproducible formulas or computations and input locators. Align currency, date, nominal/real, stock/flow, unit, population, and category definitions.

Inspect missingness, selection, revisions, measurement changes, and overlap. Do not pool incompatible metrics or studies merely to obtain one number.

## Audio and video

A transcript can support spoken words within transcription limits, not visual actions. Sparse frames do not establish continuous behavior. Preserve consequential uncertainty about speaker, timing, cuts, or editing. Use native media capabilities where available instead of pretending a text transcript captures the full evidence.

## Data-generating process and selection path

Before treating a dataset as a window onto reality, ask how reality became the observed data:

`real event/population → measurement → collection → eligibility/selection → recording → cleaning/transformation → stored dataset → analysis`

A numerically correct analysis can still be substantively wrong when the selection path excludes the cases that matter. Inspect non-observation, non-reporting, survivorship, changed definitions, instrumentation changes, missing groups, duplicated units, and incentives that affect what gets recorded. Use this only when selection could change a material claim; do not turn every small table into a full causal data audit.

[← Return to root workflow](../SKILL.md)
