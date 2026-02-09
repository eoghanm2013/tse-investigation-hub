# When to Escalate to TEE

This guide helps you decide when to escalate a case vs. continue troubleshooting.

---

## Quick Decision Tree

```
Is it a product bug?
├─ YES → Escalate to TEE
│
Is it beyond TSE documentation/training?
├─ YES → Escalate to TEE
│
Have you spent 2+ days without progress?
├─ YES → Escalate to TEE
│
Is there a working workaround?
├─ NO → Consider escalating
├─ YES → Continue, offer workaround
│
Is customer impact critical (production down)?
├─ YES → Escalate immediately
└─ NO → Continue troubleshooting
```

---

## Clear Escalation Scenarios

### ✅ Escalate Immediately

1. **Production Down / Critical Impact**
   - Service completely unavailable
   - Data loss occurring
   - Security breach suspected
   - → Escalate within 30 minutes

2. **Confirmed Product Bug**
   - Reproducible unexpected behavior
   - Works in older version, broken in newer
   - Contradicts documented behavior
   - → Escalate after confirming reproducibility

3. **Missing Functionality**
   - Customer needs feature that doesn't exist
   - API endpoint doesn't support their use case
   - → Escalate for product team evaluation

4. **Requires Code Investigation**
   - Need to read/debug product source code
   - Requires understanding internal architecture
   - Performance profiling of Datadog components
   - → Escalate (beyond TSE scope)

### ⚠️ Consider Escalating

1. **Stuck After 2 Days**
   - You've exhausted standard troubleshooting
   - No clear next steps
   - Customer is getting frustrated
   - → Escalate to get fresh perspective

2. **Workaround Not Viable**
   - You found a workaround but:
     - Too complex for customer to implement
     - Requires significant architecture changes
     - Disables critical functionality
   - → Escalate for proper solution

3. **Documentation Gap**
   - No documentation exists for this scenario
   - Documentation contradicts reality
   - Documentation is clearly outdated
   - → Escalate (and note for doc team)

4. **Inconsistent Behavior**
   - Works on some hosts but not others (identical config)
   - Works sometimes, fails other times (no obvious pattern)
   - Behavior changed without any changes on customer side
   - → Escalate after collecting evidence

### ❌ Don't Escalate Yet

1. **Insufficient Information**
   - Haven't collected basic logs/configs
   - Haven't confirmed customer's environment details
   - Haven't tried basic troubleshooting
   - → Collect more info first

2. **Configuration Issue**
   - Clear misconfiguration
   - Solution is in documentation
   - Common known issue with known fix
   - → Solve directly, document in case notes

3. **User Error**
   - Customer misunderstood feature
   - Incorrect API usage
   - Expected behavior, not a bug
   - → Explain, provide documentation, examples

4. **Third-Party Issue**
   - Issue is with customer's application
   - Problem is in external service (AWS, GCP, etc.)
   - Network/firewall issues (not Datadog's)
   - → Help customer debug, but don't escalate to TEE

---

## Time Guidelines

| Severity | Initial Triage | Escalation Threshold |
|----------|----------------|---------------------|
| **Critical** (Production down) | Immediate | 2-4 hours |
| **High** (Major functionality impacted) | Within 4 hours | 1-2 days |
| **Medium** (Some functionality impacted) | Within 1 day | 3-5 days |
| **Low** (Minor issue, has workaround) | Within 2 days | 1 week |

**Note:** These are guidelines, not strict rules. Use your judgment based on:
- Customer frustration level
- Business impact
- Progress being made
- Availability of workarounds

---

## Before You Escalate: Checklist

Use this checklist to ensure you're ready to escalate:

### Investigation Complete
- [ ] Collected environment details (versions, OS, deployment method)
- [ ] Obtained relevant logs (agent, application, tracer)
- [ ] Reviewed configuration files
- [ ] Confirmed reproducibility (if possible)
- [ ] Tested on different environments (if feasible)

### Due Diligence
- [ ] Searched Confluence for documentation
- [ ] Searched JIRA for similar past escalations
- [ ] Searched archive for similar historical cases
- [ ] Checked `solutions/known-issues.md`
- [ ] Reviewed product release notes for related changes

### Troubleshooting Attempted
- [ ] Tried obvious fixes (restart, config changes, etc.)
- [ ] Looked for recent changes (version updates, config changes)
- [ ] Tested with minimal configuration
- [ ] Enabled debug logging where applicable
- [ ] Ruled out common causes

### Documentation Ready
- [ ] Case notes document investigation path
- [ ] Clearly defined expected vs actual behavior
- [ ] Identified business impact and urgency
- [ ] Listed what's been tried and what's been ruled out
- [ ] Have escalation summary ready (see template)

---

## How to Escalate

### 1. Prepare Your Escalation
Use the template in `templates/escalation/escalation-template.md`

### 2. Create JIRA Ticket
```bash
# Option 1: Ask Cursor
> "Create JIRA escalation for ZD-12345"

# Option 2: Manual
# Go to JIRA, create SCRS ticket, use template
```

### 3. Notify Customer
Use template: `templates/customer-communication/escalation-notice.md`

### 4. Stay Involved
- Monitor JIRA ticket for updates
- Answer TEE questions promptly
- Update customer with progress
- Test any proposed solutions with customer

---

## What Happens After Escalation

### TEE Review (24-48 hours)
- TEE reviews your investigation
- May ask for additional information
- Determines if it's a bug or needs deeper investigation

### Possible Outcomes

1. **Quick Solution Found**
   - TEE identifies solution from experience
   - You implement solution with customer
   - Case resolved

2. **Escalated to Engineering**
   - TEE confirms it's a product bug
   - Creates internal engineering ticket
   - TEE provides workaround if available
   - You keep customer updated on progress

3. **More Information Needed**
   - TEE needs additional logs/configs
   - You work with customer to collect
   - Investigation continues

4. **Not a Bug**
   - TEE identifies it's configuration/usage issue
   - Provides solution
   - You implement with customer

---

## Common Mistakes

### ❌ Escalating Too Early
**Problem:** "Customer is asking for help, escalate immediately"
**Better:** Collect basic information, try obvious fixes first

### ❌ Escalating Without Context
**Problem:** "Logs aren't working, escalate"
**Better:** Provide environment, logs, what you've tried, specific error messages

### ❌ Escalating Third-Party Issues
**Problem:** "AWS load balancer isn't forwarding to agent, escalate"
**Better:** Help customer debug AWS config, only escalate if Datadog component is confirmed broken

### ❌ Not Escalating When Stuck
**Problem:** Spending a week trying the same things repeatedly
**Better:** After 2 days with no progress, escalate for fresh perspective

### ❌ Escalating Without Testing Workaround
**Problem:** Found possible workaround, escalated without testing
**Better:** Test workaround with customer first, escalate if it doesn't work

---

## Remember

- **Escalating is not failing** - It's the right process for complex issues
- **TEEs are partners** - Not critics, they're there to help
- **Customer care first** - Escalate if it's the right thing for the customer
- **Document everything** - Makes escalations more effective and helps future cases
- **Learn from escalations** - Review resolved escalations to expand your knowledge

---

## Questions?

If you're unsure whether to escalate:
- Ask in #support-triage Slack channel
- Review similar past escalations in JIRA
- When in doubt, ask a senior TSE or team lead

