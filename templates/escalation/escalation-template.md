# JIRA Escalation Template

Use this template when creating a JIRA escalation ticket (SCRS project).

---

## Escalation Checklist

Before creating the escalation, ensure you have:

- [ ] Tried standard troubleshooting steps
- [ ] Searched for similar historical cases
- [ ] Checked for known issues in Confluence/JIRA
- [ ] Collected all relevant logs/configs
- [ ] Documented what you've tried in case notes
- [ ] Identified if this is reproducible
- [ ] Assessed customer impact (severity)

---

## JIRA Ticket Format

**Summary:**
[Product Area] - [Brief description of issue]

Example: "APM - Traces not appearing for Ruby application despite successful agent connection"

---

**Environment:**
- **Customer:** [Company name + ZD ticket link]
- **Datadog Agent Version:** [version]
- **Host OS:** [OS and version]
- **Runtime/Language:** [if applicable]
- **Deployment Method:** [Docker, K8s, VM, etc.]
- **Region:** [Datadog region]
- **Number of Hosts Affected:** [count]

---

**Issue Description:**

[Clear description of what's happening vs. what should happen]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What is actually happening]

**Impact:**
[How this affects the customer - data loss, missing monitors, can't deploy, etc.]

---

**Reproduction Steps:**

1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Result]

**Reproducibility:** [Always / Sometimes / Once - be specific about frequency]

---

**Investigation Summary:**

[What you've investigated and ruled out]

**What We've Tried:**
- [Action 1] → [Result]
- [Action 2] → [Result]
- [Action 3] → [Result]

**What We've Ruled Out:**
- [Common cause 1 - why it's not this]
- [Common cause 2 - why it's not this]

---

**Relevant Logs/Data:**

**Agent Logs:**
```
[Relevant log snippets - include timestamps]
```

**Application Logs:**
```
[Relevant log snippets]
```

**Configuration:**
```yaml
[Relevant config sections]
```

**Screenshots/Evidence:**
[Attach or link to evidence]

---

**Why This Needs Escalation:**

[Specific reason - suspected bug, needs code investigation, beyond TSE scope, etc.]

---

**Customer Priority:**

- **Severity:** [Low / Medium / High / Critical]
- **Business Impact:** [Description of impact]
- **Urgency:** [When do they need resolution?]
- **Workaround Available:** [Yes/No - describe if yes]

---

**Additional Context:**

[Any other relevant information]
- Similar cases: [Link to related tickets]
- Documentation checked: [What docs you reviewed]
- Confluence searches: [What you searched for]

---

**TSE Contact:**
[Your name and preferred contact method for TEE questions]

---

## Example: Good Escalation

**Summary:** APM - Python tracer causing application memory leak in Django 4.2

**Environment:**
- **Customer:** Acme Corp (ZD-12345)
- **Datadog Agent Version:** 7.50.1
- **Host OS:** Ubuntu 22.04 LTS
- **Runtime/Language:** Python 3.11, Django 4.2.7, ddtrace 2.6.0
- **Deployment Method:** Kubernetes (EKS)
- **Region:** US1
- **Number of Hosts Affected:** 15 pods

**Issue Description:**
Application memory usage continuously grows until pods are OOM killed. Memory growth stops when ddtrace is disabled. Issue started after upgrading from ddtrace 2.5.0 to 2.6.0.

**Expected Behavior:**
Memory usage should remain stable over time with tracer enabled.

**Actual Behavior:**
Memory usage grows ~50MB/hour per pod until reaching memory limit (2GB) and being OOM killed.

**Impact:**
- Pods being killed every 8-12 hours
- Service disruptions during pod restarts
- Increased infrastructure costs from scaling up

**Reproduction Steps:**
1. Deploy Django 4.2 app with ddtrace 2.6.0
2. Monitor pod memory usage over 8 hours
3. Observe continuous memory growth
4. Disable ddtrace → memory usage stabilizes

**Reproducibility:** Always - happens on all 15 pods consistently

**Investigation Summary:**

**What We've Tried:**
- Downgraded to ddtrace 2.5.0 → Issue goes away
- Tested with minimal tracer config → Issue persists
- Enabled tracer debug logs → No obvious errors
- Memory profiling shows growth in tracer internals

**What We've Ruled Out:**
- Application code leak (issue only occurs with tracer)
- Agent version (tested with multiple agent versions)
- Configuration issue (minimal config still leaks)
- Django version (tested 4.2.5, 4.2.6, 4.2.7 - all leak)

**Relevant Logs/Data:**

Memory growth chart: [attached screenshot]

Tracer debug logs showing trace volume:
```
2026-02-04 10:15:23 | DEBUG | Traced request: POST /api/orders (15ms)
2026-02-04 10:15:24 | DEBUG | Traced request: GET /api/products (8ms)
[~50 requests/second]
```

**Why This Needs Escalation:**
Memory leak appears to be in ddtrace 2.6.0 itself (regression from 2.5.0). Needs engineering investigation into tracer memory management changes between versions.

**Customer Priority:**
- **Severity:** High
- **Business Impact:** Production service stability compromised
- **Urgency:** Need resolution within 1 week
- **Workaround Available:** Yes - downgrade to ddtrace 2.5.0 (customer testing now)

**Additional Context:**
- Similar case: SCRS-1234 (memory leak in Java tracer, fixed in 1.2.3)
- Checked release notes: ddtrace 2.6.0 mentioned "improved memory efficiency" - possible regression?
- Customer can provide heap dumps if needed

**TSE Contact:** [Your Name] - Slack @yourname or this ticket

