# Project Rules for Spec-Driven Development

## Language Configuration - CRITICAL

**MANDATORY FIRST STEP**: Read `.grove/memory/config.json`

- `language: "ja"` → **ALL outputs in Japanese ONLY (zero English allowed)**
- `language: "en"` → **ALL outputs in English ONLY (zero Japanese allowed)**
- Applies to: responses, questions, AskUserQuestion options, documentation, commit messages, error messages
- Default to English if config.json missing

**VIOLATION = TASK FAILURE**

## Template Usage

- Check `.grove/templates/*.md` YAML frontmatter for `enabled: true`
- If enabled: use template content as-is or reference
- If disabled/missing: use only structure

## Script Placeholder

`{SCRIPT}` → Read YAML frontmatter `scripts:` section, execute `sh:` value (macOS/Linux) or `ps:` value (Windows) from repo root.

Example frontmatter:
```yaml
scripts:
  sh: scripts/bash/my-script.sh --json
```
When you see `{SCRIPT}`, execute `scripts/bash/my-script.sh --json`

## Workflow

1. Constitution → 2. Specification → 3. Design (optional) → 4. Planning → 5. Task Breakdown → 6. Implementation (TDD)

## Working Agreements

- Read `.grove/memory/config.json` (language)
- Read `.grove/memory/constitution.md` (principles)
- Follow constitution's technical stack
- Use `.grove/spec.md` as source of truth

## Available Commands

**Claude Code**: `/grove.constitution`, `/grove.specify`, `/grove.clarify`, `/grove.design`, `/grove.plan`, `/grove.tasks`, `/grove.implement`, `/grove.analyze`, `/grove.checklist`, `/grove.taskstoissues`

**Codex**: `/prompts:constitution`, `/prompts:specify`, `/prompts:clarify`, `/prompts:design`, `/prompts:plan`, `/prompts:tasks`, `/prompts:implement`, `/prompts:analyze`, `/prompts:checklist`, `/prompts:taskstoissues`
