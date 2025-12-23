# Release Process

This document outlines the release process for Grove CLI.

## Prerequisites

- Ensure you have `twine` installed: `uv pip install twine`
- Ensure you have `gh` CLI installed and authenticated
- Ensure you have PyPI and TestPyPI credentials configured in `~/.pypirc`

## Release Steps

### 1. Update Version

Edit `pyproject.toml`:

```toml
version = "0.1.X"  # Update to new version
```

### 2. Update CHANGELOG.md

Add new version section with changes:

```markdown
## [0.1.X] - YYYY-MM-DD

### Added
- Feature descriptions

### Changed
- Change descriptions

### Fixed
- Bug fix descriptions
```

### 3. Build Package

```bash
# Clean old builds
rm -rf dist/

# Build new package
uv build
```

This creates:
- `dist/grove_cli-0.1.X-py3-none-any.whl`
- `dist/grove_cli-0.1.X.tar.gz`

### 4. Upload to TestPyPI (Optional but Recommended)

```bash
.venv/bin/twine upload --repository testpypi dist/*
```

View at: https://test.pypi.org/project/grove-cli/

Test installation:
```bash
uv tool install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ grove-cli
```

### 5. Upload to Production PyPI

```bash
.venv/bin/twine upload dist/*
```

View at: https://pypi.org/project/grove-cli/

### 6. Commit and Push

```bash
# Stage changes
git add pyproject.toml CHANGELOG.md

# Commit (do NOT include Claude Code attribution)
git commit -m "Release v0.1.X

- Feature 1
- Feature 2
- Feature 3"

# Push to grove branch
git push origin grove
```

### 7. Create Git Tag

```bash
git tag v0.1.X
git push origin v0.1.X
```

### 8. Create GitHub Release

```bash
gh release create v0.1.X \
  --title "v0.1.X" \
  --notes "$(cat <<'EOF'
## What's Changed

### Added
- Feature descriptions

### Changed
- Change descriptions

### Fixed
- Bug fix descriptions

**Full Changelog**: https://github.com/cardene777/grove/blob/main/CHANGELOG.md#01X---YYYY-MM-DD
EOF
)"
```

### 9. Create and Upload Template Packages

**IMPORTANT**: This step is **REQUIRED** for `grove init` to work. Without template packages, users cannot initialize Grove projects.

```bash
# Create template packages for all AI agents
bash .github/workflows/scripts/create-release-packages.sh v0.1.X

# Upload all packages to GitHub release
gh release upload v0.1.X .genreleases/*.zip
```

This creates 34 template packages (17 agents × 2 script types):
- claude, gemini, copilot, cursor-agent, qwen, opencode, windsurf, codex, kilocode, auggie, roo, codebuddy, amp, shai, q, bob, qoder
- sh (bash scripts), ps (PowerShell scripts)

### 10. Verify Release

1. Check GitHub release: https://github.com/cardene777/grove/releases
2. Check PyPI: https://pypi.org/project/grove-cli/
3. Test installation:
   ```bash
   uv tool install grove-cli
   grove --version
   ```

## Important Notes

### Version Numbering

- Follow Semantic Versioning: `MAJOR.MINOR.PATCH`
- Increment PATCH for bug fixes: `0.1.4` → `0.1.5`
- Increment MINOR for new features: `0.1.5` → `0.2.0`
- Increment MAJOR for breaking changes: `0.2.0` → `1.0.0`

### PyPI vs TestPyPI

- **TestPyPI** and **Production PyPI** are completely separate
- Version numbers used in TestPyPI do NOT affect Production PyPI
- You can use the same version number on both (recommended workflow)

### GitHub Release Requirements

Grove CLI uses GitHub API to fetch release information:
- `src/grove_cli/__init__.py` calls `https://api.github.com/repos/cardene777/grove/releases/latest`
- GitHub releases MUST be created for each version
- Tags alone are NOT sufficient

### Commit Message Guidelines

- Do NOT include Claude Code attribution in commit messages
- Keep messages concise and descriptive
- Use bullet points for multiple changes

### Branch Strategy

- Always work on `grove` branch
- Merge to `main` only for releases (if needed)
- Push tags from the release branch

### Codex Commands

Starting from v0.1.6, Codex commands are installed globally:

- **Location**: `~/.codex/prompts/` (not project-local `.codex/`)
- **Update Command**: `grove update-commands` updates all Codex commands
- **Version Check**: `grove version` shows installed Codex commands version
- **No Migration Needed**: Old `.codex/` directories in projects are ignored

Users with older versions (< 0.1.6) will automatically get global installation on next `grove init`.

## Troubleshooting

### "Version already exists" Error

If you accidentally upload a version to PyPI/TestPyPI, you cannot reuse that version number. Increment to the next version.

### GitHub Release Not Found

Ensure the tag was pushed:
```bash
git push origin v0.1.X
```

Then create the release:
```bash
gh release create v0.1.X --title "v0.1.X" --notes "Release notes..."
```

### Package Not Including Templates

Check `pyproject.toml` shared-data configuration:
```toml
[tool.hatch.build.targets.wheel.shared-data]
"templates" = "share/grove-cli/templates"
```

Verify in built package:
```bash
unzip -l dist/grove_cli-0.1.X-py3-none-any.whl | grep templates
```
