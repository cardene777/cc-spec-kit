#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
# ]
# ///
"""
Grove CLI - Setup tool for Grove projects

Usage:
    uvx specify-cli.py init <project-name>
    uvx specify-cli.py init .
    uvx specify-cli.py init --here

Or install globally:
    uv tool install --from specify-cli.py specify-cli
    specify init <project-name>
    specify init .
    specify init --here
"""

import os
import subprocess
import sys
import zipfile
import tempfile
import shutil
import shlex
import json
from pathlib import Path
from typing import List, Optional, Tuple

import typer
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich.tree import Tree
from typer.core import TyperGroup

# For cross-platform keyboard input
import readchar
import ssl
import truststore
import yaml
from datetime import datetime, timezone

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ssl_context)

# Version
__version__ = "0.1.1"

# =============================================================================
# AI Agent Support
# =============================================================================

SUPPORTED_AI_AGENTS = ["claude", "codex"]

# =============================================================================
# Language Support (ja, en)
# =============================================================================

SUPPORTED_LANGUAGES = ["ja", "en"]

LANGUAGE_NAMES = {
    "ja": "日本語 (Japanese)",
    "en": "English",
}

# Global language setting (default to English for compatibility with grove)
_current_lang = "en"

def get_lang() -> str:
    """Get current language setting."""
    return _current_lang

def set_lang(lang: str) -> None:
    """Set current language."""
    global _current_lang
    if lang in SUPPORTED_LANGUAGES:
        _current_lang = lang

# Internationalization dictionary
I18N = {
    "ja": {
        "tagline": "Grove - 仕様駆動開発ツールキット",
        "banner_subtitle": "拡張版 - 多言語対応",
        "help_usage": "'grove --help' で使用方法を表示",
        # init command messages
        "selected_language": "選択された言語",
        "selected_ai": "選択されたAIアシスタント",
        "selected_script": "選択されたスクリプトタイプ",
        "warning_not_empty": "警告: カレントディレクトリは空ではありません",
        "items_found": "個のアイテムが存在します",
        "template_merge_warning": "テンプレートファイルは既存のコンテンツとマージされ、既存のファイルを上書きする可能性があります",
        "force_skipping_confirmation": "--force が指定されました: 確認をスキップしてマージを続行します",
        "confirm_continue": "続行しますか?",
        "operation_cancelled": "操作がキャンセルされました",
        "error_unsupported_language": "エラー: サポートされていない言語",
        "supported_languages": "サポート対象",
        "error_must_specify_project": "エラー: プロジェクト名を指定するか、カレントディレクトリには '.' を使用するか、--here フラグを使用してください",
        # Project setup messages
        "project_ready": "プロジェクトの準備が完了しました。",
        "agent_folder_security": "エージェントフォルダーのセキュリティ",
        "agent_folder_security_message": "一部のエージェントは、プロジェクト内のエージェントフォルダーに認証情報、認証トークン、またはその他の識別情報や個人的な成果物を保存する場合があります。\n誤って認証情報が漏洩するのを防ぐため、{folder}（またはその一部）を.gitignoreに追加することを検討してください。",
        "next_steps": "次のステップ",
        "next_steps_already_in_dir": "すでにプロジェクトディレクトリにいます！",
        "next_steps_start_using": "AIエージェントでスラッシュコマンドを使い始める：",
        "next_steps_constitution": "プロジェクトの原則を確立",
        "next_steps_specify": "ベースライン仕様を作成",
        "next_steps_design": "デザイン仕様を作成（オプション）",
        "next_steps_plan": "実装計画を作成",
        "next_steps_tasks": "実行可能なタスクを生成",
        "next_steps_implement": "実装を実行",
        "enhancement_commands": "拡張コマンド",
        "enhancement_commands_desc": "仕様に使用できるオプションのコマンド（品質と信頼性を向上）",
        "enhancement_clarify": "計画前に曖昧な領域をデリスクするための構造化された質問（使用する場合は /grove.plan の前に実行）",
        "enhancement_analyze": "成果物間の整合性と一貫性レポート（/grove.tasks の後、/grove.implement の前）",
        "enhancement_checklist": "要件の完全性、明確性、一貫性を検証する品質チェックリストを生成（/grove.plan の後）",
        "enhancement_review": "実装の品質検証とクロスレビューを実行（/grove.implement の後）",
        "enhancement_fix": "クロスレビューで検出された問題を修正（/grove.review の後）",
        # StepTracker labels
        "tracker_title": "Grove プロジェクトを初期化",
        "tracker_precheck": "必要なツールをチェック",
        "tracker_ai_select": "AIアシスタントを選択",
        "tracker_script_select": "スクリプトタイプを選択",
        "tracker_fetch": "最新リリースを取得",
        "tracker_download": "テンプレートをダウンロード",
        "tracker_extract": "テンプレートを展開",
        "tracker_archive": "アーカイブ内容",
        "tracker_extract_summary": "展開サマリー",
        "tracker_chmod": "スクリプトに実行権限を設定",
        "tracker_cleanup": "クリーンアップ",
        "tracker_git_init": "Gitリポジトリを初期化",
        "tracker_finalize": "最終処理",
        "tracker_install_templates": "言語固有のテンプレートをインストール",
    },
    "en": {
        "tagline": "Grove - Spec-Driven Development Toolkit",
        "banner_subtitle": "Extended version with multi-language support",
        "help_usage": "Run 'grove --help' for usage information",
        # init command messages
        "selected_language": "Selected language",
        "selected_ai": "Selected AI assistant",
        "selected_script": "Selected script type",
        "warning_not_empty": "Warning: Current directory is not empty",
        "items_found": "items",
        "template_merge_warning": "Template files will be merged with existing content and may overwrite existing files",
        "force_skipping_confirmation": "--force supplied: skipping confirmation and proceeding with merge",
        "confirm_continue": "Do you want to continue?",
        "operation_cancelled": "Operation cancelled",
        "error_unsupported_language": "Error: Unsupported language",
        "supported_languages": "Supported",
        "error_must_specify_project": "Error: Must specify either a project name, use '.' for current directory, or use --here flag",
        # Project setup messages
        "project_ready": "Project ready.",
        "agent_folder_security": "Agent Folder Security",
        "agent_folder_security_message": "Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder within your project.\nConsider adding {folder} (or parts of it) to .gitignore to prevent accidental credential leakage.",
        "next_steps": "Next Steps",
        "next_steps_already_in_dir": "You're already in the project directory!",
        "next_steps_start_using": "Start using slash commands with your AI agent:",
        "next_steps_constitution": "Establish project principles",
        "next_steps_specify": "Create baseline specification",
        "next_steps_design": "Create design specification (optional)",
        "next_steps_plan": "Create implementation plan",
        "next_steps_tasks": "Generate actionable tasks",
        "next_steps_implement": "Execute implementation",
        "enhancement_commands": "Enhancement Commands",
        "enhancement_commands_desc": "Optional commands that you can use for your specs (improve quality & confidence)",
        "enhancement_clarify": "Ask structured questions to de-risk ambiguous areas before planning (run before /grove.plan if used)",
        "enhancement_analyze": "Cross-artifact consistency & alignment report (after /grove.tasks, before /grove.implement)",
        "enhancement_checklist": "Generate quality checklists to validate requirements completeness, clarity, and consistency (after /grove.plan)",
        "enhancement_review": "Execute quality verification and cross-review of implementation (after /grove.implement)",
        "enhancement_fix": "Fix issues detected in cross-review (after /grove.review)",
        # StepTracker labels
        "tracker_title": "Initialize Grove Project",
        "tracker_precheck": "Check required tools",
        "tracker_ai_select": "Select AI assistant",
        "tracker_script_select": "Select script type",
        "tracker_fetch": "Fetch latest release",
        "tracker_download": "Download template",
        "tracker_extract": "Extract template",
        "tracker_archive": "Archive contents",
        "tracker_extract_summary": "Extraction summary",
        "tracker_chmod": "Set script permissions recursively",
        "tracker_cleanup": "Cleanup",
        "tracker_git_init": "Initialize git repository",
        "tracker_finalize": "Finalize",
        "tracker_install_templates": "Installing language-specific templates",
    },
}

def t(key: str) -> str:
    """Get translated string for current language."""
    return I18N.get(_current_lang, I18N["en"]).get(key, key)

# =============================================================================
# Project Configuration Management
# =============================================================================

def load_project_config(project_dir: Path) -> dict:
    """Load project configuration from .grove/memory/config.json

    Args:
        project_dir: Project root directory

    Returns:
        Configuration dictionary (returns default if file doesn't exist)
    """
    config_file = project_dir / ".grove" / "memory" / "config.json"
    if config_file.exists():
        return json.loads(config_file.read_text())
    return {"language": "en", "version": "0.2.0"}

def save_project_config(project_dir: Path, config: dict) -> None:
    """Save project configuration to .grove/memory/config.json

    Args:
        project_dir: Project root directory
        config: Configuration dictionary to save
    """
    config_dir = project_dir / ".grove" / "memory"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.json"
    config["version"] = "0.2.0"
    if "created_at" not in config:
        config["created_at"] = datetime.now(timezone.utc).isoformat()
    config_file.write_text(json.dumps(config, indent=2, ensure_ascii=False))

def get_project_language(project_dir: Path) -> str:
    """Get language setting from project config

    Args:
        project_dir: Project root directory

    Returns:
        Language code ("ja" or "en")
    """
    config = load_project_config(project_dir)
    return config.get("language", "en")

def is_claude_code_environment(ai_param: str = None) -> bool:
    """
    Detect Claude Code environment.

    Detection method:
    1. Check --ai parameter (if ai_param is None or "claude" → Claude Code)
    2. (Optional) Check CLAUDE_CODE_VERSION environment variable

    Args:
        ai_param: AI agent parameter from command line

    Returns:
        True if Claude Code environment detected, False otherwise
    """
    # --ai parameter check
    if ai_param is None or ai_param == "claude":
        return True

    # Environment variable check (optional)
    has_env_var = os.getenv("CLAUDE_CODE_VERSION") is not None

    return has_env_var

# =============================================================================
# Template Loading
# =============================================================================

def parse_yaml_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content

    Args:
        content: Markdown file content

    Returns:
        Tuple of (frontmatter_dict, markdown_body)
    """
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    frontmatter = yaml.safe_load(parts[1])
    body = parts[2].strip()
    return frontmatter or {}, body

def get_templates_root() -> Path:
    """Get templates root directory (dev or installed)

    Returns:
        Path to templates root directory

    Raises:
        RuntimeError: If templates directory not found
    """
    # Try installed location
    installed_path = Path(sys.prefix) / "share" / "grove-cli" / "templates"
    if installed_path.exists():
        return installed_path

    # Try development location
    dev_path = Path(__file__).parent.parent.parent / "templates"
    if dev_path.exists():
        return dev_path

    raise RuntimeError("Templates directory not found")

def load_template_if_enabled(command: str, project_dir: Path) -> Optional[str]:
    """Load template if enabled flag is true

    Args:
        command: Command name (constitution, specify, plan, tasks)
        project_dir: Project root directory

    Returns:
        Template content (without frontmatter) if enabled, None otherwise
    """
    # Get language setting
    lang = get_project_language(project_dir)

    # Find template file
    templates_root = get_templates_root()
    template_file = templates_root / lang / f"{command}-template.md"

    if not template_file.exists():
        return None

    # Parse frontmatter
    content = template_file.read_text(encoding="utf-8")
    frontmatter, body = parse_yaml_frontmatter(content)

    # Check enabled flag
    if frontmatter.get("enabled", False):
        return body

    return None

# =============================================================================
# Agent Configuration
# =============================================================================

AGENT_CONFIG = {
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github/",
        "install_url": None,  # IDE-based, no CLI check needed
        "requires_cli": False,
    },
    "claude": {
        "name": "Claude Code",
        "folder": ".claude/",
        "install_url": "https://docs.anthropic.com/en/docs/claude-code/setup",
        "requires_cli": True,
    },
    "gemini": {
        "name": "Gemini CLI",
        "folder": ".gemini/",
        "install_url": "https://github.com/google-gemini/gemini-cli",
        "requires_cli": True,
    },
    "cursor-agent": {
        "name": "Cursor",
        "folder": ".cursor/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "qwen": {
        "name": "Qwen Code",
        "folder": ".qwen/",
        "install_url": "https://github.com/QwenLM/qwen-code",
        "requires_cli": True,
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode/",
        "install_url": "https://opencode.ai",
        "requires_cli": True,
    },
    "codex": {
        "name": "Codex CLI",
        "folder": ".codex/",
        "install_url": "https://github.com/openai/codex",
        "requires_cli": True,
    },
    "windsurf": {
        "name": "Windsurf",
        "folder": ".windsurf/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "kilocode": {
        "name": "Kilo Code",
        "folder": ".kilocode/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "auggie": {
        "name": "Auggie CLI",
        "folder": ".augment/",
        "install_url": "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli",
        "requires_cli": True,
    },
    "codebuddy": {
        "name": "CodeBuddy",
        "folder": ".codebuddy/",
        "install_url": "https://www.codebuddy.ai/cli",
        "requires_cli": True,
    },
    "qoder": {
        "name": "Qoder CLI",
        "folder": ".qoder/",
        "install_url": "https://qoder.com/cli",
        "requires_cli": True,
    },
    "roo": {
        "name": "Roo Code",
        "folder": ".roo/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "q": {
        "name": "Amazon Q Developer CLI",
        "folder": ".amazonq/",
        "install_url": "https://aws.amazon.com/developer/learning/q-developer-cli/",
        "requires_cli": True,
    },
    "amp": {
        "name": "Amp",
        "folder": ".agents/",
        "install_url": "https://ampcode.com/manual#install",
        "requires_cli": True,
    },
    "shai": {
        "name": "SHAI",
        "folder": ".shai/",
        "install_url": "https://github.com/ovh/shai",
        "requires_cli": True,
    },
    "bob": {
        "name": "IBM Bob",
        "folder": ".bob/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
}

# =============================================================================
# Agent Installation Helper Functions
# =============================================================================

def install_agent_config(ai: str, project_dir: Path) -> None:
    """Install agent configuration file (CLAUDE.md or AGENTS.md)

    Args:
        ai: Agent name (claude, gemini, copilot, etc.)
        project_dir: Project root directory
    """
    templates_root = get_templates_root()
    agent_config = AGENT_CONFIG[ai]

    # Determine source template (new paths)
    if ai == "claude":
        source_file = templates_root / "agents" / "claude" / "CLAUDE.md"
        dest_file = project_dir / agent_config["folder"] / "CLAUDE.md"
    else:
        source_file = templates_root / "agents" / "AGENTS.md"
        dest_file = project_dir / agent_config["folder"] / "AGENTS.md"

    if not source_file.exists():
        return

    # Copy to destination
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, dest_file)

def install_claude_code_templates(project_dir: Path) -> None:
    """Install Claude Code templates (commands, skills, agents, rules) to .claude/ directory

    This copies templates from templates/agents/claude/ to user project's .claude/ directory.

    Directory structure created:
        project-root/
        ├── CLAUDE.md          # Agent configuration (copied to project root)
        └── .claude/
            ├── commands/          # Slash Command templates (no .md extension)
            │   ├── constitution
            │   ├── specify
            │   ├── design
            │   ├── plan
            │   ├── tasks
            │   ├── sync
            │   └── implement
            ├── skills/            # Skill templates (English)
            │   ├── constitution-knowledge/
            │   │   └── SKILL.md
            │   ├── specify-knowledge/
            │   │   └── SKILL.md
            │   ├── design-creator/
            │   │   └── SKILL.md
            │   ├── plan-knowledge/
            │   │   └── SKILL.md
            │   ├── tasks-knowledge/
            │   │   └── SKILL.md
            │   ├── sync-knowledge/
            │   │   └── SKILL.md
            │   ├── implement-knowledge/
            │   │   └── SKILL.md
            │   └── load-project-context/
            │       └── SKILL.md
            ├── agents/            # Subagent templates
            │   └── executor.md
            └── rules/             # Claude Code rules
                └── constitution.md

    Args:
        project_dir: Project root directory
    """
    templates_root = get_templates_root()
    claude_templates = templates_root / "agents" / "claude"

    if not claude_templates.exists():
        console.print(f"[yellow]Warning:[/yellow] Claude Code templates not found at {claude_templates}")
        return

    claude_dir = project_dir / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy CLAUDE.md to project root
    claude_md_src = claude_templates / "CLAUDE.md"
    if claude_md_src.exists():
        shutil.copy2(claude_md_src, project_dir / "CLAUDE.md")

    # 2. Copy Slash Commands (remove .md extension for Claude Code compatibility)
    # Commands are shared across all agents in templates/agents/commands/
    commands_src = templates_root / "agents" / "commands"
    commands_dest = claude_dir / "commands"
    if commands_src.exists():
        commands_dest.mkdir(parents=True, exist_ok=True)
        for cmd_file in commands_src.iterdir():
            if cmd_file.is_file() and cmd_file.suffix == ".md":
                # Remove .md extension: "constitution.md" → "constitution"
                dest_name = cmd_file.stem
                shutil.copy2(cmd_file, commands_dest / dest_name)

    # 3. Copy Subagents
    agents_src = claude_templates / "agents"
    agents_dest = claude_dir / "agents"
    if agents_src.exists():
        agents_dest.mkdir(parents=True, exist_ok=True)
        for agent_file in agents_src.iterdir():
            if agent_file.is_file():
                shutil.copy2(agent_file, agents_dest / agent_file.name)

    # 4. Copy Rules
    rules_src = claude_templates / "rules"
    rules_dest = claude_dir / "rules"
    if rules_src.exists():
        rules_dest.mkdir(parents=True, exist_ok=True)
        for rule_file in rules_src.iterdir():
            if rule_file.is_file():
                shutil.copy2(rule_file, rules_dest / rule_file.name)

    console.print(f"[green]✓[/green] Claude Code templates installed to {claude_dir}")
    console.print(f"[dim]  - CLAUDE.md: copied to project root[/dim]")
    console.print(f"[dim]  - Commands: {len(list((commands_dest).iterdir()) if commands_dest.exists() else [])} files[/dim]")
    console.print(f"[dim]  - Agents: {len(list((agents_dest).iterdir()) if agents_dest.exists() else [])} files[/dim]")
    console.print(f"[dim]  - Rules: {len(list((rules_dest).iterdir()) if rules_dest.exists() else [])} files[/dim]")

def ensure_agent_installed(agent: str, project_dir: Path) -> None:
    """
    Ensure agent configuration is installed in project.
    Auto-download if not present.

    Args:
        agent: Agent name (claude, codex, etc.)
        project_dir: Project directory path
    """
    if agent not in AGENT_CONFIG:
        console.print(f"[red]Error:[/red] Unknown agent '{agent}'")
        console.print(f"[dim]Available agents: {', '.join(AGENT_CONFIG.keys())}[/dim]")
        raise typer.Exit(1)

    agent_config = AGENT_CONFIG[agent]
    agent_folder = project_dir / agent_config["folder"]

    if agent_folder.exists():
        # Already installed
        return

    console.print(f"[cyan]Installing {agent_config['name']} configuration...[/cyan]")

    # Download agent-specific template from GitHub
    # Use the existing download_and_extract_template function
    try:
        # Determine script type based on OS
        script_type = "ps" if os.name == "nt" else "sh"

        download_and_extract_template(
            project_path=project_dir,
            ai_assistant=agent,
            script_type=script_type,
            is_current_dir=True,  # Install into current directory
            verbose=False,
            tracker=None,
            client=client,
            debug=False,
            github_token=None
        )

        console.print(f"[green]✓[/green] {agent_config['name']} configuration installed")
    except Exception as e:
        console.print(f"[red]Error installing {agent_config['name']}:[/red] {e}")
        raise typer.Exit(1)

def select_agent_interactive() -> str:
    """
    Interactively select an AI agent from available options.

    Returns:
        Selected agent name
    """
    console.print("\n[bold cyan]Select AI Agent:[/bold cyan]")

    # Get available agents (only claude for now)
    available_agents = ["claude"]

    if len(available_agents) == 1:
        # Only one agent available, auto-select
        agent = available_agents[0]
        console.print(f"[dim]Auto-selecting {AGENT_CONFIG[agent]['name']}[/dim]")
        return agent

    # Display options
    for idx, agent in enumerate(available_agents, 1):
        agent_info = AGENT_CONFIG[agent]
        console.print(f"  {idx}. {agent_info['name']}")

    # Get user input
    while True:
        try:
            choice = console.input("[cyan]Enter number (1-{}): [/cyan]".format(len(available_agents)))
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_agents):
                selected = available_agents[choice_num - 1]
                console.print(f"[green]✓[/green] Selected {AGENT_CONFIG[selected]['name']}")
                return selected
            else:
                console.print("[red]Invalid choice. Please try again.[/red]")
        except (ValueError, KeyboardInterrupt):
            console.print("\n[yellow]Selection cancelled[/yellow]")
            raise typer.Exit(1)

# =============================================================================
# GitHub API Helper Functions
# =============================================================================

def _github_token(cli_token: str | None = None) -> str | None:
    """Return sanitized GitHub token (cli arg takes precedence) or None."""
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None

def _github_auth_headers(cli_token: str | None = None) -> dict:
    """Return Authorization header dict only when a non-empty token exists."""
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}

def _parse_rate_limit_headers(headers: httpx.Headers) -> dict:
    """Extract and parse GitHub rate-limit headers."""
    info = {}
    
    # Standard GitHub rate-limit headers
    if "X-RateLimit-Limit" in headers:
        info["limit"] = headers.get("X-RateLimit-Limit")
    if "X-RateLimit-Remaining" in headers:
        info["remaining"] = headers.get("X-RateLimit-Remaining")
    if "X-RateLimit-Reset" in headers:
        reset_epoch = int(headers.get("X-RateLimit-Reset", "0"))
        if reset_epoch:
            reset_time = datetime.fromtimestamp(reset_epoch, tz=timezone.utc)
            info["reset_epoch"] = reset_epoch
            info["reset_time"] = reset_time
            info["reset_local"] = reset_time.astimezone()
    
    # Retry-After header (seconds or HTTP-date)
    if "Retry-After" in headers:
        retry_after = headers.get("Retry-After")
        try:
            info["retry_after_seconds"] = int(retry_after)
        except ValueError:
            # HTTP-date format - not implemented, just store as string
            info["retry_after"] = retry_after
    
    return info

def _format_rate_limit_error(status_code: int, headers: httpx.Headers, url: str) -> str:
    """Format a user-friendly error message with rate-limit information."""
    rate_info = _parse_rate_limit_headers(headers)
    
    lines = [f"GitHub API returned status {status_code} for {url}"]
    lines.append("")
    
    if rate_info:
        lines.append("[bold]Rate Limit Information:[/bold]")
        if "limit" in rate_info:
            lines.append(f"  • Rate Limit: {rate_info['limit']} requests/hour")
        if "remaining" in rate_info:
            lines.append(f"  • Remaining: {rate_info['remaining']}")
        if "reset_local" in rate_info:
            reset_str = rate_info["reset_local"].strftime("%Y-%m-%d %H:%M:%S %Z")
            lines.append(f"  • Resets at: {reset_str}")
        if "retry_after_seconds" in rate_info:
            lines.append(f"  • Retry after: {rate_info['retry_after_seconds']} seconds")
        lines.append("")
    
    # Add troubleshooting guidance
    lines.append("[bold]Troubleshooting Tips:[/bold]")
    lines.append("  • If you're on a shared CI or corporate environment, you may be rate-limited.")
    lines.append("  • Consider using a GitHub token via --github-token or the GH_TOKEN/GITHUB_TOKEN")
    lines.append("    environment variable to increase rate limits.")
    lines.append("  • Authenticated requests have a limit of 5,000/hour vs 60/hour for unauthenticated.")
    
    return "\n".join(lines)

# Agent configuration with name, folder, install URL, and CLI tool requirement
AGENT_CONFIG = {
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github/",
        "install_url": None,  # IDE-based, no CLI check needed
        "requires_cli": False,
    },
    "claude": {
        "name": "Claude Code",
        "folder": ".claude/",
        "install_url": "https://docs.anthropic.com/en/docs/claude-code/setup",
        "requires_cli": True,
    },
    "gemini": {
        "name": "Gemini CLI",
        "folder": ".gemini/",
        "install_url": "https://github.com/google-gemini/gemini-cli",
        "requires_cli": True,
    },
    "cursor-agent": {
        "name": "Cursor",
        "folder": ".cursor/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "qwen": {
        "name": "Qwen Code",
        "folder": ".qwen/",
        "install_url": "https://github.com/QwenLM/qwen-code",
        "requires_cli": True,
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode/",
        "install_url": "https://opencode.ai",
        "requires_cli": True,
    },
    "codex": {
        "name": "Codex CLI",
        "folder": ".codex/",
        "install_url": "https://github.com/openai/codex",
        "requires_cli": True,
    },
    "windsurf": {
        "name": "Windsurf",
        "folder": ".windsurf/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "kilocode": {
        "name": "Kilo Code",
        "folder": ".kilocode/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "auggie": {
        "name": "Auggie CLI",
        "folder": ".augment/",
        "install_url": "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli",
        "requires_cli": True,
    },
    "codebuddy": {
        "name": "CodeBuddy",
        "folder": ".codebuddy/",
        "install_url": "https://www.codebuddy.ai/cli",
        "requires_cli": True,
    },
    "qoder": {
        "name": "Qoder CLI",
        "folder": ".qoder/",
        "install_url": "https://qoder.com/cli",
        "requires_cli": True,
    },
    "roo": {
        "name": "Roo Code",
        "folder": ".roo/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "q": {
        "name": "Amazon Q Developer CLI",
        "folder": ".amazonq/",
        "install_url": "https://aws.amazon.com/developer/learning/q-developer-cli/",
        "requires_cli": True,
    },
    "amp": {
        "name": "Amp",
        "folder": ".agents/",
        "install_url": "https://ampcode.com/manual#install",
        "requires_cli": True,
    },
    "shai": {
        "name": "SHAI",
        "folder": ".shai/",
        "install_url": "https://github.com/ovh/shai",
        "requires_cli": True,
    },
    "bob": {
        "name": "IBM Bob",
        "folder": ".bob/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
}

SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}

CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"

BANNER = """
 ██████╗ ██████╗  ██████╗ ██╗   ██╗███████╗
██╔════╝ ██╔══██╗██╔═══██╗██║   ██║██╔════╝
██║  ███╗██████╔╝██║   ██║██║   ██║█████╗
██║   ██║██╔══██╗██║   ██║╚██╗ ██╔╝██╔══╝
╚██████╔╝██║  ██║╚██████╔╝ ╚████╔╝ ███████╗
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚══════╝
"""

TAGLINE = "Grove - Spec-Driven Development Toolkit"
class StepTracker:
    """Track and render hierarchical steps without emojis, similar to Claude Code tree output.
    Supports live auto-refresh via an attached refresh callback.
    """
    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {"pending": 0, "running": 1, "done": 2, "error": 3, "skipped": 4}
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return

        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree

def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()

    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return 'up'
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return 'down'

    if key == readchar.key.ENTER:
        return 'enter'

    if key == readchar.key.ESC:
        return 'escape'

    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key

def select_with_arrows(options: dict, prompt_text: str = "Select an option", default_key: str = None) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.
    
    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with
        
    Returns:
        Selected option key
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")

        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")

        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )

    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = get_key()
                    if key == 'up':
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == 'down':
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == 'enter':
                        selected_key = option_keys[selected_index]
                        break
                    elif key == 'escape':
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    return selected_key

console = Console()

class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="specify",
    help="Setup tool for Grove spec-driven development projects",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)

def version_callback(value: bool):
    """Show version and exit."""
    if value:
        console.print(f"[cyan]Grove CLI[/cyan] version [bold]{__version__}[/bold]")
        raise typer.Exit()

@app.callback()
def main_callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    )
):
    """Grove CLI - Setup tool for Grove spec-driven development projects."""
    pass

def show_banner():
    """Display the ASCII art banner."""
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(t("tagline"), style="italic bright_yellow")))
    if "banner_subtitle" in I18N.get(_current_lang, {}):
        console.print(Align.center(Text(t("banner_subtitle"), style="dim")))
    console.print()

@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center(f"[dim]{t('help_usage')}[/dim]"))
        console.print()

def run_command(cmd: list[str], check_return: bool = True, capture: bool = False, shell: bool = False) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None

def check_tool(tool: str, tracker: StepTracker = None) -> bool:
    """Check if a tool is installed. Optionally update tracker.
    
    Args:
        tool: Name of the tool to check
        tracker: Optional StepTracker to update with results
        
    Returns:
        True if tool is found, False otherwise
    """
    # Special handling for Claude CLI after `claude migrate-installer`
    # See: https://github.com/cardene777/grove/issues/123
    # The migrate-installer command REMOVES the original executable from PATH
    # and creates an alias at ~/.claude/local/claude instead
    # This path should be prioritized over other claude executables in PATH
    if tool == "claude":
        if CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
            if tracker:
                tracker.complete(tool, "available")
            return True
    
    found = shutil.which(tool) is not None
    
    if tracker:
        if found:
            tracker.complete(tool, "available")
        else:
            tracker.error(tool, "not found")
    
    return found

def is_git_repo(path: Path = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()
    
    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def init_git_repo(project_path: Path, quiet: bool = False) -> Tuple[bool, Optional[str]]:
    """Initialize a git repository in the specified path.
    
    Args:
        project_path: Path to initialize git repository in
        quiet: if True suppress console output (tracker handles status)
    
    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True, text=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from Grove template"], check=True, capture_output=True, text=True)
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True, None

    except subprocess.CalledProcessError as e:
        error_msg = f"Command: {' '.join(e.cmd)}\nExit code: {e.returncode}"
        if e.stderr:
            error_msg += f"\nError: {e.stderr.strip()}"
        elif e.stdout:
            error_msg += f"\nOutput: {e.stdout.strip()}"
        
        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False, error_msg
    finally:
        os.chdir(original_cwd)

def handle_vscode_settings(sub_item, dest_file, rel_path, verbose=False, tracker=None) -> None:
    """Handle merging or copying of .vscode/settings.json files."""
    def log(message, color="green"):
        if verbose and not tracker:
            console.print(f"[{color}]{message}[/] {rel_path}")

    try:
        with open(sub_item, 'r', encoding='utf-8') as f:
            new_settings = json.load(f)

        if dest_file.exists():
            merged = merge_json_files(dest_file, new_settings, verbose=verbose and not tracker)
            with open(dest_file, 'w', encoding='utf-8') as f:
                json.dump(merged, f, indent=4)
                f.write('\n')
            log("Merged:", "green")
        else:
            shutil.copy2(sub_item, dest_file)
            log("Copied (no existing settings.json):", "blue")

    except Exception as e:
        log(f"Warning: Could not merge, copying instead: {e}", "yellow")
        shutil.copy2(sub_item, dest_file)

def merge_json_files(existing_path: Path, new_content: dict, verbose: bool = False) -> dict:
    """Merge new JSON content into existing JSON file.

    Performs a deep merge where:
    - New keys are added
    - Existing keys are preserved unless overwritten by new content
    - Nested dictionaries are merged recursively
    - Lists and other values are replaced (not merged)

    Args:
        existing_path: Path to existing JSON file
        new_content: New JSON content to merge in
        verbose: Whether to print merge details

    Returns:
        Merged JSON content as dict
    """
    try:
        with open(existing_path, 'r', encoding='utf-8') as f:
            existing_content = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is invalid, just use new content
        return new_content

    def deep_merge(base: dict, update: dict) -> dict:
        """Recursively merge update dict into base dict."""
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                result[key] = deep_merge(result[key], value)
            else:
                # Add new key or replace existing value
                result[key] = value
        return result

    merged = deep_merge(existing_content, new_content)

    if verbose:
        console.print(f"[cyan]Merged JSON file:[/cyan] {existing_path.name}")

    return merged

def download_template_from_github(ai_assistant: str, download_dir: Path, *, script_type: str = "sh", verbose: bool = True, show_progress: bool = True, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Tuple[Path, dict]:
    repo_owner = "cardene777"
    repo_name = "grove"
    if client is None:
        client = httpx.Client(verify=ssl_context)

    if verbose:
        console.print("[cyan]Fetching latest release information...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        response = client.get(
            api_url,
            timeout=30,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        )
        status = response.status_code
        if status != 200:
            # Format detailed error message with rate-limit info
            error_msg = _format_rate_limit_error(status, response.headers, api_url)
            if debug:
                error_msg += f"\n\n[dim]Response body (truncated 500):[/dim]\n{response.text[:500]}"
            raise RuntimeError(error_msg)
        try:
            release_data = response.json()
        except ValueError as je:
            raise RuntimeError(f"Failed to parse release JSON: {je}\nRaw (truncated 400): {response.text[:400]}")
    except Exception as e:
        console.print(f"[red]Error fetching release information[/red]")
        console.print(Panel(str(e), title="Fetch Error", border_style="red"))
        raise typer.Exit(1)

    assets = release_data.get("assets", [])
    pattern = f"grove-template-{ai_assistant}-{script_type}"
    matching_assets = [
        asset for asset in assets
        if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]

    asset = matching_assets[0] if matching_assets else None

    if asset is None:
        console.print(f"[red]No matching release asset found[/red] for [bold]{ai_assistant}[/bold] (expected pattern: [bold]{pattern}[/bold])")
        asset_names = [a.get('name', '?') for a in assets]
        console.print(Panel("\n".join(asset_names) or "(no assets)", title="Available Assets", border_style="yellow"))
        raise typer.Exit(1)

    download_url = asset["browser_download_url"]
    filename = asset["name"]
    file_size = asset["size"]

    if verbose:
        console.print(f"[cyan]Found template:[/cyan] {filename}")
        console.print(f"[cyan]Size:[/cyan] {file_size:,} bytes")
        console.print(f"[cyan]Release:[/cyan] {release_data['tag_name']}")

    zip_path = download_dir / filename
    if verbose:
        console.print(f"[cyan]Downloading template...[/cyan]")

    try:
        with client.stream(
            "GET",
            download_url,
            timeout=60,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        ) as response:
            if response.status_code != 200:
                # Handle rate-limiting on download as well
                error_msg = _format_rate_limit_error(response.status_code, response.headers, download_url)
                if debug:
                    error_msg += f"\n\n[dim]Response body (truncated 400):[/dim]\n{response.text[:400]}"
                raise RuntimeError(error_msg)
            total_size = int(response.headers.get('content-length', 0))
            with open(zip_path, 'wb') as f:
                if total_size == 0:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                else:
                    if show_progress:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                            console=console,
                        ) as progress:
                            task = progress.add_task("Downloading...", total=total_size)
                            downloaded = 0
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress.update(task, completed=downloaded)
                    else:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
    except Exception as e:
        console.print(f"[red]Error downloading template[/red]")
        detail = str(e)
        if zip_path.exists():
            zip_path.unlink()
        console.print(Panel(detail, title="Download Error", border_style="red"))
        raise typer.Exit(1)
    if verbose:
        console.print(f"Downloaded: {filename}")
    metadata = {
        "filename": filename,
        "size": file_size,
        "release": release_data["tag_name"],
        "asset_url": download_url
    }
    return zip_path, metadata

def download_and_extract_template(project_path: Path, ai_assistant: str, script_type: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Path:
    """Download the latest release and extract it to create a new project.
    Returns project_path. Uses tracker if provided (with keys: fetch, download, extract, cleanup)
    """
    current_dir = Path.cwd()

    if tracker:
        tracker.start("fetch", "contacting GitHub API")
    try:
        zip_path, meta = download_template_from_github(
            ai_assistant,
            current_dir,
            script_type=script_type,
            verbose=verbose and tracker is None,
            show_progress=(tracker is None),
            client=client,
            debug=debug,
            github_token=github_token
        )
        if tracker:
            tracker.complete("fetch", f"release {meta['release']} ({meta['size']:,} bytes)")
            tracker.add("download", "Download template")
            tracker.complete("download", meta['filename'])
    except Exception as e:
        if tracker:
            tracker.error("fetch", str(e))
        else:
            if verbose:
                console.print(f"[red]Error downloading template:[/red] {e}")
        raise

    if tracker:
        tracker.add("extract", "Extract template")
        tracker.start("extract")
    elif verbose:
        console.print("Extracting template...")

    try:
        if not is_current_dir:
            project_path.mkdir(parents=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_contents = zip_ref.namelist()
            if tracker:
                tracker.start("zip-list")
                tracker.complete("zip-list", f"{len(zip_contents)} entries")
            elif verbose:
                console.print(f"[cyan]ZIP contains {len(zip_contents)} items[/cyan]")

            if is_current_dir:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    zip_ref.extractall(temp_path)

                    extracted_items = list(temp_path.iterdir())
                    if tracker:
                        tracker.start("extracted-summary")
                        tracker.complete("extracted-summary", f"temp {len(extracted_items)} items")
                    elif verbose:
                        console.print(f"[cyan]Extracted {len(extracted_items)} items to temp location[/cyan]")

                    source_dir = temp_path
                    if len(extracted_items) == 1 and extracted_items[0].is_dir():
                        source_dir = extracted_items[0]
                        if tracker:
                            tracker.add("flatten", "Flatten nested directory")
                            tracker.complete("flatten")
                        elif verbose:
                            console.print(f"[cyan]Found nested directory structure[/cyan]")

                    for item in source_dir.iterdir():
                        dest_path = project_path / item.name
                        if item.is_dir():
                            if dest_path.exists():
                                if verbose and not tracker:
                                    console.print(f"[yellow]Merging directory:[/yellow] {item.name}")
                                for sub_item in item.rglob('*'):
                                    if sub_item.is_file():
                                        rel_path = sub_item.relative_to(item)
                                        dest_file = dest_path / rel_path
                                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                                        # Special handling for .vscode/settings.json - merge instead of overwrite
                                        if dest_file.name == "settings.json" and dest_file.parent.name == ".vscode":
                                            handle_vscode_settings(sub_item, dest_file, rel_path, verbose, tracker)
                                        else:
                                            shutil.copy2(sub_item, dest_file)
                            else:
                                shutil.copytree(item, dest_path)
                        else:
                            if dest_path.exists() and verbose and not tracker:
                                console.print(f"[yellow]Overwriting file:[/yellow] {item.name}")
                            shutil.copy2(item, dest_path)
                    if verbose and not tracker:
                        console.print(f"[cyan]Template files merged into current directory[/cyan]")
            else:
                zip_ref.extractall(project_path)

                extracted_items = list(project_path.iterdir())
                if tracker:
                    tracker.start("extracted-summary")
                    tracker.complete("extracted-summary", f"{len(extracted_items)} top-level items")
                elif verbose:
                    console.print(f"[cyan]Extracted {len(extracted_items)} items to {project_path}:[/cyan]")
                    for item in extracted_items:
                        console.print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")

                if len(extracted_items) == 1 and extracted_items[0].is_dir():
                    nested_dir = extracted_items[0]
                    temp_move_dir = project_path.parent / f"{project_path.name}_temp"

                    shutil.move(str(nested_dir), str(temp_move_dir))

                    project_path.rmdir()

                    shutil.move(str(temp_move_dir), str(project_path))
                    if tracker:
                        tracker.add("flatten", "Flatten nested directory")
                        tracker.complete("flatten")
                    elif verbose:
                        console.print(f"[cyan]Flattened nested directory structure[/cyan]")

    except Exception as e:
        if tracker:
            tracker.error("extract", str(e))
        else:
            if verbose:
                console.print(f"[red]Error extracting template:[/red] {e}")
                if debug:
                    console.print(Panel(str(e), title="Extraction Error", border_style="red"))

        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    else:
        if tracker:
            tracker.complete("extract")
    finally:
        if tracker:
            tracker.add("cleanup", "Remove temporary archive")

        if zip_path.exists():
            zip_path.unlink()
            if tracker:
                tracker.complete("cleanup")
            elif verbose:
                console.print(f"Cleaned up: {zip_path.name}")

    return project_path


def ensure_executable_scripts(project_path: Path, tracker: StepTracker | None = None) -> None:
    """Ensure POSIX .sh scripts under .grove/scripts (recursively) have execute bits (no-op on Windows)."""
    if os.name == "nt":
        return  # Windows: skip silently
    scripts_root = project_path / ".grove" / "scripts"
    if not scripts_root.is_dir():
        return
    failures: list[str] = []
    updated = 0
    for script in scripts_root.rglob("*.sh"):
        try:
            if script.is_symlink() or not script.is_file():
                continue
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except Exception:
                continue
            st = script.stat(); mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400: new_mode |= 0o100
            if mode & 0o040: new_mode |= 0o010
            if mode & 0o004: new_mode |= 0o001
            if not (new_mode & 0o100):
                new_mode |= 0o100
            os.chmod(script, new_mode)
            updated += 1
        except Exception as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")
    if tracker:
        detail = f"{updated} updated" + (f", {len(failures)} failed" if failures else "")
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            console.print(f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]")
        if failures:
            console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for f in failures:
                console.print(f"  - {f}")

def cleanup_language_templates(project_dir: Path, lang: str, tracker: StepTracker = None) -> None:
    """Clean up language-specific template directories and files.

    After extracting the template ZIP, this function:
    1. Moves selected language files from .grove/templates/{lang}/ to .grove/templates/
    2. Removes language subdirectories (.grove/templates/en/, .grove/templates/ja/)
    3. Removes any duplicate template files in .grove/templates/

    Args:
        project_dir: Project directory path
        lang: Selected language code (ja or en)
        tracker: Optional StepTracker for progress display
    """
    if tracker:
        tracker.add("cleanup-lang", "Organizing language-specific templates")
        tracker.start("cleanup-lang")

    templates_dir = project_dir / ".grove" / "templates"

    if not templates_dir.exists():
        if tracker:
            tracker.warn("cleanup-lang", "templates directory not found")
        return

    # Language-specific template files to process
    lang_specific_files = [
        "constitution-template.md",
        "spec-template.md",
    ]

    lang_dir = templates_dir / lang

    # Move selected language files to templates root
    if lang_dir.exists():
        for template_file in lang_specific_files:
            source_file = lang_dir / template_file
            dest_file = templates_dir / template_file

            if source_file.exists():
                # Remove existing file if it exists (avoid duplicates)
                if dest_file.exists():
                    dest_file.unlink()

                # Move file from language subdirectory to templates root
                shutil.move(str(source_file), str(dest_file))

    # Remove all language subdirectories
    for lang_code in SUPPORTED_LANGUAGES:
        lang_subdir = templates_dir / lang_code
        if lang_subdir.exists() and lang_subdir.is_dir():
            shutil.rmtree(lang_subdir)

    # Also remove 'agents' subdirectory if it exists (already copied to appropriate location)
    agents_dir = templates_dir / "agents"
    if agents_dir.exists() and agents_dir.is_dir():
        shutil.rmtree(agents_dir)

    if tracker:
        tracker.complete("cleanup-lang", f"organized {lang} templates")

def install_common_templates(project_dir: Path, lang: str, script_type: str, tracker: StepTracker = None) -> None:
    """Install language-specific templates to project.

    Args:
        project_dir: Project directory path
        lang: Language code (ja or en)
        script_type: Script type (sh or ps)
        tracker: Optional StepTracker for progress display

    Processing flow:
        1. Read from grove_cli/templates/{lang}/
        2. Copy to project's .grove/templates/
        3. Copy scripts based on script_type
        4. Copy memory directory
        5. Fallback: Use English if specified language doesn't exist

    Target templates:
        - constitution-template.md
        - spec-template.md
        - plan-template.md (for reference, AI generates dynamically)
        - tasks-template.md (for reference, AI generates dynamically)
        - checklist-template.md (for reference, AI generates dynamically)
    """
    if tracker:
        tracker.add("install-templates", "Installing language-specific templates")
        tracker.start("install-templates")

    # Get template directory (installed location only)
    templates_root = Path(sys.prefix) / "share" / "grove-cli" / "templates"

    if not templates_root.exists():
        if tracker:
            tracker.warn("No templates found in package directory")
        return

    templates_source = templates_root / lang

    # Fallback to English if language doesn't exist
    if not templates_source.exists():
        if tracker:
            tracker.warn(f"Language '{lang}' templates not found, using English")
        templates_source = templates_root / "en"

    if not templates_source.exists():
        if tracker:
            tracker.warn("No templates found for selected language")
        return

    # Create destination directory
    templates_dest = project_dir / ".grove" / "templates"
    templates_dest.mkdir(parents=True, exist_ok=True)

    # Language-specific template files (from templates/{lang}/)
    lang_specific_files = [
        "constitution-template.md",
        "spec-template.md",
    ]

    # Common template files (from templates/ root, language-independent)
    common_files = [
        "plan-template.md",
        "tasks-template.md",
        "checklist-template.md",
        "agent-file-template.md",
        "verification-template.md",
    ]

    copied = 0

    # Copy language-specific templates
    for template_file in lang_specific_files:
        source_file = templates_source / template_file
        if source_file.exists():
            dest_file = templates_dest / template_file
            shutil.copy2(source_file, dest_file)
            copied += 1

    # Copy common templates (language-independent)
    for template_file in common_files:
        source_file = templates_root / template_file
        if source_file.exists():
            dest_file = templates_dest / template_file
            shutil.copy2(source_file, dest_file)
            copied += 1

    # Copy scripts directory structure (based on script_type)
    scripts_root = Path(sys.prefix) / "share" / "grove-cli" / "scripts"

    if scripts_root.exists():
        scripts_dest = project_dir / ".grove" / "scripts"
        scripts_dest.mkdir(parents=True, exist_ok=True)

        # Copy only the selected script type directly to .grove/scripts/
        if script_type == "sh":
            bash_src = scripts_root / "bash"
            if bash_src.exists():
                for script_file in bash_src.glob("*.sh"):
                    shutil.copy2(script_file, scripts_dest / script_file.name)
                    copied += 1
        elif script_type == "ps":
            ps_src = scripts_root / "powershell"
            if ps_src.exists():
                for script_file in ps_src.glob("*.ps1"):
                    shutil.copy2(script_file, scripts_dest / script_file.name)
                    copied += 1

    # Copy memory directory structure
    memory_root = Path(sys.prefix) / "share" / "grove-cli" / "memory"

    if memory_root.exists():
        memory_dest = project_dir / ".grove" / "memory"
        if memory_dest.exists():
            shutil.rmtree(memory_dest)
        shutil.copytree(memory_root, memory_dest)
        copied += len(list(memory_dest.rglob("*")))

    if tracker and copied > 0:
        tracker.complete("install-templates", f"Installed {copied} template(s) ({lang})")

@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (optional if using --here, or use '.' for current directory)"),
    ai: List[str] = typer.Option(None, "--ai", help="AI agents to support (can specify multiple): claude, codex"),
    lang: str = typer.Option(None, "--lang", help="Language for templates and messages: ja (Japanese) or en (English)"),
    script_type: str = typer.Option(None, "--script", help="Script type to use: sh or ps"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="Skip checks for AI agent tools like Claude Code"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one"),
    force: bool = typer.Option(False, "--force", help="Force merge/overwrite when using --here (skip confirmation)"),
    skip_tls: bool = typer.Option(False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"),
    debug: bool = typer.Option(False, "--debug", help="Show verbose diagnostic output for network and extraction failures"),
    github_token: str = typer.Option(None, "--github-token", help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)"),
):
    """
    Initialize a new Grove project from the latest template.
    
    This command will:
    1. Check that required tools are installed (git is optional)
    2. Let you choose your AI assistant
    3. Download the appropriate template from GitHub
    4. Extract the template to a new project directory or current directory
    5. Initialize a fresh git repository (if not --no-git and no existing repo)
    6. Optionally set up AI assistant commands
    
    Examples:
        specify init my-project
        specify init my-project --ai claude
        specify init my-project --ai copilot --no-git
        specify init --ignore-agent-tools my-project
        specify init . --ai claude         # Initialize in current directory
        specify init .                     # Initialize in current directory (interactive AI selection)
        specify init --here --ai claude    # Alternative syntax for current directory
        specify init --here --ai codex
        specify init --here --ai codebuddy
        specify init --here
        specify init --here --force  # Skip confirmation when current directory not empty
    """
    # Language selection
    if lang:
        # Validate language option
        if lang not in SUPPORTED_LANGUAGES:
            set_lang("en")  # Set English temporarily for error message
            console.print(f"[red]{t('error_unsupported_language')}:[/red] {lang}")
            console.print(f"[dim]{t('supported_languages')}: {', '.join(SUPPORTED_LANGUAGES)}[/dim]")
            raise typer.Exit(1)
        selected_lang = lang
    else:
        # Interactive language selection
        console.print("\n[cyan]Select language / 言語を選択してください:[/cyan]")
        options = [
            "[1] English",
            "[2] 日本語 (Japanese)",
        ]
        for option in options:
            console.print(f"  {option}")

        choice = typer.prompt("Enter choice", type=int, default=1)
        selected_lang = "en" if choice == 1 else "ja"

    # Set language for this session
    set_lang(selected_lang)

    console.print(f"[cyan]{t('selected_language')}:[/cyan] {LANGUAGE_NAMES[selected_lang]}\n")

    show_banner()

    if project_name == ".":
        here = True
        project_name = None  # Clear project_name to use existing validation logic

    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)

    if not here and not project_name:
        console.print(f"[red]{t('error_must_specify_project')}[/red]")
        raise typer.Exit(1)

    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()

        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]{t('warning_not_empty')} ({len(existing_items)} {t('items_found')})[/yellow]")
            console.print(f"[yellow]{t('template_merge_warning')}[/yellow]")
            if force:
                console.print(f"[cyan]{t('force_skipping_confirmation')}[/cyan]")
            else:
                response = typer.confirm(t('confirm_continue'))
                if not response:
                    console.print(f"[yellow]{t('operation_cancelled')}[/yellow]")
                    raise typer.Exit(0)
    else:
        project_path = Path(project_name).resolve()
        if project_path.exists():
            error_panel = Panel(
                f"Directory '[cyan]{project_name}[/cyan]' already exists\n"
                "Please choose a different project name or remove the existing directory.",
                title="[red]Directory Conflict[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    current_dir = Path.cwd()

    setup_lines = [
        "[cyan]Grove Project Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{project_path.name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]

    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")

    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git")
        if not should_init_git:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    # Validate and process AI agents (support only claude and codex)
    if ai:
        # Validate all specified agents
        for agent in ai:
            if agent not in SUPPORTED_AI_AGENTS:
                console.print(f"[red]Error:[/red] Unsupported AI agent: {agent}")
                console.print(f"[dim]Supported agents: {', '.join(SUPPORTED_AI_AGENTS)}[/dim]")
                raise typer.Exit(1)
        # Remove duplicates while preserving order
        selected_ai_agents = list(dict.fromkeys(ai))
    else:
        # Interactive selection
        ai_choices = {
            "claude": "Claude Code",
            "codex": "OpenAI Codex",
            "both": "Both (Claude Code + Codex)"
        }
        selected_choice = select_with_arrows(
            ai_choices,
            "Choose your AI agent(s):",
            "claude"
        )
        if selected_choice == "both":
            selected_ai_agents = ["claude", "codex"]
        else:
            selected_ai_agents = [selected_choice]

    # Note: Claude Code and Codex don't require CLI tool checks
    # Configuration files will be installed regardless of whether the tools are present

    if script_type:
        if script_type not in SCRIPT_TYPE_CHOICES:
            console.print(f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_script = script_type
    else:
        default_script = "ps" if os.name == "nt" else "sh"

        if sys.stdin.isatty():
            selected_script = select_with_arrows(SCRIPT_TYPE_CHOICES, "Choose script type (or press Enter)", default_script)
        else:
            selected_script = default_script

    console.print(f"[cyan]{t('selected_ai')}:[/cyan] {', '.join(selected_ai_agents)}")
    console.print(f"[cyan]{t('selected_script')}:[/cyan] {selected_script}")

    tracker = StepTracker(t('tracker_title'))

    sys._specify_tracker_active = True

    tracker.add("precheck", t('tracker_precheck'))
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", t('tracker_ai_select'))
    tracker.complete("ai-select", f"{', '.join(selected_ai_agents)}")
    tracker.add("script-select", t('tracker_script_select'))
    tracker.complete("script-select", selected_script)
    for key, label_key in [
        ("fetch", "tracker_fetch"),
        ("download", "tracker_download"),
        ("extract", "tracker_extract"),
        ("zip-list", "tracker_archive"),
        ("extracted-summary", "tracker_extract_summary"),
        ("chmod", "tracker_chmod"),
        ("cleanup", "tracker_cleanup"),
        ("git", "tracker_git_init"),
        ("final", "tracker_finalize")
    ]:
        tracker.add(key, t(label_key))

    # Track git error message outside Live context so it persists
    git_error_message = None

    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            verify = not skip_tls
            local_ssl_context = ssl_context if verify else False
            local_client = httpx.Client(verify=local_ssl_context)

            # Download base template from GitHub
            # Use first selected AI agent for template download (base template)
            download_and_extract_template(project_path, selected_ai_agents[0], selected_script, here, verbose=False, tracker=tracker, client=local_client, debug=debug, github_token=github_token)

            # Cleanup language-specific template directories
            cleanup_language_templates(project_path, selected_lang, tracker=tracker)

            # Install language-specific templates (.grove/ directory structure)
            install_common_templates(project_path, selected_lang, selected_script, tracker=tracker)

            ensure_executable_scripts(project_path, tracker=tracker)

            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif should_init_git:
                    success, error_msg = init_git_repo(project_path, quiet=True)
                    if success:
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                        git_error_message = error_msg
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "project ready")
        except Exception as e:
            tracker.error("final", str(e))
            console.print(Panel(f"Initialization failed: {e}", title="Failure", border_style="red"))
            if debug:
                _env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("Platform", sys.platform),
                    ("CWD", str(Path.cwd())),
                ]
                _label_width = max(len(k) for k, _ in _env_pairs)
                env_lines = [f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]" for k, v in _env_pairs]
                console.print(Panel("\n".join(env_lines), title="Debug Environment", border_style="magenta"))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            pass

    console.print(tracker.render())
    console.print(f"\n[bold green]{t('project_ready')}[/bold green]")

    # Save project configuration
    save_project_config(project_path, {"language": selected_lang})

    # Install configuration files for each selected AI agent
    console.print()

    for agent_name in selected_ai_agents:
        if agent_name == "claude":
            # Download from GitHub
            ensure_agent_installed("claude", project_path)
            console.print(f"[green]✓[/green] Claude Code configuration downloaded from GitHub")
        elif agent_name == "codex":
            # Download from GitHub
            ensure_agent_installed("codex", project_path)
            console.print(f"[green]✓[/green] Codex configuration downloaded from GitHub")

    # Show git error details if initialization failed
    if git_error_message:
        console.print()
        git_error_panel = Panel(
            f"[yellow]Warning:[/yellow] Git repository initialization failed\n\n"
            f"{git_error_message}\n\n"
            f"[dim]You can initialize git manually later with:[/dim]\n"
            f"[cyan]cd {project_path if not here else '.'}[/cyan]\n"
            f"[cyan]git init[/cyan]\n"
            f"[cyan]git add .[/cyan]\n"
            f"[cyan]git commit -m \"Initial commit\"[/cyan]",
            title="[red]Git Initialization Failed[/red]",
            border_style="red",
            padding=(1, 2)
        )
        console.print(git_error_panel)

    # Agent folder security notice
    agent_folders = []
    if "claude" in selected_ai_agents:
        agent_folders.append(".claude/")
    if "codex" in selected_ai_agents:
        agent_folders.append(".codex/")

    if agent_folders:
        folders_str = ", ".join(f"[cyan]{folder}[/cyan]" for folder in agent_folders)
        message = t('agent_folder_security_message').format(folder=folders_str)
        security_notice = Panel(
            message,
            title=f"[yellow]{t('agent_folder_security')}[/yellow]",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print()
        console.print(security_notice)

    steps_lines = []
    if not here:
        go_to_folder_msg = f"プロジェクトフォルダーに移動: [cyan]cd {project_name}[/cyan]" if selected_lang == "ja" else f"Go to the project folder: [cyan]cd {project_name}[/cyan]"
        steps_lines.append(f"1. {go_to_folder_msg}")
        step_num = 2
    else:
        steps_lines.append(f"1. {t('next_steps_already_in_dir')}")
        step_num = 2

    # Add Codex-specific setup step if needed
    if "codex" in selected_ai_agents:
        codex_path = project_path / ".codex"
        quoted_path = shlex.quote(str(codex_path))
        if os.name == "nt":  # Windows
            cmd = f"setx CODEX_HOME {quoted_path}"
        else:  # Unix-like systems
            cmd = f"export CODEX_HOME={quoted_path}"

        set_env_msg = f"{step_num}. Codex実行前に [cyan]CODEX_HOME[/cyan] 環境変数を設定: [cyan]{cmd}[/cyan]" if selected_lang == "ja" else f"{step_num}. Set [cyan]CODEX_HOME[/cyan] environment variable before running Codex: [cyan]{cmd}[/cyan]"
        steps_lines.append(set_env_msg)
        step_num += 1

    steps_lines.append(f"{step_num}. {t('next_steps_start_using')}")

    steps_lines.append(f"   {step_num}.1 [cyan]/grove.constitution[/] - {t('next_steps_constitution')}")
    steps_lines.append(f"   {step_num}.2 [cyan]/grove.specify[/] - {t('next_steps_specify')}")
    steps_lines.append(f"   {step_num}.3 [cyan]/grove.design[/] - {t('next_steps_design')}")
    steps_lines.append(f"   {step_num}.4 [cyan]/grove.plan[/] - {t('next_steps_plan')}")
    steps_lines.append(f"   {step_num}.5 [cyan]/grove.tasks[/] - {t('next_steps_tasks')}")
    steps_lines.append(f"   {step_num}.6 [cyan]/grove.implement[/] - {t('next_steps_implement')}")

    steps_panel = Panel("\n".join(steps_lines), title=t('next_steps'), border_style="cyan", padding=(1,2))
    console.print()
    console.print(steps_panel)

    enhancement_lines = [
        f"{t('enhancement_commands_desc')}",
        "",
        f"○ [cyan]/grove.clarify[/] [bright_black](optional)[/bright_black] - {t('enhancement_clarify')}",
        f"○ [cyan]/grove.analyze[/] [bright_black](optional)[/bright_black] - {t('enhancement_analyze')}",
        f"○ [cyan]/grove.checklist[/] [bright_black](optional)[/bright_black] - {t('enhancement_checklist')}",
        f"○ [cyan]/grove.review[/] [bright_black](optional)[/bright_black] - {t('enhancement_review')}",
        f"○ [cyan]/grove.fix[/] [bright_black](optional)[/bright_black] - {t('enhancement_fix')}"
    ]
    enhancements_panel = Panel("\n".join(enhancement_lines), title=t('enhancement_commands'), border_style="cyan", padding=(1,2))
    console.print()
    console.print(enhancements_panel)

@app.command()
def check():
    """Check that all required tools are installed."""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")

    tracker.add("git", "Git version control")
    git_ok = check_tool("git", tracker=tracker)

    agent_results = {}
    for agent_key, agent_config in AGENT_CONFIG.items():
        agent_name = agent_config["name"]
        requires_cli = agent_config["requires_cli"]

        tracker.add(agent_key, agent_name)

        if requires_cli:
            agent_results[agent_key] = check_tool(agent_key, tracker=tracker)
        else:
            # IDE-based agent - skip CLI check and mark as optional
            tracker.skip(agent_key, "IDE-based, no CLI check")
            agent_results[agent_key] = False  # Don't count IDE agents as "found"

    # Check VS Code variants (not in agent config)
    tracker.add("code", "Visual Studio Code")
    code_ok = check_tool("code", tracker=tracker)

    tracker.add("code-insiders", "Visual Studio Code Insiders")
    code_insiders_ok = check_tool("code-insiders", tracker=tracker)

    console.print(tracker.render())

    console.print("\n[bold green]Grove CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")

    if not any(agent_results.values()):
        console.print("[dim]Tip: Install an AI assistant for the best experience[/dim]")

@app.command()
def version():
    """Display version and system information."""
    import platform
    import importlib.metadata
    
    show_banner()
    
    # Get CLI version from package metadata
    cli_version = "unknown"
    try:
        cli_version = importlib.metadata.version("specify-cli")
    except Exception:
        # Fallback: try reading from pyproject.toml if running from source
        try:
            import tomllib
            pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                    cli_version = data.get("project", {}).get("version", "unknown")
        except Exception:
            pass
    
    # Fetch latest template release version
    repo_owner = "cardene777"
    repo_name = "grove"
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    
    template_version = "unknown"
    release_date = "unknown"
    
    try:
        response = client.get(
            api_url,
            timeout=10,
            follow_redirects=True,
            headers=_github_auth_headers(),
        )
        if response.status_code == 200:
            release_data = response.json()
            template_version = release_data.get("tag_name", "unknown")
            # Remove 'v' prefix if present
            if template_version.startswith("v"):
                template_version = template_version[1:]
            release_date = release_data.get("published_at", "unknown")
            if release_date != "unknown":
                # Format the date nicely
                try:
                    dt = datetime.fromisoformat(release_date.replace('Z', '+00:00'))
                    release_date = dt.strftime("%Y-%m-%d")
                except Exception:
                    pass
    except Exception:
        pass

    info_table = Table(show_header=False, box=None, padding=(0, 2))
    info_table.add_column("Key", style="cyan", justify="right")
    info_table.add_column("Value", style="white")

    info_table.add_row("CLI Version", cli_version)
    info_table.add_row("Template Version", template_version)
    info_table.add_row("Released", release_date)
    info_table.add_row("", "")
    info_table.add_row("Python", platform.python_version())
    info_table.add_row("Platform", platform.system())
    info_table.add_row("Architecture", platform.machine())
    info_table.add_row("OS Version", platform.version())

    panel = Panel(
        info_table,
        title="[bold cyan]Grove CLI Information[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    )

    console.print(panel)
    console.print()

# =============================================================================
# Phase 4: Document Management Helper Functions
# =============================================================================

def detect_source_directory(project_dir: Path) -> Optional[Path]:
    """
    Auto-detect source directory in project.

    Args:
        project_dir: Project directory path

    Returns:
        Path to source directory, or None if not found
    """
    # Common source directory names (priority order)
    candidates = ["src", "app", "lib", "pkg", "source", "code", "core"]

    for candidate in candidates:
        src_path = project_dir / candidate
        if src_path.exists() and src_path.is_dir():
            return src_path

    return None

def generate_index_md(dir_path: Path, relative_to: Path) -> str:
    """
    Generate index.md content with directory structure and file list.

    Args:
        dir_path: Directory to document
        relative_to: Base directory for relative paths

    Returns:
        Markdown content for index.md
    """
    rel_path = dir_path.relative_to(relative_to)
    content = f"# Index: {rel_path}\n\n"
    content += "## Directory Structure\n\n```\n"

    # List files and directories
    try:
        items = sorted(dir_path.iterdir())
        for item in items:
            if item.name.startswith("."):
                continue
            if item.name in ["node_modules", "__pycache__", "venv", "env", "dist", "build"]:
                continue

            prefix = "📁 " if item.is_dir() else "📄 "
            content += f"{prefix}{item.name}\n"
    except PermissionError:
        content += "(Permission denied)\n"

    content += "```\n\n"
    content += "## Files\n\n"

    # List file documentation links
    try:
        items = sorted(dir_path.iterdir())
        for item in items:
            if item.is_file() and not item.name.startswith("."):
                stem = item.stem
                content += f"- [{item.name}](./{stem}.md)\n"
    except PermissionError:
        content += "(Permission denied)\n"

    return content

def generate_readme_md(dir_path: Path, relative_to: Path) -> str:
    """
    Generate README.md content with detailed specification template.

    Args:
        dir_path: Directory to document
        relative_to: Base directory for relative paths

    Returns:
        Markdown content for README.md
    """
    rel_path = dir_path.relative_to(relative_to)
    content = f"# {rel_path}\n\n"
    content += "## Purpose\n\n"
    content += "[Describe the purpose of this directory]\n\n"
    content += "## Architecture\n\n"
    content += "[Describe the architecture and design patterns used]\n\n"
    content += "## Key Components\n\n"
    content += "[List and describe key components]\n\n"
    content += "## Dependencies\n\n"
    content += "[List dependencies and their purposes]\n\n"
    return content

def generate_file_md(file_path: Path, relative_to: Path) -> str:
    """
    Generate {filename}.md content for individual file documentation.

    Args:
        file_path: File to document
        relative_to: Base directory for relative paths

    Returns:
        Markdown content for file documentation
    """
    rel_path = file_path.relative_to(relative_to)
    content = f"# {file_path.name}\n\n"
    content += f"**Path**: `{rel_path}`\n\n"
    content += "## Purpose\n\n"
    content += "[Describe the purpose of this file]\n\n"
    content += "## Key Functions/Classes\n\n"
    content += "[List and describe key functions or classes]\n\n"
    content += "## Dependencies\n\n"
    content += "[List dependencies]\n\n"
    content += "## Change History\n\n"
    content += f"### {datetime.now().strftime('%Y-%m-%d')}: Initial documentation\n\n"
    content += "- Created documentation\n\n"
    return content

def sync_directory_docs(src_dir: Path, docs_dir: Path, auto: bool = False) -> int:
    """
    Recursively sync documentation for directory tree.

    Args:
        src_dir: Source directory to document
        docs_dir: Documentation output directory
        auto: If True, overwrite existing files

    Returns:
        Number of files generated
    """
    count = 0

    # Create docs directory if not exists
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Generate index.md
    index_path = docs_dir / "index.md"
    if auto or not index_path.exists():
        index_content = generate_index_md(src_dir, src_dir.parent)
        index_path.write_text(index_content, encoding="utf-8")
        count += 1

    # Generate README.md
    readme_path = docs_dir / "README.md"
    if auto or not readme_path.exists():
        readme_content = generate_readme_md(src_dir, src_dir.parent)
        readme_path.write_text(readme_content, encoding="utf-8")
        count += 1

    # Generate file documentation
    try:
        for item in sorted(src_dir.iterdir()):
            if item.name.startswith("."):
                continue
            if item.name in ["node_modules", "__pycache__", "venv", "env", "dist", "build"]:
                continue

            if item.is_file():
                # Generate {filename}.md
                doc_path = docs_dir / f"{item.stem}.md"
                if auto or not doc_path.exists():
                    file_content = generate_file_md(item, src_dir.parent)
                    doc_path.write_text(file_content, encoding="utf-8")
                    count += 1

            elif item.is_dir():
                # Recursively process subdirectory
                sub_docs_dir = docs_dir / item.name
                count += sync_directory_docs(item, sub_docs_dir, auto)

    except PermissionError:
        console.print(f"[yellow]Warning:[/yellow] Permission denied for {src_dir}")

    return count

def get_changed_files(project_dir: Path) -> list[str]:
    """
    Get list of changed files using git diff.

    Args:
        project_dir: Project directory path

    Returns:
        List of changed file paths relative to project directory
    """
    try:
        # Get git diff for staged and unstaged changes
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            check=True
        )

        changed_files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return changed_files

    except subprocess.CalledProcessError:
        # Not a git repository or no changes
        return []

def find_doc_file(file_path: Path, docs_dir: Path) -> Optional[Path]:
    """
    Find corresponding documentation file for a source file.

    Args:
        file_path: Source file path (relative to project root)
        docs_dir: Documentation directory (.grove/docs/)

    Returns:
        Path to documentation file, or None if not found
    """
    # Extract relative path components
    parts = file_path.parts

    # Skip initial directories until we find src, app, lib, etc.
    src_index = -1
    for i, part in enumerate(parts):
        if part in ["src", "app", "lib", "pkg", "source", "code", "core"]:
            src_index = i
            break

    if src_index == -1:
        return None

    # Construct documentation path
    # docs_dir / src / ... / {filename}.md
    src_name = parts[src_index]
    relative_parts = parts[src_index + 1:]

    if len(relative_parts) == 0:
        return None

    # Build path to documentation file
    doc_path = docs_dir / src_name
    for part in relative_parts[:-1]:
        doc_path = doc_path / part

    # Get filename without extension
    filename = relative_parts[-1]
    stem = Path(filename).stem
    doc_path = doc_path / f"{stem}.md"

    return doc_path if doc_path.exists() else None

def append_change_history(doc_file: Path, message: str, timestamp: datetime) -> None:
    """
    Append change history to documentation file.

    Args:
        doc_file: Documentation file path
        message: Change message
        timestamp: Change timestamp
    """
    # Read existing content
    content = doc_file.read_text(encoding="utf-8")

    # Check if "## Change History" section exists
    if "## Change History" not in content:
        # Add Change History section before the end
        content += f"\n## Change History\n\n"

    # Format new entry
    date_str = timestamp.strftime("%Y-%m-%d")
    entry = f"### {date_str}: Implementation update\n\n- {message}\n\n"

    # Insert after "## Change History" header
    lines = content.splitlines(keepends=True)
    new_lines = []
    inserted = False

    for i, line in enumerate(lines):
        new_lines.append(line)
        if "## Change History" in line and not inserted:
            # Skip empty lines after header
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                new_lines.append(lines[j])
                j += 1

            # Insert new entry
            new_lines.append(entry)
            inserted = True

            # Add remaining lines
            new_lines.extend(lines[j:])
            break

    # Write updated content
    doc_file.write_text("".join(new_lines), encoding="utf-8")

def record_implementation_changes(project_dir: Path) -> int:
    """
    Record implementation changes to documentation files.

    Args:
        project_dir: Project directory path

    Returns:
        Number of documentation files updated
    """
    # Get changed files
    changed_files = get_changed_files(project_dir)
    if not changed_files:
        return 0

    docs_dir = project_dir / ".grove" / "docs"
    if not docs_dir.exists():
        return 0

    count = 0
    timestamp = datetime.now()
    today_str = timestamp.strftime("%Y-%m-%d")

    for file_str in changed_files:
        file_path = Path(file_str)

        # Find corresponding documentation file
        doc_file = find_doc_file(file_path, docs_dir)
        if doc_file:
            # Check if documentation already has today's update
            if doc_file.exists():
                content = doc_file.read_text(encoding="utf-8")
                if f"### {today_str}:" in content:
                    # Already updated today, skip
                    continue

            # Append change history only if not updated today
            message = f"Updated {file_path.name}"
            append_change_history(doc_file, message, timestamp)
            count += 1

    return count

# =============================================================================
# Phase 3: Spec-Driven Commands
# =============================================================================

class AgentExecutor:
    """Execute commands with specific AI agent."""

    def __init__(self, agent_name: str, project_dir: Path):
        """
        Initialize AgentExecutor.

        Args:
            agent_name: Agent name (claude, codex, gemini, etc.)
            project_dir: Project directory path
        """
        if agent_name not in AGENT_CONFIG:
            raise ValueError(f"Unknown agent: {agent_name}")

        self.agent = agent_name
        self.config = AGENT_CONFIG[agent_name]
        self.project_dir = project_dir

    def execute(self, command: str, prompt: str = "", template_content: Optional[str] = None) -> Path:
        """
        Execute agent command and return output file path.

        Args:
            command: Command name (constitution, specify, plan, etc.)
            prompt: Additional prompt text
            template_content: Template content to include in prompt (if enabled)

        Returns:
            Path to generated output file

        Raises:
            RuntimeError: If execution fails
        """
        console.print(f"[cyan]Executing /{command} with {self.config['name']}...[/cyan]")

        # Execute based on agent type
        if self.agent == "claude":
            return self._execute_claude(command, prompt, template_content)
        elif self.agent == "codex":
            return self._execute_codex(command, prompt, template_content)
        elif self.agent == "gemini":
            return self._execute_gemini(command, prompt, template_content)
        else:
            # Generic execution for other agents
            return self._execute_generic(command, prompt, template_content)

    def _execute_claude(self, command: str, prompt: str = "", template_content: Optional[str] = None) -> Path:
        """Execute command with Claude Code."""
        # Check if Claude is installed
        if not check_tool("claude"):
            raise RuntimeError("Claude Code is not installed. Install from: https://docs.anthropic.com/en/docs/claude-code/setup")

        # Build slash command prompt
        slash_command = f"/grove.{command}"

        # Add template content if provided
        if template_content:
            slash_command += f"\n\nTemplate:\n{template_content}"

        if prompt:
            slash_command += f"\n\n{prompt}"

        # Add async subagent for implement command
        if command == "implement":
            slash_command += """

Spawn async subagent to monitor file changes and update documentation:

Your task is to run in the background and monitor for file changes during implementation. When you detect changes:

1. **For new files**:
   - Generate documentation in `.grove/docs/` following the project structure
   - Use the same format as existing docs (Purpose, Key Functions/Classes, Dependencies, Change History)
   - Place docs in the correct subdirectory mirroring source structure

2. **For modified files**:
   - Append change history entry with timestamp and description
   - Update the file documentation if significant changes occurred

3. **For deleted files**:
   - Append deletion note to the corresponding documentation

Continue monitoring until the main implementation task completes, then notify completion.
"""

        # Execute Claude Code
        try:
            # Change to project directory
            original_dir = Path.cwd()
            os.chdir(self.project_dir)

            # Run claude command with slash command as prompt
            result = subprocess.run(
                ["claude", "--print", slash_command],
                check=True,
                capture_output=True,
                text=True
            )

            os.chdir(original_dir)

            # Determine output path based on command
            output_path = self._get_output_path(command)
            console.print(f"[green]✓[/green] Command completed")

            # Display Claude's output
            if result.stdout:
                console.print(f"\n[dim]{result.stdout}[/dim]")

            return output_path

        except subprocess.CalledProcessError as e:
            os.chdir(original_dir)
            console.print(f"[red]Error executing Claude Code:[/red] {e}")
            if e.stderr:
                console.print(f"[dim]{e.stderr}[/dim]")
            raise RuntimeError(f"Claude Code execution failed: {e}")

    def _execute_codex(self, command: str, prompt: str = "", template_content: Optional[str] = None) -> Path:
        """Execute command with Codex CLI."""
        if not check_tool("codex"):
            raise RuntimeError("Codex CLI is not installed. Install from: https://github.com/openai/codex")

        # Similar to Claude, but with codex CLI syntax
        slash_command = f"/grove.{command}"

        # Add template content if provided
        if template_content:
            slash_command += f"\n\nTemplate:\n{template_content}"

        if prompt:
            slash_command += f"\n\n{prompt}"

        # Add task-based documentation update instruction for implement command
        if command == "implement":
            slash_command += """

IMPORTANT - Documentation Update:

After completing each task, update the documentation:

1. List files you changed
2. Update corresponding documentation in `.grove/docs/`:
   - New files: Create new documentation
   - Modified files: Append change entry to Change History section
   - Deleted files: Add deletion note to documentation
3. Proceed to next task
"""

        try:
            original_dir = Path.cwd()
            os.chdir(self.project_dir)

            # Run codex command (adjust based on actual codex CLI)
            subprocess.run(
                ["codex", "run", "--command", slash_command],
                check=True,
                capture_output=True,
                text=True
            )

            os.chdir(original_dir)

            output_path = self._get_output_path(command)
            console.print(f"[green]✓[/green] Command completed")

            return output_path

        except subprocess.CalledProcessError as e:
            os.chdir(original_dir)
            console.print(f"[red]Error executing Codex:[/red] {e}")
            raise RuntimeError(f"Codex execution failed: {e}")

    def _execute_gemini(self, command: str, prompt: str = "", template_content: Optional[str] = None) -> Path:
        """Execute command with Gemini CLI."""
        if not check_tool("gemini"):
            raise RuntimeError("Gemini CLI is not installed. Install from: https://github.com/google-gemini/gemini-cli")

        slash_command = f"/grove.{command}"

        # Add template content if provided
        if template_content:
            slash_command += f"\n\nTemplate:\n{template_content}"

        if prompt:
            slash_command += f"\n\n{prompt}"

        # Add task-based documentation update instruction for implement command
        if command == "implement":
            slash_command += """

IMPORTANT - Documentation Update:

After completing each task, update the documentation:

1. List files you changed
2. Update corresponding documentation in `.grove/docs/`:
   - New files: Create new documentation
   - Modified files: Append change entry to Change History section
   - Deleted files: Add deletion note to documentation
3. Proceed to next task
"""

        try:
            original_dir = Path.cwd()
            os.chdir(self.project_dir)

            # Run gemini-cli command
            subprocess.run(
                ["gemini-cli", "execute", slash_command],
                check=True,
                capture_output=True,
                text=True
            )

            os.chdir(original_dir)

            output_path = self._get_output_path(command)
            console.print(f"[green]✓[/green] Command completed")

            return output_path

        except subprocess.CalledProcessError as e:
            os.chdir(original_dir)
            console.print(f"[red]Error executing Gemini CLI:[/red] {e}")
            raise RuntimeError(f"Gemini CLI execution failed: {e}")

    def _execute_generic(self, command: str, _prompt: str = "", _template_content: Optional[str] = None) -> Path:
        """Generic execution for other agents (placeholder)."""
        console.print(f"[yellow]Warning:[/yellow] Generic execution for {self.agent} not fully implemented")
        console.print(f"[yellow]Please manually run:[/yellow] /grove.{command}")

        # Return expected output path
        return self._get_output_path(command)

    def _get_output_path(self, command: str) -> Path:
        """Get output path for command based on responsibility separation architecture."""
        if command == "constitution":
            return self.project_dir / ".claude" / "rules" / "constitution.md"
        elif command in ["specify", "plan", "tasks"]:
            # TODO: Determine feature-id from git branch or environment variable
            feature_id = "current"
            specs_dir = self.project_dir / ".grove" / "specs" / feature_id
            return specs_dir / f"{command}.md"
        elif command == "implement":
            # implement doesn't generate a file, executes implementation
            return self.project_dir
        else:
            return self.project_dir / f"{command}.md"


@app.command()
def workflow(
    prompt: str = typer.Argument(..., help="Feature description"),
    ai: str = typer.Option(None, "--ai", help="AI agent to use for all steps"),
    project_dir: Path = typer.Option(None, "--dir", help="Project directory"),
):
    """
    Execute complete SDD workflow: constitution → specify → design → plan → tasks → implement

    Examples:
        grove workflow "Add user authentication" --ai claude
        grove workflow "Add dark mode"
    """
    if project_dir is None:
        project_dir = Path.cwd()

    # Select agent
    if ai:
        selected_agent = ai
    else:
        selected_agent = select_agent_interactive()

    ensure_agent_installed(selected_agent, project_dir)

    console.print(Panel(
        f"[bold cyan]Starting SDD Workflow[/bold cyan]\n\n"
        f"Feature: {prompt}\n"
        f"Agent: {AGENT_CONFIG[selected_agent]['name']}\n"
        f"Project: {project_dir}",
        title="Workflow Execution",
        border_style="cyan"
    ))

    # Step 1: Constitution (if not exists)
    console.print("\n[bold cyan]Step 1: Constitution[/bold cyan]")
    constitution_path = project_dir / ".claude" / "rules" / "constitution.md"
    if not constitution_path.exists():
        console.print("[cyan]Creating constitution...[/cyan]")
        template_content = load_template_if_enabled("constitution", project_dir)
        executor = AgentExecutor(selected_agent, project_dir)
        executor.execute("constitution", template_content=template_content)
        console.print("[green]✓[/green] Constitution created")
    else:
        console.print("[dim]Constitution already exists, skipping...[/dim]")

    # Step 2: Specify
    console.print("\n[bold cyan]Step 2: Specification[/bold cyan]")
    template_content = load_template_if_enabled("specify", project_dir)
    executor = AgentExecutor(selected_agent, project_dir)
    executor.execute("specify", prompt, template_content=template_content)
    console.print("[green]✓[/green] Specification created")

    # Step 3: Design
    console.print("\n[bold cyan]Step 3: Design[/bold cyan]")
    template_content = load_template_if_enabled("design", project_dir)
    executor.execute("design", template_content=template_content)
    console.print("[green]✓[/green] Design-creator skill created")

    # Step 4: Plan
    console.print("\n[bold cyan]Step 4: Implementation Plan[/bold cyan]")
    template_content = load_template_if_enabled("plan", project_dir)
    executor.execute("plan", template_content=template_content)
    console.print("[green]✓[/green] Plan created")

    # Step 5: Tasks
    console.print("\n[bold cyan]Step 5: Task Breakdown[/bold cyan]")
    template_content = load_template_if_enabled("tasks", project_dir)
    executor.execute("tasks", template_content=template_content)
    console.print("[green]✓[/green] Tasks created")

    # Step 6: Implement
    console.print("\n[bold cyan]Step 6: Implementation[/bold cyan]")
    executor.execute("implement")

    # Record implementation changes
    console.print("\n[cyan]Recording implementation changes...[/cyan]")
    updated_count = record_implementation_changes(project_dir)
    if updated_count > 0:
        console.print(f"[green]✓[/green] Updated {updated_count} documentation file(s)")
    else:
        console.print("[dim]No documentation updates needed[/dim]")

    console.print("\n[bold green]✓ Workflow completed successfully![/bold green]")

# =============================================================================
# Phase 4: Document Management (Skeleton Implementation)
# =============================================================================

@app.command()
def sync(
    project_dir: Path = typer.Option(None, "--dir", help="Project directory (default: current)"),
    src: str = typer.Option(None, "--src", help="Source directory (default: auto-detect)"),
    auto: bool = typer.Option(False, "--auto", help="Auto-generate/overwrite all docs"),
):
    """
    Sync project documentation to .grove/docs/

    Automatically generates hierarchical documentation for your source code.
    Each directory gets index.md (structure), README.md (overview), and {filename}.md (details).

    Examples:
        grove sync
        grove sync --src src
        grove sync --auto
    """
    if project_dir is None:
        project_dir = Path.cwd()

    # Claude Code environment detection (environment variable only, no --ai parameter)
    if os.getenv("CLAUDE_CODE_VERSION") is not None:
        console.print("[cyan]Claude Code detected[/cyan]")
        console.print("[yellow]Execute: /grove.sync[/yellow]")
        console.print("[dim]This will use the sync-knowledge skill[/dim]")
        return

    console.print("[cyan]Syncing project documentation...[/cyan]\n")

    # Detect or use specified source directory
    if src:
        src_dir = project_dir / src
        if not src_dir.exists():
            console.print(f"[red]Error:[/red] Source directory '{src}' not found")
            raise typer.Exit(1)
    else:
        src_dir = detect_source_directory(project_dir)
        if src_dir is None:
            console.print("[yellow]Warning:[/yellow] Could not auto-detect source directory")
            console.print("[dim]Specify with --src, or use one of: src, app, lib, pkg, source, code, core[/dim]")
            raise typer.Exit(1)

    console.print(f"  Source directory: {src_dir.relative_to(project_dir)}")

    # Create documentation directory
    docs_dir = project_dir / ".grove" / "docs" / src_dir.name
    console.print(f"  Documentation output: {docs_dir.relative_to(project_dir)}\n")

    # Sync documentation
    try:
        count = sync_directory_docs(src_dir, docs_dir, auto)
        console.print(f"\n[green]✓[/green] Documentation synced successfully")
        console.print(f"  Generated/updated {count} file(s)")
        console.print(f"  Output: {docs_dir.relative_to(project_dir)}")

    except Exception as e:
        console.print(f"[red]Error syncing documentation:[/red] {e}")
        raise typer.Exit(1)

def main():
    app()

if __name__ == "__main__":
    main()

