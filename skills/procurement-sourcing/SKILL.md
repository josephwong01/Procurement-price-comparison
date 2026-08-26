---
name: procurement-sourcing
description: Turn a procurement need into a traceable multi-platform candidate comparison using the repository's frozen requirement, query, adapter, candidate, supplier, matching, TCO, and output contracts. Use for procurement sourcing, product comparison, supplier shortlisting, or end-to-end regression; do not use to contact suppliers, place orders, or approve purchases.
---

# Procurement Sourcing

Build a reviewable procurement shortlist without pretending that unknown data is confirmed.

## Workflow

1. Locate the repository root by finding `docs/project-roadmap.md` and `schemas/`.
2. Capture the buyer's need with the latest frozen Requirement Schema. Ask only about missing facts that would materially change search or eligibility; keep assumptions explicit.
3. Generate a Query Plan from the frozen contract. Search the buyer-named platforms first, then add no more than three relevant channels when useful.
4. Record every collection attempt through the Platform Adapter contract. Preserve source URL, observed time, original value, confidence, and access failure. Never store tokens, cookies, or authorization headers.
5. Normalize successful results into Product Candidate and Supplier records. Keep observed, claimed, estimated, conflicting, and unknown values distinct.
6. Match against the requirement and deduplicate only the comparison view. Preserve all source records.
7. Calculate CNY TCO and a single composite score with the frozen model. Show non-CNY platform prices in parentheses and never treat unknown costs as zero.
8. Produce the procurement output main table plus details, exclusions, risks, evidence, and confirmations. A recommendation is provisional until its blocking confirmations are resolved.
9. Run the repository validators, including `scripts/validate_end_to_end.py`, before calling the run complete.

For artifact selection, stopping conditions, and status rules, read [references/workflow-contract.md](references/workflow-contract.md).

## Boundaries

- Stop at a candidate pool and preliminary comparison. Do not message suppliers, negotiate, order, approve, or write to ERP/OA unless separately authorized.
- Do not bypass access controls. Record a failed channel and use an allowed fallback.
- A failed or partial stage stays failed or partial in the final report. List unfinished work explicitly.
- Frozen schemas may receive compatibility fixes only; changed semantics require a new candidate version.


