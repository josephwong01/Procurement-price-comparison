# Collection route selection

The buyer must choose one route before platform collection. Both routes produce the same adapter evidence fields.

## Route A: Console/browser execution

Use when an Actor is free in the platform Console, the user is already logged in, or API access is unavailable. Operate only through the permitted browser/Console UI. Record actor name, operation, input summary without secrets, run ID, dataset ID, status, result count, cost, and observed time. Limit pages and candidates before pressing Start. Console login does not automatically expose an MCP/API tool.

## Route B: authenticated API/adapter execution

Use only when the API endpoint and callable adapter/tool are both present and the user has authorized the run. Verify the endpoint with a harmless status/read check, then run the smallest useful batch. Record HTTP status, actor/run ID, dataset ID, result count, and cost. Never write or display the token. An environment variable alone is not proof that the API channel is connected.

## Switching routes

If Route B returns a permission, plan, actor, or tool-channel error, classify it and switch to Route A only if the Console is available and the user has authorized paid usage. Do not repeatedly reconfigure tokens. If Route A fails to load the build or returns an empty dataset, stop after one diagnostic retry and mark the stage `PARTIAL` or `FAILED`.
