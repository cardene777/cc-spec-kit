# Project Language Configuration

This project uses `.specify/memory/config.json` to manage output language settings.

## How to Check Language Setting

Read `.specify/memory/config.json`:
```json
{
  "language": "ja"
}
```

## Language Rules

- `language: "ja"` → Output everything in **Japanese**
- `language: "en"` → Output everything in **English**

## What This Applies To

- All responses and explanations
- Generated documentation
- Commit messages
- Code comments
- Error messages

## Important

**Always check config.json BEFORE starting work and maintain the specified language throughout the entire task.**

## Template Usage

Templates are located in `templates/{language}/` directory. Use them if the YAML frontmatter has `enabled: true`.
