# GitHub Setup for TSE Investigation Hub

Follow these steps to push the repository to GitHub and share with your team.

---

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface

1. Go to: https://github.com/new (or your org: https://github.com/organizations/YOUR_ORG/repositories/new)

2. **Fill in details:**
   - **Repository name:** `tse-investigation-hub`
   - **Description:** "AI-powered investigation workspace for Technical Support Engineers"
   - **Visibility:** 
     - ✅ **Private** (recommended - contains internal processes)
     - ❌ Public (not recommended - internal tooling)
   - **Initialize repository:** ❌ **Do NOT check** (we already have code)
     - Don't add README
     - Don't add .gitignore
     - Don't add license

3. Click **"Create repository"**

4. Copy the SSH URL: `git@github.com:YOUR_ORG/tse-investigation-hub.git`

### Option B: Using GitHub CLI

```bash
# Install gh if you don't have it
brew install gh

# Authenticate (if needed)
gh auth login

# Create private repo
gh repo create tse-investigation-hub --private \
  --description "AI-powered investigation workspace for Technical Support Engineers" \
  --source=. \
  --remote=origin \
  --push
```

---

## Step 2: Add Remote and Push (If using Web Interface)

```bash
cd ~/tse-investigation-hub

# Add GitHub as remote
git remote add origin git@github.com:YOUR_ORG/tse-investigation-hub.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

**Replace `YOUR_ORG` with:**
- Your GitHub username (for personal repos)
- Your organization name (e.g., `DataDog` if it's an org repo)

---

## Step 3: Verify on GitHub

1. Go to: `https://github.com/YOUR_ORG/tse-investigation-hub`

2. **Check that you see:**
   - ✅ README.md with full documentation
   - ✅ All folders: cases/, docs/, scripts/, templates/
   - ✅ .gitignore is present

3. **Verify protection - should NOT see:**
   - ❌ .env file
   - ❌ .cursor/mcp.json
   - ❌ cases/ZD-* folders
   - ❌ Any customer data

4. **Check .gitignore is working:**
   - Click on `cases/` folder
   - Should only see `.template/` subfolder
   - Should NOT see `ZD-*` folders

---

## Step 4: Set Up Repository Settings

### Enable Branch Protection (Recommended)

1. Go to: `Settings` → `Branches`
2. Click `Add rule` for `main` branch
3. **Recommended settings:**
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass
   - ✅ Include administrators (optional)
   - ✅ Restrict who can push to matching branches

### Add Team Access

1. Go to: `Settings` → `Collaborators and teams`
2. Click `Add teams` or `Add people`
3. Add your TSE team with appropriate permissions:
   - **Write** - Can read, clone, push (for active contributors)
   - **Read** - Can read and clone only (for reference)

### Repository Topics (Optional)

Add topics to help discovery:
- `tse`
- `support-engineering`
- `investigation`
- `zendesk`
- `cursor-ai`
- `datadog`

---

## Step 5: Share with Team

### Send to TSEs

```
Hey team! 👋

I've set up a new TSE Investigation Hub to help us work cases more efficiently with AI assistance.

🔗 Repo: https://github.com/YOUR_ORG/tse-investigation-hub

📚 Features:
- Zendesk integration (fetch tickets in Cursor)
- Customer communication templates
- Case investigation templates
- Historical case search
- Escalation criteria guide
- Known issues tracking

🚀 Getting Started:
1. Clone the repo
2. Follow SETUP.md (15 min)
3. Check out QUICK_START.md

Questions? Check the docs or ask in #support-team
```

---

## Step 6: Regular Updates Workflow

### For Team Members Making Updates

```bash
# 1. Pull latest changes
git pull origin main

# 2. Make your changes
vim solutions/known-issues.md  # Add new bug
vim docs/apm/troubleshooting/new-guide.md  # Add guide

# 3. Commit
git add solutions/known-issues.md
git commit -m "Add known issue: Agent 7.52 memory leak"

# 4. Push
git push origin main

# OR create a branch and PR:
git checkout -b add-apm-guide
git add docs/apm/troubleshooting/new-guide.md
git commit -m "Add APM trace sampling troubleshooting guide"
git push origin add-apm-guide
# Then create PR on GitHub
```

### What to Share (Commit)

- ✅ Updated known issues
- ✅ New troubleshooting docs (anonymized)
- ✅ Improved templates
- ✅ Script improvements
- ✅ Documentation updates

### What to Keep Local (Don't Commit)

- ❌ Your cases (cases/ZD-*)
- ❌ Your credentials (.env, .cursor/mcp.json)
- ❌ Customer data
- ❌ Personal settings

---

## Troubleshooting

### Issue: Permission Denied

```
ERROR: Permission to YOUR_ORG/tse-investigation-hub.git denied
```

**Solution:**
1. Verify you have access to the repo
2. Check SSH key is added to GitHub: https://github.com/settings/keys
3. Test SSH: `ssh -T git@github.com`
4. If using org repo, verify org SSO is authorized

### Issue: Repository Doesn't Exist

```
ERROR: Repository not found
```

**Solution:**
1. Verify repo was created on GitHub
2. Check the remote URL: `git remote -v`
3. Update if wrong: `git remote set-url origin git@github.com:CORRECT_ORG/tse-investigation-hub.git`

### Issue: Accidentally Pushed Secrets

**If you accidentally pushed credentials:**

1. **IMMEDIATELY rotate the exposed credentials:**
   - Regenerate Zendesk API token
   - Regenerate Atlassian API token
   - Regenerate any other exposed secrets

2. **Remove from history** (contact team lead for help):
   ```bash
   # This requires special tools and coordination
   # DO NOT attempt without team lead approval
   # May need: git-filter-repo or BFG Repo-Cleaner
   ```

3. **Prevention:**
   - Verify `.gitignore` before committing: `git status --ignored`
   - Never use `git add -f` on ignored files
   - Review staged files: `git diff --cached`

---

## Security Checklist

Before every push, verify:

- [ ] No real credentials in files
- [ ] No customer names or data
- [ ] No Zendesk ticket IDs (ZD-*) in commits
- [ ] `.gitignore` is protecting sensitive files
- [ ] Commit message doesn't reference customer data
- [ ] Only sharing templates/docs, not actual cases

---

## Repository Structure on GitHub

After pushing, your repo should look like:

```
tse-investigation-hub/
├── .cursor/
│   └── mcp.json.example         ← Template (safe)
├── .cursorrules                 ← Shared
├── .env.example                 ← Template (safe)
├── .gitignore                   ← Protects secrets
├── GIT_STRATEGY.md              ← This guide
├── GITHUB_SETUP.md              ← GitHub setup
├── README.md                    ← Main docs
├── SETUP.md                     ← Setup guide
├── QUICK_START.md               ← Quick reference
├── STRUCTURE.md                 ← Architecture
├── cases/
│   └── .template/               ← Template only
├── docs/                        ← Product docs
├── scripts/                     ← Tools
├── solutions/                   ← Known issues
└── templates/                   ← Communication templates
```

**Missing from GitHub (by design):**
- ❌ `.env` (gitignored)
- ❌ `.cursor/mcp.json` (gitignored)
- ❌ `cases/ZD-*` (gitignored)
- ❌ `archive/*` (gitignored)

---

## Clone Instructions for Team

For new team members to get started:

```bash
# 1. Clone the repo
git clone git@github.com:YOUR_ORG/tse-investigation-hub.git
cd tse-investigation-hub

# 2. Set up credentials (NOT in git)
cp .env.example .env
# Edit .env with your tokens

cp .cursor/mcp.json.example .cursor/mcp.json
# Edit .cursor/mcp.json with your tokens

# 3. Install dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh

# 4. Open in Cursor
cursor .

# 5. Restart Cursor (Cmd+Q, reopen)

# 6. Test
# Ask Cursor: "Use MCP to fetch Zendesk ticket 12345"
```

---

**Next:** Add the remote and push (see Step 2 above)

