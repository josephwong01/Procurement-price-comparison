"""Run repository-level release checks for the procurement-sourcing MVP."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_ROOTS = ("schemas", "examples", "cases")
REQUIRED_FILES = (
    "README.md",
    ".env.example",
    "requirements-validation.txt",
    "skills/procurement-sourcing/SKILL.md",
    "skills/procurement-sourcing/agents/openai.yaml",
    "skills/procurement-sourcing/references/workflow-contract.md",
    "docs/project-roadmap.md",
    "docs/mvp-release-checklist-v0.1.md",
)
SECRET_PATTERNS = (
    re.compile(r"apify_api_[A-Za-z0-9_-]{10,}"),
    re.compile(r"(?i)(?:api[_-]?key|token)\s*[:=]\s*['\"]?[A-Za-z0-9_-]{24,}"),
)


def check_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def check_json(errors: list[str]) -> int:
    count = 0
    for directory in JSON_ROOTS:
        for path in sorted((ROOT / directory).rglob("*.json")):
            count += 1
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")
    return count


def check_skill(errors: list[str]) -> None:
    path = ROOT / "skills/procurement-sourcing/SKILL.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
    if "name: procurement-sourcing" not in text:
        errors.append("SKILL.md frontmatter name must be procurement-sourcing")
    if "description:" not in text:
        errors.append("SKILL.md frontmatter description is missing")


def check_secrets(errors: list[str]) -> int:
    scanned = 0
    allowed_suffixes = {".md", ".json", ".yaml", ".yml", ".py", ".txt", ".example", ".gitignore"}
    excluded = {"work", ".git", "__pycache__"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in excluded for part in path.parts):
            continue
        if path.name.startswith(".env") and path.name != ".env.example":
            continue
        if path.suffix.lower() not in allowed_suffixes and path.name != ".gitignore":
            continue
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible secret detected: {path.relative_to(ROOT)}")
                break
    return scanned


def run_end_to_end(errors: list[str]) -> str:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_end_to_end.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        errors.append("end-to-end validation failed: " + (completed.stdout.strip() or completed.stderr.strip()))
        return "FAILED"
    return "PASSED"


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    json_files = check_json(errors)
    check_skill(errors)
    scanned_files = check_secrets(errors)
    end_to_end = run_end_to_end(errors)
    result = {
        "status": "PASSED" if not errors else "FAILED",
        "json_files": json_files,
        "files_scanned_for_secrets": scanned_files,
        "end_to_end": end_to_end,
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
