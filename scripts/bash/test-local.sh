#!/usr/bin/env bash
# Local testing script for Grove
# Usage: ./scripts/bash/test-local.sh [project-name] [ai] [script-type] [lang]
# Example: ./scripts/bash/test-local.sh test-claude claude sh ja

set -e

# Parse arguments
PROJECT_NAME="${1:-test-project}"
AI="${2:-claude}"
SCRIPT_TYPE="${3:-sh}"
LANG="${4:-ja}"

# Save current directory (where user wants to create project)
ORIGINAL_DIR="$(pwd)"

# Get repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

echo "=========================================="
echo "Grove CLI Local Test"
echo "=========================================="
echo "Project Name: $PROJECT_NAME"
echo "AI Agent:     $AI"
echo "Script Type:  $SCRIPT_TYPE"
echo "Language:     $LANG"
echo "=========================================="

# Create temporary installation prefix
TEMP_PREFIX=$(mktemp -d)
SHARE_DIR="$TEMP_PREFIX/share/grove-cli"

echo "Setting up test environment..."
mkdir -p "$SHARE_DIR"

# Copy templates, scripts, and memory to simulate installed package
if [ -d "templates" ]; then
    cp -r templates "$SHARE_DIR/"
    echo "✓ Copied templates"
fi

if [ -d "scripts" ]; then
    cp -r scripts "$SHARE_DIR/"
    echo "✓ Copied scripts"
fi

if [ -d "memory" ]; then
    cp -r memory "$SHARE_DIR/"
    echo "✓ Copied memory"
fi

echo ""
echo "Running: grove init $PROJECT_NAME --ai $AI --script $SCRIPT_TYPE --lang $LANG"
echo ""

# Determine target directory
if [ "$PROJECT_NAME" = "." ]; then
    TARGET_DIR="$ORIGINAL_DIR"
    INIT_FLAGS="--here"
else
    TARGET_DIR="$ORIGINAL_DIR/$PROJECT_NAME"
    INIT_FLAGS=""
fi

# Set PYTHONPATH and run grove CLI with simulated sys.prefix using uv
export PYTHONPATH="$REPO_ROOT/src:$PYTHONPATH"
cd "$REPO_ROOT"
uv run python -c "
import sys
import os
from pathlib import Path
import shutil
sys.prefix = '$TEMP_PREFIX'
from grove_cli import app
import grove_cli

# Change to appropriate directory before running app
if '$PROJECT_NAME' == '.':
    os.chdir('$TARGET_DIR')
else:
    os.chdir('$ORIGINAL_DIR')

# Mock download_and_extract_template to install from local templates
def mock_download(project_path, ai_assistant, script_type, is_current_dir=False, **kwargs):
    # Define agent-specific directory structure (matching create-release-packages.sh)
    agent_config = {
        'claude': {'folder': '.claude', 'commands_dir': 'commands'},
        'codex': {'folder': '.codex', 'commands_dir': 'prompts'},
        'gemini': {'folder': '.gemini', 'commands_dir': 'commands'},
        'copilot': {'folder': '.github/agents', 'commands_dir': '../prompts'},
        'cursor-agent': {'folder': '.cursor', 'commands_dir': 'commands'},
        'qwen': {'folder': '.qwen', 'commands_dir': 'commands'},
        'opencode': {'folder': '.opencode', 'commands_dir': 'command'},
        'windsurf': {'folder': '.windsurf', 'commands_dir': 'workflows'},
        'kilocode': {'folder': '.kilocode', 'commands_dir': 'workflows'},
        'auggie': {'folder': '.augment', 'commands_dir': 'commands'},
        'roo': {'folder': '.roo', 'commands_dir': 'commands'},
        'codebuddy': {'folder': '.codebuddy', 'commands_dir': 'commands'},
        'qoder': {'folder': '.qoder', 'commands_dir': 'commands'},
        'amp': {'folder': '.agents', 'commands_dir': 'commands'},
        'shai': {'folder': '.shai', 'commands_dir': 'commands'},
        'q': {'folder': '.amazonq', 'commands_dir': 'prompts'},
        'bob': {'folder': '.bob', 'commands_dir': 'commands'},
    }

    config = agent_config.get(ai_assistant, {'folder': f'.{ai_assistant}', 'commands_dir': 'commands'})
    agent_folder = config['folder']
    commands_dir = config['commands_dir']

    agent_src = Path(sys.prefix) / 'share' / 'grove-cli' / 'templates' / 'agents' / ai_assistant

    # Copy agent-specific files if they exist
    if agent_src.exists():
        for item in agent_src.iterdir():
            if item.name in ['CLAUDE.md', 'CODEX.md', 'GEMINI.md', 'QWEN.md']:
                # Copy to project root
                shutil.copy2(item, project_path / item.name)
            elif item.is_dir() and item.name in ['commands', 'agents', 'rules']:
                # Copy to agent folder
                dest_dir = project_path / agent_folder / item.name
                dest_dir.parent.mkdir(parents=True, exist_ok=True)
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                shutil.copytree(item, dest_dir)

    # Copy shared commands (grove.*.md) - always do this
    commands_src = Path(sys.prefix) / 'share' / 'grove-cli' / 'templates' / 'agents' / 'commands'
    if commands_src.exists():
        commands_dest = project_path / agent_folder / commands_dir
        commands_dest.mkdir(parents=True, exist_ok=True)
        for cmd_file in commands_src.glob('*.md'):
            shutil.copy2(cmd_file, commands_dest / f'grove.{cmd_file.name}')

    # Copy AGENTS.md from templates/agents/ to project root
    agents_md = Path(sys.prefix) / 'share' / 'grove-cli' / 'templates' / 'agents' / 'AGENTS.md'
    if agents_md.exists():
        shutil.copy2(agents_md, project_path / 'AGENTS.md')

    # Copy vscode-settings.json for copilot
    if ai_assistant == 'copilot':
        vscode_settings = Path(sys.prefix) / 'share' / 'grove-cli' / 'templates' / 'vscode-settings.json'
        if vscode_settings.exists():
            vscode_dir = project_path / '.vscode'
            vscode_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(vscode_settings, vscode_dir / 'settings.json')

    return project_path

grove_cli.download_and_extract_template = mock_download

app()
" init ${INIT_FLAGS:-$PROJECT_NAME} --ai "$AI" --script "$SCRIPT_TYPE" --lang "$LANG"

# Cleanup
rm -rf "$TEMP_PREFIX"

echo ""
echo "=========================================="
echo "✓ Test completed successfully!"
echo "=========================================="
if [ "$PROJECT_NAME" = "." ]; then
    echo "Project initialized in: $ORIGINAL_DIR"
    echo ""
    echo "Verify the installation:"
    echo "  ls -la $ORIGINAL_DIR/.grove/"
else
    echo "Test project created at: $TARGET_DIR"
    echo ""
    echo "Verify the installation:"
    echo "  ls -la $TARGET_DIR/.grove/"
fi
echo ""
