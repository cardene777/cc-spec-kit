---
description: Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.
argument-hint: ""
handoffs:
  - label: Build Technical Plan
    agent: grove.plan
    prompt: Create a plan for the spec. I am building with...
scripts:
   sh: scripts/bash/check-prerequisites.sh --json --paths-only
   ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

**Goal**: Detect and reduce ambiguity or missing decision points in the active feature specification and record clarifications directly in the spec file.

**Note**: This clarification workflow should run BEFORE `/grove.plan`. If user skips clarification (e.g., exploratory spike), warn that downstream rework risk increases.

1. Run prerequisite script and parse paths:
   - Execute {SCRIPT} from repository root
   - Parse FEATURE_DIR and FEATURE_SPEC from JSON output
   - All paths must be absolute
   - For single quotes in args: use escape syntax 'I'\''m Groot' or double-quote "I'm Groot"
   - If JSON parsing fails: abort and instruct user to re-run `/grove.specify`

2. Load specification and perform ambiguity scan:
   - Read current spec file from FEATURE_SPEC
   - Parse fields: FEATURE_DIR, FEATURE_SPEC
   - Perform structured ambiguity & coverage scan using Clarification Taxonomy (see Guidelines)
   - For each category, mark status: Clear / Partial / Missing
   - Produce internal coverage map for prioritization
   - Do not output raw map unless no questions will be asked
   - For each category with Partial or Missing status:
     - Add candidate question opportunity
     - Skip if clarification wouldn't materially change implementation
     - Skip if information better deferred to planning phase

3. Generate prioritized queue of clarification questions:
   - Maximum 5 questions total per session
   - Do NOT output all questions at once
   - Each question must be answerable with EITHER:
     - Multiple-choice (2-5 options), OR
     - Short answer (<=5 words)
   - Only include questions with material impact on architecture, data modeling, task decomposition, test design, UX behavior, operational readiness, or compliance
   - Prioritize highest impact unresolved categories first
   - Exclude questions already answered or trivial preferences
   - Favor clarifications that reduce downstream rework risk
   - If >5 categories unresolved: select top 5 by (Impact × Uncertainty)

4. Sequential questioning loop (interactive):
   - Present EXACTLY ONE question at a time
   - For multiple-choice questions:
     - Analyze all options and determine most suitable based on best practices
     - Present recommended option prominently: `**Recommended:** Option [X] - <reasoning>`
     - Render all options as Markdown table with Option and Description columns
     - User can reply with option letter, "yes"/"recommended", or custom short answer
   - For short-answer questions:
     - Provide suggested answer: `**Suggested:** <answer> - <reasoning>`
     - User can accept with "yes"/"suggested" or provide custom answer (<=5 words)
   - After user answers:
     - If "yes"/"recommended"/"suggested": use your recommendation
     - Otherwise: validate answer maps to option or fits <=5 word constraint
     - If ambiguous: ask disambiguation (doesn't count as new question)
     - Once satisfactory: record in working memory, move to next question
   - Stop asking when:
     - All critical ambiguities resolved, OR
     - User signals completion ("done", "good", "no more"), OR
     - Reached 5 asked questions
   - Never reveal future queued questions in advance
   - If no valid questions exist at start: immediately report no critical ambiguities

5. Integrate each accepted answer incrementally:
   - Maintain in-memory representation of spec file
   - For first answer in session:
     - Ensure `## Clarifications` section exists
     - Create `### Session YYYY-MM-DD` subheading for today
   - Append bullet: `- Q: <question> → A: <final answer>`
   - Apply clarification to appropriate section(s):
     - Functional ambiguity → Update Functional Requirements
     - User interaction → Update User Stories or Actors
     - Data model → Update Data Model (fields, types, relationships)
     - Non-functional → Update Quality Attributes with measurable criteria
     - Edge case → Add to Edge Cases / Error Handling
     - Terminology → Normalize term across spec
   - If clarification invalidates earlier statement: replace (don't duplicate)
   - Save spec file AFTER each integration (atomic overwrite)
   - Preserve formatting and heading hierarchy

6. Validate after each write and final pass:
   - Clarifications session contains exactly one bullet per accepted answer
   - Total asked questions ≤ 5
   - Updated sections contain no lingering vague placeholders
   - No contradictory earlier statements remain
   - Markdown structure valid
   - Terminology consistent across all sections

7. Write updated spec back to FEATURE_SPEC

8. Report completion:
   - Number of questions asked & answered
   - Path to updated spec
   - Sections touched (list names)
   - Coverage summary table by taxonomy category:
     - Resolved (was Partial/Missing, now addressed)
     - Deferred (exceeds quota or better for planning)
     - Clear (already sufficient)
     - Outstanding (still Partial/Missing but low impact)
   - If Outstanding or Deferred remain: recommend next action (/grove.plan or /grove.clarify again)

---

## Guidelines

### Clarification Taxonomy

For ambiguity scan (step 2), use this taxonomy. For each category, mark status: Clear / Partial / Missing.

**Functional Scope & Behavior**:
- Core user goals & success criteria
- Explicit out-of-scope declarations
- User roles / personas differentiation

**Domain & Data Model**:
- Entities, attributes, relationships
- Identity & uniqueness rules
- Lifecycle/state transitions
- Data volume / scale assumptions

**Interaction & UX Flow**:
- Critical user journeys / sequences
- Error/empty/loading states
- Accessibility or localization notes

**Non-Functional Quality Attributes**:
- Performance (latency, throughput targets)
- Scalability (horizontal/vertical, limits)
- Reliability & availability (uptime, recovery expectations)
- Observability (logging, metrics, tracing signals)
- Security & privacy (authN/Z, data protection, threat assumptions)
- Compliance / regulatory constraints (if any)

**Integration & External Dependencies**:
- External services/APIs and failure modes
- Data import/export formats
- Protocol/versioning assumptions

**Edge Cases & Failure Handling**:
- Negative scenarios
- Rate limiting / throttling
- Conflict resolution (e.g., concurrent edits)

**Constraints & Tradeoffs**:
- Technical constraints (language, storage, hosting)
- Explicit tradeoffs or rejected alternatives

**Terminology & Consistency**:
- Canonical glossary terms
- Avoided synonyms / deprecated terms

**Completion Signals**:
- Acceptance criteria testability
- Measurable Definition of Done style indicators

**Misc / Placeholders**:
- TODO markers / unresolved decisions
- Ambiguous adjectives ("robust", "intuitive") lacking quantification

### Behavior Rules

- If no meaningful ambiguities found: respond "No critical ambiguities detected worth formal clarification" and suggest proceeding
- If spec file missing: instruct user to run `/grove.specify` first (do not create new spec here)
- Never exceed 5 total asked questions (clarification retries for same question don't count as new)
- Avoid speculative tech stack questions unless absence blocks functional clarity
- Respect user early termination signals ("stop", "done", "proceed")
- If no questions asked due to full coverage: output compact coverage summary (all categories Clear) then suggest advancing
- If quota reached with unresolved high-impact categories: explicitly flag under Deferred with rationale

Context for prioritization: {ARGS}
