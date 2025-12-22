# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to Grove CLI are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2025-12-23

### Added

- Self Review report templates externalized to `templates/` directory
  - `phase-self-review-template.md` for phase-level reports
  - `final-self-review-summary-template.md` for final summary reports
- Command handoffs documentation in `templates/agents/AGENTS.md`
  - Explains YAML frontmatter `handoffs` system for recommended next steps
- Command file format standards in root `AGENTS.md`
  - Outlines numbered list structure with hyphen sub-steps
  - Documents YAML frontmatter usage (handoffs, scripts)

### Changed

- **Command file format standardization** across all 8 command files:
  - Unified outline format: numbered steps (1., 2., 3.) with hyphen sub-steps (-)
  - Removed bold formatting in outlines for consistency
  - Replaced explicit "Next Steps" sections with YAML `handoffs` frontmatter
  - Affected files: `constitution.md`, `specify.md`, `design.md`, `plan.md`, `tasks.md`, `clarify.md`, `review.md`, `fix.md`
- **implement.md major simplification** (830 lines → 559 lines, 33% reduction):
  - Removed verbose Python code examples, replaced with concise bullet points
  - Externalized report templates to separate files
  - Simplified phase summary display instructions
  - Compressed CRITICAL NOTES section into Guidelines
- Updated `design.md` with comprehensive directory structure
  - Added ai/ subdirectory for decision logs and rejected options
  - Documented 2-level deep structure (context/, principles/, foundations/, components/, patterns/, flows/, ai/, tokens/, references/)

## [0.1.3] - 2025-12-22

### Added

- Automatic constitution sync to `.claude/rules/constitution.md` in prerequisite scripts
- CRITICAL enforcement section to AGENTS.md for workflow compliance
- Documentation section to task format (mandatory for all tasks)
- Git repository verification in AGENTS.md

### Changed

- Converted all command files to spec-kit format (single-line script execution)
- Simplified AGENTS.md (433 lines reduction)
- Optimized implement.md Final Summary display (reduced verbosity)
- Unified task format definitions in tasks.md
- Improved workflow enforcement and prerequisite validation

## [0.1.2] - 2025-12-21

### Added

- Documentation agent (`documentation.md`) for automated documentation generation
  - Runs in background alongside verification agent
  - Generates/updates docs in `.grove/docs/` per task
  - Integrated into implement.md workflow

### Fixed

- Replace Japanese text with English in implement.md for better cross-agent compatibility
- Improve release package creation script robustness

### Changed

- Enhanced specify.md, tasks.md, plan.md with documentation workflow integration
- Updated design.md with additional UI/UX specification requirements

## [0.1.1] - 2025-12-21

### Fixed

- Language template organization during `grove init`
  - Selected language files (constitution-template.md, spec-template.md) are now correctly placed in `.grove/templates/` directory
  - Removed duplicate language subdirectories (`.grove/templates/en/`, `.grove/templates/ja/`)
  - Removed duplicate template files that were created in both root and subdirectories
- Template confirmation options now use English-only format for better cross-agent compatibility

## [0.1.0] - 2025-12-21

### Added

- Initial PyPI release (https://pypi.org/project/grove-cli/)
- Enhanced AGENTS.md with comprehensive Grove workflow documentation (345 lines)
  - Detailed 3-layer quality assurance explanation (TDD / Self Review / Cross Review)
  - Background execution rules for Verification Agent (Claude Code only)
  - Task status management guidelines
  - Error handling procedures
  - Best practices and troubleshooting guide
- CLAUDE.md for Claude Code agent configuration

### Fixed

- GitHub repository URL in code (github/grove → cardene777/grove)
- GitHub username inconsistencies across all documentation (cardene → cardene777)
- LICENSE file to properly credit original Spec Kit authors (GitHub, Inc.)
- Environment variable name in documentation (SPEC_KIT_SRC → GROVE_SRC)
- Directory name issue (removed trailing space from "memory " → "memory")
- Language template organization during `grove init`
  - Selected language files (constitution-template.md, spec-template.md) are now correctly placed in `.grove/templates/` directory
  - Removed duplicate language subdirectories (`.grove/templates/en/`, `.grove/templates/ja/`)
  - Removed duplicate template files that were created in both root and subdirectories
- Template confirmation options now use English-only format for better cross-agent compatibility

### Changed

- Build configuration to exclude development files (.claude/, .github/, .vscode/, tests/)
- Package metadata for PyPI publication
- Version bump from 0.0.1 to 0.1.0 for initial public release

### Removed

- REFERENCE.md (consolidated into other documentation)

## [0.0.1] - 2025-12-18

### Added

- Complete rebrand from Spec Kit to Grove (`grove-cli`, `grove` command, `.grove/` directory)
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

For users migrating from original Spec Kit:

- Install new package: `pip install grove-cli` or `uv tool install grove-cli`
- Update command: Use `grove` command
- Use `.grove/` directory (not `.spec/` or other variants)
- Update slash commands: `/grove.*` (for Claude Code) or `/prompts:*` (for Codex)

### Acknowledgements

Grove is built on the foundation of [Spec Kit](https://github.com/microsoft/speckit) by GitHub, Inc.
Original authors: [Den Delimarsky](https://github.com/localden) and [John Lam](https://github.com/jflam).

Grove extends Spec Kit with:
- AI-powered quality assurance (TDD + Self Review + Cross Review)
- Background execution and verification agents
- Multi-language support
- Enhanced workflow automation

See [NOTICE](./NOTICE) for complete attribution and licensing information.
