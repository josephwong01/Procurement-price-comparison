---
name: procurement-price-comparison
description: Structure enterprise procurement requirements and prepare traceable multi-platform sourcing and price-comparison work. Use when a user needs procurement requirement clarification, sourcing strategy, comparable supplier candidates, TCO normalization, supplier scoring, or an evidence-backed comparison report. Do not place orders or select a supplier without explicit human authorization.
---

# Procurement Price Comparison

Turn an informal procurement request into a reviewable requirement, then produce sourcing and comparison outputs whose assumptions and evidence can be audited.

## Workflow

1. Parse the request with `schemas/procurement-requirement.schema.json`.
2. Classify constraints as `HARD`, `PREFERENCE`, or `INFORMATION`.
3. Determine readiness. Ask at most three blocking questions per round and never silently assume quantity, delivery deadline, tax rate, substitute brand, or customization process.
4. When search is authorized, build a platform × query × filter plan.
5. Normalize candidates before comparing them. Exclude candidates that fail hard constraints.
6. Compare standardized landed cost, not display price. Keep product fit and supplier reliability as separate scores.
7. Preserve the source URL, observation time, evidence, and confidence for every material claim.
8. Present recommendations as decision support. Flag unknowns and generate an inquiry checklist for human confirmation.

## Required references

- Read `docs/schema-guide.md` when parsing or validating requirements.
- Read `docs/workflow.md` when planning sourcing, normalization, scoring, or reports.
- Read `docs/project-roadmap.md` when extending the Skill or deciding the next implementation stage.

## Boundaries

- Do not invent unavailable price, MOQ, delivery, invoice, certification, or supplier data.
- Do not treat similar-looking products as equivalent without attribute-level matching.
- Do not contact suppliers, negotiate, submit an RFQ, place an order, or write to ERP/approval systems unless the user explicitly authorizes that action.
- Use `DATA_UNAVAILABLE`, `LOGIN_REQUIRED`, `PRICE_REQUIRES_INQUIRY`, or `MANUAL_CONFIRMATION_REQUIRED` when applicable.
