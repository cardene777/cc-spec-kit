# Local testing script for spec-kit-ex
# Usage: .\scripts\powershell\test-local.ps1 [project-name] [ai] [script-type] [lang]
# Example: .\scripts\powershell\test-local.ps1 test-claude claude ps ja

param(
    [string]$ProjectName = "test-project",
    [string]$AI = "claude",
    [string]$ScriptType = "ps",
    [string]$Lang = "ja"
)

$ErrorActionPreference = "Stop"

# Save current directory (where user wants to create project)
$OriginalDir = (Get-Location).Path

# Get repository root
$RepoRoot = (Get-Item $PSScriptRoot).Parent.Parent.FullName
Set-Location $RepoRoot

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Grove CLI Local Test" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Project Name: $ProjectName"
Write-Host "AI Agent:     $AI"
Write-Host "Script Type:  $ScriptType"
Write-Host "Language:     $Lang"
Write-Host "==========================================" -ForegroundColor Cyan

# Create temporary installation prefix
$TempPrefix = New-TemporaryFile | ForEach-Object { Remove-Item $_; New-Item -ItemType Directory -Path $_ }
$ShareDir = Join-Path $TempPrefix "share\grove-cli"

Write-Host "Setting up test environment..."
New-Item -ItemType Directory -Path $ShareDir -Force | Out-Null

# Copy templates, scripts, and memory to simulate installed package
if (Test-Path "templates") {
    Copy-Item -Path "templates" -Destination $ShareDir -Recurse -Force
    Write-Host "✓ Copied templates" -ForegroundColor Green
}

if (Test-Path "scripts") {
    Copy-Item -Path "scripts" -Destination $ShareDir -Recurse -Force
    Write-Host "✓ Copied scripts" -ForegroundColor Green
}

if (Test-Path "memory") {
    Copy-Item -Path "memory" -Destination $ShareDir -Recurse -Force
    Write-Host "✓ Copied memory" -ForegroundColor Green
}

Write-Host ""
Write-Host "Running: grove init $ProjectName --ai $AI --script $ScriptType --lang $Lang"
Write-Host ""

# Determine target directory
if ($ProjectName -eq ".") {
    $TargetDir = $OriginalDir
    $InitFlags = "--here"
} else {
    $TargetDir = Join-Path $OriginalDir $ProjectName
    $InitFlags = ""
}

# Set PYTHONPATH and run grove CLI with simulated sys.prefix using uv
$env:PYTHONPATH = "$RepoRoot\src;$env:PYTHONPATH"
Set-Location $RepoRoot

$PythonCode = @"
import sys
import os
from pathlib import Path
import shutil
sys.prefix = '$($TempPrefix.FullName.Replace('\', '/'))'
from grove_cli import app
import grove_cli

# Change to appropriate directory before running app
if '$ProjectName' == '.':
    os.chdir('$($TargetDir.Replace('\', '/'))')
else:
    os.chdir('$($OriginalDir.Replace('\', '/'))')

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
"@

if ($InitFlags) {
    uv run python -c $PythonCode init $InitFlags --ai $AI --script $ScriptType --lang $Lang
} else {
    uv run python -c $PythonCode init $ProjectName --ai $AI --script $ScriptType --lang $Lang
}

# Cleanup
Remove-Item -Path $TempPrefix -Recurse -Force

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✓ Test completed successfully!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
if ($ProjectName -eq ".") {
    Write-Host "Project initialized in: $OriginalDir"
    Write-Host ""
    Write-Host "Verify the installation:"
    Write-Host "  dir $OriginalDir\.grove\"
} else {
    Write-Host "Test project created at: $TargetDir"
    Write-Host ""
    Write-Host "Verify the installation:"
    Write-Host "  dir $TargetDir\.grove\"
}
Write-Host ""
