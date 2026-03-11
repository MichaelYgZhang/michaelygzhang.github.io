#!/usr/bin/env python3
"""
Fetch GitHub Trending repositories and generate a Jekyll blog post.

Scrapes github.com/trending, classifies repos into tech categories,
picks top 5 directions, and outputs a Markdown post to _posts/.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta

import requests
from bs4 import BeautifulSoup

# Beijing timezone (UTC+8)
BEIJING_TZ = timezone(timedelta(hours=8))

CATEGORY_KEYWORDS = {
    "AI/ML": [
        "ai", "ml", "machine-learning", "deep-learning", "neural", "llm",
        "gpt", "transformer", "diffusion", "stable-diffusion", "langchain",
        "openai", "chatgpt", "copilot", "rag", "embedding", "nlp",
        "computer-vision", "pytorch", "tensorflow", "model", "agent",
        "inference", "training", "fine-tune", "lora", "ggml", "gguf",
        "ollama", "vllm", "huggingface",
    ],
    "Web开发": [
        "web", "frontend", "backend", "react", "vue", "angular", "svelte",
        "next", "nuxt", "tailwind", "css", "html", "javascript", "typescript",
        "node", "deno", "bun", "express", "fastapi", "django", "flask",
        "rails", "laravel", "api", "rest", "graphql", "ui", "component",
    ],
    "DevOps/云原生": [
        "devops", "docker", "kubernetes", "k8s", "helm", "terraform",
        "ansible", "ci", "cd", "pipeline", "jenkins", "github-actions",
        "cloud", "aws", "azure", "gcp", "serverless", "microservice",
        "service-mesh", "istio", "envoy", "prometheus", "grafana",
        "monitoring", "observability", "infrastructure",
    ],
    "数据库/存储": [
        "database", "db", "sql", "nosql", "postgres", "mysql", "sqlite",
        "redis", "mongo", "elasticsearch", "kafka", "queue", "storage",
        "cache", "etcd", "clickhouse", "timeseries", "vector-database",
        "supabase", "prisma",
    ],
    "安全": [
        "security", "vulnerability", "exploit", "pentest", "cve", "firewall",
        "encryption", "auth", "oauth", "jwt", "zero-trust", "scanning",
        "malware", "forensic", "siem", "devsecops", "secret",
    ],
    "系统/基础设施": [
        "os", "kernel", "linux", "system", "runtime", "compiler", "wasm",
        "ebpf", "network", "proxy", "load-balancer", "dns", "performance",
        "benchmark", "scheduler", "distributed", "consensus", "raft",
    ],
    "移动开发": [
        "mobile", "ios", "android", "swift", "kotlin", "flutter", "dart",
        "react-native", "expo", "app", "swiftui", "jetpack-compose",
    ],
    "编程语言/工具": [
        "language", "compiler", "interpreter", "editor", "ide", "vim",
        "neovim", "emacs", "vscode", "terminal", "shell", "cli", "tool",
        "utility", "package-manager", "build", "linter", "formatter",
        "debugger", "profiler", "git",
    ],
}


def fetch_trending_page():
    """Fetch and parse the GitHub Trending page."""
    url = "https://github.com/trending"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_repos(soup):
    """Extract repository info from the parsed trending page."""
    articles = soup.select("article.Box-row")
    if not articles:
        raise RuntimeError(
            "No trending repos found — GitHub page structure may have changed"
        )

    repos = []
    for article in articles:
        # Repo name: h2 > a
        h2 = article.select_one("h2 a")
        if not h2:
            continue
        full_name = h2.get_text(strip=True).replace("\n", "").replace(" ", "")
        # e.g. "owner/repo"
        full_name = re.sub(r"\s+", "", full_name)
        repo_url = "https://github.com" + h2["href"].strip()

        # Description
        p = article.select_one("p")
        description = p.get_text(strip=True) if p else "No description"

        # Language
        lang_span = article.select_one("[itemprop='programmingLanguage']")
        language = lang_span.get_text(strip=True) if lang_span else "Unknown"

        # Stars & Forks — look for links with svg.octicon-star / octicon-repo-forked
        stats = article.select("a.Link--muted")
        stars = ""
        forks = ""
        for link in stats:
            svg = link.select_one("svg")
            if not svg:
                continue
            classes = svg.get("class", [])
            if "octicon-star" in classes:
                stars = link.get_text(strip=True)
            elif "octicon-repo-forked" in classes:
                forks = link.get_text(strip=True)

        # Today's stars
        today_span = article.select_one("span.d-inline-block.float-sm-right")
        today_stars = today_span.get_text(strip=True) if today_span else ""

        repos.append(
            {
                "full_name": full_name,
                "url": repo_url,
                "description": description,
                "language": language,
                "stars": stars,
                "forks": forks,
                "today_stars": today_stars,
            }
        )

    if not repos:
        raise RuntimeError(
            "Parsed 0 repos from trending page — parser may need updating"
        )
    return repos


def classify_repo(repo):
    """Classify a repo into tech categories based on keyword matching."""
    text = " ".join(
        [
            repo["full_name"],
            repo["description"],
            repo["language"],
        ]
    ).lower()

    matched = []
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            matched.append((category, score))

    if not matched:
        return ["编程语言/工具"]  # default fallback
    matched.sort(key=lambda x: x[1], reverse=True)
    return [m[0] for m in matched]


def select_top_directions(repos, top_n=5):
    """Group repos by category and return top N directions by repo count."""
    category_repos = {}
    for repo in repos:
        categories = classify_repo(repo)
        for cat in categories:
            category_repos.setdefault(cat, []).append(repo)

    # Sort categories by number of repos (descending)
    sorted_cats = sorted(category_repos.items(), key=lambda x: len(x[1]), reverse=True)
    return sorted_cats[:top_n]


def _parse_star_count(text):
    """Parse star count string like '1,234' or '1.2k' into an integer."""
    if not text:
        return 0
    text = text.strip().replace(",", "")
    # Handle "123 stars today" format
    text = text.split()[0]
    try:
        if text.lower().endswith("k"):
            return int(float(text[:-1]) * 1000)
        return int(text)
    except (ValueError, IndexError):
        return 0


def save_daily_snapshot(repos, date_str, repo_root):
    """Save today's trending data as a JSON snapshot in _data/trending/."""
    snapshot_dir = os.path.join(repo_root, "_data", "trending")
    os.makedirs(snapshot_dir, exist_ok=True)
    snapshot = []
    for r in repos:
        snapshot.append({
            "full_name": r["full_name"],
            "url": r["url"],
            "description": r["description"],
            "language": r["language"],
            "stars": r["stars"],
            "forks": r["forks"],
            "today_stars": r["today_stars"],
            "stars_numeric": _parse_star_count(r["stars"]),
            "today_stars_numeric": _parse_star_count(r["today_stars"]),
        })
    filepath = os.path.join(snapshot_dir, f"{date_str}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"Saved snapshot: {filepath}")


def load_previous_snapshot(date_str, repo_root):
    """Load yesterday's snapshot. Returns list of repo dicts or None."""
    today = datetime.strptime(date_str, "%Y-%m-%d")
    yesterday_str = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    filepath = os.path.join(repo_root, "_data", "trending", f"{yesterday_str}.json")
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def compute_comparison(today_repos, previous_snapshot):
    """Compare today's repos with yesterday's snapshot.

    Returns a dict with:
      - new_repos: list of repos new to trending today
      - removed_repos: list of repos that left trending
      - retained_repos: list of repos on both days
      - rising_repos: list of retained repos with strong star growth
      - repo_badges: dict mapping full_name -> badge info
      - stats: summary counts
      - top5_chart: top 5 repos by today_stars with yesterday comparison
    """
    if previous_snapshot is None:
        return None

    today_map = {r["full_name"]: r for r in today_repos}
    prev_map = {r["full_name"]: r for r in previous_snapshot}

    today_names = set(today_map.keys())
    prev_names = set(prev_map.keys())

    new_names = today_names - prev_names
    removed_names = prev_names - today_names
    retained_names = today_names & prev_names

    # Enrich today repos with numeric fields for comparison
    for r in today_repos:
        r.setdefault("stars_numeric", _parse_star_count(r["stars"]))
        r.setdefault("today_stars_numeric", _parse_star_count(r["today_stars"]))

    new_repos = [today_map[n] for n in new_names]
    removed_repos = [prev_map[n] for n in removed_names]
    retained_repos = [today_map[n] for n in retained_names]

    # Identify rising repos: stars_numeric gained >= 1000 OR today_stars grew >= 50%
    rising_repos = []
    for name in retained_names:
        t = today_map[name]
        p = prev_map[name]
        star_gain = t.get("stars_numeric", 0) - p.get("stars_numeric", 0)
        prev_today = p.get("today_stars_numeric", 0)
        curr_today = t.get("today_stars_numeric", 0)
        today_growth_pct = (
            (curr_today - prev_today) / prev_today * 100
            if prev_today > 0 else 0
        )
        if star_gain >= 1000 or today_growth_pct >= 50:
            rising_repos.append({
                **t,
                "star_gain": star_gain,
                "today_growth_pct": round(today_growth_pct),
            })

    # Assign badges to each today repo
    rising_names = {r["full_name"] for r in rising_repos}
    repo_badges = {}
    for name in today_names:
        if name in new_names:
            repo_badges[name] = {"type": "new", "label": "NEW"}
        elif name in rising_names:
            gain = next(r["star_gain"] for r in rising_repos if r["full_name"] == name)
            repo_badges[name] = {
                "type": "rising",
                "label": f"RISING +{gain:,} stars",
            }
        elif name in retained_names:
            p = prev_map[name]
            t = today_map[name]
            gain = t.get("stars_numeric", 0) - p.get("stars_numeric", 0)
            if gain > 0:
                repo_badges[name] = {
                    "type": "retained",
                    "label": f"Day 2 on trending | +{gain:,} stars",
                }
            else:
                repo_badges[name] = {
                    "type": "retained",
                    "label": "Day 2 on trending",
                }

    # Top 5 chart data: today repos sorted by today_stars, with yesterday values
    sorted_today = sorted(
        today_repos,
        key=lambda r: r.get("today_stars_numeric", 0),
        reverse=True,
    )[:5]
    top5_chart = []
    for r in sorted_today:
        name = r["full_name"]
        prev = prev_map.get(name)
        prev_today_stars = prev.get("today_stars_numeric", 0) if prev else 0
        curr_today_stars = r.get("today_stars_numeric", 0)
        delta = curr_today_stars - prev_today_stars
        top5_chart.append({
            "full_name": name,
            "url": r["url"],
            "today_stars": curr_today_stars,
            "yesterday_stars": prev_today_stars,
            "delta": delta,
        })

    return {
        "new_repos": sorted(new_repos, key=lambda r: r.get("today_stars_numeric", 0), reverse=True),
        "removed_repos": removed_repos,
        "retained_repos": retained_repos,
        "rising_repos": sorted(rising_repos, key=lambda r: r.get("star_gain", 0), reverse=True),
        "repo_badges": repo_badges,
        "stats": {
            "new_count": len(new_names),
            "removed_count": len(removed_names),
            "retained_count": len(retained_names),
            "rising_count": len(rising_repos),
        },
        "top5_chart": top5_chart,
    }


def compute_stats(repos, top_directions):
    """Compute aggregate statistics from scraped repos and classified directions."""
    total_repos = len(repos)
    total_stars = sum(_parse_star_count(r["stars"]) for r in repos)
    total_today = sum(_parse_star_count(r["today_stars"]) for r in repos)

    # Language distribution
    lang_counter = {}
    for r in repos:
        lang = r["language"] if r["language"] != "Unknown" else "Other"
        lang_counter[lang] = lang_counter.get(lang, 0) + 1
    top_langs = sorted(lang_counter.items(), key=lambda x: x[1], reverse=True)[:3]

    # Category stats (percentage)
    direction_stats = []
    for cat, cat_repos in top_directions:
        pct = round(len(cat_repos) / total_repos * 100) if total_repos else 0
        direction_stats.append((cat, len(cat_repos), pct))

    # Hottest repo (most today stars)
    hottest = max(repos, key=lambda r: _parse_star_count(r["today_stars"]))

    # AI penetration rate
    ai_categories = {"AI/ML"}
    ai_count = sum(
        len(cr) for cat, cr in top_directions if cat in ai_categories
    )
    ai_pct = round(ai_count / total_repos * 100) if total_repos else 0

    # Top 5 by today stars
    top5_today = sorted(
        repos, key=lambda r: _parse_star_count(r["today_stars"]), reverse=True
    )[:5]

    return {
        "total_repos": total_repos,
        "total_stars": total_stars,
        "total_today": total_today,
        "top_langs": top_langs,
        "direction_stats": direction_stats,
        "hottest": hottest,
        "ai_pct": ai_pct,
        "top5_today": top5_today,
        "num_directions": len(top_directions),
    }


def generate_executive_summary(stats, top_directions, date_str):
    """Generate pyramid-principle Executive Summary with stat cards and charts."""
    hottest = stats["hottest"]
    hottest_today = hottest["today_stars"]
    lines = []

    # --- Opening div (all content must be pure HTML inside div) ---
    top_cat = top_directions[0][0] if top_directions else "开源"
    top_pct = stats["direction_stats"][0][2] if stats["direction_stats"] else 0

    ai_label = (
        "AI 技术持续引领开源创新"
        if top_cat == "AI/ML"
        else "该方向热度居首"
    )
    lang_parts = "、".join(f"{l}({c})" for l, c in stats["top_langs"])

    lines.append('<div class="executive-summary">')
    lines.append(f"  <h2>Executive Summary</h2>")
    lines.append(f"  <h3>结论先行</h3>")
    lines.append(f"  <blockquote>")
    lines.append(
        f"    {date_str}，<strong>{top_cat}</strong> 方向以 <strong>{top_pct}%</strong> "
        f"的占比主导今日 GitHub Trending，"
        f"<strong>{hottest['full_name']}</strong> 以 {hottest_today} 领跑热度榜。"
    )
    lines.append(f"  </blockquote>")
    lines.append(f"  <h3>支撑论点</h3>")
    lines.append(f"  <blockquote>")
    lines.append(f"    <ol>")
    lines.append(
        f"      <li><strong>{top_cat}</strong> 共收录 {stats['direction_stats'][0][1]} 个项目，"
        f"占全部 {stats['total_repos']} 个趋势项目的 {top_pct}%，{ai_label}。</li>"
    )
    lines.append(
        f"      <li>编程语言 Top 3 为 {lang_parts}，反映出当前主流技术栈偏好。</li>"
    )
    lines.append(
        f"      <li>今日共计 <strong>{stats['total_today']:,}</strong> 新增 Stars，"
        f"总 Stars 累计 <strong>{stats['total_stars']:,}</strong>，开源社区活跃度强劲。</li>"
    )
    lines.append(f"    </ol>")
    lines.append(f"  </blockquote>")
    lines.append("</div>")
    lines.append("")

    # 3. 数据概览 stat cards
    lines.append("### 数据概览")
    lines.append("")
    lines.append('<div class="stats-container">')
    cards = [
        (stats["total_repos"], "趋势项目"),
        (f"{stats['total_stars']:,}", "总 Stars"),
        (f"{stats['total_today']:,}", "今日新增 Stars"),
        (stats["num_directions"], "技术方向"),
    ]
    for value, label in cards:
        lines.append(f'  <div class="stat-card">')
        lines.append(f'    <span class="stat-number">{value}</span>')
        lines.append(f'    <span class="stat-label">{label}</span>')
        lines.append(f"  </div>")
    lines.append("</div>")
    lines.append("")

    # 4. Mermaid pie chart — 技术方向分布
    lines.append("### 技术方向分布")
    lines.append("")
    lines.append('<div class="mermaid">')
    lines.append("pie title 技术方向占比")
    for cat, count, pct in stats["direction_stats"]:
        lines.append(f'    "{cat}" : {count}')
    lines.append("</div>")
    lines.append("")

    # 5. Top 5 热度排行 — CSS bar chart
    lines.append("### 热度排行 Top 5")
    lines.append("")
    max_today = max(
        _parse_star_count(r["today_stars"]) for r in stats["top5_today"]
    ) or 1
    lines.append('<div class="timeline-chart">')
    for r in stats["top5_today"]:
        val = _parse_star_count(r["today_stars"])
        height_pct = round(val / max_today * 100)
        short_name = r["full_name"].split("/")[-1][:12]
        lines.append(
            f'  <div class="timeline-bar" style="height:{height_pct}%">'
            f'<span class="timeline-value">{val}</span>'
            f'<span class="timeline-label">{short_name}</span></div>'
        )
    lines.append("</div>")
    lines.append("")

    return "\n".join(lines)


def generate_comparison_section(comparison):
    """Generate the 'Yesterday Comparison' HTML section."""
    if comparison is None:
        return ""

    cs = comparison["stats"]
    lines = []

    # Section heading
    lines.append("## 昨日对比")
    lines.append("")

    # 1. Summary stat cards
    lines.append('<div class="comparison-summary">')
    cards = [
        (cs["new_count"], "新上榜", "stat-card-new"),
        (cs["removed_count"], "已退出", "stat-card-removed"),
        (cs["retained_count"], "连续上榜", "stat-card-retained"),
        (cs["rising_count"], "热度飙升", "stat-card-rising"),
    ]
    for value, label, cls in cards:
        lines.append(f'  <div class="stat-card {cls}">')
        lines.append(f'    <span class="stat-number">{value}</span>')
        lines.append(f'    <span class="stat-label">{label}</span>')
        lines.append(f'  </div>')
    lines.append('</div>')
    lines.append("")

    # 2. New repos list
    if comparison["new_repos"]:
        lines.append("### 新上榜项目")
        lines.append("")
        for r in comparison["new_repos"]:
            today_val = r.get("today_stars_numeric", _parse_star_count(r["today_stars"]))
            lines.append(
                f'<div class="comparison-item comparison-new">'
                f'<span class="comparison-badge badge-new">NEW</span>'
                f'<a href="{r["url"]}">{r["full_name"]}</a>'
                f'<span class="repo-lang">{r["language"]}</span>'
                f'<span class="repo-today">+{today_val:,} stars today</span>'
                f'</div>'
            )
        lines.append("")

    # 3. Removed repos list
    if comparison["removed_repos"]:
        lines.append("### 退出趋势项目")
        lines.append("")
        for r in comparison["removed_repos"]:
            stars_val = r.get("stars_numeric", _parse_star_count(r.get("stars", "")))
            lines.append(
                f'<div class="comparison-item comparison-removed">'
                f'<span class="comparison-badge badge-removed">OFF</span>'
                f'<a href="{r["url"]}">{r["full_name"]}</a>'
                f'<span class="repo-lang">{r.get("language", "Unknown")}</span>'
                f'<span>{stars_val:,} stars</span>'
                f'</div>'
            )
        lines.append("")

    # 4. Top 5 comparison chart
    if comparison["top5_chart"]:
        lines.append("### 热度变化 Top 5")
        lines.append("")
        max_val = max(
            max(c["today_stars"], c["yesterday_stars"])
            for c in comparison["top5_chart"]
        ) or 1
        lines.append('<div class="comparison-chart">')
        for c in comparison["top5_chart"]:
            today_pct = round(c["today_stars"] / max_val * 100)
            yest_pct = round(c["yesterday_stars"] / max_val * 100)
            short_name = c["full_name"].split("/")[-1][:16]
            delta = c["delta"]
            delta_cls = "delta-up" if delta >= 0 else "delta-down"
            delta_sign = "+" if delta >= 0 else ""
            lines.append(f'  <div class="chart-row">')
            lines.append(f'    <span class="chart-label">{short_name}</span>')
            lines.append(f'    <div class="chart-bars">')
            lines.append(
                f'      <div class="bar-today" style="width:{today_pct}%">'
                f'<span>{c["today_stars"]:,}</span></div>'
            )
            lines.append(
                f'      <div class="bar-yesterday" style="width:{yest_pct}%">'
                f'<span>{c["yesterday_stars"]:,}</span></div>'
            )
            lines.append(f'    </div>')
            lines.append(
                f'    <span class="{delta_cls}">{delta_sign}{delta:,}</span>'
            )
            lines.append(f'  </div>')
        lines.append('</div>')
        lines.append("")

    return "\n".join(lines)


def generate_trend_analysis(stats, top_directions):
    """Generate macro trend analysis paragraphs based on today's data."""
    lines = []
    lines.append("## AI 发展趋势洞察")
    lines.append("")
    lines.append('<div class="trend-insight">')

    # Paragraph 1: Dominant direction
    top_cat, top_repos = top_directions[0]
    hottest = stats["hottest"]
    lines.append(
        f"  <p><strong>主导方向与驱动力：</strong> 今日 Trending 以 <strong>{top_cat}</strong> 方向最为突出，"
        f"共 {len(top_repos)} 个项目上榜。"
        f"其中 <a href=\"{hottest['url']}\">{hottest['full_name']}</a> 热度最高"
        f"（{hottest['today_stars']}），"
        f"体现出社区对该领域的持续关注。</p>"
    )

    # Paragraph 2: Language preferences
    lang_parts = "、".join(
        f"<strong>{l}</strong>({c} 项目)" for l, c in stats["top_langs"]
    )
    lang_extra = ""
    if stats["top_langs"] and stats["top_langs"][0][0] == "Python":
        lang_extra = (
            "Python 继续巩固其在 AI/数据领域的统治地位，"
            "同时 Rust/Go 等系统级语言在基础设施方向保持增长。"
        )
    lines.append(
        f"  <p><strong>编程语言偏好：</strong> 今日热门项目中，{lang_parts} 位列前三。"
        f"{lang_extra}</p>"
    )

    # Paragraph 3: Emerging projects
    top5 = stats["top5_today"]
    if len(top5) >= 3:
        names = "、".join(
            f"<a href=\"{r['url']}\">{r['full_name'].split('/')[-1]}</a>"
            for r in top5[:3]
        )
        lines.append(
            f"  <p><strong>值得关注的项目：</strong> {names} 等项目今日增长迅猛，"
            f"建议开发者持续跟踪其发展动态。</p>"
        )

    # Paragraph 4: Cross-domain fusion
    if len(top_directions) >= 2:
        cats = "、".join(d[0] for d in top_directions[:3])
        lines.append(
            f"  <p><strong>跨领域融合：</strong> 当前 Trending 涵盖 {cats} 等方向，"
            f"反映出技术生态日益交叉融合的趋势。"
            f"AI 能力正加速渗透到 DevOps、安全、数据库等各基础设施层面。</p>"
        )

    lines.append("</div>")
    lines.append("")
    return "\n".join(lines)


def generate_direction_summary(category, repos):
    """Generate a brief blockquote summary for a category section."""
    # Deduplicate
    seen = set()
    unique = []
    for r in repos:
        if r["full_name"] not in seen:
            seen.add(r["full_name"])
            unique.append(r)

    lang_counter = {}
    for r in unique:
        lang = r["language"] if r["language"] != "Unknown" else "Other"
        lang_counter[lang] = lang_counter.get(lang, 0) + 1
    top_lang = sorted(lang_counter.items(), key=lambda x: x[1], reverse=True)
    lang_str = "、".join(l for l, _ in top_lang[:3])

    total_today = sum(_parse_star_count(r["today_stars"]) for r in unique)

    return (
        f'<div class="direction-summary">'
        f"该方向共 <strong>{len(unique)}</strong> 个项目上榜，"
        f"主要使用 <strong>{lang_str}</strong>，"
        f"今日合计新增 <strong>{total_today:,}</strong> Stars。"
        f"</div>"
    )


def generate_markdown(repos, top_directions, date_str, comparison=None):
    """Generate an enriched Jekyll blog post with pyramid-principle structure."""
    direction_names = [d[0] for d in top_directions]
    tags_str = ", ".join(["GitHub Trending", "开源"] + direction_names)

    stats = compute_stats(repos, top_directions)

    # Get badge map from comparison data
    repo_badges = comparison["repo_badges"] if comparison else {}

    lines = [
        "---",
        "layout: post",
        f"title: GitHub Trending 技术趋势 ({date_str})",
        f"excerpt: 每日GitHub热门项目精选，覆盖{'、'.join(direction_names)}等方向",
        "category: AI",
        f"tags: [{tags_str}]",
        "---",
        "",
    ]

    # Executive Summary (pyramid principle + stat cards + charts)
    lines.append(generate_executive_summary(stats, top_directions, date_str))

    # Comparison section (between Executive Summary and Trend Analysis)
    comparison_html = generate_comparison_section(comparison)
    if comparison_html:
        lines.append(comparison_html)

    # AI Trend Analysis
    lines.append(generate_trend_analysis(stats, top_directions))

    # Per-direction sections with repo cards
    for category, cat_repos in top_directions:
        lines.append(f"## {category}")
        lines.append("")
        lines.append(generate_direction_summary(category, cat_repos))
        lines.append("")

        # Deduplicate repos within this category
        seen = set()
        for repo in cat_repos:
            if repo["full_name"] in seen:
                continue
            seen.add(repo["full_name"])

            # Repo card HTML
            lines.append('<div class="trending-repo-card">')

            # Inject comparison badge if available
            badge = repo_badges.get(repo["full_name"])
            if badge:
                badge_cls = f'badge-{badge["type"]}'
                lines.append(
                    f'  <span class="repo-badge {badge_cls}">{badge["label"]}</span>'
                )

            lines.append(
                f'  <h4><a href="{repo["url"]}">{repo["full_name"]}</a></h4>'
            )
            lines.append(
                f'  <p class="repo-desc">{repo["description"]}</p>'
            )
            lines.append('  <div class="repo-meta">')
            lines.append(
                f'    <span class="repo-lang">{repo["language"]}</span>'
            )
            if repo["stars"]:
                lines.append(f"    <span>Stars: {repo['stars']}</span>")
            if repo["forks"]:
                lines.append(f"    <span>Forks: {repo['forks']}</span>")
            if repo["today_stars"]:
                lines.append(
                    f'    <span class="repo-today">{repo["today_stars"]}</span>'
                )
            lines.append("  </div>")
            lines.append("</div>")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    today = datetime.now(BEIJING_TZ)
    date_str = today.strftime("%Y-%m-%d")

    # Determine output path (relative to repo root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    posts_dir = os.path.join(repo_root, "_posts")
    output_file = os.path.join(posts_dir, f"{date_str}-ai-github-trending.md")

    # Skip if already generated today
    if os.path.exists(output_file):
        print(f"Post already exists: {output_file}")
        sys.exit(0)

    print("Fetching GitHub Trending page...")
    soup = fetch_trending_page()

    print("Parsing repositories...")
    repos = parse_repos(soup)
    print(f"Found {len(repos)} trending repositories")

    print("Classifying and selecting top directions...")
    top_directions = select_top_directions(repos, top_n=5)

    # Load yesterday's snapshot and compute comparison
    print("Loading previous snapshot for comparison...")
    previous_snapshot = load_previous_snapshot(date_str, repo_root)
    comparison = None
    if previous_snapshot:
        print(f"Found yesterday's snapshot ({len(previous_snapshot)} repos), computing comparison...")
        comparison = compute_comparison(repos, previous_snapshot)
    else:
        print("No previous snapshot found, skipping comparison.")

    # Save today's snapshot (always, even if post already existed — overwrite is fine)
    save_daily_snapshot(repos, date_str, repo_root)

    print("Generating blog post...")
    markdown = generate_markdown(repos, top_directions, date_str, comparison)

    os.makedirs(posts_dir, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Generated: {output_file}")


if __name__ == "__main__":
    main()
