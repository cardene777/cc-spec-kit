---
description: Execute AI-powered review of task items (self-review or cross-review)
argument-hint: "[phase-name]"
handoffs:
  - label: Fix Issues (if review found problems)
    agent: grove.fix
    prompt: Fix issues found in cross-review report
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

1. Run prerequisite script and parse paths:
   - Execute {SCRIPT} from repository root
   - Parse FEATURE_DIR and AVAILABLE_DOCS from JSON output
   - All paths must be absolute
   - For single quotes in args: use escape syntax 'I'\''m Groot' or double-quote "I'm Groot"

2. Parse arguments and detect environment:
   - Extract phase name from $ARGUMENTS (optional)
   - If provided: Review only specified phase (e.g., "phase-1")
   - If empty: Review all tasks in tasks.md
   - Detect current AI Agent (FR-2 method):
     - Run `claude --help` or `code --help` → If exit code 0: AI Agent = "claude"
     - If failed, run `codex --help` → If exit code 0: AI Agent = "codex"
     - Otherwise: AI Agent = "unknown"

3. Load tasks.md and extract metadata:
   - Read FEATURE_DIR/tasks.md
   - If tasks.md not found:
     - ERROR: "tasks.md not found. Please run /grove.tasks first to generate task list."
     - HALT execution
   - Parse metadata section (YAML frontmatter or markdown)
   - Extract "Implemented By" AI Agent name
   - If metadata not found: assume AI Agent = "unknown"

4. Determine review type:
   - Compare "Implemented By" AI Agent name with Current AI Agent name
   - If same → Self Review
   - If different → Cross Review

5. Execute Self Review (if review type is Self):
   - Self Review Loop (for each task item):
     - Maximum iterations: 3 attempts per task
     - Target: All tasks with unchecked "Self Review" sub-check
   - For each task item:
     - Review: Verify implementation against requirement
       - Read spec.md for requirement details
       - Read plan.md for technical approach
       - Read implemented files mentioned in tasks.md
       - Check if implementation matches requirement
     - Result Analysis:
       - PASS: Implementation matches requirement → Update tasks.md
       - FAIL: Issues found → Proceed to Auto-Fix
     - Auto-Fix (if FAIL):
       - List all issues found
       - For each issue: Apply TDD fix (Write/update test → Fix implementation → Verify test passes)
       - Update file(s)
     - Re-Review (after fix):
       - Re-verify task item
       - If PASS → Update tasks.md
       - If FAIL → Increment iteration count (max 3 attempts)
   - Update tasks.md:
     - For each task item reviewed:
       - If PASS: Update "Self Review" sub-check to [x] with ✓
       - If FAIL: Update "Self Review" sub-check to [ ] with ✗ and reason
     - Write updated tasks.md back to file
   - Generate Self Review Report:
     - Create report directory: FEATURE_DIR/reports/{current-agent}/
     - Determine phase number from tasks.md
     - Generate report file: self-review-phase-{N}.md
     - Use FR-9 report template format (detailed format below):
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
   - Display Self Review Summary:
     - Display summary table with Task Item, Status, Issues, Fixed columns
     - Report location of detailed review report
     - If any items failed after 3 attempts: Suggest running /grove.review for cross-review

6. Execute Cross Review (if review type is Cross):
   - Cross Review Loop (for each task item):
     - No auto-fix: Cross review only generates verification reports
     - Target: All tasks with unchecked "Cross Review" sub-check
   - For each task item:
     - Review: Verify implementation against requirement
       - Read spec.md for requirement details
       - Read plan.md for technical approach
       - Read implemented files mentioned in tasks.md
       - Check if implementation matches requirement
     - Record Issues:
       - PASS: Implementation matches requirement → No issues
       - FAIL: List all issues with Severity, Location, Description, Root cause, Recommended fix, Evidence
   - Update tasks.md:
     - For each task item reviewed:
       - If PASS: Update "Cross Review" sub-check to [x] with ✓
       - If FAIL: Update "Cross Review" sub-check to [ ] with ✗ and brief reason
     - Write updated tasks.md back to file
   - Generate Cross Review Report:
     - Create report directory: FEATURE_DIR/reports/{current-agent}/
     - Generate timestamp: YYYYMMDD-HHMMSS
     - Generate report file: cross-review-{timestamp}.md
     - Use same FR-9 report template format as Self Review
     - Save report
   - Generate summary.md (FR-9 summary format):
     - Generate summary file: FEATURE_DIR/reports/{current-agent}/summary.md
     - IMPORTANT: This file is overwritten each time cross-review runs (keeps only latest)
     - Use summary.md template format (detailed format below):
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
   - Display summary.md content:
     - Read and display generated summary.md
     - Show Critical/High problems prominently
     - Display /grove.fix usage instructions
   - Display Cross Review Summary:
     - Display summary table with Task Item, Status, Critical, High, Medium, Low columns
     - Report location of detailed cross-review report
     - Report location of summary.md
     - Display /grove.fix usage instructions

7. Execution mode (applies to both Self and Cross Review):
   - Claude Code environment:
     - Use Task tool with run_in_background: true for review process (optional)
     - Allow user to continue working while review runs
     - Report when background review completes
   - Codex environment or Unknown:
     - Run review synchronously
     - Display progress as items are reviewed
     - Report when all items complete

8. Display final report:
   - Summary of all tasks reviewed
   - Total task items
   - Review type: Self Review / Cross Review
   - Passed items
   - Failed items
   - Reports generated:
     - Self Review: FEATURE_DIR/reports/{agent}/self-review-phase-{N}.md
     - Cross Review: FEATURE_DIR/reports/{agent}/cross-review-{timestamp}.md + summary.md

---

## Guidelines

### Report Template Format

See detailed FR-9 report template format in steps 5 and 6 above.

### Notes

- This command requires tasks.md to exist
- If tasks.md missing: suggest running /grove.tasks first
- Self Review: Includes auto-fix (max 3 attempts per task)
- Cross Review: No auto-fix, generates detailed reports only
