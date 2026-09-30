---
name: procurement-price-comparison
description: Structure enterprise procurement requirements and prepare traceable multi-platform sourcing and price-comparison work. Use when a user needs procurement requirement clarification, sourcing strategy, comparable supplier candidates, TCO normalization, supplier scoring, or an evidence-backed comparison report. Do not place orders or select a supplier without explicit human authorization.
---

# Procurement Price Comparison

Turn an informal procurement request into a reviewable requirement, then produce sourcing and comparison outputs whose assumptions and evidence can be audited. This Skill has two explicit modes; do not silently mix them.

## Mode routing

### A. Product-selection mode

Use when the buyer asks what products or directions would be suitable, gives a use case but no fixed product list, or wants new candidates discovered. Freeze the requirement, optionally use social trend discovery, build and score a direction/candidate pool, let the buyer confirm the shortlist, then collect prices. The Munich 2026 electronics-show S+ prize request (technology-forward, foreign-user friendly, CNY 1,000/unit, quantity 2) is the reference regression case.

### B. Multi-platform price-comparison mode

Use when the buyer supplies named products, item IDs, URLs, or a fixed shortlist. Do not invent new directions or run social discovery unless explicitly requested. Collect comparable offers across the requested platforms, normalize specification/condition/quantity/shipping/tax, calculate landed cost and confidence, and rank the supplied products. The coffee-machine request is the reference regression case: start from the supplied coffee-machine links and compare them; do not turn it into an open-ended product search.

If the buyer asks for both, complete mode A through shortlist confirmation, then start mode B. If intent is ambiguous, ask one routing question: “Do you want candidate discovery, fixed-list price comparison, or both?”

## Workflow

1. Route to mode A or B before collecting anything. Parse the request with `schemas/procurement-requirement.schema.json`.
2. Classify constraints as `HARD`, `PREFERENCE`, or `INFORMATION`.
3. Determine readiness. Ask at most three blocking questions per round and never silently assume quantity, delivery deadline, tax rate, substitute brand, or customization process.
4. In mode A, optionally run social trend discovery before candidate selection. In mode B, skip it unless explicitly requested.
5. Build a platform × query × filter plan. Mode A keeps a complete candidate pool; mode B keeps the buyer's fixed list and records any rejected item with its reason.
6. Before collection, let the buyer choose Console/browser execution or authenticated API/adapter execution. Read `skills/procurement-sourcing/references/api-routing.md`; record every attempt in `api-incident-log.md` without storing secrets.
7. Normalize candidates/offers before comparing them. Exclude hard-constraint failures and mark unknowns instead of treating them as zero.
8. In mode A, show scoring dimensions and weights before ranking. In mode B, rank primarily by normalized landed cost and fit; apply the same scoring model only when the buyer asks for a product-fit ranking. Read `skills/procurement-sourcing/references/scoring-weights.md` when scoring is used.
9. Compare standardized landed cost, not display price. Keep product fit, supplier reliability, and unresolved procurement risks separate.
10. Preserve source URL, observation time, evidence, confidence, run/dataset IDs, cost, and access status for every material claim.
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
