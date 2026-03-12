#!/usr/bin/env python3
"""
TSE Investigation Hub - Automated Setup

Configures .env and .cursor/mcp.json from provided credentials.
Can be run interactively or with CLI arguments (for agent use).

Usage:
    Interactive:  python3 scripts/setup.py
    With args:    python3 scripts/setup.py --email you@datadoghq.com --zendesk-token XXX --atlassian-token YYY
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

# Datadog-specific defaults
ZENDESK_SUBDOMAIN = "datadog"
ATLASSIAN_DOMAIN = "datadoghq.atlassian.net"
JIRA_PROJECT_KEY = "SCRS"


def prompt(msg: str, default: str = "", required: bool = True, secret: bool = False) -> str:
    """Prompt the user for input with optional default."""
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{msg}{suffix}: ").strip()
        if not value and default:
            return default
        if value:
            return value
        if not required:
            return ""
        print("  This field is required.")


def check_uv() -> bool:
    """Check if uv/uvx is installed."""
    return shutil.which("uvx") is not None or shutil.which("uv") is not None


def install_uv() -> bool:
    """Install uv via the official installer."""
    print("\nInstalling uv...")
    try:
        subprocess.run(
            ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"],
            check=True,
        )
        print("uv installed successfully.")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install uv. Install manually: https://docs.astral.sh/uv/getting-started/installation/")
        return False


def write_env(email: str, zendesk_token: str, atlassian_token: str, github_token: str) -> Path:
    """Generate .env file."""
    env_path = ROOT_DIR / ".env"

    lines = [
        "# Zendesk Configuration",
        f"ZENDESK_SUBDOMAIN={ZENDESK_SUBDOMAIN}",
        f"ZENDESK_EMAIL={email}",
        f"ZENDESK_API_TOKEN={zendesk_token}",
        "",
        "# Atlassian Configuration (JIRA & Confluence)",
        f"ATLASSIAN_DOMAIN={ATLASSIAN_DOMAIN}",
        f"ATLASSIAN_EMAIL={email}",
        f"ATLASSIAN_API_TOKEN={atlassian_token}",
        "",
        "# JIRA Project Configuration",
        f"JIRA_PROJECT_KEY={JIRA_PROJECT_KEY}",
        "",
        "# GitHub Configuration (optional)",
        f"GITHUB_TOKEN={github_token}" if github_token else "# GITHUB_TOKEN=",
        "",
        "# Datadog API Keys (optional -- for API-based investigations)",
        "# DD_API_KEY=",
        "# DD_APP_KEY=",
    ]

    env_path.write_text("\n".join(lines) + "\n")
    return env_path


def write_mcp_json(email: str, zendesk_token: str, atlassian_token: str, github_token: str) -> Path:
    """Generate .cursor/mcp.json."""
    cursor_dir = ROOT_DIR / ".cursor"
    cursor_dir.mkdir(exist_ok=True)
    mcp_path = cursor_dir / "mcp.json"

    config: dict = {"mcpServers": {}}

    config["mcpServers"]["zendesk"] = {
        "command": "python3",
        "args": [
            "scripts/zendesk_mcp_server.py",
            "--subdomain", ZENDESK_SUBDOMAIN,
            "--email", email,
            "--token", zendesk_token,
        ],
    }

    config["mcpServers"]["atlassian"] = {
        "command": "uvx",
        "args": [
            "mcp-atlassian",
            "--jira-url", f"https://{ATLASSIAN_DOMAIN}",
            "--jira-username", email,
            "--jira-token", atlassian_token,
            "--confluence-url", f"https://{ATLASSIAN_DOMAIN}/wiki",
            "--confluence-username", email,
            "--confluence-token", atlassian_token,
            "--read-only",
        ],
    }

    if github_token:
        config["mcpServers"]["github"] = {
            "command": "uvx",
            "args": ["mcp-github"],
            "env": {"GITHUB_TOKEN": github_token},
        }

    mcp_path.write_text(json.dumps(config, indent=2) + "\n")
    return mcp_path


def ensure_directories():
    """Create required directories if they don't exist."""
    for name in ["cases", "archive"]:
        d = ROOT_DIR / name
        d.mkdir(exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="TSE Investigation Hub Setup")
    parser.add_argument("--email", help="Your work email (used for Zendesk and Atlassian)")
    parser.add_argument("--zendesk-token", help="Zendesk API token")
    parser.add_argument("--atlassian-token", help="Atlassian API token")
    parser.add_argument("--github-token", default="", help="GitHub PAT (optional)")
    parser.add_argument("--reconfigure", action="store_true", help="Overwrite existing config files")
    args = parser.parse_args()

    print("=" * 50)
    print("  TSE Investigation Hub - Setup")
    print("=" * 50)

    env_path = ROOT_DIR / ".env"
    mcp_path = ROOT_DIR / ".cursor" / "mcp.json"

    if env_path.exists() and not args.reconfigure:
        if not any([args.email, args.zendesk_token, args.atlassian_token]):
            resp = input("\n.env already exists. Overwrite? [y/N]: ").strip().lower()
            if resp != "y":
                print("Setup cancelled. Use --reconfigure to force.")
                sys.exit(0)

    interactive = not all([args.email, args.zendesk_token, args.atlassian_token])

    if interactive:
        print("\nI need a few credentials to configure the workspace.")
        print("See the README for where to generate each token.\n")
        email = args.email or prompt("Work email")
        zendesk_token = args.zendesk_token or prompt("Zendesk API token")
        atlassian_token = args.atlassian_token or prompt("Atlassian API token")
        github_token = args.github_token or prompt("GitHub PAT (Enter to skip)", required=False)
    else:
        email = args.email
        zendesk_token = args.zendesk_token
        atlassian_token = args.atlassian_token
        github_token = args.github_token

    print("\nWriting .env ...")
    write_env(email, zendesk_token, atlassian_token, github_token)
    print(f"  -> {env_path}")

    print("Writing .cursor/mcp.json ...")
    write_mcp_json(email, zendesk_token, atlassian_token, github_token)
    print(f"  -> {mcp_path}")

    ensure_directories()

    if not check_uv():
        print("\nuv/uvx not found (needed for Atlassian and GitHub MCP servers).")
        if interactive:
            resp = input("Install uv now? [Y/n]: ").strip().lower()
            if resp != "n":
                install_uv()
            else:
                print("Skipped. Install later: curl -LsSf https://astral.sh/uv/install.sh | sh")
        else:
            install_uv()
    else:
        print("\nuv/uvx found.")

    print("\n" + "=" * 50)
    print("  Setup complete!")
    print("=" * 50)
    print()
    print("Next step: Restart Cursor (Cmd+Q, then reopen).")
    print("Then try: \"Investigate Zendesk ticket 12345\"")
    print()


if __name__ == "__main__":
    main()
