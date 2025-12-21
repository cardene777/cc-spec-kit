# Project Rules for Spec-Driven Development with Grove

## Language Configuration - CRITICAL

**MANDATORY FIRST STEP**: Read `.grove/memory/config.json`

- `language: "ja"` → **ALL outputs in Japanese ONLY (zero English allowed)**
- `language: "en"` → **ALL outputs in English ONLY (zero Japanese allowed)**
- Applies to: responses, questions, AskUserQuestion options, documentation, commit messages, error messages
- Default to English if config.json missing

**VIOLATION = TASK FAILURE**

---

## Grove Workflow Overview

Grove implements **Spec-Driven Development (SDD)** with **built-in quality assurance**:

```
Constitution → Specify → Design (optional) → Plan → Tasks → Implement (TDD + AI Auto-Review)
                                                               ↓
                                                         ┌─────────────┐
                                                         │ For each    │
                                                         │ task:       │
                                                         └─────────────┘
                                                               ↓
                                                    1. Write Tests (TDD)
                                                               ↓
                                                    2. Implement Code
                                                               ↓
                                                    3. Self Review (Auto)
                                                               ↓
                                                    4. Auto-Fix (if needed)
                                                               ↓
                                                         ┌─────────────┐
                                                         │ After all   │
                                                         │ tasks:      │
                                                         └─────────────┘
                                                               ↓
                                                    5. Cross Review (Auto)
```

### Phase Descriptions

1. **Constitution** (`/grove.constitution`): Define project principles, tech stack, testing strategy
2. **Specify** (`/grove.specify`): Write detailed feature specifications in `spec.md`
3. **Design** (`/grove.design`): Create UI/UX designs (optional, for frontend features)
4. **Plan** (`/grove.plan`): Create implementation plan with architecture in `plan.md`
5. **Tasks** (`/grove.tasks`): Break down plan into executable tasks in `tasks.md`
6. **Implement** (`/grove.implement`): Execute tasks with TDD + AI Auto-Review

---

## Grove's 3-Layer Quality Assurance

### Layer 1: TDD (Test-Driven Development)

**MANDATORY for all implementation tasks**:

1. Write tests FIRST (before implementation)
2. Run tests → Confirm they FAIL (Red)
3. Implement code → Make tests PASS (Green)
4. Refactor code (if needed)

**Never skip TDD**. If user requests skipping tests, warn them about quality risks.

### Layer 2: Self Review (Automated, Per-Task)

After completing each task, **Self Review automatically runs**:

**Process** (Claude Code only):
1. Spawn Verification Agent in background (`run_in_background=True`)
2. Agent executes 8-Point Quality Checklist:
   - ✓ Specification Compliance
   - ✓ Tech Stack Adherence
   - ✓ Task Completeness
   - ✓ Test Coverage
   - ✓ Error Handling
   - ✓ Security (no XSS, injection, auth bypass, etc.)
   - ✓ Performance (no N+1 queries, memory leaks, etc.)
   - ✓ Code Quality
3. Generate score (100 base, deduct for issues)
4. Write report to `FEATURE_DIR/reports/self-review/task-{ID}.md`

**Scoring**:
- Critical issue: -30 points (spec violation, security vuln, data loss)
- High issue: -20 points (major feature broken)
- Medium issue: -10 points (spec violation but works, performance)
- Low issue: -5 points (minor issues, code style)
- **PASS**: Score ≥ 80
- **FAIL**: Score < 80

**Auto-Fix Flow**:
```
Task Completed → Self Review (background)
                      ↓
                 Score < 80?
                      ↓
                    YES → Auto-Fix (1 attempt)
                      ↓
                 Re-run Self Review
                      ↓
                 Score < 80?
                      ↓
                    YES → Report to user (manual fix needed)
                    NO  → Proceed to next task
```

**Important**: Auto-Fix runs **maximum 1 time** per task. If still failing, stop and report.

### Layer 3: Cross Review (Automated, After All Tasks)

After ALL tasks are completed, **Cross Review runs**:

**Process**:
1. Review entire feature holistically
2. Check integration between tasks
3. Verify all specs are met
4. Generate report to `FEATURE_DIR/reports/cross-review/phase-{N}.md`

**If Cross Review fails**: Recommend manual review and fixes (no auto-fix at this stage).

---

## Background Execution Rules (Claude Code Only)

### When to Use Background Execution

**Always use background for Verification Agent**:
```python
Task(
    subagent_type="verification-agent",
    prompt="...",
    run_in_background=True  # ← REQUIRED
)
```

**Why**: Self Review should not block implementation. While reviewing Task 1, you can start Task 2.

### Synchronization

**After starting background agent**:
1. Continue working on next task immediately
2. Before moving to next phase, use `TaskOutput` to retrieve results:
   ```python
   TaskOutput(task_id="verification-agent-task-id", block=True)
   ```

**Important**: Always retrieve and check reports before proceeding to Cross Review.

---

## Task Status Management

**tasks.md uses 3 statuses**:

- `[ ]` = **pending** (not started)
- `[~]` = **in_progress** (currently working)
- `[x]` = **completed** (finished + Self Review passed)

**Rules**:
1. **Only ONE task** can be `[~]` at a time
2. Mark `[x]` only after Self Review passes (score ≥ 80)
3. If Self Review fails after Auto-Fix, mark as `[~]` and report to user

---

## Template Usage

- Check `.grove/templates/*.md` YAML frontmatter for `enabled: true`
- If enabled: use template content as-is or reference
- If disabled/missing: use only structure

---

## Script Placeholder

`{SCRIPT}` → Read YAML frontmatter `scripts:` section, execute `sh:` value (macOS/Linux) or `ps:` value (Windows) from repo root.

Example frontmatter:
```yaml
scripts:
  sh: scripts/bash/my-script.sh --json
```
When you see `{SCRIPT}`, execute `scripts/bash/my-script.sh --json`

---

## Working Agreements

**Before starting any work**:
1. Read `.grove/memory/config.json` (language setting)
2. Read `.grove/memory/constitution.md` (project principles, tech stack)
3. Read `.grove/spec.md` (feature specifications - source of truth)
4. Read `.grove/plan.md` (architecture and implementation strategy)

**During implementation**:
- Follow constitution's technical stack (no deviations without user approval)
- Use spec.md as source of truth for all requirements
- Write tests FIRST (TDD mandatory)
- Run Self Review after each task
- Check Self Review reports before proceeding

---

## Directory Structure

```
.grove/
├── memory/
│   ├── config.json           # Language setting
│   └── constitution.md       # Project principles
├── spec.md                   # Feature specification (source of truth)
├── plan.md                   # Implementation plan
├── tasks.md                  # Task breakdown with status
├── design/                   # UI/UX designs (optional)
│   ├── README.md
│   ├── design-system.md
│   ├── components/
│   └── layouts/
├── reports/
│   ├── self-review/          # Per-task verification reports
│   │   ├── task-T001.md
│   │   ├── task-T002.md
│   │   └── ...
│   └── cross-review/         # Phase-wide review reports
│       ├── phase-1.md
│       └── phase-2.md
├── templates/                # Reusable templates
│   ├── plan-template.md
│   ├── tasks-template.md
│   └── ...
└── checklists/               # Pre-implementation checklists
    ├── ux.md
    ├── test.md
    └── security.md
```

---

## Available Commands

**Claude Code**:
- `/grove.constitution` - Define project principles
- `/grove.specify` - Write feature specification
- `/grove.clarify` - Clarify ambiguous requirements
- `/grove.design` - Create UI/UX designs
- `/grove.plan` - Create implementation plan
- `/grove.tasks` - Break down into tasks
- `/grove.implement` - Execute tasks with TDD + AI Auto-Review
- `/grove.analyze` - Analyze codebase or feature
- `/grove.checklist` - Generate pre-implementation checklists
- `/grove.taskstoissues` - Convert tasks to GitHub Issues

**Codex**:
- `/prompts:constitution`, `/prompts:specify`, `/prompts:clarify`, `/prompts:design`, `/prompts:plan`, `/prompts:tasks`, `/prompts:implement`, `/prompts:analyze`, `/prompts:checklist`, `/prompts:taskstoissues`

---

## Error Handling

### Self Review Failures

**When Self Review score < 80**:
1. Read verification report from `reports/self-review/task-{ID}.md`
2. Identify all issues (Critical → High → Medium → Low)
3. Run Auto-Fix (1 attempt only):
   - Fix all Critical issues first
   - Then High issues
   - Then Medium/Low if time permits
4. Re-run Self Review
5. If still < 80, report to user with report path

**User notification format**:
```
⚠️  Self Review failed for Task T001 (Score: 65/100)

Issues found:
- 1 Critical: Authentication bypass vulnerability
- 2 High: Missing error handling for API failures
- 1 Medium: Performance issue in database query

Auto-Fix attempted but score still below 80.
Please review: .grove/sdd-feature-x/reports/self-review/task-T001.md
```

### Cross Review Failures

**When Cross Review fails**:
1. Read cross-review report
2. Summarize issues by severity
3. **Do NOT auto-fix** (too risky after all tasks)
4. Report to user and recommend manual review

---

## Best Practices for AI Agents

### DO

✅ Always read language config FIRST
✅ Follow TDD strictly (tests before code)
✅ Run Self Review after each task
✅ Use background execution for Verification Agent (Claude Code)
✅ Check verification reports before proceeding
✅ Mark tasks as completed only after Self Review passes
✅ Follow constitution's tech stack
✅ Use spec.md as source of truth

### DON'T

❌ Skip tests "to save time"
❌ Mark tasks completed before Self Review
❌ Ignore verification reports
❌ Auto-fix more than once per task
❌ Deviate from tech stack without approval
❌ Mix languages (respect config.json setting)
❌ Block on Self Review (use background execution)

---

## Troubleshooting

### "Verification Agent not running"
- **Check**: Are you using Claude Code? (Other agents don't support background execution yet)
- **Fix**: Use `/grove.implement` command (not manual implementation)

### "Self Review always fails"
- **Check**: Are tests written and passing?
- **Check**: Does implementation match spec.md requirements?
- **Fix**: Read verification report, address Critical/High issues first

### "Tasks not updating status"
- **Check**: Are you updating tasks.md after each task?
- **Fix**: Update `[ ]` → `[~]` when starting, `[~]` → `[x]` after Self Review passes

### "Language violations"
- **Check**: Is config.json language setting respected?
- **Fix**: Re-read config.json, regenerate all outputs in correct language

---

**Last Updated**: 2025-12-21
**Grove Version**: 0.0.1
