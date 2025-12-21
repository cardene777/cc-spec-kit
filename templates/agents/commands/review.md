---
description: Execute AI-powered review of task items (self-review or cross-review)
argument-hint: "[phase-name]"
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

0. **Sync Constitution to Claude Rules** (if needed):
   - If `.claude/rules/constitution.md` doesn't exist or contains only default comments (≤4 lines)
   - AND `.grove/memory/constitution.md` exists
   - Then copy `.grove/memory/constitution.md` to `.claude/rules/constitution.md` with AUTO-SYNCED header
   - This ensures Claude Code enforces project principles even if `/grove.constitution` wasn't run

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Parse Arguments**:
   - Extract phase name from `$ARGUMENTS` (optional)
   - If provided: Review only the specified phase (e.g., "phase-1")
   - If empty: Review all tasks in tasks.md

3. **Environment Detection** (FR-2 method):
   - Run `claude --help` or `code --help` using Bash tool
   - If exit code 0 → Current AI Agent = "claude"
   - If failed, run `codex --help` using Bash tool
   - If exit code 0 → Current AI Agent = "codex"
   - Otherwise → Current AI Agent = "unknown"

4. **Load tasks.md**:
   - Read `FEATURE_DIR/tasks.md`
   - **If tasks.md not found**:
     - ERROR: "tasks.md not found. Please run /grove.tasks first to generate task list."
     - HALT execution

5. **Extract AI Agent Metadata from tasks.md**:
   - Parse metadata section (YAML frontmatter or markdown section at top)
   - Extract "Implemented By" AI Agent name
   - If metadata not found, assume AI Agent = "unknown"

6. **Determine Review Type** (Self or Cross):
   - Compare "Implemented By" AI Agent name with Current AI Agent name
   - If same → **Self Review**
   - If different → **Cross Review**

7. **Execute Self Review** (if review type is Self):

   **7.1 Self Review Loop** (for each task item):
   - **Maximum iterations**: 3 attempts per task
   - **Target**: All tasks with unchecked "Self Review" sub-check

   For each task item:
   1. **Review**: Verify implementation against the requirement specified in task item
      - Read spec.md for requirement details
      - Read plan.md for technical approach
      - Read implemented files mentioned in tasks.md
      - Check if implementation matches requirement

   2. **Result Analysis**:
      - **PASS**: Implementation matches requirement → Proceed to step 7.2
      - **FAIL**: Issues found → Proceed to step 3

   3. **Auto-Fix** (if FAIL):
      - List all issues found
      - For each issue:
        - Read affected file(s)
        - Apply TDD fix: Write/update test → Fix implementation → Verify test passes
        - Update file(s)

   4. **Re-Review** (after fix):
      - Re-verify the task item
      - If PASS → Proceed to step 7.2
      - If FAIL → Increment iteration count
        - If iteration < 3: Repeat from step 3
        - If iteration = 3: Mark as FAIL with reason, proceed to step 7.2

   **7.2 Update tasks.md**:
   - For each task item reviewed:
     - If PASS: Update "Self Review" sub-check to `[x]` with ✓
     - If FAIL: Update "Self Review" sub-check to `[ ]` with ✗ and reason
   - Write updated tasks.md back to file

   **7.3 Generate Self Review Report**:
   - Create report directory: `FEATURE_DIR/reports/{current-agent}/`
   - Determine phase number from tasks.md (e.g., "Phase 1" → phase-1)
   - Generate report file: `self-review-phase-{N}.md`
   - Use FR-9 report template format (from SPEC.md):
     ```markdown
     # Phase {N} Verification Report

     **Date:** {YYYY-MM-DD HH:MM:SS}

     ---

     ## 1. Summary

     | Item        | Value        |
     | ----------- | ------------ |
     | Total Tasks | {total}      |
     | Passed      | {passed}     |
     | Failed      | {failed}     |
     | Phase Status| **{status}** |

     ### Risk Summary

     | Severity | Count       |
     | -------- | ----------- |
     | Critical | {count}     |
     | High     | {count}     |
     | Medium   | {count}     |
     | Low      | {count}     |

     ---

     ## 2. Task Summary

     | Task   | Type | Score  | Status  | Issues |
     | ------ | ---- | ------ | ------- | ------ |
     | {task_id} | {type} | {score} | {status} | {issues} |

     ---

     ## 3. Detailed Task Report

     ### Task {ID}

     #### 1. Information

     | Item     | Value        |
     | -------- | ------------ |
     | Type     | {type}       |
     | File     | `{filepath}` |
     | Score    | {score}      |
     | Status   | {status}     |

     ---

     #### 2. Verification Checklist

     * {item_1}
     * {item_2}
     * {item_3}

     ---

     #### 3. Verification Results

     **If no issues:**

     > No issues detected.

     **If issues found:**

     ##### Issue {N}

     | Item     | Details        |
     | -------- | -------------- |
     | Severity | {severity}     |
     | Location | `{location}`   |

     - **Description**
       {description}

     - **Root Cause**
       {reason}

     - **Recommended Fix**
       ```
       {fix_code}
       ```

     - **Evidence**
       ```
       {evidence_snippet}
       ```

     ---

     ## 4. Conclusion

     Phase {N} verification completed.
     Please prioritize Critical/High severity issues.
     ```
   - Save report

   **7.4 Self Review Summary**:
   - Display summary table:
     ```
     | Task Item | Status | Issues | Fixed |
     |-----------|--------|--------|-------|
     | T001      | ✓ PASS | 0      | -     |
     | T002      | ✗ FAIL | 2      | 1/2   |
     ```
   - Report location of detailed review report
   - If any items failed after 3 attempts: Suggest running `/grove.review` for cross-review

8. **Execute Cross Review** (if review type is Cross):

   **8.1 Cross Review Loop** (for each task item):
   - **No auto-fix**: Cross review only generates verification reports
   - **Target**: All tasks with unchecked "Cross Review" sub-check

   For each task item:
   1. **Review**: Verify implementation against the requirement specified in task item
      - Read spec.md for requirement details
      - Read plan.md for technical approach
      - Read implemented files mentioned in tasks.md
      - Check if implementation matches requirement

   2. **Record Issues**:
      - **PASS**: Implementation matches requirement → No issues
      - **FAIL**: List all issues found with:
        - Severity (Critical/High/Medium/Low)
        - Location (file:line)
        - Description
        - Root cause
        - Recommended fix (code snippet)
        - Evidence (code snippet showing the problem)

   **8.2 Update tasks.md**:
   - For each task item reviewed:
     - If PASS: Update "Cross Review" sub-check to `[x]` with ✓
     - If FAIL: Update "Cross Review" sub-check to `[ ]` with ✗ and brief reason
   - Write updated tasks.md back to file

   **8.3 Generate Cross Review Report**:
   - Create report directory: `FEATURE_DIR/reports/{current-agent}/`
   - Generate timestamp: `YYYYMMDD-HHMMSS` (e.g., "20251219-143022")
   - Generate report file: `cross-review-{timestamp}.md`
   - Use same FR-9 report template format as Self Review (step 7.3)
   - Save report

   **8.4 Generate summary.md** (FR-9 summary format):
   - Generate summary file: `FEATURE_DIR/reports/{current-agent}/summary.md`
   - **IMPORTANT**: This file is overwritten each time cross-review runs (keeps only latest)
   - Use summary.md template format:
     ```markdown
     # Cross-Review Summary

     **Date**: {YYYY-MM-DD HH:MM:SS}
     **Reviewer**: {current-agent} (claude/codex/etc)
     **Detailed Report**: `cross-review-{timestamp}.md`

     ---

     ## Verification Results Summary

     | Item        | Value   |
     | ----------- | ------- |
     | Total Tasks | {total} |
     | Passed      | {pass}  |
     | Failed      | {fail}  |

     ---

     ## Issues by Severity

     | Severity | Count   |
     | -------- | ------- |
     | Critical | {count} |
     | High     | {count} |
     | Medium   | {count} |
     | Low      | {count} |

     ---

     ## Critical/High Issues List

     ### Issue {N}: {Issue Summary}

     - **Severity**: {Critical/High}
     - **Location**: `{file:line}`
     - **Description**: {Issue description (1-2 lines)}
     - **Recommended Fix**: {Fix summary (1-2 lines)}

     (Only Critical/High issues are listed)

     ---

     ## Next Steps

     ### If Issues Exist

     To automatically fix issues, run the following command:

     ```bash
     /grove.fix
     ```

     Or to fix a specific phase only:

     ```bash
     /grove.fix phase-1
     ```

     ### If No Issues

     All verification passed. Continue with implementation.

     ---

     ## Detailed Information

     For detailed verification report, see:
     - `cross-review-{timestamp}.md`
     ```
   - Save summary.md (overwrite if exists)

   **8.5 Display summary.md Content**:
   - Read and display the generated summary.md content
   - Show Critical/High problems prominently
   - Display "/grove.fix usage instructions" section

   **8.6 Cross Review Summary**:
   - Display summary table:
     ```
     | Task Item | Status | Critical | High | Medium | Low |
     |-----------|--------|----------|------|--------|-----|
     | T001      | ✓ PASS | 0        | 0    | 0      | 0   |
     | T002      | ✗ FAIL | 1        | 2    | 1      | 0   |
     ```
   - Report location of detailed cross-review report
   - Report location of summary.md
   - Display "/grove.fix" usage instructions

9. **Execution Mode** (applies to both Self and Cross Review):
   - **Claude Code environment**:
     - Use Task tool with `run_in_background: true` for review process (optional, based on user preference)
     - Allow user to continue working while review runs
     - Report when background review completes

   - **Codex environment** or **Unknown**:
     - Run review synchronously
     - Display progress as items are reviewed
     - Report when all items complete

10. **Final Report**:
   - Summary of all tasks reviewed
   - Total task items: {count}
   - Review type: Self Review / Cross Review
   - Passed items: {count}
   - Failed items: {count}
   - Reports generated:
     - Self Review: `FEATURE_DIR/reports/{agent}/self-review-phase-{N}.md`
     - Cross Review: `FEATURE_DIR/reports/{agent}/cross-review-{timestamp}.md` + `summary.md`

Note: This command requires tasks.md to exist. If tasks.md is missing, suggest running `/grove.tasks` first.
