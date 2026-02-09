# Case: ZD-XXXXXX

> **Template:** Copy this folder when starting a new case investigation

---

## Quick Info

| Field | Value |
|-------|-------|
| **Zendesk ID** | ZD-XXXXXX |
| **Customer** | [Company Name] |
| **Product Area** | [APM / Infrastructure / Logs / RUM / Security / etc.] |
| **Priority** | [Low / Medium / High / Critical] |
| **Status** | [New / Investigating / Escalated / Resolved] |
| **Assigned TSE** | [Your Name] |
| **Started** | YYYY-MM-DD |

---

## Issue Summary

**What's Happening:**
[Brief description of the issue]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What is actually happening]

**Customer Impact:**
[How this affects their business]

---

## Environment

- **Datadog Agent:** [version]
- **Host OS:** [OS and version]
- **Runtime/Language:** [if applicable]
- **Deployment Method:** [Docker, K8s, VM, etc.]
- **Region:** [Datadog region - US1, EU1, etc.]
- **Affected Resources:** [number of hosts/services/etc.]

---

## Timeline

| Date | Event |
|------|-------|
| YYYY-MM-DD | Issue first reported |
| YYYY-MM-DD | [Major event or milestone] |
| YYYY-MM-DD | [Major event or milestone] |

---

## Investigation Links

- **Zendesk Ticket:** https://[subdomain].zendesk.com/agent/tickets/XXXXXX
- **Related JIRA:** [If escalated: SCRS-XXXX]
- **Datadog Dashboard:** [Link to relevant dashboard]
- **Host/Service Link:** [Link to specific host/service in Datadog]

---

## Assets

Store relevant files in the `assets/` folder:

- `logs/` - Agent logs, application logs, tracer logs
- `screenshots/` - Screenshots from Datadog UI, customer dashboards
- `flares/` - Flare tarballs (note: these can be large)
- `configs/` - Configuration files

---

## Related Cases

- **Similar Historical Cases:** 
  - [ZD-XXXXX] - [brief description]
  - [ZD-YYYYY] - [brief description]

- **Related Known Issues:**
  - See `solutions/known-issues.md`
  
- **Related JIRA Tickets:**
  - [SCRS-XXXX] - [description]

---

## Notes

Detailed investigation notes are in `notes.md`.

Use `notes.md` to document:
- Hypothesis and tests
- What you've tried
- Findings and evidence
- Communication with customer
- Next steps

---

## Status Updates

### [Date] - Investigation Started
[Initial findings and plan]

### [Date] - [Update]
[What happened, what you learned, what's next]

### [Date] - Resolution
[How it was resolved, what the fix was]

---

**Last Updated:** YYYY-MM-DD

