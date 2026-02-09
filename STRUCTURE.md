# TSE Investigation Hub vs TEE Hub - Structure Comparison

This document explains the differences between the TSE workspace and TEE workspace.

---

## Directory Structure Comparison

### TSE Investigation Hub (`tse-investigation-hub/`)
```
tse-investigation-hub/
├── cases/                    # Customer cases (Zendesk tickets)
│   ├── .template/
│   └── ZD-XXXXXX/           # Zendesk ticket folders
├── templates/                # Customer communication templates
│   ├── customer-communication/
│   └── escalation/
├── solutions/                # Known issues & workarounds
├── docs/escalation-criteria.md  # When to escalate to TEE
└── scripts/
    ├── zendesk_client.py
    ├── zendesk_mcp_server.py
    └── jira_client.py       # For creating escalations
```

### Security TEE Hub (`security-tee-hub/`)
```
security-tee-hub/
├── investigations/           # Internal escalations (JIRA tickets)
│   ├── .template/
│   └── SCRS-XXXX/           # JIRA escalation folders
├── docs/                    # Security-specific docs only
│   ├── appsec/
│   ├── siem/
│   ├── cws/
│   └── ...
└── scripts/
    └── jira_client.py       # Only JIRA access
```

---

## Key Differences

| Aspect | TSE Hub | TEE Hub |
|--------|---------|---------|
| **Primary Ticket Source** | Zendesk (customer tickets) | JIRA (internal escalations) |
| **User Role** | Customer-facing support | Internal technical investigation |
| **Main Goal** | Solve customer issues | Determine if bug, escalate to eng |
| **Communication** | Customer templates needed | Internal only |
| **Escalation Direction** | TO TEEs (when stuck) | TO Engineering (when bug confirmed) |
| **Product Scope** | All Datadog products | Security products only |
| **Zendesk Access** | READ/WRITE (active tickets) | READ-ONLY (reference customer cases) |
| **JIRA Access** | CREATE (escalations) | READ/WRITE (manage escalations) |

---

## Workflow Comparison

### TSE Workflow
```
1. Customer opens Zendesk ticket
2. TSE investigates (uses TSE hub)
3. TSE tries standard troubleshooting
4. If stuck → TSE escalates to TEE (creates JIRA)
5. TSE keeps customer updated
6. When resolved → TSE closes Zendesk ticket
```

### TEE Workflow
```
1. TSE escalates via JIRA (SCRS project)
2. TEE investigates using TEE hub
3. TEE performs deep investigation
4. If bug → TEE escalates to Engineering
5. If not bug → TEE provides solution to TSE
6. TSE implements solution with customer
```

---

## Product Coverage

### TSE Hub - All Products
```
docs/
├── apm/                  # Application Performance Monitoring
├── infrastructure/       # Infrastructure monitoring, agents
├── logs/                 # Log management
├── rum/                  # Real User Monitoring
├── synthetics/           # Synthetic monitoring
├── network/              # Network monitoring
├── security/             # Security products
│   ├── appsec/
│   ├── siem/
│   ├── cws/
│   └── cspm/
├── platform/             # Billing, API, auth
└── common/               # Cross-product (agent, integrations)
```

### TEE Hub - Security Only
```
docs/
├── appsec/              # Application Security
├── siem/                # Cloud SIEM
├── cws/                 # Cloud Workload Security
├── cspm/                # Cloud Security Posture Management
├── vm/                  # Vulnerability Management
├── sca/                 # Software Composition Analysis
├── iast/                # Interactive Application Security Testing
├── sast/                # Static Application Security Testing
└── common/              # Common security topics (tracer, agent)
```

---

## MCP Configuration Comparison

### TSE Hub MCP Config
```json
{
  "mcpServers": {
    "zendesk": {
      "command": "python3",
      "args": ["scripts/zendesk_mcp_server.py", ...]
    },
    "atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian", "--read-only"]  // Read-only for searching
    },
    "github": { ... },
    "glean": { ... }
  }
}
```

### TEE Hub MCP Config
```json
{
  "mcpServers": {
    "atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian", "--read-only"]  // Read-only by default
    },
    "github": { ... },
    "glean": { ... }
    // No Zendesk - TEEs work primarily in JIRA
  }
}
```

---

## .cursorrules Comparison

### TSE .cursorrules Focus
- **Customer communication** guidelines (clear, empathetic, no jargon)
- **Risk assessment** for customer-facing recommendations
- **Escalation criteria** (when to escalate to TEE)
- **Time management** (don't spend too long on escalatable issues)
- **Solution documentation** (help future TSEs)

### TEE .cursorrules Focus
- **Escalation quality assessment** (did TSE provide good context?)
- **Investigation depth** (code review, architecture analysis)
- **Bug determination** (is this a product bug?)
- **Engineering escalation** (proper formatting for dev team)
- **Risk assessment** for config changes (production impact)

---

## When to Use Which

### Use TSE Hub If You:
- Work directly with customers via Zendesk
- Handle a wide range of Datadog products
- Need customer communication templates
- Escalate complex issues to TEE
- Focus on solving issues quickly

### Use TEE Hub If You:
- Receive escalations from TSEs (via JIRA)
- Specialize in Security products
- Determine if issues are bugs
- Escalate to engineering teams
- Perform deep technical investigations

---

## Shared Resources

Both hubs can share:
- **Known issues documentation** (copy between repos)
- **Troubleshooting guides** (adapt as needed)
- **Investigation techniques** (same methodologies)
- **Escalation learnings** (document in both)

---

## Migration Path

If a TSE becomes a TEE:
1. Keep using TSE hub for any remaining Zendesk tickets
2. Set up TEE hub for JIRA escalations
3. Both hubs can coexist
4. Eventually transition fully to TEE hub

If a TEE helps with customer cases:
1. Set up TSE hub alongside TEE hub
2. Use TSE hub for direct customer work
3. Use TEE hub for escalations from other TSEs
4. Keep workstreams separate

---

## Cross-References

### TSEs referencing TEE work
- Search TEE hub's archive for similar investigations
- Check TEE docs for product-specific guides
- Reference JIRA tickets from TEE escalations

### TEEs referencing TSE work
- Check original Zendesk ticket for customer context
- Review TSE investigation notes
- Use TSE-collected logs and evidence

---

**Summary:** Both hubs use similar structure and tools, but serve different roles in the support escalation chain. TSEs are customer-facing (Zendesk), TEEs are internal technical (JIRA).

