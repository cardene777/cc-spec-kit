# AGENTS.md - Grove Developer Guide

## About Grove

**Grove** is a comprehensive toolkit for implementing Spec-Driven Development (SDD) with built-in quality assurance. It combines clear specification creation with TDD workflows and AI-powered automated review (Self Review, Auto-Fix, Cross Review).

**Grove CLI** bootstraps projects with the Grove framework, setting up directory structures, templates, and AI agent integrations.

---

## Currently Supported AI Agents

Grove **officially supports 2 AI agents**:

| Agent | Support Level | Directory | Background Self Review | Notes |
|-------|---------------|-----------|------------------------|-------|
| **Claude Code** | ✅ Full (Recommended) | `.claude/` | ✅ Yes | Full support for verification agents, background execution |
| **Codex CLI** | ✅ Basic | `.codex/` | ❌ No | Template generation only, no Grove-specific features |

### Claude Code (Recommended)

**Why Claude Code is recommended:**

- ✅ **Background Self Review**: Autonomous verification agents run in parallel
- ✅ **Verification Agent**: Native subagent support with `run_in_background=True`
- ✅ **Auto-Fix**: TDD-based automatic issue resolution
- ✅ **8-Point Quality Checklist**: Automated quality verification
- ✅ **All Grove Commands**: Full support for 12 slash commands

**Setup**: [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code/setup)

### Codex CLI (Basic Support)

**Current support:**

- ✅ Template generation (`.codex/prompts/` directory)
- ✅ Grove command files (`/grove.constitution`, `/grove.specify`, etc.)
- ❌ Background Self Review (not supported)
- ❌ Verification agents (not available)

---

## Legacy Agent Configurations

Grove CLI includes AGENT_CONFIG definitions for 15+ other AI agents inherited from Spec Kit. **These are NOT officially supported by Grove** and exist only for template generation compatibility:

- GitHub Copilot, Cursor, Gemini, Qwen, opencode, Windsurf, Kilo Code, Auggie, CodeBuddy, Qoder, Roo, Amazon Q, Amp, SHAI, IBM Bob

**Important notes about legacy agents:**

1. ❌ **No Grove-specific features**: Background Self Review, Auto-Fix, verification agents are Claude Code exclusive
2. ⚠️ **Untested**: Grove team does not test or maintain these integrations
3. 📝 **Template-only**: Only basic command file generation is supported
4. 🚧 **Use at your own risk**: May have bugs or incompatibilities with Grove workflows

If you need these agents, consider contributing to Grove by implementing proper support!

---

## General Practices

- Any changes to `src/grove_cli/__init__.py` require:
  - Version bump in `pyproject.toml`
  - Changelog entry in `CHANGELOG.md`

---

## Adding New Agent Support to Grove

### Prerequisites

Before adding a new agent, understand Grove's architecture:

1. **Template Generation** (Basic): Generate command files for any agent
2. **Grove Features** (Advanced): Background Self Review, verification agents, Auto-Fix

Adding basic template generation is straightforward. Adding full Grove feature support requires significant effort.

### Step 1: Add to AGENT_CONFIG

**File**: `src/grove_cli/__init__.py`

Add the new agent to `AGENT_CONFIG` dictionary:

```python
AGENT_CONFIG = {
    # ... existing agents ...
    "new-agent": {  # Use actual CLI executable name
        "name": "New Agent Display Name",
        "folder": ".newagent/",
        "install_url": "https://example.com/install",  # or None for IDE-based
        "requires_cli": True,  # or False for IDE-based
    },
}
```

**Key principles:**

- Use the **actual CLI executable name** as the key (e.g., `"cursor-agent"` not `"cursor"`)
- This eliminates special-case mappings throughout the codebase
- Set `requires_cli: True` only if a CLI tool check is needed

### Step 2: Update SUPPORTED_AI_AGENTS

**File**: `src/grove_cli/__init__.py`

Add the new agent to the `SUPPORTED_AI_AGENTS` list if you want it available in `grove init`:

```python
SUPPORTED_AI_AGENTS = ["claude", "codex", "new-agent"]
```

**Note**: Only add agents you intend to officially support. Legacy agents remain in AGENT_CONFIG but NOT in SUPPORTED_AI_AGENTS.

### Step 3: Update Release Scripts

**File**: `.github/workflows/scripts/create-release-packages.sh`

Add to `ALL_AGENTS` array and case statement:

```bash
ALL_AGENTS=(claude codex new-agent)

# In build_variant() function
case $agent in
    # ... existing cases ...
    new-agent)
        mkdir -p "$base_dir/.newagent/commands"
        generate_commands new-agent md "\$ARGUMENTS" "$base_dir/.newagent/commands" "$script" ;;
esac
```

### Step 4: Update Documentation

**Files to update:**

1. **README.md / README-ja.md**: Add to "Supported AI Agents" table
2. **docs/agents.md**: Add detailed agent information
3. **CHANGELOG.md**: Document the new agent addition

### Step 5: Test

Test the following:

```bash
# Template generation
grove init test-project --ai new-agent --lang en

# Verify directory structure
ls -la test-project/.newagent/

# Verify command files
ls test-project/.newagent/commands/grove.*.md
```

---

## Implementing Full Grove Features

To add **Background Self Review** support (like Claude Code):

### Requirements

1. **Subagent System**: Agent must support spawning background tasks
2. **File I/O**: Agent must read/write files autonomously
3. **Markdown Parsing**: Agent must parse verification reports
4. **Task Tracking**: Agent must use TaskOutput for synchronization

### Implementation Steps

1. **Create Verification Agent Template**:
   - File: `templates/agents/{agent}/agents/verification.md`
   - Based on: `templates/agents/claude/agents/verification.md`

2. **Update Implement Command**:
   - File: `templates/agents/commands/implement.md`
   - Add agent-specific verification logic (Step 7.2.2 and 7.3)

3. **Test Background Execution**:
   - Verify agent can spawn background tasks with `run_in_background=True`
   - Verify autonomous report generation
   - Verify TaskOutput synchronization

**Current status**: Only Claude Code has full implementation.

---

## Directory Structures by Agent

### Claude Code (Full Support)

```
.claude/
├── commands/          # Slash commands (grove.*.md)
├── agents/            # Verification agent
│   └── verification.md
└── rules/             # Project rules
    └── constitution.md
```

### Codex (Basic Support)

```
.codex/
└── prompts/           # Command prompts (grove.*.md)
```

### Legacy Agents (Template-Only)

Directories defined in AGENT_CONFIG but not actively maintained:
- `.github/agents/` (Copilot)
- `.cursor/commands/` (Cursor)
- `.gemini/commands/` (Gemini)
- `.windsurf/workflows/` (Windsurf)
- etc.

---

## Command File Formats

### Markdown Format (Claude, Codex, Cursor, etc.)

**YAML Frontmatter**:
```yaml
---
description: "Command description"
argument-hint: "<feature description>"  # Optional
handoffs:  # Define next steps
  - label: Next Command Name
    agent: grove.specify
    prompt: Pre-filled context for next command
  - label: Optional Step (recommended)
    agent: grove.design
    prompt: Create design based on spec
    send: true  # Auto-send without confirmation (optional)
scripts:  # Prerequisite scripts
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
---
```

**Outline Structure** (numbered list with hyphen sub-steps):
```markdown
## Outline

Follow this execution flow:

1. First major step:
   - Sub-step detail
   - Another sub-step
   - Example output or command

2. Second major step:
   - Load inputs
   - Process data
   - Write results

3. Third major step (if applicable)
```

**Key Rules**:
- Use numbered list (1., 2., 3.) for major steps
- Use hyphen (-) for sub-steps (NOT a., b., c. or bold)
- NO explicit "Next Steps" section (use handoffs instead)
- Handoffs auto-display after command completion

### TOML Format (Gemini, Qwen)

```toml
description = "Command description"

prompt = """
Command content with {SCRIPT} and {{args}} placeholders.
"""
```

---

## Testing Guidelines

When adding or modifying agent support:

1. **Test template generation**: `grove init test --ai {agent}`
2. **Verify file structure**: Check `.{agent}/` directory
3. **Test commands**: Try `/grove.constitution`, `/grove.specify`, etc.
4. **Document limitations**: Be clear about what's supported vs. not supported

---

## Future Roadmap

Potential areas for community contribution:

1. **Expand Codex Support**: Add verification agent for Codex
2. **GitHub Copilot Support**: Implement background Self Review
3. **Cursor Support**: Add Grove-specific features
4. **Test & Document**: Verify all legacy agents work correctly

---

## Common Pitfalls

1. **Confusing template generation with full Grove support**: Most agents only have basic template generation
2. **Using shorthand keys**: Always use actual CLI executable names in AGENT_CONFIG
3. **Forgetting to update SUPPORTED_AI_AGENTS**: New agents won't appear in `grove init` without this
4. **Claiming full support**: Only Claude Code has background Self Review; be honest about limitations

---

## Contributing

Want to add full Grove support for your favorite AI agent?

1. Fork the repository
2. Implement verification agent for your target agent
3. Test thoroughly with background execution
4. Submit PR with documentation updates

**Questions?** Open an issue on [GitHub](https://github.com/cardene777/grove/issues)

---

*Last updated: 2025-12-21*
