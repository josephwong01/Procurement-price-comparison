"""Validate TCO and composite score records."""

from __future__ import annotations
import json
import math
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:
    raise SystemExit("Install requirements-validation.txt before validation") from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "tco-score-v0.1.schema.json"
FILES = sorted((ROOT / "examples").glob("tco-score.*.example.json"))
FILES += sorted((ROOT / "cases").glob("**/tco-score-*-regression.json"))


def close(left: float, right: float, tolerance: float = 0.02) -> bool:
    return math.isclose(left, right, rel_tol=0, abs_tol=tolerance)


def business_errors(record: dict) -> list[str]:
    errors: list[str] = []
    rates = {item["from_currency"]: item["rate"] for item in record["exchange_rates"]}
    if len(rates) != len(record["exchange_rates"]):
        errors.append("exchange rate currency must be unique")
    for component in record["cost_components"]:
        original = component["original_amount"]
        if original["currency"] == "CNY":
            expected = original["amount"]
        elif original["currency"] in rates:
            expected = original["amount"] * rates[original["currency"]]
        else:
            errors.append(f"missing exchange rate for {original['currency']}")
            continue
        if not close(component["converted_cny"], expected):
            errors.append(f"{component['code']} converted_cny does not match reference rate")

    included = [item for item in record["cost_components"] if item["included_in_tco"]]
    calculated_total = sum(item["converted_cny"] for item in included)
    if record["known_cost_total_cny"] is not None and not close(record["known_cost_total_cny"], calculated_total):
        errors.append("known_cost_total_cny does not equal included components")
    if record["estimated_tco_cny"] is not None and record["known_cost_total_cny"] is not None and record["estimated_tco_cny"] < record["known_cost_total_cny"]:
        errors.append("estimated TCO cannot be below known cost total")
    if record["calculation_status"] == "UNAVAILABLE" and (record["known_cost_total_cny"] is not None or record["estimated_tco_cny"] is not None):
        errors.append("UNAVAILABLE calculation requires null totals")
    if record["calculation_status"] == "COMPLETE" and (record["estimated_tco_cny"] is None or record["unknown_costs"]):
        errors.append("COMPLETE calculation requires TCO and no unknown costs")
    codes = [item["code"] for item in record["unknown_costs"]]
    if len(codes) != len(set(codes)):
        errors.append("unknown cost code must be unique")

    display = record["price_display"]
    if display["original_amount"] is not None and display["original_amount"]["currency"] == "CNY" and "原价" in display["display_text"]:
        errors.append("CNY original price must not repeat in parentheses")
    if display["original_amount"] is not None and display["original_amount"]["currency"] != "CNY" and "原价" not in display["display_text"]:
        errors.append("foreign-currency display must retain original price")

    dimensions = record["scoring"]["dimensions"]
    dim_codes = [item["code"] for item in dimensions]
    if len(set(dim_codes)) != 5:
        errors.append("five scoring dimensions must be unique")
    if not close(sum(item["weight"] for item in dimensions), 1, 0.000001):
        errors.append("scoring weights must sum to 1")
    for item in dimensions:
        if item["score"] is None and item["weighted_score"] is not None:
            errors.append(f"{item['code']} null score requires null weighted_score")
        if item["score"] is not None and (item["weighted_score"] is None or not close(item["weighted_score"], item["score"] * item["weight"], 0.000001)):
            errors.append(f"{item['code']} weighted score mismatch")
    scoring = record["scoring"]
    if scoring["score_status"] == "NOT_SCORED" and (scoring["overall_score"] is not None or any(item["score"] is not None for item in dimensions)):
        errors.append("NOT_SCORED requires all scores null")
    if scoring["score_status"] != "NOT_SCORED":
        if any(item["weighted_score"] is None for item in dimensions):
            errors.append("scored record requires every dimension score")
        elif scoring["overall_score"] is None or not close(scoring["overall_score"], sum(item["weighted_score"] for item in dimensions), 0.000001):
            errors.append("overall score mismatch")
    if record["ranking"]["eligible"] and scoring["overall_score"] is None:
        errors.append("ranking eligibility requires overall score")
    if not record["ranking"]["eligible"] and record["ranking"]["rank"] is not None:
        errors.append("ineligible record cannot have rank")
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

