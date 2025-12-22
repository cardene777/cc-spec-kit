---
description: Create comprehensive design system and specifications for UI/UX implementation
argument-hint: "[design context or requirements]"
handoffs:
  - label: Create Technical Plan
    agent: grove.plan
    prompt: Create an implementation plan for these design specifications. I am building...
  - label: Clarify Design Requirements
    agent: grove.clarify
    prompt: Clarify the design requirements and assumptions
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

Create a comprehensive design system that guides implementation and ensures consistent UI/UX throughout the project. The output serves as both specification and reference for developers and AI agents.

**Design = 見た目ではなく意思決定の集合**

This command generates not just visual specifications, but a complete record of design decisions, principles, and rationale.

## Outline

1. Validate environment and load inputs:
   - Check Claude Code environment
   - Verify frontend-design skill availability
   - Read specification from spec.md
   - Parse user input for additional design direction

2. Initialize design directory structure:
   - Create `.grove/design/` with complete hierarchy
   - Set up context, principles, foundations, components, patterns, flows, ai, tokens, references directories
   - Prepare for organized design asset storage

3. Execute frontend-design skill:
   - Generate design foundations (color, typography, spacing)
   - Create component specifications with states
   - Define interaction patterns and flows
   - Produce implementation-ready code samples

4. Organize design system files:
   - Save context documentation (product goals, target users, constraints, non-goals)
   - Save principles (design, UX, accessibility)
   - Save foundations (color, typography, spacing, grid, motion, tone-and-voice)
   - Save component specifications (spec, states, design-decisions, examples, code)
   - Save patterns (authentication, onboarding, error-handling, empty-state)
   - Save flows (user-flows, edge-cases)

5. Record AI design decisions:
   - Create decision logs for major design choices
   - Document rejected options with rationale
   - Track design evolution and reasoning

6. Save design tokens and references:
   - Create token definitions (tokens.json, mapping.md)
   - Document design system references
   - Record competitor analysis and research

7. Create design system README and changelog:
   - Write comprehensive README with usage guide
   - Initialize changelog with design baseline
   - Document integration instructions

8. Verify output and display summary

---

## Process

### Step 1: Validate Environment and Load Inputs

1. Check Claude Code environment:
   - Verify `.claude/` directory exists
   - Confirm frontend-design skill availability
   - If NOT Claude Code: Display error message:
     ```
     Error: This design command requires Claude Code environment.
     The frontend-design skill is only available in Claude Code Marketplace.

     For other AI agents, please create design specifications manually.
     ```

2. Load specification:
   - Get current feature from git branch: `git rev-parse --abbrev-ref HEAD`
   - Extract feature number and name (format: `{number}-{feature-name}`)
   - Read `specs/{number}-{feature-name}/spec.md`

3. Parse design requirements:
   - Extract UI/UX requirements from spec.md
   - Check `$ARGUMENTS` for additional design context
   - Identify target platform (web, mobile, desktop)
   - Note technology stack preferences
   - Identify design system requirements

4. If spec.md doesn't exist:
   - Display error: "specs/{number}-{feature-name}/spec.md not found"
   - Suggest: "Run /grove.specify first to create the specification"

### Step 2: Initialize Design Directory Structure

Create `.grove/design/` with the following hierarchy:

```
.grove/design/
├── README.md
├── context/
│   ├── product-goals.md
│   ├── target-users.md
│   ├── constraints.md
│   └── non-goals.md
├── principles/
│   ├── design-principles.md
│   ├── ux-principles.md
│   └── accessibility.md
├── foundations/
│   ├── color.md
│   ├── typography.md
│   ├── spacing.md
│   ├── grid.md
│   ├── motion.md
│   └── tone-and-voice.md
├── components/
│   └── {component-name}/
│       ├── spec.md
│       ├── states.md
│       ├── design-decisions.md
│       ├── examples.png
│       └── code.{ext}
├── patterns/
│   ├── authentication.md
│   ├── onboarding.md
│   ├── error-handling.md
│   └── empty-state.md
├── flows/
│   ├── user-flows.md
│   └── edge-cases.md
├── ai/
│   ├── prompts/
│   │   ├── ui-generation.md
│   │   ├── layout.md
│   │   └── copy.md
│   ├── decision-logs/
│   │   ├── color-selection.md
│   │   ├── layout-choices.md
│   │   └── component-structure.md
│   └── rejected-options.md
├── tokens/
│   ├── tokens.json
│   └── mapping.md
├── references/
│   ├── design-systems.md
│   ├── competitor-analysis.md
│   └── research.md
└── changelog.md
```

### Step 3: Execute frontend-design Skill

1. Check if frontend-design skill is available:
   - Attempt to invoke: `Skill("frontend-design:frontend-design")`
   - If successful → skill is installed, proceed
   - If error (skill not found) → guide user to install

2. Guide user to install frontend-design skill (if needed):
   - Add Anthropic skills marketplace:
     ```
     /plugin marketplace add anthropics/skills
     ```
   - Install the frontend-design skill:
     ```
     /plugin install frontend-design@anthropic-agent-skills
     ```
   - After installation, retry skill invocation

3. Invoke frontend-design skill with specification context:
   - Project overview and feature scope
   - UI/UX requirements and user needs
   - Target platform and audience
   - Technology stack preferences
   - Any existing design system constraints

4. Request skill to generate:
   - Design system (colors, typography, spacing scales)
   - Component specifications (structure, states, variations)
   - Layout patterns and responsive approach
   - Interaction patterns (animations, transitions, feedback)
   - Implementation code samples (HTML/CSS/React/Vue as appropriate)

### Step 4: Organize Design System Files

1. Save context documentation to `context/`:
   - `product-goals.md` - project objectives and success metrics
   - `target-users.md` - user personas, needs, and usage scenarios
   - `constraints.md` - technical, business, and design constraints
   - `non-goals.md` - explicitly out of scope items (prevents AI scope creep)

2. Save principles to `principles/`:
   - `design-principles.md` - core design values (e.g., Clarity over beauty, Consistency over novelty)
   - `ux-principles.md` - user experience guidelines (e.g., Minimize cognitive load)
   - `accessibility.md` - WCAG compliance level, keyboard navigation, contrast requirements

3. Save foundations to `foundations/`:
   - `color.md` - color palette with semantic naming and usage rules
   - `typography.md` - typeface choices, size scales, line heights, weights
   - `spacing.md` - spacing scale and density guidelines
   - `grid.md` - layout grid definition, breakpoints, and column system
   - `motion.md` - animation principles, timing, easing, when to use/avoid
   - `tone-and-voice.md` - UI writing style, terminology, communication patterns

4. Save components to `components/{component-name}/`:
   - `spec.md` - component purpose, when to use/not use, variants
   - `states.md` - all component states (default, hover, active, focus, disabled, error, loading)
   - `design-decisions.md` - rationale for design choices, alternatives considered
   - `examples.png` - visual reference and usage examples (if applicable)
   - `code.{ext}` - implementation code samples (HTML, React, Vue, etc.)

5. Save patterns to `patterns/`:
   - `authentication.md` - login, signup, password reset, OAuth flows
   - `onboarding.md` - user onboarding, setup wizards, first-run experiences
   - `error-handling.md` - error states, messages, recovery actions, validation
   - `empty-state.md` - zero-data experiences, placeholder content, CTAs

6. Save flows to `flows/`:
   - `user-flows.md` - primary user journeys with step-by-step diagrams
   - `edge-cases.md` - error handling, exceptional scenarios, fallback behaviors

### Step 5: Record AI Design Decisions

1. Create AI decision logs in `ai/decision-logs/`:
   - `color-selection.md` - why specific colors chosen, accessibility considerations
   - `layout-choices.md` - layout structure rationale, responsive strategy
   - `component-structure.md` - component hierarchy, composition decisions
   - For each major design choice:
     - Decision context (what was needed)
     - Options considered (alternatives)
     - Choice made (selected approach)
     - Rationale (why this choice)

2. Document rejected design options in `ai/rejected-options.md`:
   - Option description (what was considered)
   - Why rejected (specific reasons)
   - When considered (date/phase)
   - Purpose: Prevents revisiting same rejected approaches

3. Save AI prompts used in `ai/prompts/`:
   - `ui-generation.md` - prompts used to generate UI components
   - `layout.md` - prompts for layout structure
   - `copy.md` - prompts for UI text and microcopy

### Step 6: Save Design Tokens and References

1. Create token definitions in `tokens/`:
   - `tokens.json` - structured design tokens (colors, spacing, typography as variables)
   - `mapping.md` - token usage guide, semantic naming conventions, component mappings

2. Create references in `references/`:
   - `design-systems.md` - design systems reviewed for inspiration (Material, Chakra, Ant, etc.)
   - `competitor-analysis.md` - competitive UX analysis, industry standards
   - `research.md` - user research findings, usability insights, data that informed design

### Step 7: Create Design System README and Changelog

1. Create `.grove/design/README.md` with:
   - Design system overview and purpose
   - How to use this design system
   - Token reference and customization guide
   - Component catalog with links
   - Integration instructions for implementation phase
   - Design principles summary
   - Contribution and evolution guidelines

2. Create `.grove/design/changelog.md`:
   - Record initial design system creation
   - Note version baseline (e.g., v1.0.0)
   - Document key design decisions
   - Track future design evolution with dates and rationale

### Step 8: Verify Output and Display Summary

1. Confirm all files created successfully:
   - Check directory structure completeness
   - Verify critical files exist (README, foundations, components)
   - Validate markdown formatting

2. Display completion summary:
   ```
   ✓ Design system created successfully

   Output location: .grove/design/

   Generated structure:
   - context/ (4 files: goals, users, constraints, non-goals)
   - principles/ (3 files: design, UX, accessibility)
   - foundations/ (6 files: color, typography, spacing, grid, motion, tone)
   - components/ (N components with specs, states, decisions, examples, code)
   - patterns/ (4 files: authentication, onboarding, errors, empty-states)
   - flows/ (2 files: user-flows, edge-cases)
   - ai/ (decision-logs, rejected-options, prompts)
   - tokens/ (tokens.json, mapping.md)
   - references/ (design-systems, competitor-analysis, research)
   - README.md (design system guide)
   - changelog.md (design evolution)

   Next: Run /grove.plan to create technical implementation plan
   ```

---

## Guidelines

### Design System Principles

- **Consistent**: All components follow shared design language
- **Accessible**: WCAG 2.1 AA compliance baseline (minimum)
- **Scalable**: Supports multiple platforms and themes
- **Documented**: Every decision has clear rationale
- **Evolvable**: Changelog tracks design evolution

### Component Specifications

Each component must include:
- Clear purpose and use cases
- All interactive states (default, hover, active, disabled, error, loading)
- Visual specifications (dimensions, spacing, colors using tokens)
- Accessibility requirements and keyboard interaction
- Code implementation examples
- Design decisions explaining why this approach was chosen

### Decision Documentation

Record decisions to enable:
- Design consistency across team and AI agents
- Faster onboarding for new designers/developers
- Preventing recurring debates about same approaches
- Understanding design evolution over time
- AI agents can reference past decisions for consistency

### AI Decision Records

When using AI to generate design:
- Explicitly document design choices made by AI
- Record alternatives considered and rejected
- Note any design constraints that drove decisions
- Enable human review and override capability
- Create audit trail for design rationale

---

## Claude Code Specific Instructions

1. **Skill Integration**:
   - Use frontend-design skill from Claude Code Marketplace
   - Do NOT create custom skills in `.claude/skills/`
   - Leverage marketplace skills for maintenance and updates

2. **Output Format**:
   - Save to `.grove/design/` (NOT `.claude/skills/`)
   - Generate implementation-ready code
   - Include both specifications AND code samples
   - Structure follows directory hierarchy defined above

3. **Workflow Integration**:
   - Design output feeds into /grove.plan phase
   - Plan creates technical implementation strategy
   - Implement phase uses both plan and design specifications
   - Review phase validates design consistency

---

## Success Criteria

- Frontend-design skill executes successfully (or manual fallback completed)
- Design system files organized in `.grove/design/`
- All context, principles, and foundations documented
- Component specifications include all required states
- Component code implementations provided
- Design decisions recorded in `ai/decision-logs/`
- Rejected options tracked in `ai/rejected-options.md`
- Design tokens defined in `tokens/tokens.json`
- README.md provides clear overview and integration guide
- Changelog initialized with design baseline
- Output ready for `/grove.plan` to consume
