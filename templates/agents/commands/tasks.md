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

1. Run prerequisite script and parse paths:
   - Execute {SCRIPT} from repository root
   - Parse FEATURE_DIR and AVAILABLE_DOCS from JSON output
   - All paths must be absolute
   - For single quotes in args: use escape syntax 'I'\''m Groot' or double-quote "I'm Groot"

2. Load design documents from FEATURE_DIR:
   - Required: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - Optional: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available

3. Execute task generation workflow:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. Generate tasks.md:
   - Use `templates/tasks-template.md` as structure
   - CRITICAL FORMAT REQUIREMENTS:
     - You MUST use exact task format defined in "Task Format with Sub-checks" section
     - Every task MUST have TDD Checklist and Review sub-checks
     - Task IDs in brackets: [T001], NOT **T001** or T001:
     - DO NOT use bold formatting for task IDs
     - DO NOT create custom section headers like "Phase 0: Setup"
     - Follow template structure EXACTLY
   - Fill with correct feature name from plan.md
   - Add metadata section at top (after feature name):
     ```markdown
     ---
     **Implemented By**: {Current AI Agent Name} (claude/codex/unknown)
     **Created**: {YYYY-MM-DD HH:MM:SS}
     ---
     ```
   - Detect current AI Agent:
     - Run `claude --help` or `code --help` → If success: AI Agent = "claude"
     - Run `codex --help` → If success: AI Agent = "codex"
     - Otherwise: AI Agent = "unknown"
   - Phase structure:
     - Phase 1: Setup tasks (project initialization)
     - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
     - Phase 3+: One phase per user story (in priority order from spec.md)
     - Final Phase: Polish & cross-cutting concerns
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Each task must include TDD checklist AND review sub-checks
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. Display final report:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format

Context for task generation: {ARGS}

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST follow this complete format with all sub-sections:

```markdown
## Task: [Task Description]

- [ ] T{ID} [{P}] [{Story}] Description with exact file path

### Related Spec
- spec/[filename].md#[section]

### TDD Checklist (per task)
- [ ] Red: Added new tests and confirmed they fail
- [ ] Green: Implemented minimal code to pass tests
- [ ] Refactor: Cleaned up code while keeping tests green

### Documentation
- [ ] Updated documentation for modified/created files

### Review
- [ ] Self Review: Implementation environment AI automatic verification completed
- [ ] Cross Review: Other AI Agent additional verification completed

### Constraints
- Do not modify the spec
- Do not touch other tasks
```

**Format Components**:

1. **Checkbox**: `- [ ]` (pending), `- [~]` (in-progress), `- [x]` (completed)
2. **Task ID**: T{sequential number} - T001, T002, T003...
3. **[P] marker**: OPTIONAL - for parallelizable tasks only
4. **[Story] label**: CONDITIONAL - `[US1]`, `[US2]` etc.
   - Setup/Foundational/Polish phases: NO label
   - User Story phases: REQUIRED
5. **Description**: Clear action with exact file path
6. **All sub-sections**: REQUIRED (Related Spec, TDD Checklist, Documentation, Review, Constraints)

**Examples**:

- ✅ CORRECT: Full format with all sub-sections (see template above)
- ❌ WRONG: Missing sub-sections
- ❌ WRONG: Task without TDD Checklist or Review sections

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
