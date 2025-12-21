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

You are updating the project constitution. The constitution is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the constitution template and check template usage setting:
   - **First**, read `.grove/templates/constitution-template.md` (the master template) using Read tool
   - **Check YAML frontmatter** for `enabled` field:
     - If `enabled: true`: Template contains sample content that can be used as-is or as a starting point
     - If `enabled: false` or missing: Template contains only placeholder structure
   - **Then**, try to read `.grove/memory/constitution.md` using Read tool (previously filled version with concrete values)
     - If Read succeeds → file exists
     - If Read returns error (file not found) → file does NOT exist

   **Decision logic**:
   - If `.grove/memory/constitution.md` exists → **MUST ask user for confirmation. DO NOT proceed without user choice** (use AskUserQuestion tool if available):
     - Use existing constitution as-is
     - Use existing constitution as base and improve
     - Ignore existing constitution and create from scratch
     - Keep current constitution and cancel this request
   - If `.grove/memory/constitution.md` does NOT exist AND `enabled: true` → **STOP and ask user which approach to use. NEVER use template without confirmation** (use AskUserQuestion tool if available):
     - Use template as-is
     - Use template as base and improve
     - Ignore template and create from scratch
     - Cancel this request
     - **IMPORTANT**: Wait for user's explicit choice before proceeding
   - If `.grove/memory/constitution.md` does NOT exist AND `enabled: false` → Create from scratch using placeholder structure (no template content available)

   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.grove/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.grove/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.grove/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`) if present. Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution to `.grove/memory/constitution.md` (overwrite if exists, create if not).

8. Sync constitution to Claude Code rules (if Claude Code environment detected):

   a. Check if running in Claude Code environment:
      - Try to read `.claude/commands/grove.constitution.md` using Read tool
      - If Read succeeds → Claude Code environment detected, proceed to step b
      - If Read fails (file not found) → Not Claude Code environment, skip to step 9

   b. Sync constitution to Claude Code rules:
      - Read the content from `.grove/memory/constitution.md`
      - Add header comment and write to `.claude/rules/constitution.md`:
        ```markdown
        <!-- AUTO-SYNCED from .grove/memory/constitution.md -->
        <!-- Do not edit this file directly. Update the source constitution instead. -->
        <!-- Last synced: [CURRENT_DATE] -->

        [CONSTITUTION CONTENT]
        ```
      - Report: "✓ Constitution synced to Claude Code rules (.claude/rules/constitution.md)"
      - Explain: "Claude Code will now enforce these principles in all interactions"

9. Output a final summary to the user with:
   - New version and bump rationale.
   - Claude Code rules sync status (if applicable).
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not modify the master template at `.grove/templates/constitution-template.md`; always write the filled version to `.grove/memory/constitution.md`.
