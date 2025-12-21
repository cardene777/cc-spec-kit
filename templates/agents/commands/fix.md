---
description: Fix issues found in cross-review reports and re-run self-review
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
   - If provided: Fix only the specified phase (e.g., "phase-1")
   - If empty: Fix all tasks that have cross-review reports

3. **Environment Detection** (FR-2 method):
   - Run `claude --help` or `code --help` using Bash tool
   - If exit code 0 → Current AI Agent = "claude"
   - If failed, run `codex --help` using Bash tool
   - If exit code 0 → Current AI Agent = "codex"
   - Otherwise → Current AI Agent = "unknown"

4. **Load summary.md**:
   - Read `FEATURE_DIR/reports/{current-agent}/summary.md`
   - **If summary.md not found**:
     - ERROR: "summary.md not found. Please run /grove.review first to generate cross-review report."
     - HALT execution

5. **Extract Fix Information from summary.md**:
   - Parse "Verification Results Summary" section → Get total failed count
   - Parse "Issues by Severity" section → Get Critical/High/Medium/Low counts
   - Parse "Critical/High Issues List" section → Extract all Critical/High issues:
     - Issue number
     - Problem summary
     - Severity
     - Location (file:line)
     - Description (1-2 lines)
     - Recommended fix (1-2 lines)
   - Parse "Detailed Information" section → Get detailed report filename (e.g., `cross-review-20251219-143022.md`)

6. **Load Detailed Cross-Review Report**:
   - Read `FEATURE_DIR/reports/{current-agent}/{report-filename}` (from step 5)
   - **If report not found**:
     - ERROR: "Cross-review report not found. Please run /grove.review first."
     - HALT execution

7. **Extract All Issues from Detailed Report**:
   - Parse "3. Detailed Task Report" section
   - For each Task section:
     - Extract task ID
     - Extract file path
     - Extract all Issue sections:
       - Issue number
       - Severity (Critical/High/Medium/Low)
       - Location (file:line)
       - Description
       - Root cause (Root Cause)
       - Recommended fix code (Recommended Fix)
       - Evidence code snippet (Evidence)

8. **Fix Each Issue** (TDD approach):

   **8.1 Prioritize Issues**:
   - Sort issues by severity: Critical → High → Medium → Low
   - Within same severity: Sort by file path (group fixes by file)

   **8.2 Fix Loop** (for each issue):
   1. **Display Issue**:
      - Show issue number, severity, location, description
      - Show recommended fix code

   2. **Read Affected File**:
      - Read the file mentioned in "Location" field
      - Locate the exact line number

   3. **Apply TDD Fix**:
      - **If tests exist for this file**:
        a. Read test file
        b. Write/update test to catch the issue (RED state)
        c. Run tests to confirm they fail
        d. Apply recommended fix to implementation
        e. Run tests to confirm they pass (GREEN state)
        f. Refactor if needed while keeping tests green

      - **If no tests exist**:
        a. Apply recommended fix directly to implementation
        b. Write basic test to verify the fix
        c. Run test to confirm it passes

   4. **Update File**:
      - Write the fixed code back to the file
      - Record fix in a summary list

   5. **Progress Report**:
      - Report: "Fixed issue {N}/{total}: {severity} in {file:line}"

9. **Re-run Self Review** (automatic after all fixes):

   **9.1 Trigger Self Review**:
   - Invoke the same self-review logic as `/grove.review` (self-review mode)
   - Review ALL task items again to verify fixes

   **9.2 Self Review Loop** (same as review.md step 7):
   - Maximum iterations: 3 attempts per item
   - For each task item:
     1. Review implementation against requirement
     2. If PASS → Mark "Self Review" as `[x]` with ✓
     3. If FAIL → Auto-fix (up to 3 iterations)
     4. If still FAIL after 3 iterations → Mark as `[ ]` with ✗ and reason

   **9.3 Generate Updated Self Review Report**:
   - Create/update report: `FEATURE_DIR/reports/{current-agent}/self-review-phase-{N}.md`
   - Use FR-9 report template format
   - Save report

   **9.4 Update tasks.md**:
   - Update "Self Review" sub-checks with new results
   - Write updated tasks.md back to file

10. **Fix Summary**:
   - Display fix summary table:
     ```
     | File                | Issues Fixed | Issues Remaining |
     |---------------------|--------------|------------------|
     | src/auth.ts         | 3            | 0                |
     | src/database.ts     | 2            | 1                |
     | tests/auth.test.ts  | 1            | 0                |
     ```

   - Display severity breakdown:
     ```
     | Severity | Fixed | Remaining |
     |----------|-------|-----------|
     | Critical | 2     | 0         |
     | High     | 3     | 1         |
     | Medium   | 1     | 0         |
     | Low      | 0     | 0         |
     ```

   - Display self-review result:
     ```
     | Task Item | Before | After  | Status |
     |-----------|--------|--------|--------|
     | T001      | ✗ FAIL | ✓ PASS | Fixed  |
     | T002      | ✗ FAIL | ✗ FAIL | Needs Manual Fix |
     ```

11. **Next Steps Recommendation**:
   - **If all issues fixed and self-review passes**:
     - "All issues have been fixed! Self-review passed for all items."
     - "You can now run /grove.review again from a different AI Agent for another cross-review."

   - **If some issues remain**:
     - "Some issues could not be fixed automatically. Review the following:"
     - List remaining issues with their locations
     - "Please fix these manually or run /grove.fix again after making changes."

   - **If self-review still fails after fixes**:
     - "Fixes were applied, but self-review detected new or remaining issues."
     - "Review the updated self-review report: {report-path}"
     - "Consider running /grove.review from a different AI Agent for additional insights."

12. **Execution Mode** (applies to both Fix and Self-Review):
   - **Claude Code environment**:
     - Use Task tool with `run_in_background: true` for fix process (optional)
     - Use Task tool with `run_in_background: true` for self-review process
     - Allow user to continue working while processes run
     - Report when background processes complete

   - **Codex environment** or **Unknown**:
     - Run fix process synchronously
     - Display progress as issues are fixed
     - Run self-review synchronously
     - Report when all processes complete

13. **Error Handling**:
   - **summary.md not found**: HALT with error message (step 4)
   - **Detailed report not found**: HALT with error message (step 6)
   - **Recommended fix code unclear**: Ask user for clarification
   - **File not found**: HALT with error message and suggest checking file paths
   - **Tests fail after fix**: Revert fix and mark issue as "manual fix required"
   - **Self-review fails after 3 iterations**: Mark item as failed and continue

Note: This command requires cross-review to have been run first. If summary.md is missing, suggest running `/grove.review` first.
