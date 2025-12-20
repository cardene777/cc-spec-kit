<div align="center">
    <img src="./media/logo.webp" alt="Grove Logo" width="200" height="200"/>
    <h1>🌳 Grove</h1>
    <h3><em>AI-Powered Development with Built-in Quality Assurance</em></h3>
</div>

<p align="center">
    <strong>Spec-Driven Development × TDD × AI Auto-Review = High-Quality Software, Fast</strong>
</p>

<p align="center">
    <a href="https://github.com/cardene/grove/stargazers"><img src="https://img.shields.io/github/stars/cardene/grove?style=social" alt="GitHub stars"/></a>
    <a href="https://github.com/cardene/grove/blob/main/LICENSE"><img src="https://img.shields.io/github/license/cardene/grove" alt="License: MIT"/></a>
    <a href="./README-ja.md">日本語</a>
</p>

---

## 🎯 What is Grove?

**Grove** is a spec-driven development toolkit powered by AI agents.

Traditional development requires manual "code → review → fix" cycles, which are time-consuming and error-prone.

Grove **automates from specification to implementation**, integrating **TDD workflows** and **AI auto-review** to generate high-quality code at speed.

### Why Grove?

✅ **Specs Stay Current**: Direct code generation from specs keeps documentation and code in sync
✅ **Quality Guaranteed**: TDD + 3-layer AI review for automatic quality checks
✅ **Fast Feedback**: Background parallel execution ~28% faster
✅ **AI Collaboration**: Cross-check with multiple AI agents
✅ **Multi-language**: Full Japanese and English support

## 🚀 Three Key Features

### 1. 🧪 t-wada Style TDD Integration

**Test-Driven Development** enforced for every task:

```
For each task:
  Red      → Confirm test failure
  Green    → Minimal implementation to pass
  Refactor → Improve while keeping tests green
  Review   → AI automated verification
```

Formalizes Japanese TDD tacit knowledge for AI execution.

### 2. 🔍 3-Layer AI Review System

**Implementation → Self Review → Cross Review** quality assurance:

| Layer | Executor | Timing | Purpose |
|-------|----------|--------|---------|
| **Layer 1: Implementation** | AI Agent | During implementation | Code generation with TDD workflow |
| **Layer 2: Self Review** | Same AI Agent | Immediately after (background) | 8-point auto-verification + Auto-Fix |
| **Layer 3: Cross Review** | Different AI Agent | As needed | Additional verification from different perspective |

**Self Review Automation**:
```
T001 completed → Self Review launch (background)
T002 completed → Self Review launch (background)
T003 completed → Self Review launch (background)
      ↓
All complete → Report generation → Auto-Fix (max 3 attempts)
```

**8-Point Verification Checklist**:
1. ✅ Specification Compliance
2. ✅ Tech Stack Adherence
3. ✅ Task Completeness
4. ✅ Test Coverage
5. ✅ Error Handling
6. ✅ Security
7. ✅ Performance
8. ✅ Code Quality

**Scoring**: 0-100 points (Critical: -30, High: -20, Medium: -10, Low: -5)
**Pass Criteria**: 80+ points

### 3. ⚡ Background Parallel Execution

**Traditional Sequential**:
```
Implement → Verify (wait) → Implement → Verify (wait) → ...
```

**Grove Parallel**:
```
Implement → Verify (background)
    ↓
Implement → Verify (background)
    ↓
Implement → Verify (background)
    ↓
All complete → Collect results → Fix
```

Reduces wait time and improves development speed.

## 📦 Installation

### One-time Install (Recommended)

```bash
uv tool install grove-cli --from git+https://github.com/cardene/grove.git
```

### Initialize Project

```bash
# New project
grove init my-app --ai claude --lang en

# Existing project
grove init . --ai claude --lang en

# Or
grove init --here --ai claude --lang en
```

### Upgrade

```bash
uv tool install grove-cli --force --from git+https://github.com/cardene/grove.git
```

## 🎬 Usage

### Basic Workflow

```bash
# Launch AI agent and navigate to project directory
# The following commands become available

# 1. Define project principles
/grove.constitution Create principles focused on code quality, testing standards, and performance

# 2. Create feature specification
/grove.specify Build a task management application with projects, tasks, and Kanban boards

# 3. (Optional) Frontend design specifications
/grove.design Create design system with design tokens, components, and layouts

# 4. Create technical implementation plan
/grove.plan Use React + TypeScript, Node.js, and PostgreSQL

# 5. Break down into tasks
/grove.tasks

# 6. Execute implementation (TDD + Self Review auto-run)
/grove.implement

# 7. (Optional) Cross review (run with different AI)
/grove.review

# 8. (Optional) Auto-fix issues
/grove.fix
```

### Execution Example

```
T001 Implementation completed.
🔄 T001 Self Review launched in background (job: a703da0)
   Report will be saved to: reports/self-review/task-T001.md

T002 Implementation completed.
🔄 T002 Self Review launched in background (job: aa59562)
   Report will be saved to: reports/self-review/task-T002.md

⏳ Waiting for 2 verification agents to complete...
✓ All verification agents completed

Parsing reports...
✓ T001: PASS (Score: 95/100)
✗ T002: FAIL (Score: 65/100, 3 issues)

🔧 Auto-fixing T002...
✓ T002 Auto-Fix SUCCESS (Score: 85/100)

Self Review completed.
```

## 🤖 Supported AI Agents

17+ AI agents supported:

| AI Agent | Support | Notes |
|----------|---------|-------|
| **Claude Code** | ✅ | **Recommended** - Full background Self Review support |
| Cursor | ✅ | |
| GitHub Copilot | ✅ | |
| Codex CLI | ✅ | |
| Gemini CLI | ✅ | |
| Windsurf | ✅ | |
| 12+ others | ✅ | Qoder, Amp, Auggie, CodeBuddy, IBM Bob, Jules, Kilo Code, opencode, Qwen, Roo, SHAI, etc. |

See [Supported Agents](./docs/agents.md) for details.

## 📋 Commands

### Core Commands (Development Flow)

| Command | Description |
|---------|-------------|
| `/grove.constitution` | Create project principles and development guidelines |
| `/grove.specify` | Define feature specifications (requirements, user stories) |
| `/grove.plan` | Create technical implementation plan (tech stack, architecture) |
| `/grove.tasks` | Break down into tasks (with TDD workflow) |
| `/grove.implement` | Execute implementation (TDD + Self Review auto-run) |

### Quality Assurance Commands

| Command | Description |
|---------|-------------|
| `/grove.review` | Execute AI review (Self/Cross Review auto-detected) |
| `/grove.fix` | Auto-fix review issues (TDD approach) |

### Optional Commands

| Command | Description |
|---------|-------------|
| `/grove.clarify` | Clarify underspecified areas |
| `/grove.design` | Create frontend design specifications |
| `/grove.analyze` | Cross-artifact consistency analysis |
| `/grove.checklist` | Generate custom quality checklists |

## 🔍 How Self Review Works

### 1. Background Launch

Upon implementation completion, Verification Agent launches in background:

```python
Task(
    description="Verify task T001",
    prompt="...",
    subagent_type="verification-agent",
    run_in_background=True  # Background execution
)
```

### 2. Autonomous Verification & Report Generation

Verification Agent auto-executes:

1. **Load Context**: spec.md, plan.md, tasks.md
2. **Read Implementation**: Task-specified files
3. **8-Point Verification**: Checklist-based verification
4. **Score Calculation**: 0-100 points (severity-based penalties)
5. **Generate Report**: Markdown format
6. **Save File**: `reports/self-review/task-{ID}.md`

### 3. Report Format

```markdown
# Task T001 Verification Report

**Date:** 2025-12-21 10:30:00
**Task ID:** T001
**Description:** User authentication implementation
**Phase:** Phase 1

---

## 1. Summary

| Item   | Value        |
| ------ | ------------ |
| Score  | 85/100       |
| Status | **PASS**     |
| Issues | 1            |

---

## 2. Verification Checklist

- [x] Specification Compliance: PASS
- [x] Tech Stack Adherence: PASS
- [x] Task Completeness: PASS
- [x] Test Coverage: PASS
- [x] Error Handling: FAIL
- [x] Security: PASS
- [x] Performance: PASS
- [x] Code Quality: PASS

---

## 3. Verification Results

##### Issue 1

| Item     | Details             |
| -------- | ------------------- |
| Severity | Medium              |
| Location | `src/auth.py:42`    |

- **Description**: Insufficient error handling for login failure
- **Cause**: Missing try-except block
- **Recommended Fix**: Add exception handling
- **Evidence**: [code snippet]

---

## 4. Conclusion

Task T001 verification completed. Score: 85/100

1 minor issue found, but meets pass criteria (80+).
```

### 4. Auto-Fix

Failed tasks automatically fixed:

```
🔧 Auto-fixing T002 (Score: 65/100, 3 issues)...

Issue 1 (Critical): No password hashing
  Red:    Add test
  Green:  Implement bcrypt
  Refactor: Verify test ✓

Issue 2 (High): No input validation
  Red:    Add test
  Green:  Implement validation
  Refactor: Verify test ✓

Issue 3 (Medium): Insufficient error handling
  Red:    Add test
  Green:  Add exception handling
  Refactor: Verify test ✓

Re-verification: Score 85/100 (0 issues) ✓
```

Up to 3 auto-fix attempts.

## 🌍 Multi-language Support

Full Japanese and English support:

```bash
# Japanese
grove init my-app --ai claude --lang ja

# English
grove init my-app --ai claude --lang en
```

Templates, commands, and reports generated in selected language.

## 📚 Documentation

- **[Grove Guide (Japanese)](./articles/grove.md)** - Comprehensive guide
- **[Development Methodology](./spec-driven.md)** - Full spec-driven process
- **[Installation Guide](./docs/installation.md)** - Setup instructions
- **[Quick Start](./docs/quickstart.md)** - Get started in 5 minutes
- **[Local Development](./docs/local-development.md)** - Contributing

## 🛠️ Requirements

- **OS**: Linux / macOS / Windows
- **AI Agent**: One of the [supported agents](#-supported-ai-agents)
- **Python**: 3.11+
- **Package Manager**: [uv](https://docs.astral.sh/uv/)
- **Version Control**: [Git](https://git-scm.com/)

## 💡 FAQ

### Q: How is Grove different from Spec Kit?

A: Grove extends Spec Kit with powerful features:

| Feature | Spec Kit | Grove |
|---------|---------|-------|
| Spec-Driven Development | ✅ | ✅ |
| TDD Integration | ❌ | ✅ t-wada style |
| Self Review | ❌ | ✅ Background parallel execution |
| Cross Review | ❌ | ✅ Multi-AI support |
| Auto-Fix | ❌ | ✅ TDD approach |
| Multi-language | ❌ | ✅ Japanese/English |
| Verification Agent | ❌ | ✅ Claude Code support |

### Q: Which AI agent is recommended?

A: **Claude Code** is recommended. Full support for background Self Review and Verification Agent.

Other AI agents work but Self Review runs synchronously.

### Q: Can I use with existing projects?

A: Yes. Run `grove init . --ai claude` or `grove init --here --ai claude` in your project directory.

### Q: Can I skip review?

A: Yes. Use `/grove.implement --skip-self-review` to skip Self Review.

However, not recommended for quality assurance.

## 🤝 Contributing

Pull requests and issue reports welcome!

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

## 💬 Support

- **Bug Reports**: [GitHub Issues](https://github.com/cardene/grove/issues)
- **Feature Requests**: [GitHub Issues](https://github.com/cardene/grove/issues)
- **Questions/Discussion**: [GitHub Discussions](https://github.com/cardene/grove/discussions)

## 🙏 Acknowledgements

Grove is built on the work of these projects and individuals:

**Spec Kit** (GitHub):
- [Den Delimarsky](https://github.com/localden)
- [John Lam](https://github.com/jflam)

**Grove Extensions**:
- [Cardene](https://github.com/cardene)

**TDD Methodology**:
- [t-wada](https://github.com/twada) - Test-Driven Development

Thank you to all contributors.

## 📄 License

Released under the MIT License. See [LICENSE](./LICENSE) for details.

---

<p align="center">
    <strong>🌳 Grove - High-Quality Development Toolkit for the AI Era</strong><br>
    Built with ❤️ by the Grove community
</p>
