# Requesting Additional Information Template

Use these when you need specific information from the customer.

---

## General Information Request

Hi [Customer Name],

Thank you for the details so far. To continue investigating, I need a bit more information:

**[Category 1]:**
- [Specific question or request]

**[Category 2]:**
- [Specific question or request]

**[Category 3]:**
- [Specific question or request]

Once I have this, I'll be able to [what this will help you do].

Thanks!

Best regards,
[Your Name]

---

## Agent/Infrastructure Information

Hi [Customer Name],

To help diagnose this issue, could you please provide:

**Agent Information:**
- Datadog Agent version: `sudo datadog-agent version`
- Host operating system and version
- Installation method (Docker, Kubernetes, package manager, etc.)

**Environment Details:**
- How many hosts are affected?
- When did this issue first start?
- Any recent changes to the environment?

**Logs:**
- Agent logs from an affected host (last 24 hours): `/var/log/datadog/agent.log`

You can collect all this automatically with a flare:
```bash
sudo datadog-agent flare
```

This will generate a case ID that you can share with me.

Best regards,
[Your Name]

---

## APM/Tracing Information

Hi [Customer Name],

To investigate this tracing issue, I need:

**Tracer Information:**
- Language and tracer version
- Application framework and version
- How is the application deployed? (containers, VMs, serverless, etc.)

**Issue Details:**
- Trace ID or span ID of an affected trace (if available)
- Approximate timestamp when the issue occurred
- Expected vs. actual behavior

**Configuration:**
- Tracer configuration (environment variables or config file)
- Any custom instrumentation?

**Logs:**
- Application logs showing the issue
- Tracer debug logs (if possible to enable)

Let me know if you need help enabling debug logs for your tracer.

Best regards,
[Your Name]

---

## Logs/Pipeline Information

Hi [Customer Name],

To troubleshoot this log processing issue, could you please share:

**Log Details:**
- Example raw log (before processing)
- Expected vs. actual output
- Log source (application, integration, custom)
- Approximate volume (logs/second or logs/day)

**Pipeline Information:**
- Pipeline name
- Processor configuration (screenshot or export)
- Any recent changes to the pipeline?

**Timeline:**
- When did this issue start?
- Are all logs affected or specific patterns?

Best regards,
[Your Name]

---

## "I've Already Sent This" Response

Hi [Customer Name],

Thank you for the previous information. I apologize, but I need to request a few additional specific details:

[Be very specific about exactly what you need and why]

I know you've shared [what they already sent], but for this specific investigation I need [very specific thing] because [brief reason].

I appreciate your patience!

Best regards,
[Your Name]

