# README FOR AI.md -- MAGI Strategic Advisor

---

## Purpose

This document is the single authoritative build instruction for any AI agent tasked with generating, maintaining, or extending the MAGI Strategic Advisor skill package. Every file in the project must be produced in strict accordance with the rules defined here. No deviation is permitted without explicit amendment to this document.

---

## 1. Hard Constraints

The following constraints are non-negotiable. Every generated file must pass all of them before being considered complete.

| ID | Constraint | Enforcement |
|----|-----------|-------------|
| HC-01 | All compiled content (SKILL.md, references/, scripts/, prompts/) must be written entirely in English | Reject any file containing non-English prose in compiled sections |
| HC-02 | No emoji characters are permitted in any compiled file | Scan all output files for Unicode emoji ranges and reject on match |
| HC-03 | SKILL.md must contain only index entries and quick-reference tables | Reject if SKILL.md exceeds 120 lines or contains inline code blocks longer than 3 lines |
| HC-04 | All code templates, patterns, and implementation details must reside in references/method-patterns.md | Reject if code blocks appear in SKILL.md or README FOR AI.md (EXEMPTION: README FOR AI.md is exempt as a meta-document that must include code examples to specify expected file formats and structures; this exemption applies only to specification/example code blocks, not to reusable code templates) |
| HC-05 | Files in prompts/ are user-facing copy-paste artifacts, not agent-auto-invoked skills | prompts/ files must be self-contained and portable to any AI chat window |
| HC-06 | The project must follow harness engineering principles | Every module must be independently testable with defined inputs and outputs |
| HC-07 | The project must satisfy five design principles: standardized, generic, modular, compact, automated | See Section 6 for detailed compliance checklist |

---

## 2. File Tree

The project must produce exactly the following structure. No additional files may be created at the root level. Subdirectories may only contain the files listed below.

```
magi-advisor/
|-- SKILL.md
|-- README FOR AI.md
|-- references/
|   |-- magi-framework.md
|   |-- decision-matrix.md
|   |-- method-patterns.md
|-- prompts/
|   |-- 01-implement-method.md
|   |-- 02-robustness-checks.md
|-- scripts/
|   |-- weighted-scoring.py
|   |-- risk-matrix-gen.py
```

### 2.1 File Responsibility Matrix

| File | Role | Loaded By | Contains |
|------|------|-----------|----------|
| SKILL.md | Entry index and quick-reference | Agent runtime on every invocation | Trigger conditions, capability table, file routing map, output format spec |
| README FOR AI.md | Build instruction for AI agents | AI agent at project generation time | This document |
| references/magi-framework.md | Core decision framework definition | Agent when analysis mode is activated | Persona definitions, voting rules, confidence levels, weight system |
| references/decision-matrix.md | Scoring matrix templates | Agent when quantitative evaluation is needed | Single-option matrix, multi-option matrix, veto checklist, scoring norms |
| references/method-patterns.md | All code templates and implementation patterns | Agent when generating or modifying scripts | Python function signatures, class definitions, data structures, CLI interfaces |
| prompts/01-implement-method.md | User-facing prompt for method implementation | Human user (copy-paste into any AI chat) | Self-contained prompt with role, task, constraints, output format |
| prompts/02-robustness-checks.md | User-facing prompt for robustness validation | Human user (copy-paste into any AI chat) | Self-contained prompt for stress-testing a decision or plan |
| scripts/weighted-scoring.py | Weighted scoring calculator | Agent or user via Python runtime | magi_score(), print_results(), CLI entry point |
| scripts/risk-matrix-gen.py | Risk matrix generator | Agent or user via Python runtime | build_risk_entry(), generate_text_matrix(), generate_html_matrix(), CLI entry point |

---

## 3. SKILL.md Specification

SKILL.md is the first file the agent reads. It must be compact and serve exclusively as a routing index. It must NOT contain implementation details, code templates, or lengthy procedural descriptions.

### 3.1 Required Sections

SKILL.md must contain exactly these sections in this order:

```
# MAGI Strategic Advisor

## Trigger Conditions
[Table: scenario -> activation signal -> action]

## Capability Index
[Table: capability -> description -> reference file -> prompt file]

## Quick-Reference: Output Format
[Condensed output template, max 15 lines]

## Quick-Reference: Voting Rules
[Table: vote pattern -> verdict -> action]

## Quick-Reference: Veto Conditions
[Bulleted list, one line per condition]

## File Routing Map
[Table: user intent -> primary file to load -> secondary files if needed]

```

### 3.2 Size Constraint

SKILL.md must not exceed 120 lines. If content grows beyond this limit, extract the overflow into the appropriate reference file and replace with a one-line pointer.

---

## 4. references/method-patterns.md Specification

This file is the single repository for all code templates, data structures, and implementation patterns used across the project. No other file may contain inline code blocks exceeding 3 lines.

### 4.1 Required Sections

The following shows the required heading structure for method-patterns.md. Heading markers (## / ###) are template placeholders indicating hierarchy levels, not actual document headings.

```
# Method Patterns

## 1. Data Structures
### 1.1 Risk Entry Schema
### 1.2 Option Score Schema
### 1.3 Persona Judgment Schema

## 2. Core Functions
### 2.1 classify_risk(score: int) -> dict
### 2.2 build_risk_entry(...) -> dict
### 2.3 magi_score(options: dict, weights: dict) -> list
### 2.4 generate_text_matrix(risks: list) -> str
### 2.5 generate_html_matrix(risks: list, output_path: str) -> str

## 3. CLI Interfaces
### 3.1 weighted-scoring.py CLI
### 3.2 risk-matrix-gen.py CLI

## 4. Extension Patterns
### 4.1 Adding a New Persona
### 4.2 Adding a New Risk Domain
### 4.3 Adding a New Output Format

```

### 4.2 Code Template Format

Every code template in method-patterns.md must follow this structure:

~~~
### [Function/Class Name]

**Signature:** `[exact function signature]`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|

**Returns:** `[return type and description]`

**Implementation:**

```python
[complete, runnable code block]
```

**Usage Example:**

```python
[2-5 lines demonstrating typical invocation]
```

~~~

---

## 5. prompts/ Dual-Mode Specification

Files in prompts/ operate in a fundamentally different mode from all other project files. They are NOT invoked by the agent runtime. They are standalone artifacts designed for human users to copy and paste into any AI conversation window.

### 5.1 Design Principles for prompts/ Files

| Principle | Requirement |
|-----------|-------------|
| Self-contained | Each file must function independently without referencing any other project file |
| Portable | Must work when pasted into ChatGPT, Claude, Gemini, or any LLM interface |
| Zero-dependency | Must not assume the target AI has access to references/, scripts/, or SKILL.md |
| Numbered prefix | Files use numeric prefix (01-, 02-, ...) to indicate suggested usage order |
| Plain markdown | Must use only standard markdown; no custom directives or agent-specific syntax |

### 5.2 Required Structure for Each Prompt File

```
# [Title]

## Context
[2-3 sentences explaining what this prompt does and when to use it]

## Instructions
[The actual prompt content the user copies]

## Expected Output
[Description of what the AI should produce]

## Customization Notes
[Variables the user should replace before pasting, marked with {{placeholder}} syntax]

```

### 5.3 Prompt File Definitions

#### 01-implement-method.md

Purpose: A prompt that instructs an AI to implement a specific decision analysis method (e.g., weighted scoring, risk matrix, multi-criteria evaluation) from scratch, given a scenario description.

Required placeholders:
- `{{SCENARIO}}` -- the decision scenario to analyze
- `{{METHOD}}` -- the analysis method to apply
- `{{CONSTRAINTS}}` -- any hard constraints or boundaries

#### 02-robustness-checks.md

Purpose: A prompt that instructs an AI to stress-test an existing decision, plan, or analysis by applying adversarial perspectives, edge cases, and failure mode analysis.

Required placeholders:
- `{{DECISION}}` -- the decision or plan to stress-test
- `{{CONTEXT}}` -- background information and constraints
- `{{FOCUS_AREAS}}` -- specific dimensions to probe (optional)

---

## 6. Five Design Principles Compliance

Every file and module in this project must satisfy all five principles. The following checklist must pass for each principle.

### 6.1 Standardized

- [ ] All files use consistent heading hierarchy (H1 for title, H2 for sections, H3 for subsections)
- [ ] All tables use the same column alignment convention
- [ ] All code follows PEP 8 (Python) with 4-space indentation
- [ ] All identifiers use snake_case (variables, functions, files)
- [ ] All status labels use text only: PASS / FAIL / PENDING / N/A

### 6.2 Generic

- [ ] No domain-specific jargon without definition in magi-framework.md
- [ ] No hardcoded values in scripts; all thresholds and weights are parameterized
- [ ] No assumptions about the user's industry, organization size, or technical stack
- [ ] Prompt files use placeholder syntax instead of concrete examples

### 6.3 Modular

- [ ] Each file has a single, clearly defined responsibility
- [ ] Scripts can be imported as modules or run standalone
- [ ] Reference files can be loaded independently without cross-dependencies
- [ ] Adding or removing a module does not break other modules

### 6.4 Compact

- [ ] SKILL.md does not exceed 120 lines
- [ ] No file contains redundant information that exists in another file
- [ ] Code templates include only the essential implementation, not verbose comments
- [ ] Tables are used instead of prose wherever structured data is presented

### 6.5 Automated

- [ ] Scripts include CLI entry points with argparse for command-line execution
- [ ] Scripts include `if __name__ == "__main__"` blocks with sample data
- [ ] Risk matrix generator supports --html and --json output flags
- [ ] Weighted scoring script supports --json output flag
- [ ] All scripts exit with code 0 on success and non-zero on error

---

## 7. Harness Engineering Compliance

This project follows harness engineering principles, meaning every component is designed as a testable unit with defined interfaces, deterministic behavior, and clear pass/fail criteria.

### 7.1 Interface Contracts

Each script must define its interface contract at the top of the file in this format:

```python
"""
INTERFACE CONTRACT
==================
Input:  [exact input format and type]
Output: [exact output format and type]
Side effects: [none | file write to X | stdout only]
Exit codes: 0 = success, 1 = input validation error, 2 = runtime error
Dependencies: [stdlib only | list external packages]
"""

```

### 7.2 Deterministic Behavior

- Given identical input, scripts must produce identical output
- No use of random seeds, timestamps, or environment variables in core logic
- HTML output must use fixed styles, not dynamic theming

### 7.3 Testability

Each function in method-patterns.md must be verifiable with a minimal test case:

```python
# Minimal verification (not a full test suite)
assert classify_risk(25)["level"] == "red"
assert classify_risk(1)["level"] == "green"
assert magi_score(sample)["total"] > 0

```

---

## 8. Generation Workflow

When an AI agent is tasked with generating this project, it must follow this exact sequence:

### Step 1: Scaffold

Create the directory structure exactly as specified in Section 2. Do not add, remove, or rename any file.

### Step 2: Generate references/ First

Generate files in this order:
1. references/magi-framework.md
2. references/decision-matrix.md
3. references/method-patterns.md

Rationale: These files define the vocabulary, data structures, and logic that all other files depend on.

### Step 3: Generate scripts/

Generate files in this order:
1. scripts/weighted-scoring.py
2. scripts/risk-matrix-gen.py

Each script must:
- Import only from Python standard library
- Include the INTERFACE CONTRACT docstring
- Include the `if __name__ == "__main__"` block with sample data
- Pass all assertions defined in Section 7.3

### Step 4: Generate prompts/

Generate files in this order:
1. prompts/01-implement-method.md
2. prompts/02-robustness-checks.md

Each file must be self-contained and pass the portability test described in Section 5.1.

### Step 5: Generate SKILL.md Last

SKILL.md is generated last because it is purely an index that references all other files. It must be verified against the 120-line limit.

### Step 6: Validation

Run the following checks on the complete project:

```
VALIDATION CHECKLIST
====================
[ ] HC-01: All files are in English
[ ] HC-02: No emoji in any file
[ ] HC-03: SKILL.md is under 120 lines and contains no code blocks > 3 lines
[ ] HC-04: No code templates outside references/method-patterns.md
[ ] HC-05: prompts/ files are self-contained and portable
[ ] HC-06: All scripts have INTERFACE CONTRACT and pass minimal assertions
[ ] HC-07: All five design principles pass (Section 6)
[ ] File count: exactly 8 files (excluding this README)
[ ] Directory count: exactly 3 subdirectories (references/, prompts/, scripts/)

```

For programmatic verification, create a `validate_project.py` script in the project root that checks all HC constraints automatically. The script should:

1. Parse each file and scan for Unicode emoji ranges (reject on match for HC-02)
2. Count lines in SKILL.md and verify <= 120 (HC-03)
3. Scan for code blocks in SKILL.md and README FOR AI.md outside exempted sections (HC-04)
4. Verify prompts/ files are self-contained with no cross-references to other project files (HC-05)
5. Verify all scripts have INTERFACE CONTRACT docstrings (HC-06)
6. Count total files (excluding README) and verify == 8
7. Verify directory structure matches the defined tree exactly

Run this script after Step 6 of the Generation Workflow to automate validation.

---

## 9. Extension Protocol

When extending this project with new capabilities, follow these rules:

| Action | Rule |
|--------|------|
| Add a new analysis mode | Create a new file in prompts/ with the next numeric prefix (03-, 04-, ...) |
| Add a new script | Place in scripts/, add interface contract, add entry to method-patterns.md |
| Add a new reference | Place in references/, add routing entry to SKILL.md File Routing Map |
| Add a new persona | Extend magi-framework.md, update decision-matrix.md dimensions, update method-patterns.md schemas |
| Modify existing files | Update the file, then verify SKILL.md index entries still point to correct locations |

---

## 10. Anti-Patterns

The following practices are explicitly forbidden:

| Anti-Pattern | Why It Is Forbidden | Correct Alternative |
|-------------|---------------------|---------------------|
| Embedding code in SKILL.md | Violates HC-03 and HC-04 | Reference method-patterns.md by section number |
| Using emoji as status markers | Violates HC-02 | Use text labels: PASS, FAIL, HIGH, LOW |
| Hardcoding weights in scripts | Violates generic principle | Accept weights as function parameters with defaults |
| Cross-referencing prompts/ from agent files | Violates dual-mode separation | prompts/ files are human-only artifacts |
| Writing procedural narratives in SKILL.md | Violates compact principle | Use tables and one-line pointers |
| Adding comments in non-English | Violates HC-01 | All comments, docstrings, and labels in English |
| Creating files outside the defined tree | Violates modular principle | Use extension protocol in Section 9 |

---

## 11. Glossary

| Term | Definition |
|------|-----------|
| MAGI | Multi-perspective Analysis and Governance Interface; the project name inspired by the MAGI supercomputer system |
| MELCHIOR | The rational-scientist persona; data-driven, logic-first analysis |
| BALTHASAR | The prudent-guardian persona; risk-averse, bottom-line-oriented analysis |
| CASPER | The intuitive-observer persona; holistic, pattern-recognition analysis |
| Harness engineering | An approach where every component is a testable unit with defined inputs, outputs, and pass/fail criteria |
| Dual-mode | The separation between agent-invoked files (SKILL.md, references/, scripts/) and human-facing files (prompts/) |
| Progressive disclosure | The pattern where SKILL.md provides only routing; detailed content is loaded on demand from reference files |
| Veto condition | A hard constraint that, when triggered, overrides all scoring and rejects a proposal regardless of aggregate score |

---

## 12. Version and Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-09-11 | Initial release. Full project specification with 8 deliverable files across 3 module directories (excluding this README). |
