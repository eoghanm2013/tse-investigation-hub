# Git Strategy for TSE Investigation Hub

This document outlines what should and shouldn't be committed to git for team sharing.

---

## ✅ COMMIT TO GIT (Share with Team)

### Core Documentation
```
✅ README.md                      # Main documentation
✅ SETUP.md                       # Setup instructions
✅ QUICK_START.md                 # Quick reference
✅ STRUCTURE.md                   # Architecture explanation
✅ GIT_STRATEGY.md                # This file
```

### Configuration Templates
```
✅ .env.example                   # Credential template (NO real tokens)
✅ .cursor/mcp.json.example       # MCP config template (NO real tokens)
✅ .gitignore                     # Protect sensitive data
✅ .cursorrules                   # AI behavior rules
```

### Scripts & Tools
```
✅ scripts/zendesk_client.py      # Zendesk CLI tool
✅ scripts/zendesk_mcp_server.py  # Zendesk MCP server
✅ scripts/jira_client.py         # JIRA CLI tool
```

### Templates (Empty/Generic)
```
✅ cases/.template/               # Case investigation template
   ✅ cases/.template/README.md
   ✅ cases/.template/notes.md
   ✅ cases/.template/assets/     # Empty folder structure

✅ templates/customer-communication/
   ✅ acknowledgment.md
   ✅ requesting-info.md
   ✅ solution.md
   ✅ escalation-notice.md

✅ templates/escalation/
   ✅ escalation-template.md
```

### Documentation Structure
```
✅ docs/                          # Product documentation
   ✅ escalation-criteria.md
   ✅ apm/                        # Empty folders for team to populate
   ✅ infrastructure/
   ✅ logs/
   ✅ rum/
   ✅ synthetics/
   ✅ security/
   ✅ network/
   ✅ platform/
   ✅ common/
   ✅ _templates/                 # Doc templates
```

### Solution Tracking (Template)
```
✅ solutions/known-issues.md      # Template/structure
   (Team updates this, commits updates to share knowledge)
```

### Reference Materials
```
✅ reference/                     # Shared reference docs
   ✅ jira-project-codes.md       # If exists
   ✅ Any team-wide reference materials
```

---

## ❌ DO NOT COMMIT (Keep Local)

### Credentials & Secrets
```
❌ .env                           # Real API tokens
❌ .cursor/mcp.json               # Real credentials
❌ Any file with passwords/tokens
```

### Customer Data (CRITICAL!)
```
❌ cases/ZD-*                     # All actual case folders
❌ archive/*                      # All archived tickets
❌ Any customer logs
❌ Any customer configurations
❌ Any customer screenshots
❌ Any PII (Personally Identifiable Information)
```

### Personal/Local Files
```
❌ .DS_Store                      # macOS metadata
❌ .vscode/                       # Personal editor settings
❌ .idea/                         # Personal IDE settings
❌ *.swp, *.swo                   # Vim swap files
❌ __pycache__/                   # Python cache
❌ *.pyc, *.pyo                   # Python compiled files
❌ *.log                          # Log files
```

### Temporary/Test Files
```
❌ test-*.py                      # Personal test scripts
❌ scratch/                       # Scratch work
❌ tmp/                           # Temporary files
```

---

## 🟡 MAYBE COMMIT (Case-by-Case)

### Anonymized Documentation
```
🟡 docs/[product]/troubleshooting/  # Troubleshooting guides
   - ✅ IF: Customer data is anonymized
   - ✅ IF: It helps the team
   - ❌ IF: Contains any customer identifiers
```

### Sanitized Examples
```
🟡 docs/[product]/examples/       # Example configs
   - ✅ IF: Completely generic/sanitized
   - ❌ IF: Based on real customer setup
```

### Updated Known Issues
```
🟡 solutions/known-issues.md      # Updated with new bugs
   - ✅ DO commit updates to share with team
   - ❌ DON'T include customer names
   - ✅ DO reference JIRA tickets (SCRS-XXXX)
   - ❌ DON'T reference Zendesk tickets (ZD-XXXXX)
```

---

## Current Status Check

### ⚠️ ISSUE: Case Folder in Workspace
```
❌ cases/ZD-2488538/              # This should NOT be committed!
```

**This folder contains:**
- Customer case investigation
- Potentially sensitive data
- Should be local only

**Action Required:**
The `.gitignore` already protects this (`cases/*` with `!cases/.template/`), 
but verify it's not tracked if you init git.

---

## Recommended .gitignore (Already Configured)

```gitignore
# Environment & Credentials
.env
.cursor/mcp.json

# Case folders (may contain customer data)
cases/*
!cases/.template/

# Archive (may contain customer data)
archive/*

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Editors
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

**Status:** ✅ Already properly configured

---

## Git Initialization Steps

### 1. Initialize Repository
```bash
cd ~/tse-investigation-hub
git init
```

### 2. Verify .gitignore is Working
```bash
# Check what would be added
git status

# Should NOT see:
# - .env
# - .cursor/mcp.json
# - cases/ZD-* (any actual cases)
# - archive/* (any archives)

# SHOULD see:
# - README.md
# - SETUP.md
# - scripts/*.py
# - templates/**/*.md
# - etc.
```

### 3. Initial Commit
```bash
git add .
git commit -m "Initial commit: TSE Investigation Hub structure"
```

### 4. Add Remote (if using GitHub/GitLab)
```bash
# Option A: GitHub
git remote add origin git@github.com:YOUR_ORG/tse-investigation-hub.git

# Option B: GitLab
git remote add origin git@gitlab.com:YOUR_ORG/tse-investigation-hub.git

git push -u origin main
```

---

## Team Collaboration Workflow

### For Team Members Cloning the Repo

```bash
# 1. Clone
git clone git@github.com:YOUR_ORG/tse-investigation-hub.git
cd tse-investigation-hub

# 2. Set up credentials (NOT in git)
cp .env.example .env
# Edit .env with your tokens

cp .cursor/mcp.json.example .cursor/mcp.json
# Edit .cursor/mcp.json with your tokens

# 3. Ready to use!
# cases/ and archive/ folders are local only
```

### Sharing Knowledge Updates

**DO share:**
```bash
# Update known issues
vim solutions/known-issues.md
git add solutions/known-issues.md
git commit -m "Add known issue: Agent 7.52 memory leak"
git push

# Add troubleshooting doc
vim docs/apm/troubleshooting/trace-sampling.md
git add docs/apm/troubleshooting/trace-sampling.md
git commit -m "Add APM trace sampling troubleshooting guide"
git push

# Improve template
vim templates/customer-communication/solution.md
git add templates/customer-communication/solution.md
git commit -m "Add rollback section to solution template"
git push
```

**DON'T share:**
```bash
# ❌ Never commit actual cases
git add cases/ZD-12345/  # NO!

# ❌ Never commit credentials
git add .env  # NO!
git add .cursor/mcp.json  # NO!

# ❌ Never commit customer data
git add archive/  # NO!
```

---

## File-by-File Analysis

| File/Folder | Commit? | Reason |
|-------------|---------|--------|
| `README.md` | ✅ YES | Team documentation |
| `SETUP.md` | ✅ YES | Setup instructions |
| `QUICK_START.md` | ✅ YES | Quick reference |
| `STRUCTURE.md` | ✅ YES | Architecture docs |
| `GIT_STRATEGY.md` | ✅ YES | This file! |
| `.cursorrules` | ✅ YES | AI behavior (no secrets) |
| `.gitignore` | ✅ YES | Protection config |
| `.env.example` | ✅ YES | Template only |
| `.env` | ❌ NO | Real credentials |
| `.cursor/mcp.json.example` | ✅ YES | Template only |
| `.cursor/mcp.json` | ❌ NO | Real credentials |
| `scripts/*.py` | ✅ YES | Tools for everyone |
| `cases/.template/` | ✅ YES | Template structure |
| `cases/ZD-*` | ❌ NO | Customer data |
| `archive/*` | ❌ NO | Customer data |
| `templates/**/*.md` | ✅ YES | Communication templates |
| `docs/escalation-criteria.md` | ✅ YES | Team guidelines |
| `docs/[product]/` | ✅ YES | Empty structure |
| `solutions/known-issues.md` | ✅ YES | Template + updates |
| `reference/` | ✅ YES | Shared references |

---

## Security Checklist

Before pushing to git, verify:

- [ ] No `.env` file committed
- [ ] No `.cursor/mcp.json` committed
- [ ] No `cases/ZD-*` folders committed
- [ ] No `archive/` contents committed
- [ ] No customer names in commit messages
- [ ] No API tokens in any files
- [ ] No passwords in any files
- [ ] No customer logs or configs
- [ ] No PII (emails, names, IPs, etc.)
- [ ] `.gitignore` is properly configured

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Committing Real Credentials
```bash
# Wrong:
git add .env
git add .cursor/mcp.json

# Right:
# These are gitignored, but never force-add them
```

### ❌ Mistake 2: Committing Customer Cases
```bash
# Wrong:
git add cases/ZD-12345/

# Right:
# Only cases/.template/ should be in git
```

### ❌ Mistake 3: Customer Data in Docs
```bash
# Wrong:
echo "Customer Acme Corp had this issue..." > docs/apm/example.md

# Right:
echo "A customer experienced this issue..." > docs/apm/example.md
# Anonymize everything!
```

### ❌ Mistake 4: Force Adding Ignored Files
```bash
# Wrong:
git add -f .env  # Force adds ignored file!

# Right:
# Never use -f to add files that are gitignored for security
```

---

## Audit Commands

### Check what's staged before committing:
```bash
git status
git diff --cached
```

### Check for accidentally committed secrets:
```bash
# Search for potential tokens
git log -p | grep -i "token\|password\|secret\|api_key"

# Check specific file history
git log -p -- .env
```

### Remove accidentally committed file:
```bash
# If you committed but haven't pushed:
git rm --cached .env
git commit --amend

# If you already pushed (more serious):
# Contact your team lead - may need to:
# 1. Rotate all exposed credentials
# 2. Force push (if allowed)
# 3. Use git-filter-repo or BFG Repo-Cleaner
```

---

## Summary

### ✅ Safe to Share (Commit)
- Documentation, templates, scripts
- Empty folder structures
- Configuration templates (`.example` files)
- Anonymized troubleshooting guides
- Team knowledge (known issues, escalation criteria)

### ❌ Never Share (Local Only)
- Real credentials (`.env`, `mcp.json`)
- Customer cases (`cases/ZD-*`)
- Archived tickets (`archive/*`)
- Any customer data or PII
- Personal editor settings

### 🎯 Goal
Create a **shared knowledge base and tooling** for the TSE team while **protecting customer data and credentials**.

---

**Next Step:** Initialize git and make first commit (see "Git Initialization Steps" above)

