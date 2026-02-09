# Known Issues & Workarounds

Track active product bugs and limitations here. Update as issues are fixed.

---

## How to Use This Document

**Before escalating**, check if the issue is already known.

**When you discover a new bug**, add it here with:
- JIRA ticket reference
- Affected versions
- Workaround (if available)
- Expected fix timeline (if known)

**When an issue is fixed**, move it to the "Recently Resolved" section with the fix version.

---

## Active Issues

### APM

#### Python Tracer Memory Leak in Django 4.2
- **JIRA:** SCRS-XXXX
- **Affected Versions:** ddtrace 2.6.0+
- **Symptoms:** Memory usage grows continuously until OOM
- **Workaround:** Downgrade to ddtrace 2.5.x
- **Status:** Fix in progress, expected in 2.7.1
- **Related Zendesk Cases:** ZD-12345, ZD-12389

#### Node.js Tracer Not Capturing Express Routes with Regex
- **JIRA:** SCRS-XXXX
- **Affected Versions:** dd-trace-js 4.x
- **Symptoms:** Routes defined with regex patterns not traced
- **Workaround:** Use string paths instead of regex, or manually instrument
- **Status:** Product limitation, feature request filed
- **Related Zendesk Cases:** ZD-11234

---

### Infrastructure Monitoring

#### Agent 7.50.x High CPU on Large Docker Environments
- **JIRA:** SCRS-XXXX
- **Affected Versions:** Agent 7.50.0 - 7.50.3
- **Symptoms:** Agent using 50-100% CPU on hosts with 100+ containers
- **Workaround:** Disable live containers check: `container_collection.enabled: false`
- **Status:** Fixed in 7.50.4 (released 2026-02-01)
- **Related Zendesk Cases:** ZD-10123, ZD-10145

---

### Logs

#### Log Pipeline Processor Dropping Logs Over 256KB
- **JIRA:** SCRS-XXXX
- **Affected Versions:** All
- **Symptoms:** Large logs silently dropped by pipeline processors
- **Workaround:** Use log truncation before sending to Datadog, or split large logs
- **Status:** Product limitation (by design for performance)
- **Related Zendesk Cases:** ZD-9876

---

### RUM

#### Session Replay Missing First 5 Seconds After Page Load
- **JIRA:** SCRS-XXXX
- **Affected Versions:** RUM Browser SDK 4.40.x - 4.42.x
- **Symptoms:** First few seconds of session not captured in replay
- **Workaround:** Upgrade to 4.43.0+
- **Status:** Fixed in 4.43.0
- **Related Zendesk Cases:** ZD-11567

---

### Synthetics

#### API Tests Failing with "Connection Reset" from US1 Locations
- **JIRA:** SCRS-XXXX
- **Affected Versions:** N/A (infrastructure issue)
- **Symptoms:** Intermittent connection reset errors from AWS:us-east-1 location
- **Workaround:** Use alternative US locations (us-west-2, us-central-1)
- **Status:** Investigating with infrastructure team
- **Related Zendesk Cases:** ZD-12678, ZD-12690

---

### Security (AppSec)

#### PHP Tracer Crashing with Opcache Enabled
- **JIRA:** SCRS-XXXX
- **Affected Versions:** dd-trace-php 0.95.0 - 0.96.x
- **Symptoms:** PHP-FPM workers crash when opcache + tracer both enabled
- **Workaround:** Disable opcache.jit: `opcache.jit=0`
- **Status:** Fix in 0.97.0 (expected Feb 15, 2026)
- **Related Zendesk Cases:** ZD-1885, ZD-12001
- **Documentation:** See `docs/security/appsec/troubleshooting/php-sidecar-crashes.md`

---

### Code Security

#### Duplicate Committer Billing from Email Variations
- **JIRA:** SCRS-1747
- **Affected Versions:** All
- **Symptoms:** Same developer counted multiple times as separate committers due to different email addresses (work email, personal email, GitHub noreply variations). Results in unexpected billing spikes.
- **Example:** 
  - `developer@company.com` → Committer 1
  - `developer@gmail.com` → Committer 2 (same person!)
  - `developer@users.noreply.github.com` → Committer 3 (same person!)
- **Root Cause:** Code Security billing based on `author_email` field from git commits, NOT GitHub user ID. No email deduplication.
- **Workaround:** 
  1. Standardize git email configs across team:
     ```bash
     git config --global user.email "work@company.com"
     ```
  2. Review GitHub email settings: https://github.com/settings/emails
  3. Disable scanning on repositories with many inactive contributors
  4. Check committer breakdown using metrics:
     ```
     datadog.estimated_usage.code_security.sast.committers by {author_email}
     datadog.estimated_usage.code_security.sca.committers by {author_email}
     ```
- **Status:** Product limitation - No fix planned Q1 2026. Product team confirmed will not address this quarter.
- **Customer Impact:** High frustration, unexpected costs, lack of visibility into who is being counted
- **Related Zendesk Cases:** ZD-2488538, ZD-2267949, ZD-2349706
- **Documentation:** See `cases/ZD-2488538/INVESTIGATION_SUMMARY.md` for detailed troubleshooting

#### Bot Accounts Not Filtered in Committer Billing
- **JIRA:** SCRS-1747 (related)
- **Affected Versions:** All
- **Symptoms:** CI/CD automation bots (Dependabot, Renovate, custom bots) counted as committers, causing unexpected billing
- **Known Filtered Bots:** `noreply@github.com`, `actions@github.com`, `*@users.noreply.github.com`
- **Known Gaps:** Bot email format variations may slip through filters
- **Workaround:** 
  1. Disable Code Security scanning on repos where bots are primary committers
  2. Navigate to Code Security > Setup and toggle off specific repositories
- **Status:** Feature request for configurable bot filtering - no ETA
- **Related Zendesk Cases:** ZD-2488538
- **Documentation:** See `cases/ZD-2488538/INVESTIGATION_SUMMARY.md`

#### No Visibility into Committer Breakdown in UI
- **JIRA:** None (product gap)
- **Affected Versions:** All
- **Symptoms:** Customers cannot see which specific email addresses are being billed as committers in the Datadog UI
- **Impact:** Customers unable to self-diagnose billing spikes, must contact support
- **Workaround:** 
  - TSEs/TEEs must query Metrics Explorer:
    ```
    datadog.estimated_usage.code_security.sast.committers by {author_email}
    datadog.estimated_usage.code_security.sca.committers by {author_email}
    ```
  - Can also segment by `repository` and `git_provider`
- **Status:** Feature request - Add committer breakdown view in Code Security UI - no ETA
- **Related Zendesk Cases:** ZD-2488538, ZD-2267949, ZD-2349706

---

## Recently Resolved (Last 30 Days)

### Agent Flare Command Hanging on macOS 14.x
- **JIRA:** SCRS-1234
- **Fixed In:** Agent 7.51.0 (released 2026-01-28)
- **Symptoms:** `datadog-agent flare` would hang indefinitely on macOS Sonoma
- **What Changed:** Fixed file descriptor leak in flare generation
- **Affected Customers:** ZD-11890, ZD-11901

### Dashboard API Returning 500 for Large Time Ranges
- **JIRA:** SCRS-1567
- **Fixed In:** Platform release 2026-01-25
- **Symptoms:** Dashboard API calls with >30 day time range returned 500
- **What Changed:** Increased query timeout and added pagination
- **Affected Customers:** ZD-10234

---

## Product Limitations (Not Bugs)

These are by design, but commonly asked about:

### Metrics
- **Retention:** Standard metrics retained for 15 months, custom metrics for 15 months
- **Tag Cardinality:** Max 1000 unique tag values per metric per host (prevents metric explosion)
- **Datapoint Frequency:** Minimum 1 second resolution (can't send sub-second data)

### Logs
- **Log Size:** Individual logs truncated at 256KB (performance protection)
- **Search History:** Log Explorer search limited to 15 months retention
- **Index Exclusion:** Can't exclude logs from indexes retroactively

### APM
- **Span Limit:** Traces with >100 spans may be partially dropped
- **Trace Retention:** Live Search 15 minutes, Indexed traces per retention plan
- **Custom Span Tags:** Limited to 20 custom tags per span

### Infrastructure
- **Agent Platform:** Agent only runs on supported OSes (see docs for list)
- **Container Metrics:** Some metrics unavailable in serverless/Fargate environments
- **Live Containers:** Limited to 2000 containers per account in Live Containers view

---

## How to Add an Issue

When you discover a new confirmed bug:

```markdown
#### [Brief Description]
- **JIRA:** SCRS-XXXX
- **Affected Versions:** [version range]
- **Symptoms:** [what customer sees]
- **Workaround:** [if available, otherwise "None available"]
- **Status:** [current status and ETA if known]
- **Related Zendesk Cases:** ZD-XXXXX, ZD-YYYYY
```

---

**Last Updated:** 2026-02-04
**Maintained By:** TSE Team

