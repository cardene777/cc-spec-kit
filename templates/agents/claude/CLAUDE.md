**READ @AGENTS.md ABOVE FIRST - IT CONTAINS CRITICAL LANGUAGE AND TEMPLATE RULES**

# Claude Code Specific Rules

## Question Guidelines

- **ALWAYS** use `AskUserQuestion` tool (never plain text questions)
- Each option must have: **Rating** (⭐ 1-5) + **Reasoning** (1-2 sentences)
- Rating scale: ⭐⭐⭐⭐⭐ (5/5) highly recommended → ⭐ (1/5) avoid
- Place highest-rated option first

## Using Skills

When command definitions use `Skill("skill-name")` notation, invoke the skill by mentioning it naturally in your request.

Example: `Skill("pdf")` → "Use the PDF skill to extract information from..."
