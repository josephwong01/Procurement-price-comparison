"""Validate candidate matching and deduplication records."""

from __future__ import annotations
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:
    raise SystemExit("Install requirements-validation.txt before validation") from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "candidate-resolution-v0.1.schema.json"
FILES = sorted((ROOT / "examples").glob("candidate-match.*.example.json"))
FILES += sorted((ROOT / "examples").glob("duplicate-cluster.*.example.json"))
FILES += sorted((ROOT / "cases").glob("**/duplicate-cluster-*-regression.json"))


def match_errors(record: dict) -> list[str]:
    errors: list[str] = []
    criteria = record["criteria"]
    ids = [item["criterion_id"] for item in criteria]
    if len(ids) != len(set(ids)):
        errors.append("criterion_id must be unique")
    hard_fails = [item for item in criteria if item["level"] == "HARD" and item["result"] == "FAIL"]
    hard_unknown = [item for item in criteria if item["level"] == "HARD" and item["result"] in {"PARTIAL", "UNKNOWN"}]
    if bool(hard_fails) != record["hard_failure"]:
        errors.append("hard_failure must exactly reflect HARD criterion failures")
    if hard_fails and record["overall_result"] != "FAIL":
        errors.append("HARD failure requires overall_result=FAIL")
    if any(item["confidence"] not in {"HIGH", "MEDIUM"} for item in hard_fails):
        errors.append("HARD failure requires HIGH or MEDIUM confidence; otherwise use UNKNOWN")
    if hard_fails and record["writeback"]["candidate_status"] != "EXCLUDED":
        errors.append("HARD failure requires EXCLUDED writeback")
    if hard_fails and not record["writeback"]["exclusion_reasons"]:
        errors.append("HARD failure requires exclusion reasons")
    if not hard_fails and hard_unknown and record["overall_result"] not in {"PARTIAL", "UNKNOWN"}:
        errors.append("unresolved HARD criterion requires PARTIAL or UNKNOWN")
    if record["overall_result"] == "PASS" and any(item["level"] == "HARD" and item["result"] not in {"PASS", "NOT_APPLICABLE"} for item in criteria):
        errors.append("PASS requires all applicable HARD criteria to pass")
    if record["writeback"]["requirement_match_overall"] != record["overall_result"]:
        errors.append("writeback overall result must match record overall result")
    if any(item["result"] in {"PARTIAL", "UNKNOWN"} for item in criteria) and not record["missing_information"]:
        errors.append("partial or unknown criteria require missing_information")
    return errors


def cluster_errors(record: dict) -> list[str]:
    errors: list[str] = []
    members = record["members"]
    ids = [item["candidate_id"] for item in members]
    if len(ids) != len(set(ids)):
        errors.append("cluster member candidate_id must be unique")
    if record["canonical_candidate_id"] not in ids:
        errors.append("canonical_candidate_id must be a member")
    canonical_roles = [item for item in members if item["member_role"] == "CANONICAL"]
    if len(canonical_roles) != 1 or canonical_roles[0]["candidate_id"] != record["canonical_candidate_id"]:
        errors.append("cluster requires exactly one matching CANONICAL member")
    for relation in record["relationships"]:
        if relation["left_candidate_id"] not in ids or relation["right_candidate_id"] not in ids:
            errors.append("relationship endpoint must be a cluster member")
        if relation["left_candidate_id"] == relation["right_candidate_id"]:
            errors.append("relationship endpoints must differ")
    if record["resolution"] == "MERGE_EXACT_DUPLICATES":
        if any(item["relationship_type"] != "EXACT_DUPLICATE" or item["confidence"] != "HIGH" for item in record["relationships"]):
            errors.append("merge requires only HIGH-confidence exact duplicates")
        strong_key_sets = [{"product_url"}, {"platform_product_id"}, {"brand", "model", "selected_sku"}]
        for item in record["relationships"]:
            keys = set(item["matching_keys"])
            if not any(required <= keys for required in strong_key_sets) or item["conflicting_keys"]:
                errors.append("exact duplicate merge requires strong identifiers and no conflicting keys")
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
        checks = match_errors(record) if record.get("record_type") == "MATCH_RECORD" else cluster_errors(record)
        result["errors"].extend(f"{path.name}:business: {error}" for error in checks)
    if result["errors"]:
        result["status"] = "FAILED"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())

