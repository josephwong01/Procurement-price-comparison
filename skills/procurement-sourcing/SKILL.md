---
name: procurement-sourcing
description: Turn a procurement need into a traceable multi-platform candidate comparison using the repository's frozen requirement, query, adapter, candidate, supplier, matching, TCO, and output contracts. Use for procurement sourcing, product comparison, supplier shortlisting, or end-to-end regression; do not use to contact suppliers, place orders, or approve purchases.
---

# Procurement Sourcing

Build a reviewable procurement shortlist without pretending that unknown data is confirmed.

## Workflow

### 0. 首次运行与采集通道（必须先做）

首次使用或换工作区时，先分别检查 Skill、`APIFY_TOKEN` 和采集通道；三者互不等价。不要因为 Token 存在就假设 Apify 工具已连接，也不要把缺少 MCP 当成唯一失败条件。

按以下顺序选择允许的采集路径：

1. 若当前会话实际暴露 Apify/Actor/Dataset 工具，使用该工具并记录运行证据。
2. 若工具未暴露，使用 Codex 内置浏览器打开 `https://console.apify.com/`，让用户在浏览器中手动登录（不得索取密码、Token 或 Cookie），登录后通过 Console 运行授权 Actor、查看 Runs/Datasets。
3. Chrome 扩展或 Chrome Native Host 缺失不等于 Apify 故障；只要 Codex 内置浏览器可访问并登录 Console，就可继续。
4. 只有内置浏览器无法访问 Console 且没有 Apify 工具时，才报告缺少采集通道并停止，不要重复配置 Token、申请 Google 权限或修改采购文件。

采集通道决策和常见故障见 [Apify 连接常见问题](../../docs/apify-browser-console-faq.md)。

1. Locate the repository root by finding `docs/project-roadmap.md` and `schemas/`.
2. Capture the buyer's need with the latest frozen Requirement Schema. Ask only about missing facts that would materially change search or eligibility; keep assumptions explicit. When quantity is greater than one, distinguish unit-price, line-total, and all-in budget. If the wording is ambiguous, either ask once or proceed with a reversible stated assumption and leave confirmation open.
3. If social trend discovery is requested, run it after requirement freeze and before candidate selection. Read [social-trend-discovery-v0.1.md](../../docs/social-trend-discovery-v0.1.md). It creates direction-level leads only.
4. Generate a Query Plan and preserve the full candidate pool, including user additions, explicit exclusions, budget risks, and unresolved candidates.
5. Before collection, let the buyer choose Console/browser execution or authenticated API/adapter execution. Read [references/api-routing.md](references/api-routing.md); record every attempt in [references/api-incident-log.md](references/api-incident-log.md) without secrets.
6. Record every collection attempt through the Platform Adapter contract. Preserve source URL, observed time, original value, confidence, run/dataset IDs, cost, and access failure. Separate technical execution success from procurement usefulness.
7. Normalize successful results into Product Candidate and Supplier records. Keep observed, claimed, estimated, conflicting, and unknown values distinct. On validation failure, return to the same direction and choose a replacement; do not relax hard constraints.
8. Match against the requirement and deduplicate only the comparison view. Preserve all source records.
9. Before scoring, show dimensions and default weights and let the buyer keep or change them. Read [references/scoring-weights.md](references/scoring-weights.md) and recompute all candidates under one selected weight set.
10. Calculate CNY TCO and a composite score with the selected model. Show non-CNY platform prices in parentheses and never treat unknown costs as zero.
11. Produce the procurement output main table plus details, exclusions, risks, evidence, API/adapter log, and confirmations. A recommendation is provisional until its blocking confirmations are resolved.
12. When shortlisted candidates still need supplier confirmation, prepare an RFQ question set and a structured answer sheet for manual use. Read [references/rfq-preparation.md](references/rfq-preparation.md). Do not send it.
13. Run the repository validators, including `scripts/validate_end_to_end.py`, before calling the run complete.

For artifact selection, stopping conditions, and status rules, read [references/workflow-contract.md](references/workflow-contract.md).

## Boundaries

- Stop at a candidate pool and preliminary comparison. Do not message suppliers, negotiate, order, approve, or write to ERP/OA unless separately authorized.
- RFQ preparation means drafting questions and an answer structure only. It does not imply opening customer-service chat, submitting a form, or contacting a supplier.
- Do not bypass access controls. Record a failed channel and use an allowed fallback.
- Social collection is limited to approved official APIs, low-volume public-page reading, or user-supplied public links. Do not use Apify Actors for Reddit/X social discovery. For later authorized e-commerce comparison, Apify Actors are allowed when source, input, cost limit, access result, and Dataset provenance are recorded; do not bypass controls or conceal failures.
- Do not use CAPTCHA bypass, proxy/fingerprint evasion, cookie theft/reuse, unauthorized bulk extraction, or infinite retries. Console availability does not prove an API/MCP channel exists.
- A failed or partial stage stays failed or partial in the final report. List unfinished work explicitly.
- Frozen schemas may receive compatibility fixes only; changed semantics require a new candidate version.
