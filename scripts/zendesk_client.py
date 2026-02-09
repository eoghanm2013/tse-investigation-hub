#!/usr/bin/env python3
"""
Zendesk Client for TSE Hub

Utility for querying and managing Zendesk tickets.
Reads credentials from ../.env file.

Usage:
    python zendesk_client.py get 12345              # Get single ticket
    python zendesk_client.py list --status open     # List open tickets
    python zendesk_client.py search "priority:urgent"  # Search tickets
    python zendesk_client.py archive 12345          # Archive ticket to markdown
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Load environment from .env
def load_env():
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        print(f"Error: .env file not found at {env_path}")
        sys.exit(1)
    
    env = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    return env

ENV = load_env()
SUBDOMAIN = ENV.get("ZENDESK_SUBDOMAIN")
EMAIL = ENV.get("ZENDESK_EMAIL")
TOKEN = ENV.get("ZENDESK_API_TOKEN")

if not all([SUBDOMAIN, EMAIL, TOKEN]):
    print("Error: Missing required environment variables:")
    print("  ZENDESK_SUBDOMAIN, ZENDESK_EMAIL, ZENDESK_API_TOKEN")
    sys.exit(1)

BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2"


def make_request(endpoint: str, method: str = "GET", data: Optional[dict] = None) -> dict:
    """Make authenticated request to Zendesk API."""
    url = f"{BASE_URL}/{endpoint}"
    
    # Basic auth: email/token:token base64 encoded
    credentials = base64.b64encode(f"{EMAIL}/token:{TOKEN}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {credentials}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    req_data = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        if e.fp:
            print(e.read().decode())
        sys.exit(1)


def get_ticket(ticket_id: str) -> dict:
    """Fetch a single Zendesk ticket."""
    return make_request(f"tickets/{ticket_id}.json")


def list_tickets(status: str = "open", per_page: int = 25) -> List[dict]:
    """List tickets by status."""
    params = urllib.parse.urlencode({
        "status": status,
        "per_page": per_page,
        "sort_by": "updated_at",
        "sort_order": "desc"
    })
    result = make_request(f"tickets.json?{params}")
    return result.get("tickets", [])


def search_tickets(query: str, per_page: int = 25) -> List[dict]:
    """Search tickets using Zendesk search syntax."""
    params = urllib.parse.urlencode({
        "query": f"type:ticket {query}",
        "per_page": per_page
    })
    result = make_request(f"search.json?{params}")
    return result.get("results", [])


def get_ticket_comments(ticket_id: str) -> List[dict]:
    """Get all comments for a ticket."""
    result = make_request(f"tickets/{ticket_id}/comments.json")
    return result.get("comments", [])


def format_ticket_markdown(ticket_data: dict, include_comments: bool = True) -> str:
    """Convert Zendesk ticket to markdown format."""
    ticket = ticket_data.get("ticket", ticket_data)
    
    # Extract key fields
    ticket_id = ticket.get("id", "Unknown")
    subject = ticket.get("subject", "No subject")
    status = ticket.get("status", "unknown").upper()
    priority = ticket.get("priority", "unknown")
    created_at = ticket.get("created_at", "")[:10]
    updated_at = ticket.get("updated_at", "")[:10]
    
    # Requester and assignee
    requester_id = ticket.get("requester_id", "Unknown")
    assignee_id = ticket.get("assignee_id", "Unassigned")
    
    # Tags
    tags = ticket.get("tags", [])
    
    # Description (first comment is the description)
    description = ticket.get("description", "No description")
    
    md = f"""# ZD-{ticket_id}: {subject}

## Metadata
| Field | Value |
|-------|-------|
| **Status** | {status} |
| **Priority** | {priority} |
| **Requester ID** | {requester_id} |
| **Assignee ID** | {assignee_id} |
| **Created** | {created_at} |
| **Updated** | {updated_at} |
| **Tags** | {', '.join(tags) if tags else 'None'} |
| **URL** | https://{SUBDOMAIN}.zendesk.com/agent/tickets/{ticket_id} |

## Description
{description}
"""
    
    # Optionally add comments
    if include_comments:
        comments = get_ticket_comments(str(ticket_id))
        if comments:
            md += "\n## Comments\n"
            for c in comments:
                author_id = c.get("author_id", "Unknown")
                created = c.get("created_at", "")[:10]
                body = c.get("body", "")
                public = "Public" if c.get("public", False) else "Internal"
                md += f"\n### Author {author_id} ({created}) [{public}]\n{body}\n"
    
    md += f"\n---\n*Archived: {datetime.now().isoformat()}*\n"
    return md


def archive_ticket(ticket_id: str):
    """Fetch ticket and save to archive folder, organized by MM-YYYY."""
    archive_dir = Path(__file__).parent.parent / "archive"
    archive_dir.mkdir(exist_ok=True)
    
    print(f"Fetching ZD-{ticket_id}...")
    ticket_data = get_ticket(ticket_id)
    ticket = ticket_data.get("ticket", {})
    
    # Get created date for folder organization
    created = ticket.get("created_at", "")
    if created and len(created) >= 10:
        # Format: 2026-01-22T... → 01-2026
        year = created[0:4]
        month = created[5:7]
        folder_name = f"{month}-{year}"
    else:
        folder_name = "unknown"
    
    # Create month folder if needed
    month_folder = archive_dir / folder_name
    month_folder.mkdir(parents=True, exist_ok=True)
    
    md = format_ticket_markdown(ticket_data, include_comments=True)
    
    output_path = month_folder / f"ZD-{ticket_id}.md"
    with open(output_path, "w") as f:
        f.write(md)
    
    print(f"Archived to {output_path}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "get" and len(sys.argv) >= 3:
        ticket = get_ticket(sys.argv[2])
        print(format_ticket_markdown(ticket, include_comments=False))
    
    elif command == "list":
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--status", default="open", help="Ticket status")
        parser.add_argument("--per-page", type=int, default=25, help="Results per page")
        args, _ = parser.parse_known_args(sys.argv[2:])
        
        tickets = list_tickets(status=args.status, per_page=args.per_page)
        for t in tickets:
            ticket_id = t.get("id")
            subject = t.get("subject", "")[:60]
            status = t.get("status", "").upper()
            priority = t.get("priority", "")
            print(f"ZD-{ticket_id}: {subject}... [{status}] [{priority}]")
    
    elif command == "search" and len(sys.argv) >= 3:
        query = sys.argv[2]
        tickets = search_tickets(query)
        for t in tickets:
            ticket_id = t.get("id")
            subject = t.get("subject", "")[:60]
            status = t.get("status", "").upper()
            print(f"ZD-{ticket_id}: {subject}... [{status}]")
    
    elif command == "archive" and len(sys.argv) >= 3:
        archive_ticket(sys.argv[2])
    
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()

