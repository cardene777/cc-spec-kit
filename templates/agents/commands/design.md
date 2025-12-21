---
description: Create design specifications using Claude Code's frontend-design skill
argument-hint: "[design requirements]"
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-spec
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireSpec
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Objective

Create design specifications using Claude Code Marketplace's `frontend-design` skill to generate UI/UX design code that will guide the implementation phase.

This step is executed after 'specify' to ensure consistent UI/UX design throughout the project.

## Process

### Step 0: Sync Constitution to Claude Rules (if needed)

Before starting the design workflow:
- If `.claude/rules/constitution.md` doesn't exist or contains only default comments (≤4 lines)
- AND `.grove/memory/constitution.md` exists
- Then copy `.grove/memory/constitution.md` to `.claude/rules/constitution.md` with AUTO-SYNCED header
- This ensures Claude Code enforces project principles even if `/grove.constitution` wasn't run

### Step 1: Check Claude Code Environment

1. Verify you are running in Claude Code environment:
   - Check for `.claude/` directory existence
   - Check if this is Claude Code by looking for Claude Code-specific features

2. **If NOT Claude Code**: Display error message:
   ```
   Error: This design command requires Claude Code environment.
   The frontend-design skill is only available in Claude Code Marketplace.

   For other AI agents, please create design specifications manually in .grove/design.md
   ```

### Step 2: Check and Install frontend-design Skill

1. **Check if frontend-design skill is available** by attempting to use it:
   - Invoke: `Skill("frontend-design")`
   - If successful → skill is installed, proceed to Step 3
   - If error (skill not found) → proceed to step 2

2. **Guide user to install frontend-design skill**:

   a. Add Anthropic skills marketplace (if not already added):
      ```
      /plugin marketplace add anthropics/skills
      ```

   b. Install the frontend-design skill:
      ```
      /plugin install frontend-design@anthropic-agent-skills
      ```

   c. After installation, confirm with user and retry `Skill("frontend-design")` from Step 2.1

3. **If installation fails or skill is unavailable**:
   - Display error and offer manual design creation as fallback (see Step 6 Alternative)

### Step 3: Load Specification

1. Determine the current feature from git branch:
   - Get current branch name using: `git rev-parse --abbrev-ref HEAD`
   - Extract feature number and name from branch (format: `{number}-{feature-name}`)
   - Example: "001-todo-master" → number=001, name=todo-master

2. Read `specs/{number}-{feature-name}/spec.md` file

3. Extract key requirements:
   - Functional requirements
   - UI/UX requirements
   - Target platform (web, mobile, desktop)
   - Technology stack preferences
   - Design system requirements (if specified)

4. If spec.md doesn't exist, display error:
   ```
   Error: specs/{number}-{feature-name}/spec.md not found.
   Please run /grove.specify first to create the specification.
   ```

### Step 4: Execute frontend-design Skill

1. Invoke the `frontend-design` skill with the specification content
2. Provide context from spec.md:
   - Project overview
   - Feature requirements
   - UI/UX requirements
   - Target audience
   - Platform specifications

3. Request the skill to generate:
   - Design system (colors, typography, spacing)
   - Component specifications
   - Layout structures
   - Interaction patterns
   - Responsive design approach
   - **Implementation code** (HTML/CSS/React/Vue components as appropriate)

### Step 5: Save Design Output

1. Create `.grove/design/` directory if it doesn't exist

2. Save the generated design files:
   - **Design System**: `.grove/design/design-system.md`
     - Color palette, typography, spacing scales
   - **Components**: `.grove/design/components/`
     - Individual component specifications and code
   - **Layouts**: `.grove/design/layouts/`
     - Page layout specifications and code
   - **Assets**: `.grove/design/assets/`
     - Any generated assets (if applicable)

3. Create `.grove/design/README.md` with:
   - Overview of the design system
   - How to use the components
   - Link to full design specifications
   - Implementation notes

### Step 6: Verify Output

1. Confirm all files are created successfully
2. Display summary:
   ```
   ✓ Design specifications created successfully

   Output location: .grove/design/

   Generated files:
   - design-system.md (Design tokens and system)
   - components/ (Component specifications)
   - layouts/ (Layout specifications)
   - README.md (Design overview)

   Next steps:
   - Review the design specifications
   - Run /grove.plan to create technical implementation plan
   ```

### Step 6 Alternative: Manual Design Creation (Fallback)

**Use this approach if frontend-design skill is not available:**

1. Use AskUserQuestion to ask user which approach they prefer:
   - Option A: Create complete design system manually (recommended)
   - Option B: Create basic design guidelines only
   - Option C: Skip design phase and proceed to implementation

2. If user chooses Option A or B:
   - Read the spec.md file
   - Generate design specifications based on requirements
   - Create `.grove/design/` structure manually
   - Write design-system.md, component specs, and implementation code
   - Follow the same output structure as Step 5

3. If user chooses Option C:
   - Warn about potential UI/UX inconsistency
   - Proceed directly to /grove.plan phase

## Claude Code Specific Instructions

**This command is optimized for Claude Code environment**:

1. **Use Skill Integration**:
   - Leverage the `frontend-design` skill from Claude Code Marketplace
   - Do NOT create custom skills in `.claude/skills/`
   - Use marketplace skills for better maintenance and updates

2. **Output Format**:
   - Save to `.grove/design/` (NOT `.claude/skills/`)
   - Generate implementation-ready code
   - Include both specifications AND code samples

3. **Workflow Integration**:
   - Design output will be read by `/grove.plan`
   - Plan will reference these designs for technical implementation
   - Implement phase will use both plan + design

## Output

**Location**: `.grove/design/`

**Structure**:
```
.grove/design/
├── README.md              # Design overview
├── design-system.md       # Design tokens and system
├── components/            # Component specs & code
│   ├── Button.md
│   ├── Card.md
│   └── ...
└── layouts/               # Layout specs & code
    ├── MainLayout.md
    └── ...
```

## Success Criteria

- frontend-design skill is installed and executed successfully
- Design specifications are saved to `.grove/design/`
- Design system includes colors, typography, spacing
- Component specifications include implementation code
- README.md provides clear overview and usage instructions
- Output is ready to be referenced by plan and implement phases
