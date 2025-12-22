---
description: Fix issues found in cross-review reports and re-run self-review
argument-hint: "[phase-name]"
handoffs:
  - label: Run Cross-Review Again (verify fixes)
    agent: grove.review
    prompt: Run cross-review to verify all fixes are correct
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
   - If provided: Fix only specified phase (e.g., "phase-1")
   - If empty: Fix all tasks that have cross-review reports
   - Detect current AI Agent (FR-2 method):
     - Run `claude --help` or `code --help` → If exit code 0: AI Agent = "claude"
     - If failed, run `codex --help` → If exit code 0: AI Agent = "codex"
     - Otherwise: AI Agent = "unknown"

3. Load summary.md:
   - Read FEATURE_DIR/reports/{current-agent}/summary.md
   - If summary.md not found:
     - ERROR: "summary.md not found. Please run /grove.review first to generate cross-review report."
     - HALT execution

4. Extract fix information from summary.md:
   - Parse "Verification Results Summary" → Get total failed count
   - Parse "Issues by Severity" → Get Critical/High/Medium/Low counts
   - Parse "Critical/High Issues List" → Extract all Critical/High issues with Issue number, Severity, Location, Description, Recommended fix
   - Parse "Detailed Information" → Get detailed report filename

5. Load detailed cross-review report:
   - Read FEATURE_DIR/reports/{current-agent}/{report-filename}
   - If report not found:
     - ERROR: "Cross-review report not found. Please run /grove.review first."
     - HALT execution

6. Extract all issues from detailed report:
   - Parse "3. Detailed Task Report" section
   - For each Task section: Extract task ID, file path, all Issue sections with Issue number, Severity, Location, Description, Root cause, Recommended fix code, Evidence

7. Fix each issue using TDD approach:
   - Prioritize issues: Sort by severity (Critical → High → Medium → Low), then by file path
   - Fix Loop (for each issue):
     - Display issue: Show issue number, severity, location, description, recommended fix code
     - Read affected file: Read file mentioned in Location field, locate exact line number
     - Apply TDD Fix:
       - If tests exist: Read test → Write/update test (RED) → Apply fix → Run tests (GREEN) → Refactor
       - If no tests: Apply fix → Write basic test → Run test to confirm pass
     - Update file: Write fixed code back to file, record fix in summary list
     - Progress report: "Fixed issue {N}/{total}: {severity} in {file:line}"

8. Re-run Self Review (automatic after all fixes):
   - Trigger Self Review: Invoke same self-review logic as /grove.review
   - Review ALL task items again to verify fixes
   - Self Review Loop (same as review.md):
     - Maximum iterations: 3 attempts per item
     - For each task item: Review → PASS (mark [x]) or FAIL (auto-fix up to 3 iterations)
   - Generate Updated Self Review Report: Create/update FEATURE_DIR/reports/{current-agent}/self-review-phase-{N}.md
   - Update tasks.md: Update "Self Review" sub-checks with new results

9. Display fix summary:
   - Display fix summary table with File, Issues Fixed, Issues Remaining columns
   - Display severity breakdown with Severity, Fixed, Remaining columns
   - Display self-review result with Task Item, Before, After, Status columns
   - Report key outcomes:
     - If all issues fixed and self-review passes: "All issues fixed! Self-review passed."
     - If some issues remain: List remaining issues with locations
     - If self-review still fails: Display updated self-review report path

10. Execution mode (applies to both Fix and Self-Review):
   - Claude Code environment:
     - Use Task tool with run_in_background: true for fix and self-review (optional)
     - Allow user to continue working while processes run
     - Report when background processes complete
   - Codex environment or Unknown:
     - Run fix process synchronously
     - Display progress as issues are fixed
     - Run self-review synchronously
     - Report when all processes complete

---

## Guidelines

### Error Handling

- summary.md not found: HALT with error message (step 3)
- Detailed report not found: HALT with error message (step 5)
- Recommended fix code unclear: Ask user for clarification
- File not found: HALT with error message and suggest checking file paths
- Tests fail after fix: Revert fix and mark issue as "manual fix required"
- Self-review fails after 3 iterations: Mark item as failed and continue

### Notes

- This command requires cross-review to have been run first
- If summary.md missing: suggest running /grove.review first
- TDD approach: Write test (RED) → Apply fix → Run test (GREEN) → Refactor
- Self-review automatically re-runs after fixes to verify correctness
