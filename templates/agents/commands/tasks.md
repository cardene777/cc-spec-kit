---
description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
argument-hint: ""
handoffs:
  - label: Analyze For Consistency
    agent: grove.analyze
    prompt: Run a project analysis for consistency
    send: true
  - label: Implement Project
    agent: grove.implement
    prompt: Start the implementation in phases
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - **Add metadata section at the top** (after feature name):
     ```markdown
     ---
     **Implemented By**: {Current AI Agent Name} (claude/codex/unknown)
     **Created**: {YYYY-MM-DD HH:MM:SS}
     ---
     ```
   - To detect current AI Agent:
     - Run `claude --help` or `code --help` → If success: AI Agent = "claude"
     - Run `codex --help` → If success: AI Agent = "codex"
     - Otherwise: AI Agent = "unknown"
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - **Each task must include TDD checklist AND review sub-checks** (see Task Format with Sub-checks below)
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

6. **Next Steps Section**: After the report, ALWAYS output the following section exactly as shown:

   ```markdown
   ## Next Steps

   Task file has been generated. To start implementation, run the following command.

   ### Start Implementation

   ```bash
   /grove.implement
   ```

   Execute all tasks sequentially following the TDD cycle (Red→Green→Refactor).

   ### Verify Task Consistency (Optional)

   ```bash
   /grove.analyze
   ```

   Check consistency across constitution, specifications, plan, and tasks.
   ```

   **IMPORTANT**: This section must be displayed in the user's configured language (ja/en from config.json).

Context for task generation: {ARGS}

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label  
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **Description**: Clear action with exact file path

**Examples**:

- ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
- ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
- ❌ WRONG: `- [ ] [US1] Create User model` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

### Task Format with Sub-checks

**IMPORTANT**: Each task should include:
1. **TDD checklist** - Confirmation checklist to verify TDD was properly executed
2. **Review sub-checks** - Self Review and Cross Review tracking

**Task Template**:

```markdown
## Task: [Task Description]

- [ ] T001 Create database connection logic in src/db.py

### Related Spec
- spec/[filename].md#[section]

### TDD Checklist (per task)
- [ ] Red: Added new tests and confirmed they fail
- [ ] Green: Implemented minimal code to pass tests
- [ ] Refactor: Cleaned up code while keeping tests green

### Review
- [ ] Self Review: Implementation environment AI automatic verification completed
- [ ] Cross Review: Other AI Agent additional verification completed

### Constraints
- Do not modify the spec
- Do not touch other tasks
```

**Key Points**:
- **Review Sub-checks**:
  - Each task has 2 sub-checks: Self Review and Cross Review
  - Self Review: Checked by `/grove.implement` after task completion (automatic)
  - Cross Review: Checked by `/grove.review` from different AI Agent (manual)
- **TDD Checklist**:
  - The TDD checklist is checked **once per task** upon completion
  - It verifies that the TDD cycle (Red→Green→Refactor) was executed during implementation
  - It is NOT a step-by-step guide, but a post-implementation confirmation
  - If a checklist item cannot be completed, document the reason
  - The checklist confirms observability: "Was TDD actually executed?"
