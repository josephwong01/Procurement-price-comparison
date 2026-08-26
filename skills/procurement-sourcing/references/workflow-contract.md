# Workflow contract

## Authoritative contracts

Use the frozen files when both frozen and candidate files exist:

| Stage | Contract |
|---|---|
| Requirement | `schemas/procurement-requirement-v0.2-candidate.schema.json` (and the compatible platform-scope candidate extension when needed) |
| Query | `schemas/query-plan-v0.1.schema.json` |
| Collection | `schemas/platform-adapter-result-v0.1.schema.json` |
| Candidate | `schemas/product-candidate-v0.1.schema.json` |
| Supplier | `schemas/supplier-v0.1.schema.json` |
| Match and dedup | `schemas/candidate-resolution-v0.1.schema.json` |
| TCO and score | `schemas/tco-score-v0.1.schema.json` |
| Final comparison | latest compatible `schemas/procurement-output-v0.1-candidate*.schema.json` |

Read the corresponding `docs/*v0.1.md` or `docs/requirement-schema-v0.2.md` only when field meaning or a business rule is unclear.

## Minimum run evidence

A complete run records:

- one requirement snapshot;
- one query plan;
- an adapter result for every attempted channel, including failures;
- candidate and supplier records for retained offers;
- match results and any duplicate clusters;
- a TCO/score record for each ranked candidate;
- one final procurement output;
- an end-to-end manifest naming the artifacts actually used.

Historical regression may reuse independently captured artifacts. If candidate identifiers differ across old snapshots, mark the run `PARTIAL` and state that it proves orchestration and contract compatibility, not a fresh live sourcing result.

## Status rules

- `COMPLETE`: required stages exist, validators pass, identifiers and references are consistent, and no stage is simulated.
- `PARTIAL`: the pipeline runs but a source, linkage, or business confirmation is missing. Preserve usable results and list gaps.
- `FAILED`: no usable final comparison can be produced or a required validation fails.

Never upgrade `PARTIAL` or `FAILED` merely because execution was attempted.

## Human gates

Buyer confirmation is required before treating unresolved hard requirements, supplier claims, exact freight/tax, availability, lead time, or final selection as approved. The skill may recommend what to confirm and generate an RFQ draft, but supplier contact remains out of scope for the MVP.


