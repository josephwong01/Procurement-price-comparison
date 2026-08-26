"""Validate Query Plan v0.1-candidate examples and planner business rules."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:
    raise SystemExit("Install requirements-validation.txt before validation") from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "query-plan-v0.1.schema.json"
FILES = sorted((ROOT / "examples").glob("query-plan.*.example.json"))
FILES += sorted((ROOT / "cases").glob("**/query-plan-*-regression.json"))


def business_errors(record: dict) -> list[str]:
    errors: list[str] = []
    tasks = record["platform_tasks"]
    task_ids = [task["task_id"] for task in tasks]
    if len(task_ids) != len(set(task_ids)):
        errors.append("task_id must be unique")
    priorities = [task["priority"] for task in tasks]
    if len(priorities) != len(set(priorities)):
        errors.append("task priority must be unique")

    query_ids: list[str] = []
    filter_ids: list[str] = []
    for task in tasks:
        query_ids.extend(query["query_id"] for query in task["queries"])
        filter_ids.extend(item["filter_id"] for item in task["filters"])
        target = task["result_target"]
        if target["max_candidates"] < target["min_candidates"]:
            errors.append(f"{task['task_id']} max_candidates is below min_candidates")
        if task["execution_status"] == "SKIPPED" and not task["skip_reason"]:
            errors.append(f"{task['task_id']} SKIPPED requires skip_reason")
        if task["execution_status"] != "SKIPPED" and task["skip_reason"] is not None:
            errors.append(f"{task['task_id']} skip_reason only allowed for SKIPPED")
        result = task["execution_result"]
        if task["execution_status"] in {"PENDING", "RUNNING", "SKIPPED"} and result is not None:
            errors.append(f"{task['task_id']} non-final execution status requires execution_result=null")
        if task["execution_status"] in {"COMPLETED", "PARTIAL", "FAILED"} and result is None:
            errors.append(f"{task['task_id']} executed status requires execution_result")
        if result is not None and result["detail_record_count"] > result["search_result_count"]:
            errors.append(f"{task['task_id']} detail count exceeds search result count")
    if len(query_ids) != len(set(query_ids)):
        errors.append("query_id must be unique across the plan")
    if len(filter_ids) != len(set(filter_ids)):
        errors.append("filter_id must be unique across the plan")

    context = record["planning_context"]
    if record["plan_status"] == "READY":
        if context["requirement_status"] != "SEARCH_READY":
            errors.append("READY plan requires SEARCH_READY requirement")
        if context["blocking_questions"]:
            errors.append("READY plan cannot have blocking_questions")
    if record["plan_status"] == "COMPLETED" and any(task["execution_status"] in {"PENDING", "RUNNING"} for task in tasks):
        errors.append("COMPLETED plan cannot contain pending or running tasks")

    discovery = record["discovery_policy"]
    supplemental_ids = [task["target"]["platform_id"] for task in tasks if task["scope_role"] == "SUPPLEMENTAL_DISCOVERY"]
    if discovery["max_platforms"] < discovery["min_platforms"]:
        errors.append("discovery max_platforms is below min_platforms")
    if not discovery["enabled"] and (discovery["min_platforms"] or discovery["max_platforms"] or supplemental_ids):
        errors.append("disabled discovery must have zero bounds and no supplemental task")
    if len(supplemental_ids) > discovery["max_platforms"]:
        errors.append("supplemental tasks exceed discovery max_platforms")
    if record["plan_status"] == "READY" and len(supplemental_ids) < discovery["min_platforms"]:
        errors.append("READY plan has fewer supplemental tasks than discovery min_platforms")
    if set(discovery["selected_platform_ids"]) - set(supplemental_ids):
        errors.append("selected discovery platform must have a supplemental task")

    for rule in record["fallback_rules"]:
        if rule["target_task_id"] is not None and rule["target_task_id"] not in task_ids:
            errors.append(f"unknown fallback target: {rule['target_task_id']}")
    return errors


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    result = {"status":"PASSED","draft":"2020-12","schema":str(SCHEMA_PATH.relative_to(ROOT)),"files":len(FILES),"errors":[]}
    for path in FILES:
        record = json.loads(path.read_text(encoding="utf-8"))
        for error in validator.iter_errors(record):
            location = ".".join(str(part) for part in error.path) or "$"
            result["errors"].append(f"{path.name}:{location}: {error.message}")
        result["errors"].extend(f"{path.name}:business: {error}" for error in business_errors(record))
    if result["errors"]:
        result["status"] = "FAILED"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())

