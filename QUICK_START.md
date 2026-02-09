# TSE Investigation Hub - Quick Start

**TL;DR:** This workspace helps TSEs investigate customer cases using AI-assisted workflows.

---

## What Is This?

A Cursor AI workspace specifically designed for Technical Support Engineers (TSEs) to:
- 📋 Investigate Zendesk tickets efficiently
- 🤖 Use AI to search historical cases and documentation
- 📝 Document investigations systematically
- 🚀 Escalate to TEE with proper context
- 💬 Communicate clearly with customers

---

## 5-Minute Setup

```bash
# 1. Navigate to workspace
cd ~/tse-investigation-hub

# 2. Set up credentials
cp .env.example .env
# Edit .env with your API tokens

# 3. Configure MCP
cp .cursor/mcp.json.example .cursor/mcp.json
# Edit .cursor/mcp.json with same tokens

# 4. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 5. Restart Cursor (Cmd+Q, reopen)
```

**Full setup guide:** See [SETUP.md](SETUP.md)

---

## Using It

### Start Investigation
Ask Cursor:
> "Investigate Zendesk ticket 12345"

Cursor will:
1. ✅ Fetch ticket from Zendesk
2. ✅ Check if similar cases exist
3. ✅ Search for known issues
4. ✅ Create investigation folder
5. ✅ Generate notes template

### During Investigation
- **Drop files** into `cases/ZD-12345/assets/`
- **Ask Cursor** to search Confluence, GitHub, or historical cases
- **Document findings** in `notes.md`
- **Use templates** from `templates/` for customer communication

### Need to Escalate?
Ask Cursor:
> "Create JIRA escalation for ZD-12345"

Cursor will help you create a properly formatted SCRS ticket.

### Resolved the Issue?
```bash
# Archive the case
python3 scripts/zendesk_client.py archive 12345
```

---

## Key Features

### 🤖 AI-Powered Investigation
- Search historical cases automatically
- Find similar issues in Confluence/JIRA
- Get suggestions for troubleshooting steps
- Identify known issues automatically

### 📚 Customer Communication Templates
Pre-written templates for:
- Acknowledging tickets
- Requesting information
- Providing solutions
- Escalation notices

Located in: `templates/customer-communication/`

### 🎯 Escalation Guidance
Clear criteria for when to escalate to TEE:
- Decision tree
- Time guidelines
- Checklist before escalating
- JIRA template

Located in: `docs/escalation-criteria.md`

### 📖 Known Issues Tracking
Centralized list of current product bugs and workarounds.

Located in: `solutions/known-issues.md`

### 🔍 Case Structure
Every case has:
- README with metadata
- Investigation notes
- Timeline of events
- Assets folder (logs, screenshots, configs)
- Links to related cases

---

## Folder Guide

| Folder | Purpose | You'll Use It To... |
|--------|---------|---------------------|
| `cases/` | Active investigations | Store current customer cases |
| `archive/` | Resolved cases | Search historical solutions |
| `docs/` | Product documentation | Find troubleshooting guides |
| `templates/` | Communication templates | Draft customer responses |
| `solutions/` | Known issues | Check for tracked bugs |
| `scripts/` | CLI tools | Manual ticket operations |

---

## Common Commands

### Zendesk
```bash
# Get ticket details
python3 scripts/zendesk_client.py get 12345

# List open tickets
python3 scripts/zendesk_client.py list --status open

# Search tickets
python3 scripts/zendesk_client.py search "priority:urgent"

# Archive to markdown
python3 scripts/zendesk_client.py archive 12345
```

### JIRA (for escalations)
```bash
# Search SCRS project
python3 scripts/jira_client.py search "project = SCRS AND status = Open"

# Get escalation details
python3 scripts/jira_client.py get SCRS-1234
```

### Using Cursor AI
```
"Investigate Zendesk ticket 12345"
"Search historical cases for [issue description]"
"What are common causes of [problem]?"
"Create JIRA escalation for ZD-12345"
"Search Confluence for [topic]"
"Show me similar cases from the archive"
```

---

## Example Workflow

### 1. New Ticket Arrives
```
Customer: "Logs not appearing in Datadog"
```

### 2. Start Investigation
**Ask Cursor:**
> "Investigate Zendesk ticket 54321"

**Cursor creates:**
- `cases/ZD-54321/` folder
- `README.md` with metadata
- `notes.md` for documentation

### 3. Research
**Ask Cursor:**
> "Search for similar cases about missing logs"

**Cursor searches:**
- Historical archive cases
- Confluence documentation
- Known issues list
- Related JIRA tickets

### 4. Troubleshoot
- Request agent logs from customer
- Save to `cases/ZD-54321/assets/logs/`
- Test hypotheses, document in `notes.md`
- Use Cursor to search for specific error messages

### 5. Solution Found
- Apply fix with customer
- Document in `notes.md`
- Use template: `templates/customer-communication/solution.md`
- Archive case: `python3 scripts/zendesk_client.py archive 54321`

### 6. (Or) Need to Escalate
**If stuck after 2 days:**
> "Create JIRA escalation for ZD-54321"

**Cursor helps format:**
- All investigation details
- What's been tried
- Evidence collected
- Customer impact

---

## Best Practices

### ✅ Do
- Document as you investigate (easier than doing it later)
- Use templates for customer communication (consistent, professional)
- Search archive before starting investigation (someone may have solved this)
- Ask Cursor for help searching (it's faster than manual)
- Escalate when appropriate (don't waste days on TEE-level issues)

### ❌ Don't
- Commit customer data to git (it's all gitignored for safety)
- Skip the investigation workflow (documentation helps future cases)
- Be afraid to escalate (it's the right process)
- Give production config advice without considering risks
- Forget to update `solutions/known-issues.md` when you find bugs

---

## Getting Help

### Cursor AI Can Help With:
- Finding similar cases
- Searching documentation
- Suggesting troubleshooting steps
- Formatting escalations
- Drafting customer responses

### Ask Your Team For:
- Escalation decisions
- Customer communication review
- Complex technical questions
- Prioritization guidance

### Resources:
- **Setup Issues:** [SETUP.md](SETUP.md)
- **Escalation Help:** [docs/escalation-criteria.md](docs/escalation-criteria.md)
- **Structure Questions:** [STRUCTURE.md](STRUCTURE.md)
- **Full README:** [README.md](README.md)

---

## Troubleshooting

**Cursor not recognizing Zendesk commands?**
→ Check [SETUP.md](SETUP.md#troubleshooting), verify MCP config, restart Cursor

**Can't fetch tickets?**
→ Verify API tokens in `.env` and `.cursor/mcp.json`

**Scripts not working?**
→ Check Python 3.8+ installed: `python3 --version`

**MCP errors?**
→ Check Cursor's MCP panel (bottom right) for specific error messages

---

**You're all set! Start with:** `"Investigate Zendesk ticket [ID]"`

