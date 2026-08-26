"""Validate platform adapter result records and referenced artifacts."""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:
    raise SystemExit("Install requirements-validation.txt before validation") from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "platform-adapter-result-v0.1.schema.json"
FILES = sorted((ROOT / "examples").glob("adapter-result.*.example.json"))
SECRET_PATTERNS = [re.compile(r"apify_api_[A-Za-z0-9_-]{10,}"), re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{12,}")]


def business_errors(record: dict) -> list[str]:
    errors: list[str] = []
    family = record["adapter"]["adapter_family"]
    method = record["source"]["access_method"]
    allowed = {
        "APIFY_MARKETPLACE": {"API"}, "PUBLIC_WEB": {"PUBLIC_WEB"},
        "AUTHENTICATED_BROWSER": {"BROWSER"}, "SCREENSHOT_MANUAL": {"SCREENSHOT", "MANUAL"},
        "GENERIC_API": {"API"},
    }
    if method not in allowed[family]:
        errors.append("access_method does not match adapter_family")
    if record["source"]["platform_code"] not in record["adapter"]["platform_codes"]:
        errors.append("source platform is not declared by adapter")

    input_ids = [item["input_id"] for item in record["input_records"]]
    output_ids = [item["artifact_id"] for item in record["output_artifacts"]]
    mapping_ids = [item["mapping_id"] for item in record["field_mappings"]]
    if len(input_ids) != len(set(input_ids)):
        errors.append("input_id must be unique")
    if len(output_ids) != len(set(output_ids)):
        errors.append("artifact_id must be unique")
    if len(mapping_ids) != len(set(mapping_ids)):
        errors.append("mapping_id must be unique")
    for item in record["field_mappings"]:
        if item["input_id"] not in input_ids:
            errors.append(f"unknown mapping input: {item['input_id']}")
        if item["target_artifact_id"] not in output_ids:
            errors.append(f"unknown mapping output: {item['target_artifact_id']}")
    for item in record["unmapped_fields"]:
        if item["input_id"] not in input_ids:
            errors.append(f"unknown unmapped-field input: {item['input_id']}")

    if record["execution_status"] == "SUCCEEDED" and (not record["output_artifacts"] or record["errors"]):
        errors.append("SUCCEEDED requires outputs and no errors")
    if record["execution_status"] == "PARTIAL" and not (record["warnings"] or record["errors"]):
        errors.append("PARTIAL requires warnings or errors")
    if record["execution_status"] == "FAILED" and not record["errors"]:
        errors.append("FAILED requires errors")
    if record["source"]["authentication_used"] and any(not item["redacted"] for item in record["input_records"]):
        errors.append("authenticated inputs must be marked redacted")

    serialized = json.dumps(record, ensure_ascii=False)
    if any(pattern.search(serialized) for pattern in SECRET_PATTERNS):
        errors.append("record appears to contain a secret")

    for artifact in record["output_artifacts"]:
        path = ROOT / artifact["artifact_path"]
        if not path.is_file():
            errors.append(f"referenced artifact does not exist: {artifact['artifact_path']}")
            continue
        if artifact["artifact_type"] == "EVIDENCE_ONLY":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        actual_id = data.get("candidate_id") if artifact["artifact_type"] == "PRODUCT_CANDIDATE" else data.get("supplier_id")
        if actual_id != artifact["artifact_id"]:
            errors.append(f"artifact id mismatch: {artifact['artifact_path']}")
        if data.get("schema_version") != artifact["schema_version"]:
            errors.append(f"artifact schema version mismatch: {artifact['artifact_path']}")
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

