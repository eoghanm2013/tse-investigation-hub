# TSE Investigation Hub

Centralized workspace for Technical Support Engineers working on Datadog customer cases.

> **New here?** Follow the **[Setup Guide](SETUP.md)** for step-by-step instructions.

---

## Quick Start

### 1. Clone/Create the workspace
```bash
cd ~/
git clone git@github.com:YOUR_ORG/tse-investigation-hub.git
# OR if starting fresh:
mkdir tse-investigation-hub && cd tse-investigation-hub
```

### 2. Set up credentials
```bash
cp .env.example .env
# Edit .env with your Zendesk, Atlassian, and GitHub tokens
```

### 3. Configure MCP (Cursor AI)
```bash
cp .cursor/mcp.json.example .cursor/mcp.json
# Edit .cursor/mcp.json with your tokens
```

### 4. Install dependencies
```bash
# Install uv (for MCP servers)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 5. Restart Cursor
Quit completely (Cmd+Q) and reopen.

### 6. Test it
Ask Cursor:
> "Use MCP to fetch Zendesk ticket 12345"

---

## Structure

```
tse-investigation-hub/
├── .cursor/
│   ├── mcp.json              # YOUR config (gitignored)
│   └── mcp.json.example      # Template
├── .cursorrules              # AI behavior for TSEs
├── cases/                    # Active customer cases
│   ├── .template/            # Template for new cases
│   └── ZD-XXXXXX/            # One folder per ticket (gitignored)
├── archive/                  # Archived cases by month (gitignored)
├── docs/                     # Product documentation
│   ├── apm/                  # Application Performance Monitoring
│   ├── infrastructure/       # Infrastructure monitoring
│   ├── logs/                 # Log management
│   ├── rum/                  # Real User Monitoring
│   ├── synthetics/           # Synthetic monitoring
│   ├── security/             # Security products
│   ├── network/              # Network monitoring
│   ├── platform/             # Billing, API, auth
│   └── common/               # Agent, integrations
├── templates/                # Customer communication templates
│   ├── customer-communication/
│   └── escalation/
├── solutions/                # Known issues & workarounds
├── scripts/                  # Utility scripts
└── reference/                # Reference materials
```

---

## Workflow

### Starting a Case Investigation

**Option 1: Ask Cursor**
> "Investigate Zendesk ticket 12345"

Cursor will:
1. Fetch the ticket from Zendesk
2. Assess what info you have
3. Search for similar historical cases
4. Create case notes in `cases/ZD-12345/`

**Option 2: Manual**
```bash
cp -r cases/.template cases/ZD-12345
```

### During Investigation
- Cursor pulls live Zendesk data via MCP
- Drop logs, screenshots, flares into `cases/ZD-12345/assets/`
- Document findings in `notes.md`
- Search archive for similar past cases
- Check `solutions/known-issues.md` for tracked bugs

### Customer Communication
Use templates from `templates/customer-communication/`:
- Acknowledgment
- Requesting information
- Providing solution
- Escalation notice

### When to Escalate to TEE
Check `docs/escalation-criteria.md` for guidance on:
- When to escalate vs. continue troubleshooting
- What info to include in escalation
- How to create JIRA escalation ticket

### Archiving Cases
```bash
python scripts/zendesk_client.py archive 12345
```

---

## API Access

### Zendesk (Primary)
- **READ/WRITE** access to customer tickets
- View, update, comment on cases
- Search ticket history

### JIRA (For Escalations)
- **READ-ONLY by default**
- Create escalation tickets when needed
- Reference existing engineering tickets

### GitHub (For Research)
- **READ-ONLY**
- Search Datadog codebases during investigations

### Confluence (Documentation)
- **READ-ONLY**
- Access internal documentation
- Search troubleshooting guides

---

## Product Areas

| Area | Description |
|------|-------------|
| **APM** | Application Performance Monitoring, traces, profiling |
| **Infrastructure** | Hosts, containers, agent installation |
| **Logs** | Log management, pipelines, parsing |
| **RUM** | Real User Monitoring, Session Replay |
| **Synthetics** | Synthetic monitoring, API tests, browser tests |
| **Security** | AppSec, SIEM, CWS, CSPM, Vulnerability Management |
| **Network** | Network Performance Monitoring, NetFlow |
| **Platform** | Billing, API, authentication, integrations |

---

## Scripts

### zendesk_client.py
```bash
# Get a ticket
python scripts/zendesk_client.py get 12345

# List open tickets
python scripts/zendesk_client.py list --status open

# Search tickets
python scripts/zendesk_client.py search "priority:urgent"

# Archive ticket
python scripts/zendesk_client.py archive 12345
```

### jira_client.py
```bash
# Search for related escalations
python scripts/jira_client.py search "status = Open AND labels = security"

# Get escalation details
python scripts/jira_client.py get SCRS-1234
```

---

## Safety

⚠️ **Customer Data Protection**
- All case folders are gitignored
- Never commit customer data, logs, or PII
- Archive folders are gitignored
- Credentials stay local

📝 **Writing to Zendesk**
- Cursor can update tickets and add comments
- Always review before sending to customer
- Use internal comments for investigation notes

---

## Troubleshooting

### MCP not loading
1. Verify config: `cat .cursor/mcp.json`
2. Check uvx: `~/.local/bin/uvx --version`
3. Restart Cursor (Cmd+Q)

### Zendesk API errors
| Code | Issue | Fix |
|------|-------|-----|
| 401 | Bad token | Regenerate API token |
| 403 | No permissions | Check token is API token (not OAuth) |
| 429 | Rate limited | Wait 60 seconds |

---

## Contributing

1. Document solutions in `solutions/`
2. Create troubleshooting docs from resolved cases
3. Share communication templates
4. Keep product docs updated

---

**Questions?** Ask in #support or open an issue on this repo.

