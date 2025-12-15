<language>Auto (from config.json)</language>
<character_code>UTF-8</character_code>

# Project Language Configuration

**IMPORTANT**: This project uses a language configuration file to determine output language.

## Language Detection

ALWAYS check `.specify/memory/config.json` at the start of every task:

```json
{
  "language": "ja"  // or "en"
}
```

## Output Language Rules

- If `language: "ja"` → **ALL outputs must be in Japanese**
- If `language: "en"` → **ALL outputs must be in English**

This applies to:
- All responses and explanations
- Commit messages
- Documentation (spec.md, plan.md, tasks.md, etc.)
- Code comments
- Error messages

## Critical Requirements

- **NEVER output in English when `language` is set to `"ja"`**
- **NEVER output in Japanese when `language` is set to `"en"`**
- Check config.json BEFORE starting any work
- If config.json is missing, ask the user for their preferred language

## Template Usage

When executing constitution, specify, plan, or tasks commands:
- Templates are located in `templates/{language}/`
- Only use template content if YAML frontmatter has `enabled: true`
- Apply template structure to your output

## Example Workflow

1. Read `.specify/memory/config.json`
2. Confirm language setting (ja or en)
3. Check if template exists and is enabled
4. Generate output in the configured language
5. Follow template structure if enabled
