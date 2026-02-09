# 🚀 TSE Investigation Hub - Setup Guide

Get up and running in ~15 minutes.

---

## Prerequisites

Before starting, ensure you have:

- [ ] **Cursor IDE** installed ([cursor.com](https://cursor.com))
- [ ] **Git** installed
- [ ] **Python 3.8+** installed
- [ ] Access to **Zendesk** (API token access)
- [ ] Access to **Datadog's Atlassian** (JIRA/Confluence)
- [ ] Access to **Datadog's GitHub org** (optional, for code research)

---

## Step 1: Set Up the Workspace

```bash
# Option A: Clone if this is a shared repo
git clone git@github.com:YOUR_ORG/tse-investigation-hub.git
cd tse-investigation-hub

# Option B: Use the existing folder if already created
cd ~/tse-investigation-hub
git init  # If you want to track it with git
```

---

## Step 2: Install `uv` (MCP Server Runner)

MCP servers run via `uvx`. Install it:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
~/.local/bin/uvx --version
```

If the command isn't found after installation, add to your shell profile:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## Step 3: Get Your API Tokens

### Zendesk API Token

1. Log into Zendesk as an Admin
2. Go to: **Admin Center → Apps and integrations → APIs → Zendesk API → Settings**
3. Under "Token Access", click **"Add API Token"**
4. Name it: `TSE Investigation Hub`
5. Copy the token (you won't see it again!)
6. Note your subdomain (e.g., `yourcompany` from `yourcompany.zendesk.com`)

### Atlassian Token (JIRA & Confluence)

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **"Create API token"**
3. Name it: `TSE Hub`
4. Copy the token

### GitHub Token (Optional)

1. Go to: https://github.com/settings/tokens?type=beta
2. Click **"Generate new token"**
3. Name it: `TSE Hub`
4. Set expiration (90 days recommended)
5. Under **"Repository access"**, select: `All repositories` (or specific Datadog repos)
6. Under **"Permissions"**, enable:
   - `Contents` → Read-only
   - `Metadata` → Read-only
7. Click **"Generate token"**
8. **Important:** For Datadog private repos, click **"Configure SSO"** and authorize for DataDog org

---

## Step 4: Configure Environment Variables

```bash
# Copy the template
cp .env.example .env

# Edit with your values
nano .env  # or use your preferred editor
```

Fill in your credentials:

```bash
# Zendesk
ZENDESK_SUBDOMAIN=yourcompany
ZENDESK_EMAIL=your.email@company.com
ZENDESK_API_TOKEN=paste_your_zendesk_token_here

# Atlassian (for escalations and documentation)
ATLASSIAN_DOMAIN=yourcompany.atlassian.net
ATLASSIAN_EMAIL=your.email@company.com
ATLASSIAN_API_TOKEN=paste_your_atlassian_token_here

# JIRA Project
JIRA_PROJECT_KEY=SCRS

# GitHub (optional, for code research)
GITHUB_TOKEN=paste_your_github_token_here
```

Save and close.

---

## Step 5: Configure MCP (Cursor AI Integration)

This connects Cursor to Zendesk, JIRA, Confluence, and GitHub.

```bash
# Copy the template
cp .cursor/mcp.json.example .cursor/mcp.json

# Edit with your values
nano .cursor/mcp.json
```

Replace the placeholders:

```json
{
  "mcpServers": {
    "zendesk": {
      "command": "python3",
      "args": [
        "scripts/zendesk_mcp_server.py",
        "--subdomain", "YOUR_ZENDESK_SUBDOMAIN",     ← Replace
        "--email", "your.email@company.com",         ← Replace
        "--token", "YOUR_ZENDESK_API_TOKEN"          ← Replace
      ]
    },
    "atlassian": {
      "command": "uvx",
      "args": [
        "mcp-atlassian",
        "--jira-url", "https://yourcompany.atlassian.net",
        "--jira-username", "your.email@company.com",
        "--jira-token", "YOUR_ATLASSIAN_API_TOKEN",
        "--confluence-url", "https://yourcompany.atlassian.net/wiki",
        "--confluence-username", "your.email@company.com",
        "--confluence-token", "YOUR_ATLASSIAN_API_TOKEN",
        "--read-only"
      ]
    },
    "github": {
      "command": "uvx",
      "args": ["mcp-github"],
      "env": {
        "GITHUB_TOKEN": "YOUR_GITHUB_PAT"
      }
    }
  }
}
```

Save and close.

---

## Step 6: Restart Cursor

**Important:** MCP only loads when Cursor starts.

1. Quit Cursor completely: **Cmd+Q** (not just close window)
2. Reopen Cursor
3. Open the `tse-investigation-hub` folder

---

## Step 7: Verify Everything Works

### Test Zendesk
Ask Cursor:
> "Use MCP to fetch Zendesk ticket 12345"

**Expected:** Cursor shows ticket details

**If it fails:**
- Check `scripts/zendesk_mcp_server.py` exists and is executable
- Verify credentials in `.cursor/mcp.json`
- Check Cursor's MCP panel for error messages

### Test JIRA
Ask Cursor:
> "Search JIRA for open SCRS tickets"

**Expected:** Cursor returns list of tickets

### Test Confluence
Ask Cursor:
> "Search Confluence for APM troubleshooting"

**Expected:** Cursor returns matching pages

### Test Python Scripts (Fallback)
```bash
# Test Zendesk script
python3 scripts/zendesk_client.py list --status open

# Test JIRA script  
python3 scripts/jira_client.py list-open
```

---

## 🎉 You're Ready!

Try your first investigation:

> "Investigate Zendesk ticket 12345"

Cursor will:
1. Fetch the ticket
2. Assess what information you have
3. Search for similar cases
4. Create investigation folder and notes

---

## Troubleshooting

### MCP Not Loading

**Symptom:** Cursor doesn't recognize Zendesk/JIRA commands

**Fix:**
1. Check config exists: `cat .cursor/mcp.json`
2. Verify JSON is valid (no trailing commas, quotes correct)
3. Check Python 3 is available: `python3 --version`
4. Check uvx works: `~/.local/bin/uvx --version`
5. Fully restart Cursor (Cmd+Q, not just close)
6. Check Cursor's MCP panel (bottom right) for errors

### "uvx not found"

**Fix:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.zshrc  # or restart terminal
```

### Zendesk 401 Unauthorized

**Symptom:** `HTTP Error 401`

**Fix:**
1. Verify you're using an API token (not password)
2. Check token format includes `/token` in username: `email/token:token`
3. Regenerate Zendesk API token
4. Update `.cursor/mcp.json` and `.env`
5. Restart Cursor

### Zendesk 403 Forbidden

**Symptom:** `HTTP Error 403`

**Fix:**
1. Verify your Zendesk account has API access enabled
2. Check you're an agent (not end-user)
3. Verify token permissions in Zendesk admin

### JIRA 401 or 403

**Symptom:** JIRA searches fail

**Fix:**
1. Regenerate Atlassian API token
2. Verify you have access to SCRS project
3. Update `.cursor/mcp.json` and `.env`
4. Restart Cursor

### GitHub 401 or 403

**Symptom:** GitHub searches fail

**Fix:**
1. Check token hasn't expired
2. For Datadog repos: Authorize SSO at https://github.com/settings/tokens
3. Verify token has `Contents: Read` permission
4. Update `.cursor/mcp.json`
5. Restart Cursor

### Python Scripts Not Working

**Symptom:** `ModuleNotFoundError` or import errors

**Fix:**
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Scripts use standard library only (no pip install needed)
# Check .env file exists and has correct values
cat .env
```

### MCP Tools Return Errors

**Symptom:** Cursor can call tools but they return errors

**Fix:**
1. Check credentials in `.env` match `.cursor/mcp.json`
2. Test scripts directly to isolate issue:
   ```bash
   python3 scripts/zendesk_client.py list --status open
   ```
3. Check API rate limits (Zendesk: 700 req/min per account)
4. Verify network access (firewall, VPN, etc.)

---

## Next Steps

### Customize Your Workspace

1. **Update `solutions/known-issues.md`** with current product bugs
2. **Add product documentation** to relevant `docs/` folders
3. **Customize templates** in `templates/` for your team's style
4. **Create your first case** to test the workflow

### Learn the Workflow

1. Read `.cursorrules` to understand how Cursor will assist you
2. Review `docs/escalation-criteria.md` for escalation guidelines
3. Check out the templates in `templates/`
4. Browse `cases/.template/` to see the case structure

### Start Investigating

Pick a ticket and ask Cursor:
> "Investigate Zendesk ticket XXXXX"

---

## File Structure After Setup

```
tse-investigation-hub/
├── .cursor/
│   ├── mcp.json              ← Your config (gitignored)
│   └── mcp.json.example      ← Template
├── .env                      ← Your tokens (gitignored)
├── .cursorrules              ← AI behavior rules
├── cases/
│   └── .template/            ← Template for new cases
├── archive/                  ← Will fill with archived tickets
├── docs/                     ← Product documentation
├── templates/                ← Communication templates
├── solutions/                ← Known issues tracking
├── scripts/                  ← Python utilities
├── README.md
└── SETUP.md                  ← You are here
```

---

## Getting Help

- **Slack:** #support-team (or your team channel)
- **Issues:** Open a GitHub issue on this repo
- **Cursor:** Just ask! The AI knows how this hub works

---

**Happy investigating! 🔍**

