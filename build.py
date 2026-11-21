#!/usr/bin/env python3
"""Generate the static 2026 AI Interview Handbook site."""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

import markdown
from markdown.extensions.toc import TocExtension

ROOT = Path(__file__).resolve().parent
SRC = Path("/home/ubuntu/grok/ai-interview-prep-2026")
OUT = ROOT / "dist"

CHAPTERS = [
    {
        "file": "README.md",
        "slug": "overview",
        "id": "—",
        "title": "Overview",
        "group": "Start here",
        "nav": "Overview",
    },
    {
        "file": "00-how-to-use.md",
        "slug": "00-how-to-use",
        "id": "00",
        "title": "How to Use This Interview System",
        "group": "Start here",
        "nav": "How to use",
    },
    {
        "file": "01-2026-market-analysis.md",
        "slug": "01-2026-market-analysis",
        "id": "01",
        "title": "2026 AI Interview Market Analysis",
        "group": "Start here",
        "nav": "Market analysis",
    },
    {
        "file": "02-interview-process-by-role.md",
        "slug": "02-interview-process-by-role",
        "id": "02",
        "title": "Interview Process by Role",
        "group": "Start here",
        "nav": "Process by role",
    },
    {
        "file": "03-skill-matrix.md",
        "slug": "03-skill-matrix",
        "id": "03",
        "title": "Master Interview Skill Matrix",
        "group": "Start here",
        "nav": "Skill matrix",
    },
    {
        "file": "04-topic-probability-ranking.md",
        "slug": "04-topic-probability-ranking",
        "id": "04",
        "title": "Most Frequently Asked Topics",
        "group": "Start here",
        "nav": "Topic ranking",
    },
    {
        "file": "05-answer-frameworks.md",
        "slug": "05-answer-frameworks",
        "id": "05",
        "title": "Answer Frameworks",
        "group": "Start here",
        "nav": "Answer frameworks",
    },
    {
        "file": "roles/00-primary-eight.md",
        "slug": "roles",
        "id": "R",
        "title": "Primary Eight Roles",
        "group": "Start here",
        "nav": "Pick a role",
    },
    {
        "file": "guides/06-python.md",
        "slug": "06-python",
        "id": "06",
        "title": "Python for AI Engineers",
        "group": "Core engineering",
        "nav": "Python",
    },
    {
        "file": "guides/07-sql.md",
        "slug": "07-sql",
        "id": "07",
        "title": "SQL for AI Engineers",
        "group": "Core engineering",
        "nav": "SQL",
    },
    {
        "file": "guides/08-apis.md",
        "slug": "08-apis",
        "id": "08",
        "title": "APIs for AI Engineers",
        "group": "Core engineering",
        "nav": "APIs",
    },
    {
        "file": "guides/09-llm.md",
        "slug": "09-llm",
        "id": "09",
        "title": "LLMs",
        "group": "AI systems",
        "nav": "LLMs",
    },
    {
        "file": "guides/10-rag.md",
        "slug": "10-rag",
        "id": "10",
        "title": "RAG",
        "group": "AI systems",
        "nav": "RAG",
    },
    {
        "file": "guides/11-agentic-ai.md",
        "slug": "11-agentic-ai",
        "id": "11",
        "title": "Agentic AI",
        "group": "AI systems",
        "nav": "Agentic AI",
    },
    {
        "file": "guides/12-mcp.md",
        "slug": "12-mcp",
        "id": "12",
        "title": "Model Context Protocol",
        "group": "AI systems",
        "nav": "MCP",
    },
    {
        "file": "guides/13-multi-agent.md",
        "slug": "13-multi-agent",
        "id": "13",
        "title": "Multi-Agent Systems",
        "group": "AI systems",
        "nav": "Multi-agent",
    },
    {
        "file": "guides/14-vector-databases.md",
        "slug": "14-vector-databases",
        "id": "14",
        "title": "Vector Databases",
        "group": "AI systems",
        "nav": "Vector DBs",
    },
    {
        "file": "guides/15-cloud-ai.md",
        "slug": "15-cloud-ai",
        "id": "15",
        "title": "Cloud AI Platforms",
        "group": "Production",
        "nav": "Cloud AI",
    },
    {
        "file": "guides/16-docker-kubernetes.md",
        "slug": "16-docker-kubernetes",
        "id": "16",
        "title": "Docker and Kubernetes",
        "group": "Production",
        "nav": "Docker / K8s",
    },
    {
        "file": "guides/17-llmops.md",
        "slug": "17-llmops",
        "id": "17",
        "title": "LLMOps",
        "group": "Production",
        "nav": "LLMOps",
    },
    {
        "file": "guides/18-aiops.md",
        "slug": "18-aiops",
        "id": "18",
        "title": "AIOps",
        "group": "Production",
        "nav": "AIOps",
    },
    {
        "file": "guides/19-ai-security.md",
        "slug": "19-ai-security",
        "id": "19",
        "title": "AI Security",
        "group": "Production",
        "nav": "AI Security",
    },
    {
        "file": "design/20-system-design.md",
        "slug": "20-system-design",
        "id": "20",
        "title": "AI System Design Interviews",
        "group": "Design",
        "nav": "System design",
    },
    {
        "file": "design/21-architecture-problems.md",
        "slug": "21-architecture-problems",
        "id": "21",
        "title": "Architecture Problems",
        "group": "Design",
        "nav": "Architecture",
    },
    {
        "file": "banks/22-troubleshooting.md",
        "slug": "22-troubleshooting",
        "id": "22",
        "title": "Troubleshooting Production AI",
        "group": "Design",
        "nav": "Troubleshooting",
    },
    {
        "file": "career/23-project-defense.md",
        "slug": "23-project-defense",
        "id": "23",
        "title": "Project Defense",
        "group": "Career",
        "nav": "Project defense",
    },
    {
        "file": "career/24-behavioral.md",
        "slug": "24-behavioral",
        "id": "24",
        "title": "Behavioral Interviews",
        "group": "Career",
        "nav": "Behavioral",
    },
    {
        "file": "career/25-tell-me-about-yourself.md",
        "slug": "25-tell-me-about-yourself",
        "id": "25",
        "title": "Tell Me About Yourself",
        "group": "Career",
        "nav": "Tell me about yourself",
    },
    {
        "file": "career/26-career-transition.md",
        "slug": "26-career-transition",
        "id": "26",
        "title": "Career Transition into AI",
        "group": "Career",
        "nav": "Career transition",
    },
    {
        "file": "career/27-hr-salary.md",
        "slug": "27-hr-salary",
        "id": "27",
        "title": "Recruiter Screen, Offers, Negotiation",
        "group": "Career",
        "nav": "Offers & salary",
    },
    {
        "file": "career/28-psychology-rejections-tactics.md",
        "slug": "28-psychology-rejections-tactics",
        "id": "28",
        "title": "Interviewer Psychology & Rejections",
        "group": "Career",
        "nav": "Psychology",
    },
    {
        "file": "career/34-questions-to-ask.md",
        "slug": "34-questions-to-ask",
        "id": "34",
        "title": "Questions to Ask the Interviewer",
        "group": "Career",
        "nav": "Questions to ask",
    },
    {
        "file": "mocks/29-mock-interviews.md",
        "slug": "29-mock-interviews",
        "id": "29",
        "title": "Mock Interviews",
        "group": "Practice",
        "nav": "Mock interviews",
    },
    {
        "file": "mocks/30-pressure-mode.md",
        "slug": "30-pressure-mode",
        "id": "30",
        "title": "Pressure Mode",
        "group": "Practice",
        "nav": "Pressure mode",
    },
    {
        "file": "mocks/31-rapid-fire.md",
        "slug": "31-rapid-fire",
        "id": "31",
        "title": "Rapid-Fire",
        "group": "Practice",
        "nav": "Rapid-fire",
    },
    {
        "file": "banks/00-role-question-banks.md",
        "slug": "question-banks",
        "id": "Q",
        "title": "Role-Specific Question Banks",
        "group": "Practice",
        "nav": "Question banks",
    },
    {
        "file": "banks/01-core-twenty-full-answers.md",
        "slug": "core-twenty",
        "id": "C20",
        "title": "Core 20 Full Answers",
        "group": "Practice",
        "nav": "Core 20 answers",
    },
    {
        "file": "cheatsheets/32-cheat-sheets.md",
        "slug": "32-cheat-sheets",
        "id": "32",
        "title": "Cheat Sheets",
        "group": "Reference",
        "nav": "Cheat sheets",
    },
    {
        "file": "cheatsheets/33-24h-60min.md",
        "slug": "33-24h-60min",
        "id": "33",
        "title": "24-Hour Checklist and 60-Minute Sheet",
        "group": "Reference",
        "nav": "24h / 60min",
    },
    {
        "file": "35-scorecard-checklists.md",
        "slug": "35-scorecard-checklists",
        "id": "35",
        "title": "Scorecard and Weakness Detection",
        "group": "Reference",
        "nav": "Scorecards",
    },
]

ROLES = [
    ("01", "AIOps Engineer", "Correlate noise, RCA, safe remediation, ITSM."),
    ("02", "Cloud AI Engineer", "Land models, RAG, and agents on one cloud with IAM, networking, and cost."),
    ("03", "Intelligent Automation Engineer", "Turn messy processes into human-in-the-loop workflows."),
    ("04", "AI Security Engineer", "Threat-model RAG, agents, and MCP. Fail closed on authz."),
    ("05", "Forward Deployed / AI Deployment", "Scope messy customer problems, ship v0, then operate."),
    ("06", "GenAI / Agentic AI Engineer", "Ship measurable RAG and agent systems. Evals are the product."),
    ("07", "AI Solutions Engineer", "Discover fit, translate, demo, and recommend not buying."),
    ("08", "AI Solutions Architect", "End-to-end estate, governance, cost, security, operating model."),
]

FILE_TO_SLUG = {c["file"]: c["slug"] for c in CHAPTERS}
BASENAME_TO_SLUG = {Path(c["file"]).name: c["slug"] for c in CHAPTERS}


def rewrite_md_links(text: str) -> str:
    def repl(match: re.Match) -> str:
        label, url = match.group(1), match.group(2)
        if url.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        path, frag = (url.split("#", 1) + [""])[:2]
        path = path.strip()
        if not path.endswith(".md"):
            return match.group(0)
        base = os.path.basename(path)
        slug = BASENAME_TO_SLUG.get(base)
        if not slug:
            slug = Path(base).stem
        href = f"/{slug}"
        if frag:
            href += f"#{frag}"
        return f"[{label}]({href})"

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)


def md_to_html(text: str) -> str:
    md = markdown.Markdown(
        extensions=[
            "tables",
            "fenced_code",
            "sane_lists",
            "smarty",
            TocExtension(permalink=False),
        ]
    )
    return md.convert(rewrite_md_links(text))


def strip_text(md_text: str) -> str:
    t = re.sub(r"```.*?```", " ", md_text, flags=re.S)
    t = re.sub(r"[#>*`_[\]()|]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:400]


def nav_html() -> str:
    groups: dict[str, list] = {}
    for ch in CHAPTERS:
        groups.setdefault(ch["group"], []).append(ch)
    blocks = []
    for group, items in groups.items():
        links = "".join(
            f'<a class="nav-link" href="/{ch["slug"]}"><span class="n">{ch["id"]}</span>{ch["nav"]}</a>'
            for ch in items
        )
        blocks.append(f'<div class="nav-group"><div class="nav-label">{group}</div>{links}</div>')
    return "".join(blocks)


def spa_shell() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>2026 AI Interview Handbook</title>
  <meta name="description" content="Production-grade interview system for eight 2026 AI roles." />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <div class="topbar">
    <button id="menu-toggle" class="search-btn" style="width:auto">Menu</button>
    <a class="brand-kicker" href="/" style="text-decoration:none">2026 Handbook</a>
    <button id="search-open-mobile" class="search-btn" style="width:auto">Search</button>
  </div>
  <div class="shell">
    <aside class="sidebar" id="sidebar">
      <a class="brand" href="/">
        <div class="mark">26</div>
        <div class="brand-text">
          <div class="brand-kicker">Interview system</div>
          <div class="brand-name">AI Handbook</div>
        </div>
      </a>
      <button class="search-btn" id="search-open" type="button">
        <span>Search chapters</span><kbd>/</kbd>
      </button>
      <nav>{nav_html()}</nav>
    </aside>
    <main class="main" id="content">
      <div class="article">
        <div class="kicker" id="kicker">Loading</div>
        <div id="article"><p>Loading handbook…</p></div>
      </div>
    </main>
  </div>
  <div class="overlay" id="search-overlay">
    <div class="search-box">
      <input id="search-input" placeholder="Search the handbook…" autocomplete="off" />
      <div class="search-results" id="search-results"></div>
    </div>
  </div>
  <script src="/app.js"></script>
</body>
</html>
"""


def homepage_body() -> str:
    role_cards = "\n".join(
        f'<a class="card" href="/roles"><div class="num">Role {n}</div><h3>{name}</h3><p>{blurb}</p></a>'
        for n, name, blurb in ROLES
    )
    groups: dict[str, list] = {}
    for ch in CHAPTERS:
        groups.setdefault(ch["group"], []).append(ch)
    index_blocks = []
    for group, items in groups.items():
        links = "".join(
            f'<a href="/{c["slug"]}"><span class="id">{c["id"]}</span><span>{c["title"]}</span></a>'
            for c in items
        )
        index_blocks.append(f"<h3>{group}</h3><div class='chapter-index'>{links}</div>")
    return f"""
    <section class="hero">
      <h1>Walk into the interview with a system, not a script.</h1>
      <p class="lede">A performance handbook for 2026 AI production loops: RAG, agents, evals, security, cloud, and the career conversation around them.</p>
      <div class="meta-row">
        <span class="chip">Version 2026.09</span>
        <span class="chip">40 chapters</span>
        <span class="chip">8 primary roles</span>
        <span class="chip">Press / to search</span>
      </div>
    </section>
    <h2 class="section-title">Pick one primary role</h2>
    <div class="grid">{role_cards}</div>
    <h2 class="section-title">How to study</h2>
    <div class="path-grid">
      <div class="path"><strong>Path A</strong><h3>8–10 days</h3><p>One role. Skill matrix core-5. Answer frameworks. Two mocks. Scorecard the gaps.</p></div>
      <div class="path"><strong>Path B</strong><h3>4 weeks</h3><p>Market + process, then topic guides, then design and troubleshooting, then career and pressure mode.</p></div>
      <div class="path"><strong>Path C</strong><h3>Night-before</h3><p>Chapter 33, cheat sheets, tell-me-about-yourself, and the questions you will ask them.</p></div>
    </div>
    <h2 class="section-title">Book map</h2>
    {''.join(index_blocks)}
    """


def write_favicon() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" fill="#0d0e11"/>
  <rect x="3" y="3" width="26" height="26" fill="none" stroke="#e0a35a" stroke-width="1.5"/>
  <text x="16" y="21" text-anchor="middle" font-size="11" fill="#e0a35a" font-family="Georgia">26</text>
</svg>
"""


def compact_html(html: str) -> str:
    html = re.sub(r">\s+<", "><", html)
    return html.strip()


def main() -> None:
    import gzip

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    pages = {
        "home": compact_html(homepage_body()),
        "404": "<h1>This page is not in the handbook.</h1><p><a href='/'>Return home</a></p>",
    }
    meta = {
        "home": {"title": "Home", "kicker": "2026 AI Interview Handbook"},
        "404": {"title": "Not found", "kicker": "404"},
    }
    search = [
        {
            "title": "Home",
            "slug": "home",
            "href": "/",
            "group": "Start here",
            "text": "AI interview handbook roles RAG agents evals security cloud",
        }
    ]
    for ch in CHAPTERS:
        raw = (SRC / ch["file"]).read_text(encoding="utf-8")
        pages[ch["slug"]] = compact_html(md_to_html(raw))
        meta[ch["slug"]] = {
            "title": ch["title"],
            "kicker": f"Chapter {ch['id']} · {ch['group']}",
        }
        search.append(
            {
                "title": ch["title"],
                "slug": ch["slug"],
                "href": f"/{ch['slug']}",
                "group": ch["group"],
                "text": strip_text(raw),
            }
        )

    pack = {
        "pages": pages,
        "meta": meta,
        "search": search,
        "footer": '<div class="footer">2026 AI Interview Preparation Handbook · research window Jan–Sep 2026 · not generic LeetCode prep.</div>',
    }
    blob = json.dumps(pack, separators=(",", ":")).encode("utf-8")
    gz = gzip.compress(blob, compresslevel=9)

    (OUT / "index.html").write_text(spa_shell(), encoding="utf-8")
    (OUT / "404.html").write_text(spa_shell(), encoding="utf-8")
    (OUT / "favicon.svg").write_text(write_favicon(), encoding="utf-8")
    shutil.copy(ROOT / "styles.css", OUT / "styles.css")
    shutil.copy(ROOT / "app.js", OUT / "app.js")
    (OUT / "content.json.gz").write_bytes(gz)
    (OUT / "vercel.json").write_text(
        json.dumps(
            {
                "cleanUrls": True,
                "trailingSlash": False,
                "rewrites": [{"source": "/:path*", "destination": "/index.html"}],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"content.json.gz {len(gz)} bytes from {len(blob)} json")
    print(f"Wrote {len(list(OUT.iterdir()))} files to {OUT}")


if __name__ == "__main__":
    main()
