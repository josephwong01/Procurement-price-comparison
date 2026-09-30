# API/adapter incident log

Use this as the historical regression record and append new incidents with date, route, symptom, diagnosis, action, cost, and outcome. Never include tokens, cookies, passwords, or authorization headers.

## 2026-09-29: Apify API route rejected

- Route: authenticated API call to `sian.agency/taobao-tmall-product-scraper`.
- Symptom: HTTP call and run creation returned successfully, but datasets contained zero items; Console log showed `DETECTED USER TIER: FREE` and `Free-tier API access is disabled for this actor`.
- Diagnosis: API token was valid; the actor's free access was restricted to Console execution. This was not a missing-token problem.
- Action: stop API retries and use the logged-in Apify Console/browser route. Record Console run and dataset IDs separately.
- Outcome: Console product-detail run returned one valid Air2 item; API-produced zero-row datasets were retained as failed/empty evidence.

## 2026-09-29: External Chrome Native Host confusion

- Route: external Chrome extension/native-host diagnostics.
- Symptom: Native Host and extension were not visible in the workspace.
- Diagnosis: the successful historical workflow used Codex's in-app browser, not external Chrome. Native Host absence did not prove Apify Console was unavailable.
- Action: return to the already logged-in in-app/browser Console; do not reinstall extensions or request unrelated permissions.
- Outcome: Console Actors/Runs/Datasets pages were reachable.

## Logging rule

Technical success and procurement usefulness are separate. A `SUCCEEDED` run with zero relevant rows is not a successful sourcing result.
