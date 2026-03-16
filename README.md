# TSE Investigation Hub

Centralized Cursor workspace for Datadog Technical Support Engineers. Investigate customer tickets, search internal docs, escalate to engineering -- all from one place.

## Setup (2 minutes)

**Prerequisites:** [Cursor](https://cursor.com), Git

1. **Clone and open**
   ```bash
   git clone https://github.com/eoghanm2013/tse-investigation-hub.git
   ```
   Open the folder in Cursor.

2. **Tell Cursor: "Set me up"**
   Cursor runs the setup script. Atlassian and Glean use SSO (no tokens needed). You'll optionally be asked for a GitHub PAT.

3. **Restart Cursor** (Cmd+Q, then reopen)
   Atlassian and Glean will prompt a one-time SSO login on first use.

That's it.

### Optional: GitHub token

If you want code search, generate a PAT at [github.com/settings/tokens](https://github.com/settings/tokens?type=beta) with Contents + Metadata read. Authorize SSO for the DataDog org.

## What you can do

Ask Cursor things like:

- *"Investigate Zendesk ticket 12345"* -- fetches the ticket, searches for similar cases, creates investigation notes
- *"Search JIRA for open SCRS tickets"* -- queries escalation tickets
- *"Search Confluence for APM troubleshooting"* -- finds internal docs
- *"Search Glean for recent security product updates"* -- searches Slack, Confluence, everything
- *"Draft a customer response for ZD-12345"* -- uses communication templates

## Structure

```
cases/           Active investigations (ZD-XXXXX folders, gitignored)
archive/         Resolved cases by month (gitignored)
docs/            Product troubleshooting docs
solutions/       Known issues and workarounds
templates/       Customer communication and escalation templates
scripts/         Utility scripts (setup, Zendesk client, JIRA client)
reference/       JIRA project codes, internal references
```

## Reconfiguring

Need to add GitHub or update config? Tell Cursor *"reconfigure my workspace"* or run:
```bash
python3 scripts/setup.py --reconfigure
```

## Local Web UI

Run `./app/run.sh` to launch a browser-based dashboard for browsing cases, archive, and docs without touching the terminal. It's entirely optional — the workspace works fully through Cursor alone — but gives a quick visual overview when you want one.

## Safety

- All `cases/` and `archive/` folders are gitignored (customer data never committed)
- Credentials stay local (gitignored)
- Cursor confirms before sending public comments to customers
