#!/usr/bin/env python3
"""Validate the repository against the README_FOR_AI contract.

INTERFACE CONTRACT
==================
Input:  Repository root path through --root; defaults to the parent directory
Output: Validation findings to stdout
Side effects: None
Exit codes: 0 = validation passed, 1 = contract violations, 2 = runtime error
Dependencies: Python standard library only
"""

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "Makefile",
    "README_FOR_AI.md",
    "README.md",
    "SECURITY.md",
    "SUPPORT.md",
    "SKILL.md",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/workflows/ci.yml",
    "references/decision-matrix.md",
    "references/magi-framework.md",
    "references/method-patterns.md",
    "prompts/01-implement-method.md",
    "prompts/02-robustness-checks.md",
    "scripts/risk-matrix-gen.py",
    "scripts/validate-project.py",
    "scripts/weighted-scoring.py",
)

EMOJI_RANGES = (
    (0x1F000, 0x1FAFF),
    (0x2600, 0x27BF),
)


def contains_emoji(text: str) -> bool:
    """Return whether text contains a character in the prohibited ranges."""
    return any(
        start <= ord(character) <= end
        for character in text
        for start, end in EMOJI_RANGES
    )


def validate(root: Path) -> list[str]:
    """Return all contract violations found below root."""
    findings = []

    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            findings.append(f"Missing required file: {relative_path}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file() and len(skill_path.read_text(encoding="utf-8").splitlines()) >= 120:
        findings.append("SKILL.md must contain fewer than 120 lines")

    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # Binary files (for example __pycache__ bytecode) cannot contain emoji
        if contains_emoji(text):
            findings.append(f"Emoji character found: {path.relative_to(root)}")

    for prompt_name, placeholders in {
        "prompts/01-implement-method.md": ("{{SCENARIO}}", "{{METHOD}}", "{{CONSTRAINTS}}"),
        "prompts/02-robustness-checks.md": ("{{DECISION}}", "{{CONTEXT}}", "{{FOCUS_AREAS}}"),
    }.items():
        prompt_path = root / prompt_name
        if prompt_path.is_file():
            prompt_text = prompt_path.read_text(encoding="utf-8")
            for placeholder in placeholders:
                if placeholder not in prompt_text:
                    findings.append(f"Missing placeholder {placeholder}: {prompt_name}")

    for script_name in ("scripts/weighted-scoring.py", "scripts/risk-matrix-gen.py"):
        script_path = root / script_name
        if script_path.is_file():
            script_text = script_path.read_text(encoding="utf-8")
            if "INTERFACE CONTRACT" not in script_text:
                findings.append(f"Missing interface contract: {script_name}")
            if "argparse" not in script_text:
                findings.append(f"Missing argparse CLI: {script_name}")

    # HISTORICAL BURDEN (commented out, retained for traceability):
    # The pattern below referenced the pre-0.2.0 prompt filenames
    # (prompts/risk-assessment.md, prompts/multi-option-compare.md,
    # prompts/strategic-analysis.md). Those names were superseded by the
    # current 01-/02- numbered scheme and the files never existed under
    # these names. Kept disabled rather than deleted so the rename history
    # remains auditable.
    #     r"prompts/(risk-assessment|multi-option-compare|strategic-analysis)\.md"
    stale_paths = re.compile(r"(SKILL\.MD|Changelog\.md)")
    for path in (root / "README_FOR_AI.md", root / "SKILL.md", root / "README.md"):
        if path.is_file() and stale_paths.search(path.read_text(encoding="utf-8")):
            findings.append(f"Stale path reference: {path.relative_to(root)}")

    return findings


def main() -> int:
    """Run repository validation."""
    parser = argparse.ArgumentParser(description="Validate the MAGI project contract.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()

    try:
        findings = validate(args.root.resolve())
    except OSError as error:
        print(f"Runtime error: {error}", file=sys.stderr)
        return 2

    if findings:
        print("Validation failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
