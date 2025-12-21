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

0. **Sync Constitution to Claude Rules** (if needed):
   - If `.claude/rules/constitution.md` doesn't exist or contains only default comments (≤4 lines)
   - AND `.grove/memory/constitution.md` exists
   - Then copy `.grove/memory/constitution.md` to `.claude/rules/constitution.md` with AUTO-SYNCED header
   - This ensures Claude Code enforces project principles even if `/grove.constitution` wasn't run

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Load design specifications (if available)**:
   - Check for `.grove/design/` directory
   - If exists, read design specifications:
     - `.grove/design/README.md` (design overview)
     - `.grove/design/design-system.md` (colors, typography, spacing)
     - `.grove/design/components/` (component specs and code)
     - `.grove/design/layouts/` (layout specs and code)
   - Extract design constraints:
     - Required UI framework (React, Vue, Angular, etc.)
     - CSS methodology (Tailwind, CSS Modules, CSS-in-JS, etc.)
     - Design tokens (color palette, typography scale, spacing)
     - Component architecture patterns
     - Responsive breakpoints
     - Accessibility requirements
   - If design directory doesn't exist, note: "No design specifications found. Plan will focus on backend/logic only."

4. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - **Integrate design constraints** into Technical Context:
     - UI framework choice (from design specs)
     - Styling approach (from design specs)
     - Component structure (from design specs)
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION, include design-related research if needed)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: **Include design implementation guidance**:
     - Map design components to technical implementation
     - Specify how to integrate design system tokens
     - Document component implementation order
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

5. **Stop and report**: Command ends after Phase 1 planning. Report branch, IMPL_PLAN path, and generated artifacts.

   **CRITICAL - MANDATORY Next Step Output**:
   After reporting artifacts, you MUST output the next step. This is NOT optional.

   Output EXACTLY:
   ```
   ## Next Steps

   Plan has been created successfully!

   To create implementation tasks, run:
   /grove.tasks

   This will break down the plan into specific, actionable development tasks.
   ```

   **IMPORTANT**:
   - This next steps section is MANDATORY and must ALWAYS be displayed
   - Do NOT replace with generic text like "review the plan" or "start implementation"
   - The `/grove.tasks` command MUST be explicitly shown

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `{AGENT_SCRIPT}`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
