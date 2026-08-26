"""Validate Supplier v0.1-candidate examples and cross-field business rules."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:
    raise SystemExit("Install requirements-validation.txt before validation") from exc


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "supplier-v0.1.schema.json"
FILES = sorted((ROOT / "examples").glob("supplier.*.example.json"))
FILES += sorted((ROOT / "cases").glob("**/supplier-*-regression.json"))


def path_text(path) -> str:
    return ".".join(str(part) for part in path) or "$"


def business_errors(record: dict) -> list[str]:
    errors: list[str] = []
    profiles = record["platform_profiles"]
    profile_ids = [profile["profile_id"] for profile in profiles]
    if len(profile_ids) != len(set(profile_ids)):
        errors.append("platform profile_id must be unique")

    evidence_ids = [item["evidence_id"] for item in record["evidence"]]
    if len(evidence_ids) != len(set(evidence_ids)):
        errors.append("evidence_id must be unique")
    evidence_set = set(evidence_ids)

    refs: list[str] = []
    for profile in profiles:
        refs.extend(profile["evidence_refs"])
        for rating in profile["ratings"]:
            refs.extend(rating["evidence_refs"])
    for signal in record["business_signals"]:
        refs.extend(signal["evidence_refs"])
        subject = signal["subject_profile_id"]
        if subject is not None and subject not in profile_ids:
            errors.append(f"unknown subject_profile_id: {subject}")
    for item in record["capabilities"]["items"]:
        refs.extend(item["evidence_refs"])
        if item["status"] in {"CONFIRMED", "CLAIMED", "PARTIAL"} and not item["evidence_refs"]:
            errors.append(f"capability {item['code']} requires evidence")
    for qualification in record["qualifications"]:
        refs.extend(qualification["evidence_refs"])
    for risk in record["assessment"]["risks"]:
        refs.extend(risk["evidence_refs"])
    missing_refs = sorted(set(refs) - evidence_set)
    if missing_refs:
        errors.append(f"unknown evidence refs: {missing_refs}")

    assessment = record["assessment"]
    if assessment["score_status"] == "NOT_SCORED" and assessment["overall_score"] is not None:
        errors.append("NOT_SCORED requires overall_score=null")
    if assessment["score_status"] in {"PROVISIONAL", "FINAL"} and assessment["overall_score"] is None:
        errors.append("scored supplier requires overall_score")
    if record["record_status"] == "EXCLUDED" and not assessment["exclusion_reasons"]:
        errors.append("EXCLUDED requires exclusion_reasons")
    return errors


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    result = {"status": "PASSED", "draft": "2020-12", "schema": str(SCHEMA_PATH.relative_to(ROOT)), "files": len(FILES), "errors": []}
    for file_path in FILES:
        record = json.loads(file_path.read_text(encoding="utf-8"))
        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
            result["errors"].append(f"{file_path.name}:{path_text(error.path)}: {error.message}")
        for error in business_errors(record):
            result["errors"].append(f"{file_path.name}:business: {error}")
    if result["errors"]:
        result["status"] = "FAILED"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())

