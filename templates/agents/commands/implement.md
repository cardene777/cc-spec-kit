---
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
argument-hint: ""
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - Scan all checklist files in the checklists/ directory
   - For each checklist, count:
     - Total items: All lines matching `- [ ]` or `- [X]` or `- [x]`
     - Completed items: Lines matching `- [X]` or `- [x]`
     - Incomplete items: Lines matching `- [ ]`
   - Create a status table:

     ```text
     | Checklist | Total | Completed | Incomplete | Status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ PASS |
     | test.md   | 8     | 5         | 3          | ✗ FAIL |
     | security.md | 6   | 6         | 0          | ✓ PASS |
     ```

   - Calculate overall status:
     - **PASS**: All checklists have 0 incomplete items
     - **FAIL**: One or more checklists have incomplete items

   - **If any checklist is incomplete**:
     - Display the table with incomplete item counts
     - **STOP** and ask: "Some checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
     - Wait for user response before continuing
     - If user says "no" or "wait" or "stop", halt execution
     - If user says "yes" or "proceed" or "continue", proceed to step 3

   - **If all checklists are complete**:
     - Display the table showing all checklists passed
     - Automatically proceed to step 3

3. **Prerequisites Check (TDD Integration)**:
   - **REQUIRED**: Verify spec.md exists (ERROR if missing: "spec.md not found. Please run /grove.spec first.")
   - **REQUIRED**: Verify plan.md exists (ERROR if missing: "plan.md not found. Please run /grove.plan first.")
   - **REQUIRED**: Verify tasks.md exists (ERROR if missing: "tasks.md not found. Please run /grove.tasks first.")
   - **OPTIONAL**: Try to read `.grove/design/README.md` to check if design specifications exist for UI implementation guidance

4. Load and analyze the implementation context:
   - **REQUIRED**: Read tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **REQUIRED**: Read spec.md for feature requirements
   - **OPTIONAL**: Try to read data-model.md using Read tool (if Read succeeds, use for entities and relationships; if error, skip)
   - **OPTIONAL**: Try to read contracts/ files using Read tool (if exist, use for API specifications and test requirements; if not, skip)
   - **OPTIONAL**: Try to read research.md using Read tool (if exists, use for technical decisions and constraints; if not, skip)
   - **OPTIONAL**: Try to read quickstart.md using Read tool (if exists, use for integration scenarios; if not, skip)
   - **OPTIONAL**: Try to read `.grove/design/README.md` using Read tool (if exists, read design specifications for UI implementation):
     - design-system.md (design tokens: colors, typography, spacing)
     - components/ (component specifications and code)
     - layouts/ (layout specifications and code)

5. **Project Setup Verification**:
   - **REQUIRED**: Create/verify ignore files based on actual project setup:

   **Detection & Creation Logic**:
   - Check if the following command succeeds to determine if the repository is a git repo (create/verify .gitignore if so):

     ```sh
     git rev-parse --git-dir 2>/dev/null
     ```

   - Check if Dockerfile* exists or Docker in plan.md → create/verify .dockerignore
   - Check if .eslintrc* exists → create/verify .eslintignore
   - Check if eslint.config.* exists → ensure the config's `ignores` entries cover required patterns
   - Check if .prettierrc* exists → create/verify .prettierignore
   - Check if .npmrc or package.json exists → create/verify .npmignore (if publishing)
   - Check if terraform files (*.tf) exist → create/verify .terraformignore
   - Check if .helmignore needed (helm charts present) → create/verify .helmignore

   **If ignore file already exists**: Verify it contains essential patterns, append missing critical patterns only
   **If ignore file missing**: Create with full pattern set for detected technology

   **Common Patterns by Technology** (from plan.md tech stack):
   - **Node.js/JavaScript/TypeScript**: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
   - **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
   - **Java**: `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
   - **C#/.NET**: `bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
   - **Go**: `*.exe`, `*.test`, `vendor/`, `*.out`
   - **Ruby**: `.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
   - **PHP**: `vendor/`, `*.log`, `*.cache`, `*.env`
   - **Rust**: `target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
   - **Kotlin**: `build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
   - **C++**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
   - **C**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `Makefile`, `config.log`, `.idea/`, `*.log`, `.env*`
   - **Swift**: `.build/`, `DerivedData/`, `*.swiftpm/`, `Packages/`
   - **R**: `.Rproj.user/`, `.Rhistory`, `.RData`, `.Ruserdata`, `*.Rproj`, `packrat/`, `renv/`
   - **Universal**: `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

   **Tool-Specific Patterns**:
   - **Docker**: `node_modules/`, `.git/`, `Dockerfile*`, `.dockerignore`, `*.log*`, `.env*`, `coverage/`
   - **ESLint**: `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
   - **Prettier**: `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - **Terraform**: `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
   - **Kubernetes/k8s**: `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

6. **Initial Documentation Sync** (if needed):
   - Check if `.grove/docs/` directory exists using Read tool (try to read any file in it)
   - **If not exists** (Read tool returns error):
     - Display: `"📚 Initializing project documentation..."`
     - Run `grove sync --auto` via Bash
     - Wait for completion
     - Display: `"✓ Documentation structure initialized"`
   - **If exists**:
     - Skip sync (documentation already exists)

7. Parse tasks.md structure and extract:
   - **Task phases**: Setup, Tests, Core, Integration, Polish
   - **Task dependencies**: Sequential vs parallel execution rules
   - **Task details**: ID, description, file paths, parallel markers [P]
   - **Execution flow**: Order and dependency requirements

8. **Execute implementation with background Self Review**:

   **⚠️ CRITICAL ENFORCEMENT RULES**:
   - **NEVER skip any step for any reason** (including "simple" or "setup" tasks)
   - **NEVER mark checkboxes without actual verification**
   - **NEVER assume "no test needed"** - all tasks require verification
   - **MUST execute TDD Cycle for every task** (Red→Green→Refactor)
   - **MUST execute Self Review for every task** (unless `--skip-self-review` flag)
   - **VIOLATION = WORKFLOW FAILURE** - restart from current task

   **8.1. Environment Detection and Initialization (once at start)**:
   - Run `claude --help` or `code --help` (exit code 0 → Claude Code environment)
   - Run `codex --help` (exit code 0 → Codex environment)
   - Otherwise → Unknown environment (proceed with sync review)
   - Check if `$ARGUMENTS` contains `--skip-self-review` to skip all Self Review steps
   - **Initialize background job tracking** (Claude Code only):
     - Create empty dictionary to track: `background_jobs = {}`  # Verification jobs
     - Create empty dictionary to track: `doc_jobs = {}`         # Documentation jobs
     - Format: `{task_id: job_id}` for later retrieval

   **8.2. For each task in current phase (execute in order)**:

   **7.2.1. TDD Cycle (Red → Green → Refactor) - MANDATORY FOR ALL TASKS**:

   **1. Red (REQUIRED)**: Write a failing test first
      - **MUST** add new test cases for the functionality to be implemented
      - **MUST** run tests and confirm they fail (RED state)
      - **MUST** show test output proving failure
      - If .grove/design/ exists: Reference design-system.md tokens when writing UI tests
      - **Examples of valid tests for "simple" tasks**:
        - Setup task: `test -d expected_directory && echo "PASS" || echo "FAIL"`
        - Config task: Validate JSON/YAML syntax with parser
        - File creation: Check file exists and has expected content
      - **NO EXCEPTIONS**: Even directory creation tasks need verification tests

   2. **Green (REQUIRED)**: Implement minimal code to pass the test
      - **MUST** write the simplest implementation that makes tests pass
      - If .grove/design/ exists: Follow component specifications from components/
      - **MUST** run tests and confirm they pass (GREEN state)
      - **MUST** show test output proving success

   3. **Refactor (REQUIRED)**: Clean up code while keeping tests green
      - **MUST** improve code structure, remove duplication
      - If .grove/design/ exists: Apply design tokens from design-system.md
      - **MUST** keep tests passing throughout refactoring
      - **MUST** run tests after refactoring to confirm GREEN state

   4. **Update TDD checklist (ONLY AFTER VERIFICATION)**:
      - **ONLY mark [X] if you actually executed the step and have evidence**
      - [X] Red: Added new tests and confirmed they fail ← MUST show failed test output
      - [X] Green: Implemented minimal code to pass tests ← MUST show passed test output
      - [X] Refactor: Cleaned up code while keeping tests green ← MUST show passed test output
      - **NEVER mark [X] based on assumption or "it should work"**

   **7.2.2. Self Review (background execution) - MANDATORY UNLESS SKIPPED**:

   **Skip condition**: ONLY skip if `--skip-self-review` flag is present in `$ARGUMENTS`.
   **Otherwise**: Launch Self Review in background (Claude Code) or execute synchronously (others).

   **A. Claude Code Environment (BACKGROUND EXECUTION with report generation)**:

   - **Determine report path**: `FEATURE_DIR/reports/self-review/task-{task_id}.md`
   - **Create report directory if needed**: `mkdir -p FEATURE_DIR/reports/self-review/`
   - **Launch verification agent in background using Task tool**

   **Launch Method**:
   Use Task tool with the following parameters:

   ```python
   Task(
       description="Verify {task_id} and generate report",
       prompt="""
Verify task {task_id} implementation and generate verification report.

**Input Parameters**:
- task_id: {task_id}
- task_description: {task_description from tasks.md}
- task_files: [{list of file paths from task}]
- current_phase: {current_phase_number}
- report_path: {FEATURE_DIR}/reports/self-review/task-{task_id}.md

**Your Mission**:
1. Read context files (spec.md, plan.md, tasks.md)
2. Read all implementation files from task_files list
3. Execute 8-point verification checklist (see verification.md)
4. Calculate score (0-100 based on severity deductions)
5. Generate Markdown report following verification.md template
6. Save report to report_path using Write tool
7. Complete (no return value needed - main agent will read report file)
""",
       subagent_type="verification-agent",
       run_in_background=True  # ← CRITICAL: Must run in background
   )
   ```

   **After Launch**:
   - Store job ID: `background_jobs[task_id] = job_id`
   - Display: `"🔄 {task_id} Self Review launched in background (job: {job_id})"`
   - Display: `"   Report will be saved to: reports/self-review/task-{task_id}.md"`
   - **Immediately proceed to step 8.2.2b** (don't wait for result)

   **B. Codex or Other Environments (SYNCHRONOUS EXECUTION)**:

   - **MUST** use verification template: `.grove/templates/verification-template.md`
   - **Execute verification synchronously**:
     1. Read task context (spec.md, plan.md, tasks.md)
     2. Execute verification checklist (all 8 items)
     3. Calculate score (0-100) based on severity deductions
     4. Document issues if found
   - **Display verification results immediately**
   - **Proceed to step 8.2.2b after completion**

   **8.2.2b. Documentation Update (background execution) - Claude Code ONLY**:

   **Claude Code Environment (BACKGROUND EXECUTION)**:

   - **Launch documentation agent in background using Task tool**

   **Launch Method**:
   Use Task tool with the following parameters:

   ```python
   Task(
       description="Update documentation for {task_id}",
       prompt="""
Update documentation for task {task_id}.

**Input Parameters**:
- task_id: {task_id}
- task_description: {task_description from tasks.md}
- task_files: [{list of file paths from task}]
- source_dir: {auto-detected or from plan.md}
- feature_dir: {FEATURE_DIR}

Follow the documentation workflow defined in documentation.md.
""",
       subagent_type="documentation-agent",
       run_in_background=True  # ← CRITICAL: Must run in background
   )
   ```

   **After Launch**:
   - Store job ID: `doc_jobs[task_id] = job_id`
   - Display: `"📚 {task_id} Documentation update launched in background (job: {job_id})"`
   - **Immediately proceed to step 8.2.3** (don't wait for result)

   **Codex or Other Environments**:
   - Skip documentation update (not supported in background)
   - Documentation can be updated manually as needed
   - **Proceed to step 8.2.3**

   **8.2.3. Update tasks.md (TDD checklist only for now)**:

   **Claude Code Environment** (background Self Review):
   - Mark TDD checklist items as [X] (only if you showed test output):
     - [X] Red: Added new tests and confirmed they fail
     - [X] Green: Implemented minimal code to pass tests
     - [X] Refactor: Cleaned up code while keeping tests green
   - **Leave Self Review checkbox UNCHECKED**: `[ ] Self Review: Automated verification completed`
     - Results pending (running in background)
     - Will be updated in step 7.5 after collecting results
   - **DO NOT mark task checkbox [X] yet**
     - Task completion pending Self Review results
   - Write updated tasks.md

   **Codex or Other Environments** (synchronous Self Review):
   - Mark TDD checklist items as [X]
   - Mark "Self Review" sub-check with result (already obtained):
     - `[x] Self Review: Automated verification completed ✓ (Score: {score}/100)` if score ≥ 80
     - `[ ] Self Review: Automated verification completed ✗ (Score: {score}/100, {issue_count} issues)` if score < 80
   - Mark task checkbox as [X] ONLY if:
     - TDD checklist all [X]
     - Self Review [x] (PASS)
   - **NEVER mark task [X] if Self Review failed**
   - Write updated tasks.md

   **8.2.4. Progress Report (REQUIRED)**:

   **Claude Code Environment** (background Self Review + Documentation):
   - Display:
     ```
     Task {task_id} Implementation Complete:
     - Implementation: ✓ Complete
     - TDD Cycle: ✓ Red→Green→Refactor executed
     - Self Review: 🔄 Running in background (job: {verification_job_id})
     - Documentation: 🔄 Running in background (job: {doc_job_id})
     - Status: ⏳ Awaiting background job results
     - Next: Moving to next task
     ```
   - Move to next task immediately

   **Codex or Other Environments** (synchronous Self Review):
   - Display:
     ```
     Task {task_id} Summary:
     - Implementation: ✓ Complete
     - TDD Cycle: ✓ Red→Green→Refactor executed
     - Self Review: {✓ PASS / ✗ FAIL} (Score: {score}/100)
     - Documentation: Skipped (manual update available)
     - Issues Fixed: {count}
     - Status: {✓ COMPLETE / ✗ FAILED}
     ```
   - Move to next task

   **8.3. Wait for Background Job Completion and Parse Reports (after current phase completion)**:

   **When to execute**:
   - After all tasks in current phase have completed TDD implementation
   - Before moving to next phase
   - Or after all phases if implementing entire feature

   **Claude Code Environment ONLY**:

   - Display: `"⏳ Waiting for {len(background_jobs)} verification agents to complete..."`

   **Step 1: Wait for all background jobs to complete**:

   - For each task_id in background_jobs:
     ```python
     job_id = background_jobs[task_id]

     # Wait for job completion (ignore return value)
     TaskOutput(
         task_id=job_id,
         block=True,      # Wait for completion
         timeout=300000   # 5 minutes max
     )
     # Return value ignored - will read report file directly
     ```

   - Display: `"✓ All verification agents completed"`

   **Step 1b: Wait for all documentation jobs to complete**:

   - Display: `"⏳ Waiting for {len(doc_jobs)} documentation agents to complete..."`

   - For each task_id in doc_jobs:
     ```python
     job_id = doc_jobs[task_id]

     # Wait for job completion (ignore return value)
     TaskOutput(
         task_id=job_id,
         block=True,      # Wait for completion
         timeout=300000   # 5 minutes max
     )
     # Return value ignored - documentation files already written
     ```

   - Display: `"✓ All documentation agents completed"`
   - Display: `"📚 Documentation updated in .grove/docs/"`

   **Step 2: Parse report files**:

   - For each task_id in background_jobs.keys():
     ```python
     # Read report file
     report_path = f"FEATURE_DIR/reports/self-review/task-{task_id}.md"
     report_content = read_file(report_path)

     # Parse "## 1. Summary" section
     # Extract from Markdown table:
     # | Score | 95/100       |  ← Extract "95"
     # | Status| **PASS**     |  ← Extract "PASS"
     # | Issues| 3            |  ← Extract "3"

     score = extract_score_from_table(report_content)       # e.g., 95
     status = extract_status_from_table(report_content)     # e.g., "PASS"
     issues_count = extract_issues_from_table(report_content)  # e.g., 0

     # Store results
     review_results[task_id] = {
         "score": score,
         "status": status,
         "issues_count": issues_count,
         "report_path": f"reports/self-review/task-{task_id}.md"
     }
     ```

   **Markdown Table Parsing Methods**:
   ```python
   def extract_score_from_table(report_content):
       # Find line: "| Score | 95/100  |"
       # Extract "95" from "95/100"
       match = re.search(r'\|\s*Score\s*\|\s*(\d+)/100', report_content)
       return int(match.group(1)) if match else 0

   def extract_status_from_table(report_content):
       # Find line: "| Status| **PASS** |" or "| Status| **FAIL** |"
       match = re.search(r'\|\s*Status\s*\|\s*\*\*(\w+)\*\*', report_content)
       return match.group(1) if match else "UNKNOWN"

   def extract_issues_from_table(report_content):
       # Find line: "| Issues| 3 |"
       match = re.search(r'\|\s*Issues\s*\|\s*(\d+)', report_content)
       return int(match.group(1)) if match else 0
   ```

   - Display progress for each task:
     ```
     ✓ T001: PASS (Score: 95/100, Report: reports/self-review/task-T001.md)
     ✗ T002: FAIL (Score: 65/100, 3 issues, Report: reports/self-review/task-T002.md)
     ✓ T003: PASS (Score: 100/100, Report: reports/self-review/task-T003.md)
     ✗ T004: FAIL (Score: 70/100, 2 issues, Report: reports/self-review/task-T004.md)
     ✓ T005: PASS (Score: 85/100, Report: reports/self-review/task-T005.md)
     ```

   - Display summary:
     ```
     Self Review Collection Complete:
     - Total: {total}
     - PASS: {pass_count}
     - FAIL: {fail_count}
     - Reports saved in: FEATURE_DIR/reports/self-review/
     ```

   **Codex or Other Environments**:
   - Skip this step (already completed synchronously in 7.2.2)

   **7.4. Auto-Fix Failed Tasks (after collecting results)**:

   **Execute for**:
   - All tasks with status = "FAIL" (score < 80)
   - Maximum 3 attempts per task

   **For each FAIL task**:

   - Read task report file: `FEATURE_DIR/{review_results[task_id]["report_path"]}`
   - Extract issues from report:
     - Parse "### Task {ID}" section
     - Extract all "##### Issue {N}" sections
     - For each issue, extract: Severity, Location, Description, Cause, Recommended Fix, Evidence
   - Display: `"🔧 Auto-fixing {task_id} (Score: {score}/100, {issues_count} issues)..."`

   **Auto-Fix Loop** (iteration = 1 to 3):

   1. **List Issues** (extracted from task report):
      ```
      Issues found in {task_id}:

      Issue 1 (Critical):
      - Location: src/app/auth.py:42
      - Description: Password not hashed before storage
      - Cause: Missing bcrypt.hashpw() call
      - Fix: Add password hashing

      Issue 2 (Medium):
      - Location: src/app/auth.py:58
      - Description: Missing error handling for invalid credentials
      - Cause: No try-except block
      - Fix: Add exception handling
      ```

   2. **Apply Fixes**:
      - For each issue:
        - Read affected file(s)
        - Apply TDD fix:
          1. Update/add test to cover the issue
          2. Run test (should fail)
          3. Apply recommended fix from verification report
          4. Run test (should pass)
        - Update file(s)
      - Display: `"Applied {fixed_count}/{len(issues)} fixes"`

   3. **Re-verify** (synchronous, NOT background):
      - Execute verification again using same method:
        - Claude Code: Launch verification agent WITHOUT `run_in_background` flag
        - Codex: Use verification template
      - Get new score and issues
      - Display: `"Re-verification: Score {new_score}/100 ({new_issue_count} issues)"`

   4. **Result**:
      - If new_score ≥ 80:
        - Display: `"✓ {task_id} Auto-Fix SUCCESS (Score: {new_score}/100)"`
        - Update review_results[task_id] with new score/status
        - Break loop (move to next FAIL task)
      - If new_score < 80 and iteration < 3:
        - Display: `"Attempt {iteration}/3 FAIL (Score: {new_score}/100), retrying..."`
        - Continue to iteration + 1
      - If new_score < 80 and iteration = 3:
        - Display: `"✗ {task_id} Auto-Fix FAILED after 3 attempts"`
        - Display: `"Final Score: {new_score}/100"`
        - Display: `"Remaining issues: {new_issue_count}"`
        - List remaining issues
        - Keep FAIL status in review_results

   **7.5. Update tasks.md with Self Review Results**:

   - For each task in current phase:

     **If review_results[task_id].status == "PASS"**:
     - Mark "Self Review" as: `[x] Self Review: Automated verification completed ✓ (Score: {score}/100)`
     - Mark task checkbox as: `[X]` (if not already marked)

     **If review_results[task_id].status == "FAIL"**:
     - Mark "Self Review" as: `[ ] Self Review: Automated verification completed ✗ (Score: {score}/100, {issue_count} issues remaining)`
     - **DO NOT mark task checkbox** as [X]

   - Write updated tasks.md

   **7.6. Generate Phase Self Review Report**:

   - Create report directory: `FEATURE_DIR/reports/self-review/`
   - Determine current phase from tasks.md (e.g., "Phase 1" → `phase-1`)
   - Generate report file: `self-review-phase-{N}.md`

   - Report content:

     ````markdown
     # Phase {N} Self Review Report

     **Date**: {YYYY-MM-DD HH:MM:SS}
     **Agent**: {AI Agent Name from tasks.md metadata}
     **Phase**: Phase {N}

     ---

     ## 1. Summary

     | Item               | Value        |
     | ------------------ | ------------ |
     | Total Tasks        | {total}      |
     | TDD Complete       | {total}      |
     | Self Review PASS   | {pass_count} |
     | Self Review FAIL   | {fail_count} |
     | Phase Status       | **{PASS/FAIL}** |

     ### Issues by Severity

     | Severity | Count       |
     | -------- | ----------- |
     | Critical | {count}     |
     | High     | {count}     |
     | Medium   | {count}     |
     | Low      | {count}     |

     ---

     ## 2. Task Summary

     | Task | Type | Score | Status | Issues | Auto-Fixed |
     | ---- | ---- | ----- | ------ | ------ | ---------- |
     | {task_id} | {type} | {score}/100 | {PASS/FAIL} | {count} | {count} |

     (Add one row per task)

     ---

     ## 3. Detailed Task Reports

     Individual task reports are available in the `reports/self-review/` directory:

     | Task ID | Description | Score | Status | Report |
     | ------- | ----------- | ----- | ------ | ------ |
     | {task_id} | {brief_description} | {score}/100 | {PASS/FAIL} | [`task-{task_id}.md`](task-{task_id}.md) |

     (Add one row per task)

     **For detailed verification results, issues, and evidence, see individual task reports above.**

     ---

     ## 4. Conclusion

     Phase {N} implementation and Self Review completed.

     **{If all PASS}**:
     - All tasks passed Self Review
     - Phase ready for next stage
     - Consider running `/grove.review` for cross-review by another AI agent

     **{If any FAIL}**:
     - {fail_count} tasks require attention
     - Priority: Address Critical/High severity issues first
     - Run `/grove.review` for cross-review
     - After cross-review, run `/grove.fix` to address issues
     ````

   - Save report to: `FEATURE_DIR/reports/self-review/self-review-phase-{N}.md`
   - Display: `"📄 Self Review report saved: {report_path}"`

   **8.7. Phase Summary Display**:

   - Display detailed summary table:
     ```
     ╔═══════════════════════════════════════════════════════╗
     ║         Phase {N} Implementation Summary              ║
     ╠═══════════════════════════════════════════════════════╣
     ║ Total Tasks:        {total}                          ║
     ║ TDD Complete:       {total} / {total} (100%)         ║
     ║ Self Review PASS:   {pass} / {total} ({percent}%)    ║
     ║ Self Review FAIL:   {fail} / {total} ({percent}%)    ║
     ║ Phase Status:       {✓ PASS / ✗ FAIL}               ║
     ╚═══════════════════════════════════════════════════════╝

     Task Details:
     | Task  | Implementation | Self Review     | Status   |
     |-------|---------------|-----------------|----------|
     | T001  | ✓ Complete    | ✓ PASS (95/100) | COMPLETE |
     | T002  | ✓ Complete    | ✗ FAIL (65/100) | FAILED   |
     | T003  | ✓ Complete    | ✓ PASS (100/100)| COMPLETE |
     | T004  | ✓ Complete    | ✗ FAIL (70/100) | FAILED   |
     | T005  | ✓ Complete    | ✓ PASS (85/100) | COMPLETE |

     {If any failures}:
     ⚠️  Action Required:
     - {fail_count} tasks failed Self Review
     - See detailed report: reports/self-review/self-review-phase-{N}.md
     - Recommended next steps:
       1. Review failed tasks in tasks.md
       2. Run `/grove.review` for cross-review by another AI agent
       3. After cross-review, run `/grove.fix` to address identified issues
     ```

   - Clear background_jobs and doc_jobs dictionaries for next phase (if any)

   **Execution Rules - STRICTLY ENFORCED**:
   - **Phase-by-phase execution**: Complete each phase before moving to the next
   - **Respect dependencies**: Run sequential tasks in order, parallel tasks [P] can run together
   - **TDD per task + Self Review per phase**: Execute TDD for each task, collect Self Review results at phase end
   - **Task completion**: Mark task complete only after Self Review PASS
   - **File-based coordination**: Tasks affecting the same files must run sequentially
   - **Background execution**: Claude Code launches verification and documentation agents in background for maximum parallelism
   - **Documentation updates**: Real-time per task (background in Claude Code, skip in others)
   - **Batch fixes**: Auto-fix all failed tasks together after collecting results (no conflicts)
   - **NO SHORTCUTS**: Every task goes through full workflow regardless of perceived simplicity
   - **EVIDENCE REQUIRED**: Must show test output and verification scores, not just assertions

9. Error handling:
   - Halt execution if any non-parallel task fails
   - For parallel tasks [P], continue with successful tasks, report failed ones
   - Provide clear error messages with context for debugging
   - Suggest next steps if implementation cannot proceed
   - If Self Review fails after 3 attempts, continue to next task but report the failure

10. Completion validation:
   - Verify all required tasks are completed
   - Check that implemented features match the original specification
   - Validate that tests pass and coverage meets requirements
   - Confirm the implementation follows the technical plan
   - Report final status with summary of completed work

11. **Final Self Review Summary (all phases complete)**:

   **11.1 Aggregate All Phase Results**:
   - Read `FEATURE_DIR/tasks.md`
   - Extract all task items with their Self Review status across all phases
   - Count:
     - Total tasks (all phases)
     - Tasks with Self Review PASS `[x]`
     - Tasks with Self Review FAIL `[ ]`
     - Tasks without Self Review (if --skip-self-review was used)
   - Aggregate severity counts from all phase reports:
     - Critical issues (total across phases)
     - High issues
     - Medium issues
     - Low issues

   **11.2 Generate Consolidated Summary Report**:
   - Create report directory: `FEATURE_DIR/reports/self-review/`
   - Extract metadata from tasks.md to get "Implemented By" AI Agent name
   - List all completed phases from tasks.md
   - Generate report file: `self-review-summary.md`
   - Report content:

     ````markdown
     # Self Review Summary - All Phases

     **Date**: {YYYY-MM-DD HH:MM:SS}
     **Agent**: {AI Agent Name}
     **Phases Completed**: {Phase 1, Phase 2, Phase 3, ...}

     ---

     ## Overall Summary

     | Item               | Value        |
     | ------------------ | ------------ |
     | Total Phases       | {phase_count} |
     | Total Tasks        | {total}      |
     | TDD Complete       | {total} / {total} (100%) |
     | Self Review PASS   | {pass_count} / {total} ({percent}%) |
     | Self Review FAIL   | {fail_count} / {total} ({percent}%) |
     | Overall Status     | **{✓ PASS / ✗ FAIL}** |

     ### Issues by Severity (All Phases)

     | Severity | Count       |
     | -------- | ----------- |
     | Critical | {total_critical} |
     | High     | {total_high}     |
     | Medium   | {total_medium}   |
     | Low      | {total_low}      |

     ---

     ## Phase Breakdown

     | Phase   | Tasks | PASS | FAIL | Status |
     | ------- | ----- | ---- | ---- | ------ |
     | Phase 1 | {count} | {pass} | {fail} | {✓/✗} |
     | Phase 2 | {count} | {pass} | {fail} | {✓/✗} |
     | Phase 3 | {count} | {pass} | {fail} | {✓/✗} |
     ...

     Detailed phase reports:
     - Phase 1: `reports/self-review/self-review-phase-1.md`
     - Phase 2: `reports/self-review/self-review-phase-2.md`
     - Phase 3: `reports/self-review/self-review-phase-3.md`
     ...

     ---

     ## Failed Tasks Summary (if any)

     | Task ID | Phase | Type | Score | Issues | Description |
     | ------- | ----- | ---- | ----- | ------ | ----------- |
     | {ID}    | {phase} | {type} | {score}/100 | {count} | {brief_desc} |

     (List all tasks with Self Review FAIL across all phases)

     For detailed issue information, see individual phase reports above.

     ---

     ## Success Metrics

     - **Task Completion Rate**: {total - fail_count} / {total} ({percent}%)
     - **Self Review Pass Rate**: {pass_count} / {total} ({percent}%)
     - **Average Score**: {avg_score}/100
     - **Critical Issues**: {critical_count} (target: 0)
     - **High Issues**: {high_count} (target: 0)

     ---

     ## Next Steps

     **{If any failed tasks}**:
     1. Review failed tasks in tasks.md
     2. Review detailed issues in phase reports: `reports/self-review/self-review-phase-*.md`
     3. Run `/grove.review` for cross-review by another AI agent
     4. After cross-review, run `/grove.fix` to address identified issues
     5. Priority: Address Critical and High severity issues first

     **{If all passed}**:
     - ✓ All {total} tasks passed Self Review
     - ✓ Implementation quality verified
     - Next: Consider running `/grove.review` for additional cross-review
     - Ready for: Integration testing, deployment, or next feature

     ---

     ## Implementation Timeline

     - Feature implementation started: {start_timestamp}
     - Feature implementation completed: {end_timestamp}
     - Total implementation time: {duration}
     - Average time per task: {avg_time}
     - Phases completed: {phase_count}

     ---

     ## Quality Indicators

     **Strengths** (if all or most tasks passed):
     - ✓ Specification compliance maintained
     - ✓ Tech stack adherence verified
     - ✓ Test coverage adequate
     - ✓ Code quality standards met

     **Areas for Improvement** (if failures exist):
     - ⚠️ {fail_count} tasks require attention
     - ⚠️ {critical_count + high_count} high-priority issues
     - ⚠️ Review phase reports for specific improvements
     ````

   - Save report to: `FEATURE_DIR/reports/self-review/self-review-summary.md`
   - Display: `"📄 Final Self Review summary saved: {report_path}"`

   **11.3 Display Final Summary**:

   - Display comprehensive summary:
     ```
     ╔═══════════════════════════════════════════════════════════════╗
     ║            IMPLEMENTATION COMPLETE - FINAL SUMMARY             ║
     ╠═══════════════════════════════════════════════════════════════╣
     ║ Feature:            {feature_name}                            ║
     ║ Total Phases:       {phase_count}                             ║
     ║ Total Tasks:        {total}                                   ║
     ║                                                                ║
     ║ TDD Cycle:          {total} / {total} (100%) ✓               ║
     ║ Self Review PASS:   {pass} / {total} ({percent}%)            ║
     ║ Self Review FAIL:   {fail} / {total} ({percent}%)            ║
     ║                                                                ║
     ║ Critical Issues:    {critical_count}                          ║
     ║ High Issues:        {high_count}                              ║
     ║ Medium Issues:      {medium_count}                            ║
     ║ Low Issues:         {low_count}                               ║
     ║                                                                ║
     ║ Overall Status:     {✓ PASS / ✗ FAIL}                        ║
     ╚═══════════════════════════════════════════════════════════════╝

     Phase-by-Phase Results:
     | Phase   | Tasks | PASS      | FAIL     | Status   | Report |
     |---------|-------|-----------|----------|----------|--------|
     | Phase 1 | 5     | 4 (80%)   | 1 (20%)  | ✗ FAIL   | self-review-phase-1.md |
     | Phase 2 | 7     | 7 (100%)  | 0 (0%)   | ✓ PASS   | self-review-phase-2.md |
     | Phase 3 | 10    | 9 (90%)   | 1 (10%)  | ✗ FAIL   | self-review-phase-3.md |

     {If any failures}:
     ⚠️  ATTENTION REQUIRED: {fail_count} tasks failed Self Review

     Failed Tasks:
     - T002 (Phase 1): Score 65/100 - 3 issues (1 Critical, 2 Medium)
     - T015 (Phase 3): Score 70/100 - 2 issues (1 High, 1 Low)

     Recommended Actions:
     1. Review detailed phase reports in: reports/self-review/
     2. Run `/grove.review` for cross-review by another AI agent
     3. After cross-review, run `/grove.fix` to address issues
     4. Priority: Fix Critical and High severity issues first

     {If all passed}:
     🎉 SUCCESS: All {total} tasks passed Self Review!

     Quality Metrics:
     - Average Score: {avg_score}/100
     - Task Completion: 100%
     - Self Review Pass Rate: 100%

     Next Steps:
     - Consider running `/grove.review` for additional cross-review
     - Ready for integration testing and deployment
     ```

   - Display report locations:
     ```
     📊 Self Review Reports:
     - Summary: {FEATURE_DIR}/reports/self-review/self-review-summary.md
     - Phase 1: {FEATURE_DIR}/reports/self-review/self-review-phase-1.md
     - Phase 2: {FEATURE_DIR}/reports/self-review/self-review-phase-2.md
     ...
     ```

   - Display next command suggestions:
     ```
     💡 Suggested Next Commands:
     {If failures}:
     - `/grove.review` - Cross-review by another AI agent
     - `/grove.fix` - Auto-fix issues after cross-review

     {If all passed}:
     - `/grove.review` - Optional additional quality check
     - `/grove.taskstoissues` - Convert tasks to GitHub issues for tracking
     ```

---

## CRITICAL NOTES

**Workflow Enforcement**:
- This command enforces STRICT adherence to TDD + Self Review workflow
- **NEVER skip steps** even for "simple" or "setup" tasks
- **NEVER mark checkboxes** without showing actual verification output
- **NEVER assume** tests pass without running them
- **VIOLATION = FAILURE**: If you skip any required step, restart from current task

**Evidence Requirements**:
- TDD Red: MUST show failed test output
- TDD Green: MUST show passed test output
- TDD Refactor: MUST show passed test output after refactoring
- Self Review: MUST show verification score (0-100) and issue list

**Prerequisites**:
- This command assumes a complete task breakdown exists in tasks.md
- If tasks are incomplete or missing, suggest running `/grove.tasks` first to regenerate the task list

**Quality Assurance**:
- Every task gets Self Review with 3 auto-fix attempts
- Only tasks with score ≥ 80 are marked as complete
- Failed tasks are documented with reason and suggested for `/grove.review` cross-review
