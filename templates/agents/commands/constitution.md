---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
argument-hint: "[project description or principles]"
handoffs:
  - label: Build Specification
    agent: grove.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.grove/memory/constitution.md`. This file defines the non-negotiable principles and governance rules for this project.

Follow this execution flow:

1. Load all available inputs:
   - Read constitution template: `.grove/templates/constitution-template.md`
   - Try to read existing constitution: `.grove/memory/constitution.md` (if exists)
   - Check `$ARGUMENTS` for user instructions or new principles

2. Generate updated constitution (intelligent merge):
   - Base structure: From constitution-template.md
   - Existing content: From memory/constitution.md (if exists)
   - User instructions: From $ARGUMENTS (if provided)
   - Fill placeholders with meaningful values:
     - `[PROJECT_NAME]`: Infer from directory name, README, or ask if unclear
     - `[PRINCIPLE_N_NAME]` and `[PRINCIPLE_N_DESCRIPTION]`: Use existing or create from input
     - `CONSTITUTION_VERSION`: Increment appropriately (MAJOR.MINOR.PATCH)
     - `RATIFICATION_DATE`: Keep original or use today if new
     - `LAST_AMENDED_DATE`: Update to today
   - Ensure no unexplained bracket tokens remain
   - Version increment rules:
     - MAJOR (X.0.0): Backward incompatible changes (principle removal, major redefinition)
     - MINOR (0.X.0): New principle added or materially expanded guidance
     - PATCH (0.0.X): Clarifications, wording fixes, non-semantic refinements

3. Consistency propagation (ensure dependent templates align):
   - Read and update if needed:
     - `.grove/templates/plan-template.md`: Constitution checks and principle alignment
     - `.grove/templates/spec-template.md`: Scope/requirements alignment
     - `.grove/templates/tasks-template.md`: Task categorization (observability, versioning, testing)
     - `README.md`, `docs/quickstart.md` (if exist): Update principle references

4. Generate sync impact report (prepend as HTML comment):
   - Version change: old → new
   - Modified principles: old title → new title (if renamed)
   - Added sections
   - Removed sections
   - Templates updated: ✅ updated / ⚠ pending (with file paths)
   - Follow-up TODOs: if any placeholders intentionally deferred

5. Validation before writing:
   - No unexplained bracket tokens (except deferred with justification)
   - Version matches report
   - Dates in ISO format (YYYY-MM-DD)
   - Principles are declarative, testable, specific
   - Governance section complete (amendment procedure, versioning, compliance)

6. Write constitution to `.grove/memory/constitution.md`:
   - Overwrite if exists
   - Create if new
   - Note: Will be automatically synced to `.claude/rules/constitution.md` by prerequisite scripts on next command execution

7. Display summary to user:
   - Version change and bump rationale
   - Key changes list
   - Templates updated count
   - Sync status (saved to memory, will sync to rules)
   - Suggested commit message: `docs: update constitution to v[X.Y.Z] ([change summary])`

---

## Formatting & Style Requirements

- Use Markdown headings exactly as in template (preserve hierarchy)
- Keep lines under 100 characters for readability
- Single blank line between sections
- No trailing whitespace
- Principles should be declarative and testable
- Avoid vague language ("should" → use "MUST" with rationale)

## Common Placeholders

- `[PROJECT_NAME]`: Name of the project (e.g., "TaskFlow", "SpecDrive")
- `[PRINCIPLE_N_NAME]`: Principle title (e.g., "Test-First Development")
- `[PRINCIPLE_N_DESCRIPTION]`: Principle explanation and rationale
- `[CONSTITUTION_VERSION]`: Semantic version (e.g., "1.0.0")
- `[RATIFICATION_DATE]`: Original adoption date (YYYY-MM-DD)
- `[LAST_AMENDED_DATE]`: Most recent amendment date (YYYY-MM-DD)

## Examples of Good Principles

**Good** (specific, testable):
- "Every feature must have passing tests before code review"
- "All libraries expose CLI interface with JSON output"
- "Breaking changes require MAJOR version bump"

**Bad** (vague, untestable):
- "Code should be well-tested"
- "Use good judgment for versioning"
- "Follow best practices"
