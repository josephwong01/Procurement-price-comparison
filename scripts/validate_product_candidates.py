#!/usr/bin/env python3
"""Business-rule validator for Product Candidate records.

This validator complements JSON Schema validation. It checks invariants that span
fields or records and intentionally uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ALLOWED_TYPES = {"STANDARD_PRODUCT", "EQUIPMENT", "CUSTOM_PRODUCT", "SERVICE"}
RANKABLE_STATUSES = {"ELIGIBLE"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("root must be an object")
    return value


def collect_evidence_refs(candidate: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    offer = candidate.get("offer", {})
    for price_key in ("search_display_price", "selected_sku_price", "quoted_price"):
        price = offer.get(price_key)
        if isinstance(price, dict):
            refs.extend(price.get("evidence_refs", []))
    for criterion in candidate.get("requirement_match", {}).get("criteria", []):
        refs.extend(criterion.get("evidence_refs", []))
    for attribute in candidate.get("category_data", {}).get("attributes", []):
        refs.extend(attribute.get("evidence_refs", []))
    return [ref for ref in refs if isinstance(ref, str) and ref]


def candidate_signature(candidate: dict[str, Any]) -> tuple[Any, ...] | None:
    source = candidate.get("source", {})
    supplier = candidate.get("supplier", {})
    identity = candidate.get("identity", {})
    offer = candidate.get("offer", {})
    quote = offer.get("quoted_price") or {}
    quote_money = quote.get("money") or {}
    selected_price = offer.get("selected_sku_price") or {}
    selected_money = selected_price.get("money") or {}
    supplier_key = supplier.get("supplier_id") or supplier.get("name")
    sku_or_quote_known = bool(
        identity.get("selected_sku")
        or quote_money.get("amount") is not None
        or selected_money.get("amount") is not None
    )
    if not supplier_key or not sku_or_quote_known:
        return None
    return (
        source.get("platform_code"),
        supplier_key,
        identity.get("selected_sku"),
        quote_money.get("amount"),
        quote_money.get("currency"),
        selected_money.get("amount"),
        selected_money.get("currency"),
    )


def validate_candidate(candidate: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    procurement_type = candidate.get("procurement_type")
    category_kind = candidate.get("category_data", {}).get("kind")
    status = candidate.get("candidate_status")
    assessment = candidate.get("assessment", {})

    if procurement_type not in ALLOWED_TYPES:
        errors.append(f"{label}: invalid procurement_type {procurement_type!r}")
    if procurement_type != category_kind:
        errors.append(f"{label}: procurement_type does not match category_data.kind")

    evidence = candidate.get("evidence", [])
    evidence_ids = [item.get("evidence_id") for item in evidence if isinstance(item, dict)]
    duplicates = [key for key, count in Counter(evidence_ids).items() if key and count > 1]
    if duplicates:
        errors.append(f"{label}: duplicate evidence IDs: {duplicates}")
    missing_refs = sorted(set(collect_evidence_refs(candidate)) - set(evidence_ids))
    if missing_refs:
        errors.append(f"{label}: missing evidence references: {missing_refs}")

    dimensions = assessment.get("score_dimensions", [])
    overall_score = assessment.get("overall_score")
    if dimensions:
        weights = [item.get("weight") for item in dimensions]
        if not all(isinstance(value, (int, float)) for value in weights):
            errors.append(f"{label}: every score dimension must have a numeric weight")
        else:
            weight_sum = sum(weights)
            if not math.isclose(weight_sum, 1.0, abs_tol=1e-9):
                errors.append(f"{label}: score weights sum to {weight_sum}, expected 1")
        scores = [item.get("score") for item in dimensions]
        if all(isinstance(value, (int, float)) for value in scores + weights):
            calculated = round(sum(score * weight for score, weight in zip(scores, weights)), 2)
            if not isinstance(overall_score, (int, float)) or not math.isclose(
                overall_score, calculated, abs_tol=0.01
            ):
                errors.append(
                    f"{label}: overall_score {overall_score!r} does not equal {calculated}"
                )
    elif overall_score is not None:
        errors.append(f"{label}: overall_score must be null when score_dimensions is empty")

    exclusion_reasons = assessment.get("exclusion_reasons", [])
    if status == "EXCLUDED" and not exclusion_reasons:
        errors.append(f"{label}: excluded candidate must include exclusion_reasons")
    if status != "EXCLUDED" and exclusion_reasons:
        errors.append(f"{label}: non-excluded candidate must not include exclusion_reasons")

    recommendation_role = assessment.get("recommendation_role")
    if status not in RANKABLE_STATUSES and recommendation_role != "NONE":
        errors.append(f"{label}: non-eligible candidate cannot have a recommendation role")
    if status not in RANKABLE_STATUSES and overall_score is not None:
        errors.append(f"{label}: non-eligible candidate must not be scored or ranked")

    commercial_terms = candidate.get("offer", {}).get("commercial_terms", {})
    if "lead_time_days" not in commercial_terms:
        errors.append(f"{label}: offer.commercial_terms.lead_time_days is required")
    if "lead_time_start_event" not in commercial_terms:
        errors.append(f"{label}: offer.commercial_terms.lead_time_start_event is required")

    return errors


def validate_collection(records: list[tuple[Path, dict[str, Any]]]) -> list[str]:
    errors: list[str] = []
    candidate_ids = [record.get("candidate_id") for _, record in records]
    duplicate_ids = [key for key, count in Counter(candidate_ids).items() if key and count > 1]
    if duplicate_ids:
        errors.append(f"collection: duplicate candidate IDs: {duplicate_ids}")

    signatures: dict[tuple[Any, ...], list[str]] = {}
    for path, record in records:
        signature = candidate_signature(record)
        if signature is None:
            continue
        signatures.setdefault(signature, []).append(f"{path.name}:{record.get('candidate_id')}")
    for signature, labels in signatures.items():
        if len(labels) > 1 and any(value is not None for value in signature):
            errors.append(f"collection: possible duplicate candidates: {labels}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    records: list[tuple[Path, dict[str, Any]]] = []
    errors: list[str] = []
    for path in args.paths:
        try:
            record = load_json(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: cannot load JSON: {exc}")
            continue
        records.append((path, record))
        errors.extend(validate_candidate(record, path.name))

    errors.extend(validate_collection(records))
    if errors:
        print(json.dumps({"status": "FAILED", "files": len(records), "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status": "PASSED", "files": len(records), "errors": []}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
