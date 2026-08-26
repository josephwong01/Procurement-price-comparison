"""Validate stage-10 skill packaging and end-to-end run manifests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = sorted((ROOT / "cases").glob("**/end-to-end-run-v0.1.json"))
REQUIRED_STAGES = {
    "REQUIREMENT", "QUERY_PLAN", "ADAPTER", "CANDIDATE", "SUPPLIER",
    "MATCH_DEDUP", "TCO_SCORE", "FINAL_OUTPUT",
}
VALIDATORS = [
    ["validate_product_candidate_schema.py", "--schema", "schemas/product-candidate-v0.1.schema.json",
     "examples/product-candidate.standard-product.bluetooth-speaker.example.json",
     "examples/product-candidate.equipment.coffee-machine.example.json",
     "examples/product-candidate.custom-product.ip-mascot.example.json",
     "examples/product-candidate.service.residential-design.example.json"],
    ["validate_product_candidates.py",
     "examples/product-candidate.standard-product.bluetooth-speaker.example.json",
     "examples/product-candidate.equipment.coffee-machine.example.json",
     "examples/product-candidate.custom-product.ip-mascot.example.json",
     "examples/product-candidate.service.residential-design.example.json"],
    ["validate_suppliers.py"],
    ["validate_query_plans.py"],
    ["validate_candidate_resolutions.py"],
    ["validate_tco_scores.py"],
    ["validate_adapter_results.py"],
]


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    record = json.loads(path.read_text(encoding="utf-8"))
    required = {"run_version", "run_id", "case_type", "status", "requirement_id", "artifacts", "limitations"}
    missing = sorted(required - record.keys())
    if missing:
        return [f"{path.name}: missing keys: {', '.join(missing)}"]
    if record["run_version"] != "0.1":
        errors.append(f"{path.name}: unsupported run_version")
    if record["status"] not in {"COMPLETE", "PARTIAL", "FAILED"}:
        errors.append(f"{path.name}: invalid status")
    stages = [item.get("stage") for item in record["artifacts"]]
    if set(stages) != REQUIRED_STAGES or len(stages) != len(REQUIRED_STAGES):
        errors.append(f"{path.name}: artifacts must contain each required stage exactly once")
    for item in record["artifacts"]:
        artifact_path = ROOT / item.get("path", "")
        if not artifact_path.is_file():
            errors.append(f"{path.name}: missing artifact {item.get('path')}")
            continue
        try:
            artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: unreadable artifact {item.get('path')}: {exc}")
            continue
        field = item.get("id_field")
        if artifact.get(field) != item.get("expected_id"):
            errors.append(f"{path.name}: {item.get('stage')} identifier mismatch")
        artifact_requirement = artifact.get("requirement_id")
        if artifact_requirement is not None and artifact_requirement != record["requirement_id"]:
            errors.append(f"{path.name}: {item.get('stage')} requirement_id mismatch")
        if item.get("stage") == "FINAL_OUTPUT":
            output_requirement = artifact.get("requirement_reference", {}).get("requirement_id")
            if output_requirement != record["requirement_id"]:
                errors.append(f"{path.name}: final output requirement reference mismatch")
    if record["status"] == "COMPLETE" and record["limitations"]:
        errors.append(f"{path.name}: COMPLETE run cannot retain limitations")
    return errors


def main() -> int:
    errors: list[str] = []
    skill_path = ROOT / "skills" / "procurement-sourcing" / "SKILL.md"
    if not skill_path.is_file():
        errors.append("procurement-sourcing SKILL.md is missing")
    for manifest in MANIFESTS:
        errors.extend(validate_manifest(manifest))
    if not MANIFESTS:
        errors.append("no end-to-end manifest found")
    validator_results: dict[str, str] = {}
    for command in VALIDATORS:
        name, *arguments = command
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / name), *arguments],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        validator_results[name] = "PASSED" if completed.returncode == 0 else "FAILED"
        if completed.returncode != 0:
            errors.append(f"{name} failed: {completed.stdout.strip() or completed.stderr.strip()}")
    result = {
        "status": "PASSED" if not errors else "FAILED",
        "manifests": len(MANIFESTS),
        "validators": validator_results,
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

