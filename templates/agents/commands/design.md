---
description: Create design specifications using Claude Code's frontend-design skill
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

### Step 1: Check Claude Code Environment

1. Verify you are running in Claude Code environment:
   - Check for `.claude/` directory existence
   - Check if this is Claude Code by looking for Claude Code-specific features

2. **If NOT Claude Code**: Display error message:
   ```
   Error: This design command requires Claude Code environment.
   The frontend-design skill is only available in Claude Code Marketplace.

   For other AI agents, please create design specifications manually in .specify/design.md
   ```

### Step 2: Install frontend-design Skill

1. Check if `frontend-design` skill is already installed:
   - Look for existing skill configuration
   - Check skill availability

2. **If NOT installed**: Install from Claude Code Marketplace:
   ```
   /plugin marketplace
   ```
   - Search for "frontend-design"
   - Install the skill
   - Confirm installation success

### Step 3: Load Specification

1. Read `.specify/spec.md` file
2. Extract key requirements:
   - Functional requirements
   - UI/UX requirements
   - Target platform (web, mobile, desktop)
   - Technology stack preferences
   - Design system requirements (if specified)

3. If spec.md doesn't exist, display error:
   ```
   Error: .specify/spec.md not found.
   Please run /speckit.specify first to create the specification.
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

1. Create `.specify/design/` directory if it doesn't exist

2. Save the generated design files:
   - **Design System**: `.specify/design/design-system.md`
     - Color palette, typography, spacing scales
   - **Components**: `.specify/design/components/`
     - Individual component specifications and code
   - **Layouts**: `.specify/design/layouts/`
     - Page layout specifications and code
   - **Assets**: `.specify/design/assets/`
     - Any generated assets (if applicable)

3. Create `.specify/design/README.md` with:
   - Overview of the design system
   - How to use the components
   - Link to full design specifications
   - Implementation notes

### Step 6: Verify Output

1. Confirm all files are created successfully
2. Display summary:
   ```
   ✓ Design specifications created successfully

   Output location: .specify/design/

   Generated files:
   - design-system.md (Design tokens and system)
   - components/ (Component specifications)
   - layouts/ (Layout specifications)
   - README.md (Design overview)

   Next steps:
   - Review the design specifications
   - Run /speckit.plan to create technical implementation plan
   ```

## Claude Code Specific Instructions

**This command is optimized for Claude Code environment**:

1. **Use Skill Integration**:
   - Leverage the `frontend-design` skill from Claude Code Marketplace
   - Do NOT create custom skills in `.claude/skills/`
   - Use marketplace skills for better maintenance and updates

2. **Output Format**:
   - Save to `.specify/design/` (NOT `.claude/skills/`)
   - Generate implementation-ready code
   - Include both specifications AND code samples

3. **Workflow Integration**:
   - Design output will be read by `/speckit.plan`
   - Plan will reference these designs for technical implementation
   - Implement phase will use both plan + design

## Output

**Location**: `.specify/design/`

**Structure**:
```
.specify/design/
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
- Design specifications are saved to `.specify/design/`
- Design system includes colors, typography, spacing
- Component specifications include implementation code
- README.md provides clear overview and usage instructions
- Output is ready to be referenced by plan and implement phases
