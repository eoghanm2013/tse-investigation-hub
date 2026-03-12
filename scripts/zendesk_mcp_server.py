#!/usr/bin/env python3
"""
Zendesk MCP Server for Cursor AI

Provides Model Context Protocol interface to Zendesk Support API.
Allows reading, searching, and updating Zendesk tickets.

Usage (via uvx):
    uvx scripts/zendesk_mcp_server.py \\
        --subdomain YOUR_SUBDOMAIN \\
        --email your.email@company.com \\
        --token YOUR_ZENDESK_API_TOKEN \\
        --read-only
"""

import json
import sys
import argparse
import base64
import urllib.request
import urllib.error
import urllib.parse
from typing import Any, Dict, List, Optional
from datetime import datetime


class ZendeskClient:
    """Zendesk API client for MCP server."""
    
    def __init__(self, subdomain: str, email: str, token: str, read_only: bool = True):
        self.subdomain = subdomain
        self.email = email
        self.token = token
        self.read_only = read_only
        self.base_url = f"https://{subdomain}.zendesk.com/api/v2"
    
    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[dict] = None) -> dict:
        """Make authenticated request to Zendesk API."""
        url = f"{self.base_url}/{endpoint}"
        
        # Basic auth: email/token:token base64 encoded
        credentials = base64.b64encode(f"{self.email}/token:{self.token}".encode()).decode()
        
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
            error_body = e.read().decode() if e.fp else ""
            return {"error": f"HTTP {e.code}: {e.reason}", "details": error_body}
        except Exception as e:
            return {"error": str(e)}
    
    def get_ticket(self, ticket_id: str) -> dict:
        """Get a single ticket by ID."""
        return self._make_request(f"tickets/{ticket_id}.json")
    
    def list_tickets(self, status: str = "open", per_page: int = 25) -> dict:
        """List tickets by status."""
        # Sort by updated_at descending
        params = urllib.parse.urlencode({"status": status, "per_page": per_page, "sort_by": "updated_at", "sort_order": "desc"})
        return self._make_request(f"tickets.json?{params}")
    
    def search_tickets(self, query: str, per_page: int = 25) -> dict:
        """Search tickets using Zendesk search query syntax."""
        params = urllib.parse.urlencode({"query": f"type:ticket {query}", "per_page": per_page})
        return self._make_request(f"search.json?{params}")
    
    def get_ticket_comments(self, ticket_id: str) -> dict:
        """Get all comments for a ticket."""
        return self._make_request(f"tickets/{ticket_id}/comments.json")
    
    def add_comment(self, ticket_id: str, comment: str, public: bool = False) -> dict:
        """Add a comment to a ticket (requires write access)."""
        if self.read_only:
            return {"error": "Server is in read-only mode"}
        
        data = {
            "ticket": {
                "comment": {
                    "body": comment,
                    "public": public
                }
            }
        }
        return self._make_request(f"tickets/{ticket_id}.json", method="PUT", data=data)
    
    def update_ticket(self, ticket_id: str, updates: dict) -> dict:
        """Update ticket fields (requires write access)."""
        if self.read_only:
            return {"error": "Server is in read-only mode"}
        
        data = {"ticket": updates}
        return self._make_request(f"tickets/{ticket_id}.json", method="PUT", data=data)


class MCPServer:
    """Model Context Protocol server implementation."""
    
    def __init__(self, client: ZendeskClient):
        self.client = client
    
    def handle_tools_list(self) -> dict:
        """Return available tools."""
        tools = [
            {
                "name": "zendesk_get_ticket",
                "description": "Get details of a specific Zendesk ticket by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "Ticket ID (e.g., '12345')"
                        }
                    },
                    "required": ["ticket_id"]
                }
            },
            {
                "name": "zendesk_list_tickets",
                "description": "List tickets by status (open, pending, solved, closed)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "description": "Ticket status filter",
                            "enum": ["new", "open", "pending", "hold", "solved", "closed"],
                            "default": "open"
                        },
                        "per_page": {
                            "type": "integer",
                            "description": "Number of results per page (max 100)",
                            "default": 25
                        }
                    }
                }
            },
            {
                "name": "zendesk_search_tickets",
                "description": "Search tickets using Zendesk query syntax. Examples: 'status:open priority:urgent', 'tags:security', 'subject:error'",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (Zendesk syntax)"
                        },
                        "per_page": {
                            "type": "integer",
                            "description": "Number of results per page (max 100)",
                            "default": 25
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "zendesk_get_comments",
                "description": "Get all comments for a specific ticket",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "Ticket ID"
                        }
                    },
                    "required": ["ticket_id"]
                }
            }
        ]
        
        # Add write tools if not read-only
        if not self.client.read_only:
            tools.extend([
                {
                    "name": "zendesk_add_comment",
                    "description": "Add a comment to a ticket (internal or public)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "ticket_id": {"type": "string", "description": "Ticket ID"},
                            "comment": {"type": "string", "description": "Comment body"},
                            "public": {"type": "boolean", "description": "Whether comment is public to customer", "default": False}
                        },
                        "required": ["ticket_id", "comment"]
                    }
                },
                {
                    "name": "zendesk_update_ticket",
                    "description": "Update ticket fields (status, priority, tags, etc.)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "ticket_id": {"type": "string", "description": "Ticket ID"},
                            "updates": {
                                "type": "object",
                                "description": "Fields to update (e.g., {status: 'pending', priority: 'high'})"
                            }
                        },
                        "required": ["ticket_id", "updates"]
                    }
                }
            ])
        
        return {"tools": tools}
    
    def handle_tool_call(self, name: str, arguments: dict) -> dict:
        """Execute a tool call."""
        try:
            if name == "zendesk_get_ticket":
                result = self.client.get_ticket(arguments["ticket_id"])
            elif name == "zendesk_list_tickets":
                result = self.client.list_tickets(
                    status=arguments.get("status", "open"),
                    per_page=arguments.get("per_page", 25)
                )
            elif name == "zendesk_search_tickets":
                result = self.client.search_tickets(
                    query=arguments["query"],
                    per_page=arguments.get("per_page", 25)
                )
            elif name == "zendesk_get_comments":
                result = self.client.get_ticket_comments(arguments["ticket_id"])
            elif name == "zendesk_add_comment":
                result = self.client.add_comment(
                    ticket_id=arguments["ticket_id"],
                    comment=arguments["comment"],
                    public=arguments.get("public", False)
                )
            elif name == "zendesk_update_ticket":
                result = self.client.update_ticket(
                    ticket_id=arguments["ticket_id"],
                    updates=arguments["updates"]
                )
            else:
                result = {"error": f"Unknown tool: {name}"}
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2)
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({"error": str(e)}, indent=2)
                    }
                ],
                "isError": True
            }
    
    def handle_message(self, message: dict) -> dict:
        """Handle incoming MCP message."""
        method = message.get("method")
        
        if method == "tools/list":
            return self.handle_tools_list()
        elif method == "tools/call":
            params = message.get("params", {})
            return self.handle_tool_call(params.get("name"), params.get("arguments", {}))
        elif method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "zendesk-mcp-server",
                    "version": "1.0.0"
                }
            }
        else:
            return {"error": f"Unknown method: {method}"}
    
    def run(self):
        """Run the MCP server (stdio transport)."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            try:
                message = json.loads(line)
                response = self.handle_message(message)
                
                # Add jsonrpc and id to response
                response["jsonrpc"] = "2.0"
                if "id" in message:
                    response["id"] = message["id"]
                
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32700, "message": "Parse error"},
                    "id": None
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32603, "message": str(e)},
                    "id": message.get("id") if 'message' in locals() else None
                }
                print(json.dumps(error_response), flush=True)


def main():
    parser = argparse.ArgumentParser(description="Zendesk MCP Server")
    parser.add_argument("--subdomain", required=True, help="Zendesk subdomain (e.g., 'mycompany')")
    parser.add_argument("--email", required=True, help="Zendesk user email")
    parser.add_argument("--token", required=True, help="Zendesk API token")
    parser.add_argument("--read-only", action="store_true", help="Enable read-only mode (no write operations)")
    
    args = parser.parse_args()
    
    client = ZendeskClient(
        subdomain=args.subdomain,
        email=args.email,
        token=args.token,
        read_only=args.read_only
    )
    
    server = MCPServer(client)
    server.run()


if __name__ == "__main__":
    main()

