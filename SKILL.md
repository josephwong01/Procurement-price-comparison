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
4. Before candidate selection, optionally run social trend discovery: extract and score keywords, read only approved official APIs or low-volume public pages, and produce evidence-linked direction signals. Social signals expand directions but never replace platform verification.
5. Build a platform × query × filter plan, then keep a complete candidate pool with user additions, explicit exclusions, budget risks, and unresolved candidates.
6. Before collection, let the buyer choose Console/browser execution or authenticated API/adapter execution. Read `skills/procurement-sourcing/references/api-routing.md`; record every attempt in `api-incident-log.md` without storing secrets.
7. Normalize candidates before comparing them. Exclude candidates that fail hard constraints and use the documented same-direction fallback when validation fails.
8. Before final scoring, show the scoring dimensions and default weights. Let the buyer keep or adjust them, then recompute every candidate under one selected weight set. Read `skills/procurement-sourcing/references/scoring-weights.md`.
9. Compare standardized landed cost, not display price. Keep product fit, supplier reliability, and unresolved procurement risks separate.
10. Preserve the source URL, observation time, evidence, confidence, run/dataset IDs, cost, and access status for every material claim.
11. Present recommendations as decision support. Flag unknowns, exclusions, API failures, and generate an inquiry checklist for human confirmation.

## Required references

- Read `docs/schema-guide.md` when parsing or validating requirements.
- Read `docs/workflow.md` when planning sourcing, normalization, scoring, or reports.
- Read `docs/project-roadmap.md` when extending the Skill or deciding the next implementation stage.

## Boundaries

- Do not invent unavailable price, MOQ, delivery, invoice, certification, or supplier data.
- Do not treat similar-looking products as equivalent without attribute-level matching.
- Do not bypass social-platform login, CAPTCHA, rate limits, robots rules, or access controls. Do not use Apify Actors or third-party scraping services for Reddit/X social-trend collection. Apify Actors may be used for authorized e-commerce comparison when cost, source, and access status are recorded.
- Do not use CAPTCHA bypass, proxy/fingerprint evasion, cookie theft/reuse, unauthorized bulk extraction, or infinite retries. A Console route is an allowed fallback, not proof that an API/MCP channel exists.
- Do not contact suppliers, negotiate, submit an RFQ, place an order, or write to ERP/approval systems unless the user explicitly authorizes that action.
- Use `DATA_UNAVAILABLE`, `LOGIN_REQUIRED`, `PRICE_REQUIRES_INQUIRY`, or `MANUAL_CONFIRMATION_REQUIRED` when applicable.
