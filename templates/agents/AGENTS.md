# Project Rules for Spec-Driven Development with Grove

## ⚠️ CRITICAL: Prerequisite Script Execution

**EXECUTE THIS BEFORE ANYTHING ELSE - NO EXCEPTIONS**

When you see a Grove slash command (`/grove.implement`, `/grove.plan`, etc.):

### STEP 1: Execute Prerequisite Script (MANDATORY FIRST STEP)

**The command file has YAML frontmatter like this**:
```yaml
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks
```

**What you MUST do FIRST**:
1. **Check the `scripts:` section** in the YAML frontmatter above
2. **Determine your OS**: macOS/Linux → use `sh:`, Windows → use `ps:`
3. **Run the script using Bash tool** from repository root
4. **Parse the JSON output**
5. **Extract and save paths**: `FEATURE_DIR`, `AVAILABLE_DOCS`, etc.

**Example**:
```bash
scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
```

Returns:
```json
{
  "FEATURE_DIR": "/absolute/path/to/specs/001-todo-master",
  "AVAILABLE_DOCS": ["research.md", "quickstart.md"]
}
```

### STEP 2: Use Parsed Paths (NEVER GUESS PATHS)

After running the script, use ONLY the absolute paths it returned:

- ✅ **CORRECT**: `{FEATURE_DIR}/spec.md` (from script output)
- ❌ **WRONG**: `.grove/spec.md` (DO NOT USE)
- ❌ **WRONG**: `specs/001-todo-master/spec.md` (DO NOT GUESS)

### If You Skip the Script

**CONSEQUENCE**: You will look in wrong locations, miss files, and fail the task.

### STEP 3: Verify Git Repository (RECOMMENDED)

**Check if the project is a git repository**:
```bash
git rev-parse --git-dir 2>/dev/null
```

**If NOT a git repo** (command fails):
- Display warning: `"⚠️  Warning: Not a git repository. Version control is recommended for Spec-Driven Development."`
- Ask user: `"Initialize git repository now? (yes/no)"`
- **If user says "yes"**:
  ```bash
  git init && git add . && git commit -m "Initial commit"
  ```
  - Display: `"✓ Git repository initialized"`
- **If user says "no"**:
  - Display: `"Proceeding without git. Note: .gitignore will not be created."`
  - Continue with task

**If IS a git repo** (command succeeds):
- Continue with task (no action needed)

---

## Language Configuration - CRITICAL

**MANDATORY FIRST STEP**: Read `.grove/memory/config.json`

- `language: "ja"` → **ALL outputs in Japanese ONLY (zero English allowed)**
- `language: "en"` → **ALL outputs in English ONLY (zero Japanese allowed)**
- Applies to: responses, questions, AskUserQuestion options, documentation, commit messages, error messages
- Default to English if config.json missing

**VIOLATION = TASK FAILURE**

---

## Grove Workflow

**SDD Workflow**: Constitution → Specify → Design (optional) → Plan → Tasks → Implement

**Implementation Loop** (for each task):
1. Write Tests (TDD Red)
2. Implement Code (TDD Green)
3. Self Review (Auto, background)
4. Auto-Fix (if score < 80, 1 attempt max)

**After All Tasks**: Cross Review (Auto)

**Commands**:
- `/grove.constitution` - Define project principles
- `/grove.specify` - Write feature spec
- `/grove.plan` - Create implementation plan
- `/grove.tasks` - Break down into tasks
- `/grove.implement` - Execute with TDD + Auto-Review

---

## 3-Layer Quality Assurance

### Layer 1: TDD (MANDATORY)

1. Write tests FIRST → Run tests → Confirm FAIL (Red)
2. Implement code → Make tests PASS (Green)
3. Refactor (if needed)

**Never skip TDD**.

### Layer 2: Self Review (Per-Task, Auto)

**Claude Code only** - Spawns Verification Agent in background:

**8-Point Checklist**:
- Specification Compliance
- Tech Stack Adherence
- Task Completeness
- Test Coverage
- Error Handling
- Security (XSS, injection, auth, etc.)
- Performance (N+1, leaks, etc.)
- Code Quality

**Scoring**:
- Critical: -30 (spec violation, security, data loss)
- High: -20 (major broken)
- Medium: -10 (spec violation but works)
- Low: -5 (minor)
- **PASS**: ≥80 | **FAIL**: <80

**Auto-Fix**: Max 1 attempt. If still <80, report to user.

**Report**: `FEATURE_DIR/reports/self-review/task-{ID}.md`

### Layer 3: Cross Review (After All Tasks, Auto)

- Review entire feature holistically
- Check integration between tasks
- **No auto-fix** at this stage
- **Report**: `FEATURE_DIR/reports/cross-review/phase-{N}.md`

---

## Task Status (tasks.md)

- `[ ]` = pending
- `[~]` = in_progress (only ONE at a time)
- `[x]` = completed (Self Review passed, score ≥80)

---

## Background Execution (Claude Code)

**Verification Agent always runs in background**:
```python
Task(
    subagent_type="verification-agent",
    prompt="...",
    run_in_background=True  # REQUIRED
)
```

**Synchronization**: Use `TaskOutput(task_id="...", block=True)` before next phase.

---

## Template & Script Placeholders

- **Template**: Check `.grove/templates/*.md` YAML frontmatter for `enabled: true`
- **Script**: `{SCRIPT}` → Execute `sh:` (macOS/Linux) or `ps:` (Windows) from YAML frontmatter

---

## Working Agreements

**Before starting**:
1. Read `.grove/memory/config.json` (language)
2. Read `.grove/memory/constitution.md` (principles, tech stack)
3. Read `FEATURE_DIR/spec.md` (requirements - source of truth)
4. Read `FEATURE_DIR/plan.md` (architecture)

**During implementation**:
- Follow constitution tech stack (no deviations)
- Use spec.md as source of truth
- Write tests FIRST (TDD mandatory)
- Run Self Review after each task
- Check reports before proceeding

---

## Directory Structure

```
specs/{branch}/              # Feature directory (FEATURE_DIR)
├── spec.md                  # Feature spec (source of truth)
├── plan.md                  # Implementation plan
├── tasks.md                 # Task breakdown
├── reports/
│   ├── self-review/         # Per-task reports
│   └── cross-review/        # Phase reports
└── checklists/              # Pre-implementation checklists

.grove/
├── memory/
│   ├── config.json          # Language setting
│   └── constitution.md      # Project principles
├── design/                  # UI/UX designs (optional)
└── templates/               # Reusable templates
```

---

## Best Practices

**DO**:
- ✅ Read language config FIRST
- ✅ Follow TDD strictly
- ✅ Run Self Review after each task
- ✅ Use background execution (Claude Code)
- ✅ Mark `[x]` only after Self Review passes
- ✅ Follow constitution tech stack

**DON'T**:
- ❌ Skip tests
- ❌ Mark completed before Self Review
- ❌ Auto-fix >1 time per task
- ❌ Mix languages

---

**Last Updated**: 2025-12-22
**Grove Version**: 0.1.3
