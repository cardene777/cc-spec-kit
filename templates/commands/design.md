---
description: Create design specifications for UI/UX implementation guidance
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

Create design specifications that hold UI/UX design specifications and provide implementation guidance for the implementation phase.

This step is executed between 'specify' and 'plan' to ensure consistent UI/UX design throughout the project.

## Process

### Step 1: Detect Agent Type

Determine if you are running in Claude Code environment:
- Check for `.claude/` directory existence
- Check for skill-creator availability
- **If Claude Code**: proceed with skill-based approach (output to `.claude/skills/design-creator/skill.md`)
- **If other agent**: proceed with markdown file approach (output to `.specify/design.md`)

### Step 2: Check for Existing Design Files

1. Look for design files in `.specify/design/` directory
2. Supported formats: PNG, SVG, PDF, Sketch (.sketch), Adobe XD (.xd), Figma exports, Penpot, Framer, and other design files
3. Analyze files regardless of directory structure within .specify/design/
4. Design tools supported:
   - **Figma**: Exported images (PNG, SVG) or Figma files
   - **Sketch**: Sketch files or exported images
   - **Adobe XD**: XD files or exported images
   - **Penpot**: Exported files
   - **Framer**: Exported files
   - **Others**: PDF, wireframes, mockups, etc.

### Step 3: Prepare Design Specifications

**If design files exist:**
- Analyze all design files (regardless of source tool or format)
- Extract UI components, layouts, interactions
- Extract design system (colors, typography, spacing)
- Document design patterns and visual styles
- Identify component variants and states
- Note accessibility considerations from designs

**If no design files exist:**
- Review functional requirements from spec.md
- Generate UI/UX design based on requirements
- Create comprehensive design system:
  - Color palette with semantic naming (primary, secondary, background, text, success, warning, error)
  - Typography scale and usage (headings, body, captions)
  - Spacing/sizing system (xs, sm, md, lg, xl)
  - Component library (buttons, inputs, cards, etc.)
  - Layout patterns and grid system
  - Responsive design approach

### Step 4: Create Design Specification File

**For Claude Code (skill-based approach)**:

Use skill-creator to create `.claude/skills/design-creator/skill.md` with the following sections:

1. **Design System**
   - Color palette (primary, secondary, background, text, etc.)
   - Typography (font families, sizes, weights)
   - Spacing scale (xs, sm, md, lg, xl)
   - Border radius, shadows, and other visual tokens

2. **Component Library**
   - Component definitions (Button, Card, Input, etc.)
   - Variants and states for each component
   - Props and usage guidelines

3. **Layout & Grid System**
   - Grid specifications
   - Responsive breakpoints
   - Container widths

4. **Interaction Patterns**
   - Navigation patterns
   - Form interactions
   - Loading states
   - Error handling UI

5. **Accessibility Guidelines**
   - WCAG compliance requirements
   - Keyboard navigation
   - Screen reader support
   - Color contrast requirements

6. **Implementation Guidance**
   - Preferred CSS methodology (BEM, CSS Modules, Tailwind, CSS-in-JS)
   - Component organization patterns
   - Naming conventions
   - File structure recommendations
   - Best practices for maintainability
   - Performance considerations (lazy loading, code splitting)
   - Browser/device support targets

**For Other Agents (markdown file approach)**:

Create `.specify/design.md` with the same structure as above, formatted as a markdown document:

1. **Design System** section
2. **Component Library** section
3. **Layout & Grid System** section
4. **Interaction Patterns** section
5. **Accessibility Guidelines** section
6. **Implementation Guidance** section

## Output

**Claude Code**: Skill file at `.claude/skills/design-creator/skill.md`
**Other Agents**: Markdown file at `.specify/design.md`

These files will be automatically referenced during implementation to guide UI development.

## Success Criteria

- Design specification file is created at the appropriate location
- All design system tokens are documented with specific values
- Component library includes all major UI components
- Accessibility guidelines are comprehensive and actionable
- Implementation guidance is clear and technology-appropriate
