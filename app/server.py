#!/usr/bin/env python3
"""
TSE Hub - Local web interface for TSE customer case investigations.

Usage:
    python server.py              # Start on http://localhost:5002
    python server.py --port 8080  # Custom port
"""

import os
import re
import sys
import json
import time
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

from flask import Flask, render_template, request, jsonify, abort, Response

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension

# ── Paths ────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = ROOT / "cases"
ARCHIVE_DIR = ROOT / "archive"
SOLUTIONS_DIR = ROOT / "solutions"
TEMPLATES_DIR = ROOT / "templates"
DOCS_DIR = ROOT / "docs"

# ── JIRA Client ──────────────────────────────────────────────────────────────

sys.path.insert(0, str(ROOT / "scripts"))


def _jira_fetch(key: str) -> dict | None:
    """Fetch a single JIRA issue. Returns None on failure."""
    try:
        import jira_client as jc
        return jc.get_issue(key)
    except Exception:
        return None


def _extract_jira_activity(issue: dict, max_comments: int = 2) -> dict:
    """Extract status, summary, assignee, updated, and last N comments."""
    fields = issue.get("fields", {})
    try:
        import jira_client as jc
    except Exception:
        jc = None

    status = fields.get("status", {}).get("name", "Unknown")
    updated = fields.get("updated", "")[:16].replace("T", " ")
    summary = fields.get("summary", "")

    assignee_field = fields.get("customfield_11300", []) or []
    assignees = [a.get("displayName", "") for a in assignee_field if a] if assignee_field else []

    comments_raw = fields.get("comment", {}).get("comments", [])
    recent_comments = []
    for c in comments_raw[-max_comments:]:
        author = c.get("author", {}).get("displayName", "Unknown")
        date = c.get("created", "")[:10]
        body = ""
        if jc:
            body = jc.extract_text(c.get("body", {}))
        if len(body) > 300:
            body = body[:300] + "..."
        recent_comments.append({"author": author, "date": date, "body": body})

    return {
        "key": issue.get("key", ""),
        "status": status,
        "summary": summary,
        "updated": updated,
        "assignees": assignees,
        "last_comments": recent_comments,
        "url": f"https://datadoghq.atlassian.net/browse/{issue.get('key', '')}",
    }


def extract_scrs_keys(text: str) -> list[str]:
    """Find all SCRS-XXXX references in text."""
    return sorted(set(re.findall(r"\bSCRS-\d+\b", text)))


def fetch_escalations(scrs_keys: list[str]) -> list[dict]:
    """Fetch JIRA details for a list of SCRS keys."""
    results = []
    for key in scrs_keys:
        issue = _jira_fetch(key)
        if issue:
            results.append(_extract_jira_activity(issue))
    return results


# ── Flask App ────────────────────────────────────────────────────────────────

app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent / "templates"),
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def render_md(text: str) -> str:
    """Render markdown to HTML with syntax highlighting and tables."""
    extensions = [
        FencedCodeExtension(),
        CodeHiliteExtension(css_class="codehilite", guess_lang=False),
        TableExtension(),
        TocExtension(permalink=False),
        "nl2br",
    ]
    return markdown.markdown(text, extensions=extensions)


def read_md_file(path: Path) -> dict | None:
    """Read a markdown file and return metadata + rendered HTML."""
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8")
    title_match = re.match(r"^#\s+(.+)", raw, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.stem
    return {
        "title": title,
        "raw": raw,
        "html": render_md(raw),
        "path": str(path.relative_to(ROOT)),
        "modified": datetime.fromtimestamp(path.stat().st_mtime),
    }


# ── Status / Meta ────────────────────────────────────────────────────────────

VALID_STATUSES = ["new", "investigating", "waiting-on-customer", "escalated", "resolved"]
STATUS_LABELS = {
    "new": "New",
    "investigating": "Investigating",
    "waiting-on-customer": "Waiting on Customer",
    "escalated": "Escalated",
    "resolved": "Resolved",
}
STATUS_COLORS = {
    "new": "purple",
    "investigating": "blue",
    "waiting-on-customer": "amber",
    "escalated": "red",
    "resolved": "green",
}


def _read_meta(case_dir: Path) -> dict:
    """Read meta.json from a case folder, returning defaults if missing."""
    meta_path = case_dir / "meta.json"
    meta = {"status": "new", "assignee": "", "priority": ""}
    if meta_path.exists():
        try:
            data = json.loads(meta_path.read_text())
            if data.get("status") in VALID_STATUSES:
                meta["status"] = data["status"]
            if data.get("assignee"):
                meta["assignee"] = str(data["assignee"]).strip()
            if data.get("priority"):
                meta["priority"] = str(data["priority"]).strip()
        except Exception:
            pass
    return meta


# ── Product Area Detection ───────────────────────────────────────────────────

PRODUCT_AREA_RULES = [
    ("apm", "APM", [
        r"\bapm\b", r"\btrac(e|es|ing)\b", r"\bprofil(e|er|ing)\b",
        r"\bspan\b", r"\bservice\s*map", r"\bdd-trace",
    ]),
    ("infrastructure", "Infrastructure", [
        r"\binfrastructure\b", r"\bagent\s*(v?\d|check|flare|config)",
        r"\bhost\s*monitor", r"\bcontainer\s*monitor",
        r"\bkubernetes\b", r"\becs\b", r"\bprocess\s*agent",
    ]),
    ("logs", "Logs", [
        r"\blog\s*(management|collection|pipeline|parsing|archive|index)",
        r"\bpipeline\b", r"\bparsing\s*rule", r"\blog\s*explorer",
    ]),
    ("rum", "RUM", [
        r"\brum\b", r"\breal\s*user\s*monitor", r"\bsession\s*replay",
        r"\bbrowser\s*sdk\b",
    ]),
    ("synthetics", "Synthetics", [
        r"\bsynthetic", r"\bapi\s*test", r"\bbrowser\s*test",
        r"\bcontinuous\s*testing",
    ]),
    ("security", "Security", [
        r"\bsecurity\b", r"\bappsec\b", r"\bsiem\b", r"\bcspm\b",
        r"\bcws\b", r"\bvulnerability\s*manage",
    ]),
    ("network", "Network", [
        r"\bnetwork\s*(performance|device|monitor)", r"\bnpm\b",
        r"\bnetflow\b", r"\bdns\s*monitor",
    ]),
    ("platform", "Platform", [
        r"\bbilling\b", r"\bsso\b", r"\bsaml\b", r"\bapi\s*key",
        r"\bdashboard\s*(widget|template|api)",
        r"\brbac\b", r"\baudit\s*trail",
    ]),
    ("other", "Other", []),
]

_COMPILED_AREA_RULES = [
    (key, label, [re.compile(p, re.IGNORECASE) for p in patterns])
    for key, label, patterns in PRODUCT_AREA_RULES
]

PRODUCT_AREA_LABELS = {key: label for key, label, _pats in PRODUCT_AREA_RULES}


def detect_product_area(text: str) -> str:
    """Detect product area from text. Returns area key, falls back to 'other'."""
    for key, _label, patterns in _COMPILED_AREA_RULES:
        for pat in patterns:
            if pat.search(text):
                return key
    return "other"


# ── Data Source Extraction ───────────────────────────────────────────────────

_SOURCE_TYPES = [
    ("jira", "JIRA", [
        re.compile(r"https?://datadoghq\.atlassian\.net/browse/([\w-]+)", re.I),
    ], [
        re.compile(r"\b(SCRS-\d+|SECENG-\d+)\b"),
    ]),
    ("zendesk", "Zendesk", [
        re.compile(r"https?://[\w.-]*zendesk\.com[\w/._?&#%-]*", re.I),
    ], [
        re.compile(r"\bZD-\d+\b"),
    ]),
    ("confluence", "Confluence", [
        re.compile(r"https?://datadoghq\.atlassian\.net/wiki/[\w/+.-]+", re.I),
    ], []),
    ("datadog_docs", "Datadog Docs", [
        re.compile(r"https?://docs\.datadoghq\.com/[\w/._?&#%-]+", re.I),
    ], []),
    ("github", "GitHub", [
        re.compile(r"https?://github\.com/[\w.-]+/[\w.-]+[\w/._?&#%-]*", re.I),
    ], []),
    ("slack", "Slack", [
        re.compile(r"https?://dd\.(?:enterprise\.)?slack\.com/[\w/.-]+", re.I),
    ], []),
]


def extract_sources(raw_text: str) -> list:
    """Extract data source references from markdown text."""
    sources = []
    for src_key, src_label, url_patterns, ref_patterns in _SOURCE_TYPES:
        refs_seen = set()
        refs = []

        for url_pat in url_patterns:
            for match in url_pat.finditer(raw_text):
                url = match.group(0).rstrip(")")
                display = url
                if src_key == "jira" and match.lastindex and match.lastindex >= 1:
                    display = match.group(1)
                dedup_key = (url, display)
                if dedup_key not in refs_seen:
                    refs_seen.add(dedup_key)
                    refs.append({"url": url, "display": display})

        for ref_pat in ref_patterns:
            for match in ref_pat.finditer(raw_text):
                ref_text = match.group(0)
                already = False
                for r in refs:
                    d = r.get("display") or ""
                    u = r.get("url") or ""
                    if ref_text in d or ref_text in u:
                        already = True
                        break
                if already:
                    continue
                dedup_key = (ref_text, ref_text)
                if dedup_key not in refs_seen:
                    refs_seen.add(dedup_key)
                    url = None
                    if src_key == "jira":
                        url = f"https://datadoghq.atlassian.net/browse/{ref_text}"
                    refs.append({"url": url, "display": ref_text})

        if refs:
            sources.append({"key": src_key, "label": src_label, "refs": refs})

    return sources


# ── Case Loader ──────────────────────────────────────────────────────────────

def get_cases() -> list:
    """List all active cases sorted by last modified (newest first)."""
    if not CASES_DIR.exists():
        return []
    cases = []
    for d in CASES_DIR.iterdir():
        if not d.is_dir() or d.name.startswith("."):
            continue
        case_key = d.name
        notes_path = d / "notes.md"
        readme_path = d / "README.md"

        title = case_key
        for check_path in (readme_path, notes_path):
            if check_path.exists():
                first_line = check_path.read_text(encoding="utf-8").split("\n")[0]
                heading = re.match(r"^#\s+(.+)", first_line)
                if heading:
                    title = heading.group(1).strip()
                    break

        meta = _read_meta(d)
        md_files = sorted(d.glob("*.md"))
        mod_times = [f.stat().st_mtime for f in d.rglob("*") if f.is_file()]
        last_modified = datetime.fromtimestamp(max(mod_times)) if mod_times else None

        area_text = title
        for p in (notes_path, readme_path):
            if p.exists():
                try:
                    area_text += " " + p.read_text(encoding="utf-8", errors="ignore")[:2000]
                except Exception:
                    pass
        product_area = detect_product_area(area_text)

        cases.append({
            "key": case_key,
            "title": title,
            "has_notes": notes_path.exists(),
            "has_readme": readme_path.exists(),
            "files": [f.name for f in md_files],
            "file_count": len(md_files),
            "last_modified": last_modified,
            "status": meta["status"],
            "assignee": meta["assignee"],
            "priority": meta["priority"],
            "product_area": product_area,
        })

    cases.sort(key=lambda x: x["last_modified"] or datetime.min, reverse=True)
    return cases


# ── Archive Loader ───────────────────────────────────────────────────────────

def get_archive_months() -> list:
    """List archive months with ticket counts."""
    if not ARCHIVE_DIR.exists():
        return []

    def _month_sort_key(d):
        try:
            parts = d.name.split("-")
            return (int(parts[1]), int(parts[0]))
        except (IndexError, ValueError):
            return (0, 0)

    months = []
    for d in sorted(ARCHIVE_DIR.iterdir(), key=_month_sort_key, reverse=True):
        if not d.is_dir():
            continue
        tickets = sorted(d.glob("*.md"), reverse=True)
        ticket_list = []
        for t in tickets:
            title = t.stem
            content_preview = ""
            try:
                content_preview = t.read_text(encoding="utf-8", errors="ignore")[:2000]
                for line in content_preview.split("\n", 5):
                    heading = re.match(r"^#\s+(.+)", line)
                    if heading:
                        title = heading.group(1).strip()
                        break
            except Exception:
                pass
            area = detect_product_area(content_preview)
            ticket_list.append({
                "key": t.stem,
                "path": str(t.relative_to(ROOT)),
                "title": title,
                "product_area": area,
            })
        months.append({"name": d.name, "count": len(ticket_list), "tickets": ticket_list})
    return months


# ── Templates Loader ─────────────────────────────────────────────────────────

def get_template_categories() -> list:
    """Load template categories and their files."""
    if not TEMPLATES_DIR.exists():
        return []
    categories = []
    for sub in sorted(TEMPLATES_DIR.iterdir()):
        if not sub.is_dir() or sub.name.startswith("."):
            continue
        files = []
        for f in sorted(sub.glob("*.md")):
            files.append({
                "name": f.stem.replace("-", " ").replace("_", " ").title(),
                "filename": f.name,
                "path": str(f.relative_to(ROOT)),
            })
        if files:
            categories.append({
                "name": sub.name.replace("-", " ").replace("_", " ").title(),
                "dir_name": sub.name,
                "files": files,
            })
    return categories


# ── Known Issues Loader ──────────────────────────────────────────────────────

def get_known_issues() -> dict | None:
    """Load and render solutions/known-issues.md."""
    ki_path = SOLUTIONS_DIR / "known-issues.md"
    return read_md_file(ki_path)


# ── Docs Loader ──────────────────────────────────────────────────────────────

def get_docs_tree(base_dir: Path = None) -> list:
    """Build a tree of documentation files."""
    if base_dir is None:
        base_dir = DOCS_DIR
    if not base_dir.exists():
        return []
    tree = []
    for item in sorted(base_dir.iterdir()):
        if item.name.startswith(".") or item.name.startswith("_"):
            continue
        if item.is_dir():
            children = get_docs_tree(item)
            if children:
                tree.append({"type": "dir", "name": item.name, "children": children})
        elif item.suffix == ".md":
            tree.append({
                "type": "file",
                "name": item.stem,
                "path": str(item.relative_to(ROOT)),
            })
    return tree


# ── Search ───────────────────────────────────────────────────────────────────

def search_files(query: str, max_results: int = 50) -> list:
    """Search all markdown files for a query string (case-insensitive)."""
    results = []
    query_lower = query.lower()
    search_dirs = [CASES_DIR, ARCHIVE_DIR, SOLUTIONS_DIR, DOCS_DIR, TEMPLATES_DIR]

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for md_file in search_dir.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
            except Exception:
                continue

            if query_lower not in content.lower():
                continue

            lines = content.split("\n")
            snippets = []
            for i, line in enumerate(lines):
                if query_lower in line.lower():
                    start = max(0, i - 1)
                    end = min(len(lines), i + 2)
                    snippet = "\n".join(lines[start:end]).strip()
                    snippets.append(snippet)
                    if len(snippets) >= 2:
                        break

            title_match = re.match(r"^#\s+(.+)", content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else md_file.stem
            rel = md_file.relative_to(ROOT)
            section = str(rel).split("/")[0]

            results.append({
                "title": title,
                "path": str(rel),
                "section": section,
                "snippets": snippets,
                "modified": datetime.fromtimestamp(md_file.stat().st_mtime),
            })
            if len(results) >= max_results:
                return results

    results.sort(key=lambda r: r["modified"], reverse=True)
    return results


# ── Context Processor ────────────────────────────────────────────────────────

@app.context_processor
def inject_globals():
    """Make counts and metadata available to all templates."""
    case_count = len(get_cases())
    archive_months = get_archive_months()
    return {
        "nav_case_count": case_count,
        "nav_archive_count": sum(m["count"] for m in archive_months),
        "nav_doc_count": len(list(DOCS_DIR.rglob("*.md"))) if DOCS_DIR.exists() else 0,
    }


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    cases = get_cases()
    archive_months = get_archive_months()
    total_archived = sum(m["count"] for m in archive_months)
    known_issues = get_known_issues()
    ki_count = 0
    if known_issues:
        ki_count = len(re.findall(r"^###\s+", known_issues["raw"], re.MULTILINE))
    return render_template(
        "dashboard.html",
        cases=cases,
        archive_months=archive_months,
        total_archived=total_archived,
        known_issues_count=ki_count,
    )


@app.route("/cases")
def cases_list():
    cases = get_cases()
    assignees = sorted(set(c["assignee"] for c in cases if c["assignee"]))
    seen_areas = set()
    product_areas = []
    for c in cases:
        area = c.get("product_area", "other")
        if area not in seen_areas:
            seen_areas.add(area)
            product_areas.append(area)
    canonical_order = [key for key, _, _ in PRODUCT_AREA_RULES]
    product_areas.sort(key=lambda a: (a == "other", canonical_order.index(a) if a in canonical_order else 999))
    return render_template(
        "cases.html",
        cases=cases,
        assignees=assignees,
        statuses=VALID_STATUSES,
        status_labels=STATUS_LABELS,
        status_colors=STATUS_COLORS,
        product_areas=product_areas,
        area_labels=PRODUCT_AREA_LABELS,
    )


@app.route("/case/<key>")
def case_detail(key):
    case_dir = CASES_DIR / key
    if not case_dir.exists() or not case_dir.is_dir():
        abort(404)

    md_files = {}
    for f in sorted(case_dir.glob("*.md")):
        data = read_md_file(f)
        if data:
            md_files[f.name] = data

    readme = md_files.get("README.md")
    notes = md_files.get("notes.md")
    other_files = {k: v for k, v in md_files.items() if k not in ("README.md", "notes.md")}

    assets_dir = case_dir / "assets"
    assets = []
    if assets_dir.exists():
        for asset in assets_dir.rglob("*"):
            if asset.is_file() and not asset.name.startswith("."):
                assets.append({
                    "name": asset.name,
                    "path": str(asset.relative_to(ROOT)),
                    "size": asset.stat().st_size,
                    "is_image": asset.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".webp"),
                })

    all_cases = get_cases()
    all_keys = [c["key"] for c in all_cases]
    current_idx = all_keys.index(key) if key in all_keys else -1
    prev_key = all_keys[current_idx - 1] if current_idx > 0 else None
    next_key = all_keys[current_idx + 1] if 0 <= current_idx < len(all_keys) - 1 else None

    meta = _read_meta(case_dir)

    all_raw = ""
    for _name, fdata in md_files.items():
        all_raw += fdata["raw"] + "\n"
    sources = extract_sources(all_raw)

    scrs_keys = extract_scrs_keys(all_raw)
    escalations = fetch_escalations(scrs_keys) if scrs_keys else []

    return render_template(
        "case_detail.html",
        key=key,
        readme=readme,
        notes=notes,
        other_files=other_files,
        assets=assets,
        prev_key=prev_key,
        next_key=next_key,
        meta=meta,
        valid_statuses=VALID_STATUSES,
        status_labels=STATUS_LABELS,
        status_colors=STATUS_COLORS,
        sources=sources,
        sources_count=sum(len(s["refs"]) for s in sources),
        escalations=escalations,
    )


@app.route("/known-issues")
def known_issues():
    data = get_known_issues()
    return render_template("known_issues.html", known_issues=data)


@app.route("/templates")
def templates_page():
    categories = get_template_categories()
    return render_template("templates_list.html", categories=categories)


@app.route("/templates/<category>/<filename>")
def template_detail(category, filename):
    tmpl_path = TEMPLATES_DIR / category / filename
    if not tmpl_path.suffix:
        tmpl_path = tmpl_path.with_suffix(".md")
    data = read_md_file(tmpl_path)
    if not data:
        abort(404)
    return render_template("template_detail.html", template=data, category=category)


@app.route("/archive")
def archive():
    months = get_archive_months()
    return render_template("archive.html", months=months, area_labels=PRODUCT_AREA_LABELS)


@app.route("/archive/<month>/<ticket_key>")
def archive_ticket(month, ticket_key):
    ticket_path = ARCHIVE_DIR / month / f"{ticket_key}.md"
    data = read_md_file(ticket_path)
    if not data:
        abort(404)
    content_preview = ""
    try:
        content_preview = ticket_path.read_text(encoding="utf-8", errors="ignore")[:2000]
    except Exception:
        pass
    area = detect_product_area(content_preview)
    return render_template(
        "archive_ticket.html",
        ticket=data,
        key=ticket_key,
        month=month,
        product_area=area,
        area_label=PRODUCT_AREA_LABELS.get(area, area),
    )


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    results = []
    if query:
        results = search_files(query)
    return render_template("search.html", query=query, results=results)


@app.route("/api/search")
def api_search():
    """JSON search endpoint for AJAX."""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])
    results = search_files(query, max_results=20)
    for r in results:
        r["modified"] = r["modified"].isoformat()
    return jsonify(results)


# ── Error Handlers ───────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TSE Hub local web server")
    parser.add_argument("--port", type=int, default=5002, help="Port (default: 5002)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    print(f"\n  TSE Hub running at http://localhost:{args.port}\n")
    print(f"  Workspace: {ROOT}")
    print(f"  Cases: {len(get_cases())}")
    print(f"  Archive months: {len(get_archive_months())}")
    print()

    app.run(host="127.0.0.1", port=args.port, debug=args.debug)
