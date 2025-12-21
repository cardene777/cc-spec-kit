# Supported AI Agents

Grove supports 17+ AI agents, allowing you to choose the development environment that best fits your workflow.

## 🌟 Recommended Agent

### Claude Code

**Claude Code** is the recommended AI agent for Grove projects because it offers:

- ✅ **Full Background Self Review Support**: Autonomous verification agents run in parallel during implementation
- ✅ **Native Task Support**: Built-in `run_in_background=True` for parallel execution
- ✅ **Complete TDD Workflow**: Red-Green-Refactor cycle with automatic verification
- ✅ **Best Integration**: Designed specifically for Grove's 3-layer review system

**Setup**: Follow the [Claude Code setup guide](https://docs.anthropic.com/en/docs/claude-code/setup)

---

## 📋 All Supported Agents

Grove provides configuration templates for the following AI agents:

### IDE-Based Agents (No CLI Required)

| Agent | Description | Grove Support | Configuration Folder |
|-------|-------------|---------------|---------------------|
| **Claude Code** | Anthropic's official CLI | ✅ Full (Recommended) | `.claude/` |
| **GitHub Copilot** | GitHub's AI pair programmer | ✅ Full | `.github/agents/` |
| **Cursor** | AI-first code editor | ✅ Full | `.cursor/` |
| **Windsurf** | AI-powered development environment | ✅ Full | `.windsurf/` |
| **Kilo Code** | Lightweight AI code assistant | ✅ Full | `.kilocode/` |
| **Roo Code** | Intelligent code generation | ✅ Full | `.roo/` |

### CLI-Based Agents

| Agent | Description | Grove Support | Configuration Folder | Installation URL |
|-------|-------------|---------------|---------------------|-----------------|
| **Codex CLI** | OpenAI Codex command-line interface | ✅ Full | `.codex/` | [GitHub](https://github.com/openai/codex) |
| **Gemini CLI** | Google Gemini command-line interface | ✅ Full | `.gemini/` | [GitHub](https://github.com/google-gemini/gemini-cli) |
| **Qwen Code** | Alibaba's AI code assistant | ✅ Full | `.qwen/` | [GitHub](https://github.com/QwenLM/qwen-code) |
| **opencode** | Open-source code generation | ✅ Full | `.opencode/` | [Website](https://opencode.ai) |
| **Auggie CLI** | AugmentCode CLI tool | ✅ Full | `.augment/` | [Docs](https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli) |
| **CodeBuddy** | AI coding companion | ✅ Full | `.codebuddy/` | [Website](https://www.codebuddy.ai/cli) |
| **Qoder CLI** | AI-powered development tool | ✅ Full | `.qoder/` | [Website](https://qoder.com/cli) |
| **Amazon Q Developer CLI** | AWS's AI coding assistant | ✅ Full | `.amazonq/` | [AWS](https://aws.amazon.com/developer/learning/q-developer-cli/) |
| **Amp** | Amplified development workflow | ✅ Full | `.agents/` | [Manual](https://ampcode.com/manual#install) |
| **SHAI** | Open-source AI assistant | ✅ Full | `.shai/` | [GitHub](https://github.com/ovh/shai) |
| **IBM Bob** | IBM's AI developer assistant | ✅ Full | `.bob/` | Enterprise solution |

---

## 🚀 How to Add Agents to Your Project

### Option 1: During Project Initialization

Specify one or more AI agents when creating a new project:

```bash
# Single agent
grove init my-app --ai claude --lang en

# Multiple agents
grove init my-app --ai claude --ai codex --lang en

# Interactive selection
grove init my-app
```

### Option 2: Add to Existing Project

Add additional AI agents to an existing Grove project:

```bash
# Navigate to your project
cd my-app

# Add Codex to existing Claude project
grove init . --ai codex

# Add multiple agents
grove init . --ai claude --ai codex
```

**Note**: Existing agent configurations won't be overwritten. Only new agents will be added.

---

## 🔧 Configuration Details

### Directory Structure by Agent

Each AI agent has a specific configuration directory structure:

```
project/
├── .claude/              # Claude Code
│   ├── commands/         # Slash commands
│   ├── agents/           # Custom agents (verification, etc.)
│   └── rules/            # Project rules
│
├── .codex/               # Codex CLI
│   └── prompts/          # Command prompts
│
├── .github/              # GitHub Copilot
│   ├── agents/           # Agent definitions
│   └── prompts/          # Companion prompts
│
├── .cursor/              # Cursor
│   └── commands/         # Cursor commands
│
├── .gemini/              # Gemini CLI
│   └── commands/         # Command definitions
│
├── .windsurf/            # Windsurf
│   └── workflows/        # Workflow definitions
│
└── .grove/               # Shared Grove configuration
    ├── templates/        # Language-specific templates
    └── scripts/          # Platform-specific scripts
```

### Commands Available

All agents have access to the following Grove commands:

| Command | Purpose |
|---------|---------|
| `/grove.constitution` | Define project principles |
| `/grove.specify` | Create feature specifications |
| `/grove.clarify` | Clarify underspecified areas |
| `/grove.design` | Create frontend design specs |
| `/grove.plan` | Create technical implementation plan |
| `/grove.tasks` | Break down into TDD tasks |
| `/grove.implement` | Execute implementation with TDD |
| `/grove.review` | Run Self Review or Cross Review |
| `/grove.fix` | Auto-fix review issues |
| `/grove.analyze` | Analyze cross-artifact consistency |
| `/grove.checklist` | Generate quality checklists |
| `/grove.taskstoissues` | Convert tasks to GitHub issues |

---

## 💡 Feature Comparison

| Feature | Claude Code | Other Agents |
|---------|-------------|--------------|
| Background Self Review | ✅ Full support | ⚠️ Synchronous only |
| Verification Agent | ✅ Native subagent | ❌ Not available |
| Auto-Fix with TDD | ✅ Full support | ✅ Full support |
| Cross Review | ✅ Full support | ✅ Full support |
| All Grove Commands | ✅ 12 commands | ✅ 12 commands |
| Multi-language Templates | ✅ Japanese/English | ✅ Japanese/English |

---

## 🆘 Troubleshooting

### Agent Not Found

If Grove can't find your AI agent configuration:

1. Verify the agent is installed:
   ```bash
   # For CLI-based agents
   which <agent-command>

   # For IDE-based agents, launch the IDE
   ```

2. Reinitialize agent configuration:
   ```bash
   cd your-project
   grove init . --ai <agent-name>
   ```

### Commands Not Available

If slash commands aren't showing up:

1. Check configuration directory exists:
   ```bash
   ls -la .claude/commands/  # or .codex/prompts/, etc.
   ```

2. Verify command files are present:
   ```bash
   ls .claude/commands/grove.*.md
   ```

3. Restart your AI agent

---

## 📚 Related Documentation

- [Quick Start](./quickstart.md) - Get started with Grove in 5 minutes
- [Installation Guide](./installation.md) - Detailed setup instructions
- [Main README](../README.md) - Project overview and features

---

**Need help?** [Open an issue](https://github.com/cardene777/grove/issues) or visit [GitHub Discussions](https://github.com/cardene777/grove/discussions)
