---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
argument-hint: ""
handoffs:
  - label: Create Tasks
    agent: grove.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: grove.checklist
    prompt: Create a checklist for the following domain...
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. Run prerequisite script and parse paths:
   - Execute {SCRIPT} from repository root
   - Parse FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH from JSON output
   - All paths must be absolute
   - For single quotes in args: use escape syntax 'I'\''m Groot' or double-quote "I'm Groot"

2. Load context and design specifications:
   - Read FEATURE_SPEC for feature requirements
   - Read `.grove/memory/constitution.md` for project principles
   - Load IMPL_PLAN template (already copied by script)
   - Check for `.grove/design/` directory
   - If design exists, read specifications:
     - README.md (design overview)
     - foundations/ (color, typography, spacing, grid, motion, tone-and-voice)
     - components/ (component specs and code)
     - patterns/ (authentication, onboarding, error-handling, empty-state)
     - tokens/ (tokens.json, mapping.md)
   - Extract design constraints if available:
     - UI framework (React, Vue, Angular, etc.)
     - CSS methodology (Tailwind, CSS Modules, CSS-in-JS, etc.)
     - Design tokens (color palette, typography, spacing)
     - Component architecture patterns
     - Responsive breakpoints
     - Accessibility requirements
   - If no design directory: note "No design specifications found. Plan will focus on backend/logic only."

3. Execute plan workflow:
   - Fill Technical Context section (mark unknowns as "NEEDS CLARIFICATION")
   - Integrate design constraints into Technical Context:
     - UI framework choice (from design specs)
     - Styling approach (from design specs)
     - Component structure (from design specs)
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION, include design-related research)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Include design implementation guidance:
     - Map design components to technical implementation
     - Specify how to integrate design system tokens
     - Document component implementation order
   - Phase 1: Update agent context by running agent script
   - Re-evaluate Constitution Check post-design

4. Stop and report:
   - Command ends after Phase 1 planning
   - Report branch name
   - Report IMPL_PLAN path
   - Report generated artifacts (research.md, data-model.md, contracts/, quickstart.md)

## Phases

### Phase 0: Outline & Research

1. Extract unknowns from Technical Context:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. Generate and dispatch research agents:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. Consolidate findings in `research.md`:
   - Use format: Decision, Rationale, Alternatives considered
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. Extract entities from feature spec → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. Generate API contracts from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. Agent context update:
   - Run `{AGENT_SCRIPT}`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
