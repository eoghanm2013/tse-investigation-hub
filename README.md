# TSE Investigation Hub

Centralized Cursor workspace for Datadog Technical Support Engineers. Investigate customer tickets, search internal docs, escalate to engineering -- all from one place.

## Setup (2 minutes)

**Prerequisites:** [Cursor](https://cursor.com), Python 3.8+, Git

1. **Clone and open**
   ```bash
   git clone git@github.com:YOUR_ORG/tse-investigation-hub.git
   cd tse-investigation-hub
   ```
   Open the folder in Cursor.

2. **Tell Cursor: "Set me up"**
   Cursor will ask for your tokens and configure everything automatically.

3. **Restart Cursor** (Cmd+Q, then reopen)

That's it.

### Where to get tokens

| Token | Where |
|-------|-------|
| **Zendesk** | Admin Center > Apps and integrations > APIs > Zendesk API > Add API Token |
| **Atlassian** | https://id.atlassian.com/manage-profile/security/api-tokens |
| **GitHub** (optional) | https://github.com/settings/tokens?type=beta -- needs Contents + Metadata read; authorize SSO for DataDog org |

## What you can do

Ask Cursor things like:

- *"Investigate Zendesk ticket 12345"* -- fetches the ticket, searches for similar cases, creates investigation notes
- *"Search JIRA for open SCRS tickets"* -- queries escalation tickets
- *"Search Confluence for APM troubleshooting"* -- finds internal docs
- *"Draft a customer response for ZD-12345"* -- uses communication templates

## Structure

```
cases/           Active investigations (ZD-XXXXX folders, gitignored)
archive/         Resolved cases by month (gitignored)
docs/            Product troubleshooting docs
solutions/       Known issues and workarounds
templates/       Customer communication and escalation templates
scripts/         Utility scripts (Zendesk client, JIRA client, setup)
reference/       JIRA project codes, internal references
```

## Reconfiguring

Need to update tokens? Tell Cursor *"reconfigure my workspace"* or run:
```bash
python3 scripts/setup.py --reconfigure
```

## Safety

- All `cases/` and `archive/` folders are gitignored (customer data never committed)
- Credentials stay local in `.env` (gitignored)
- Cursor confirms before sending public comments to customers
