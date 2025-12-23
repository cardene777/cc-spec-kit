---
description: Create or update the feature specification from a natural language feature description.
argument-hint: "<feature description>"
handoffs:
  - label: Design UI/UX (recommended for user-facing features)
    agent: grove.design
    prompt: Create design specifications based on the spec
  - label: Create Technical Plan (backend/API features)
    agent: grove.plan
    prompt: Create a plan for the spec. I am building with...
  - label: Clarify Spec Requirements
    agent: grove.clarify
    prompt: Clarify specification requirements
    send: true
scripts:
  sh: scripts/bash/create-new-feature.sh --json "{ARGS}"
  ps: scripts/powershell/create-new-feature.ps1 -Json "{ARGS}"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Follow this execution flow:

1. Load all available inputs:
   - Read spec template: `.grove/templates/spec-template.md`
   - Check `$ARGUMENTS` for feature description (if provided)

2. Generate concise short name (2-4 words) for branch:
   - Analyze feature description and extract meaningful keywords
   - Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
   - Keep concise but descriptive
   - Examples:
     - "I want to add user authentication" → "user-auth"
     - "Implement OAuth2 integration for the API" → "oauth2-api-integration"
     - "Create a dashboard for analytics" → "analytics-dashboard"
     - "Fix payment processing timeout bug" → "fix-payment-timeout"

3. Check for existing branches before creating new one:
   - Fetch all remote branches: `git fetch --all --prune`
   - Find highest feature number across all sources for the short-name:
     - Remote branches: `git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'`
     - Local branches: `git branch | grep -E '^[* ]*[0-9]+-<short-name>$'`
     - Specs directories: Check for directories matching `specs/[0-9]+-<short-name>`
   - Determine next available number: Find highest N, use N+1
   - Run script with calculated number and short-name:
     - Bash: `{SCRIPT} --json --number 5 --short-name "user-auth" "Add user authentication"`
     - PowerShell: `{SCRIPT} -Json -Number 5 -ShortName "user-auth" "Add user authentication"`
   - Important notes:
     - Check all three sources (remote/local branches, specs directories)
     - Only match branches/directories with exact short-name pattern
     - If no existing found, start with number 1
     - Run script only once per feature
     - JSON output contains BRANCH_NAME and SPEC_FILE paths
     - For single quotes in args: use escape syntax `'I'\''m Groot'` or double-quote `"I'm Groot"`

4. Generate specification (intelligent creation):
   - Base structure: From spec-template.md
   - Feature description: From $ARGUMENTS (if provided)
   - Fill sections with feature-specific content derived from description or template examples
   - For unclear aspects:
     - Make informed guesses based on context and industry standards
     - Only mark with [NEEDS CLARIFICATION: specific question] if:
       - Choice significantly impacts feature scope or user experience
       - Multiple reasonable interpretations exist with different implications
       - No reasonable default exists
     - LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total
     - Prioritize clarifications: scope > security/privacy > user experience > technical details
   - Required sections to complete:
     - Overview: Feature purpose and context
     - User Scenarios & Testing: Primary user flows and acceptance scenarios
     - Functional Requirements: Testable, technology-agnostic requirements
     - Success Criteria: Measurable outcomes (time, performance, volume, satisfaction)
     - Key Entities: Data entities if applicable
     - Assumptions: Document any assumptions made
     - Out of Scope: Clear boundaries

5. Write specification to SPEC_FILE:
   - Use template structure
   - Replace placeholders with concrete details from feature description
   - Preserve section order and headings

6. Specification quality validation:
   - Create spec quality checklist at `FEATURE_DIR/checklists/requirements.md` with validation items:
     - Content Quality: No implementation details, focused on user value, written for non-technical stakeholders, all mandatory sections completed
     - Requirement Completeness: No [NEEDS CLARIFICATION] markers, requirements testable and unambiguous, success criteria measurable and technology-agnostic, acceptance scenarios defined, edge cases identified, scope bounded, dependencies and assumptions identified
     - Feature Readiness: Requirements have clear acceptance criteria, user scenarios cover primary flows, meets measurable outcomes, no implementation details leak
   - Run validation check against each checklist item
   - Handle validation results:
     - All pass: Mark checklist complete, proceed to step 7
     - Items fail (excluding [NEEDS CLARIFICATION]): List failing items, update spec to address issues, re-run validation (max 3 iterations), if still failing after 3 iterations document remaining issues and warn user
     - [NEEDS CLARIFICATION] markers remain: Extract all markers (max 3 most critical), present options to user with properly formatted markdown tables, wait for user responses, update spec with user's answers, re-run validation
   - Update checklist after each validation iteration

7. Display completion summary:
   - Specification created successfully
   - File location: SPEC_FILE
   - Validation status
   - Next steps: See handoffs section (automatically displayed)

---

## Guidelines

### Quick Guidelines

- Focus on **WHAT** users need and **WHY**
- Avoid HOW to implement (no tech stack, APIs, code structure)
- Written for business stakeholders, not developers
- DO NOT create embedded checklists in spec (separate command)

### Section Requirements

- Mandatory sections: Must be completed for every feature
- Optional sections: Include only when relevant
- When section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation

1. Make informed guesses: Use context, industry standards, common patterns to fill gaps
2. Document assumptions: Record reasonable defaults in Assumptions section
3. Limit clarifications: Maximum 3 [NEEDS CLARIFICATION] markers - use only for critical decisions
4. Prioritize clarifications: scope > security/privacy > user experience > technical details
5. Think like a tester: Every vague requirement should fail "testable and unambiguous" checklist item
6. Common areas needing clarification (only if no reasonable default exists):
   - Feature scope and boundaries (include/exclude specific use cases)
   - User types and permissions (if multiple conflicting interpretations possible)
   - Security/compliance requirements (when legally/financially significant)

### Examples of Reasonable Defaults (don't ask)

- Data retention: Industry-standard practices for the domain
- Performance targets: Standard web/mobile app expectations unless specified
- Error handling: User-friendly messages with appropriate fallbacks
- Authentication method: Standard session-based or OAuth2 for web apps
- Integration patterns: RESTful APIs unless specified otherwise

### Success Criteria Guidelines

Success criteria must be:
1. Measurable: Include specific metrics (time, percentage, count, rate)
2. Technology-agnostic: No mention of frameworks, languages, databases, tools
3. User-focused: Describe outcomes from user/business perspective, not system internals
4. Verifiable: Can be tested/validated without knowing implementation details

**Good examples**:
- "Users can complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"
- "Task completion rate improves by 40%"

**Bad examples** (implementation-focused):
- "API response time is under 200ms" (too technical, use "Users see results instantly")
- "Database can handle 1000 TPS" (implementation detail, use user-facing metric)
- "React components render efficiently" (framework-specific)
- "Redis cache hit rate above 80%" (technology-specific)
