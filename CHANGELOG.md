# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to Grove CLI are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2025-12-18

### Added

- Complete rebrand from Spec Kit EX to Grove (`grove-cli`, `grove` command, `.grove/` directory)
- Constitution sync to `.claude/rules/constitution.md` for Claude Code rule enforcement
- TDD workflow integration (t-wada method) in `/grove.implement` command
- Background parallel execution for Self Review (Claude Code support)
- Autonomous verification agent with 8-point quality checklist
- Auto-Fix functionality for failed tasks (TDD approach, max 3 attempts)
- Cross Review support for multi-AI verification
- Self Review reports in `reports/self-review/task-{ID}.md`
- Design step for UI/UX specifications via `/grove.design` command
- Multi-language support (Japanese/English) with `--lang` flag
- Language-specific templates (constitution, spec) and common templates (plan, tasks, checklist)
- Template `enabled` field for customization control
- Read tool for file existence checking (eliminates confirmation prompts)
- 12 slash commands: constitution, specify, clarify, design, plan, tasks, implement, review, fix, analyze, checklist, taskstoissues

### Breaking Changes

For users migrating from Spec Kit EX:

- Uninstall old package: `uv tool uninstall specify-ex-cli`
- Install new package: `uv tool install grove-cli`
- Update command: `specify-ex` → `grove`
- Rename directory: `.specify/` → `.grove/`
- Update slash commands: `/speckit.*` → `/grove.*``