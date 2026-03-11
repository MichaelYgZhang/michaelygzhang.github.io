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

    # Sort by today_stars descending to assign rank
    sorted_repos = sorted(
        repos,
        key=lambda r: _parse_star_count(r["today_stars"]),
        reverse=True,
    )
    rank_map = {r["full_name"]: i + 1 for i, r in enumerate(sorted_repos)}

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
            "forks_numeric": _parse_star_count(r["forks"]),
            "rank": rank_map[r["full_name"]],
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


def load_recent_snapshots(date_str, repo_root, days=7):
    """Load recent N days of snapshots (excluding today).

    Returns {date_str: [repos]} dict for each day that has a snapshot file.
    """
    today = datetime.strptime(date_str, "%Y-%m-%d")
    snapshots = {}
    for i in range(1, days + 1):
        d = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        filepath = os.path.join(repo_root, "_data", "trending", f"{d}.json")
        if not os.path.exists(filepath):
            continue
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                snapshots[d] = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
    return snapshots


def compute_comparison(today_repos, previous_snapshot, recent_snapshots=None, date_str=None):
    """Compare today's repos with yesterday's snapshot.

    Returns a dict with:
      - new_repos: list of repos new to trending today
      - removed_repos: list of repos that left trending
      - retained_repos: list of repos on both days
      - rising_repos: list of retained repos with strong star growth
      - repo_badges: dict mapping full_name -> badge info
      - stats: summary counts
      - top5_chart: top 5 repos by today_stars with yesterday comparison
      - aggregate_metrics: growth total, growth rate, avg heat, retention/turnover
      - repo_deltas: per-repo star/fork/heat/rank changes
      - consecutive_days: per-repo consecutive days on trending
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

    # Compute consecutive days on trending using recent_snapshots
    consecutive_days = {}
    if recent_snapshots and date_str:
        today_dt = datetime.strptime(date_str, "%Y-%m-%d")
        for name in today_names:
            streak = 1  # today counts as day 1
            for i in range(1, 8):
                d = (today_dt - timedelta(days=i)).strftime("%Y-%m-%d")
                if d not in recent_snapshots:
                    break
                snap_names = {r["full_name"] for r in recent_snapshots[d]}
                if name in snap_names:
                    streak += 1
                else:
                    break
            consecutive_days[name] = streak
    else:
        for name in today_names:
            consecutive_days[name] = 2 if name in retained_names else 1

    # Compute rank for today's repos (by today_stars descending)
    sorted_today_by_heat = sorted(
        today_repos,
        key=lambda r: r.get("today_stars_numeric", 0),
        reverse=True,
    )
    today_rank_map = {r["full_name"]: i + 1 for i, r in enumerate(sorted_today_by_heat)}

    # Build previous rank map (use stored rank or compute from today_stars)
    prev_rank_map = {}
    if previous_snapshot:
        # Check if rank field exists in snapshot
        has_rank = any(r.get("rank") is not None for r in previous_snapshot)
        if has_rank:
            for r in previous_snapshot:
                prev_rank_map[r["full_name"]] = r.get("rank", 0)
        else:
            sorted_prev = sorted(
                previous_snapshot,
                key=lambda r: r.get("today_stars_numeric", 0),
                reverse=True,
            )
            prev_rank_map = {r["full_name"]: i + 1 for i, r in enumerate(sorted_prev)}

    # Compute repo_deltas for retained repos
    repo_deltas = {}
    for name in retained_names:
        t = today_map[name]
        p = prev_map[name]
        t_stars = t.get("stars_numeric", 0)
        p_stars = p.get("stars_numeric", 0)
        t_forks = _parse_star_count(t.get("forks", ""))
        p_forks = p.get("forks_numeric", _parse_star_count(p.get("forks", "")))
        t_heat = t.get("today_stars_numeric", 0)
        p_heat = p.get("today_stars_numeric", 0)
        t_rank = today_rank_map.get(name, 0)
        p_rank = prev_rank_map.get(name, 0)

        repo_deltas[name] = {
            "star_change": t_stars - p_stars,
            "fork_change": t_forks - p_forks,
            "heat_change": t_heat - p_heat,
            "rank_change": p_rank - t_rank,  # positive = moved up
            "today_rank": t_rank,
            "prev_rank": p_rank,
        }

    # Compute aggregate metrics
    today_total_heat = sum(r.get("today_stars_numeric", 0) for r in today_repos)
    prev_total_heat = sum(r.get("today_stars_numeric", 0) for r in previous_snapshot)
    total_star_growth = sum(
        today_map[n].get("stars_numeric", 0) - prev_map[n].get("stars_numeric", 0)
        for n in retained_names
    )
    avg_heat = round(today_total_heat / len(today_repos)) if today_repos else 0
    retention_rate = round(len(retained_names) / len(prev_names) * 100) if prev_names else 0
    turnover_rate = 100 - retention_rate
    heat_growth_rate = (
        round((today_total_heat - prev_total_heat) / prev_total_heat * 100)
        if prev_total_heat > 0 else 0
    )

    aggregate_metrics = {
        "total_star_growth": total_star_growth,
        "heat_growth_rate": heat_growth_rate,
        "avg_heat": avg_heat,
        "retention_rate": retention_rate,
        "turnover_rate": turnover_rate,
        "today_total_heat": today_total_heat,
        "prev_total_heat": prev_total_heat,
    }

    # Assign badges to each today repo
    rising_names = {r["full_name"] for r in rising_repos}
    repo_badges = {}
    for name in today_names:
        days = consecutive_days.get(name, 1)
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
            day_label = f"Day {days} on trending" if days >= 2 else "Day 2 on trending"
            if gain > 0:
                repo_badges[name] = {
                    "type": "retained",
                    "label": f"{day_label} | +{gain:,} stars",
                }
            else:
                repo_badges[name] = {
                    "type": "retained",
                    "label": day_label,
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
        "aggregate_metrics": aggregate_metrics,
        "repo_deltas": repo_deltas,
        "consecutive_days": consecutive_days,
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
    agg = comparison.get("aggregate_metrics", {})
    repo_deltas = comparison.get("repo_deltas", {})
    consecutive_days = comparison.get("consecutive_days", {})
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

    # 1b. Aggregate metrics dashboard
    if agg:
        growth_total = agg.get("total_star_growth", 0)
        growth_sign = "+" if growth_total >= 0 else ""
        growth_rate = agg.get("heat_growth_rate", 0)
        rate_sign = "+" if growth_rate >= 0 else ""
        rate_arrow = "▲" if growth_rate >= 0 else "▼"
        avg_heat = agg.get("avg_heat", 0)
        retention = agg.get("retention_rate", 0)

        lines.append('<div class="metrics-dashboard">')
        metric_cards = [
            (f"{growth_sign}{growth_total:,}", "今日增长总量",
             "▲" if growth_total >= 0 else "▼"),
            (f"{avg_heat:,}", "平均热度", ""),
            (f"{retention}%", "留存率", ""),
            (f"{rate_sign}{growth_rate}%", "增长率", rate_arrow),
        ]
        for value, label, arrow in metric_cards:
            arrow_html = f' <span class="metric-arrow">{arrow}</span>' if arrow else ""
            lines.append(f'  <div class="metric-card">')
            lines.append(f'    <span class="metric-value">{value}{arrow_html}</span>')
            lines.append(f'    <span class="metric-label">{label}</span>')
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

    # 4. Consecutive streak repos
    streak_repos = [
        (name, consecutive_days.get(name, 1))
        for name in consecutive_days
        if consecutive_days.get(name, 1) >= 2
    ]
    if streak_repos:
        # Sort by streak descending, then by rank
        streak_repos.sort(key=lambda x: (-x[1], repo_deltas.get(x[0], {}).get("today_rank", 99)))
        lines.append("### 连续上榜项目")
        lines.append("")
        today_map = {r["full_name"]: r for r in comparison.get("retained_repos", [])}
        for name, days in streak_repos:
            delta = repo_deltas.get(name, {})
            rank_change = delta.get("rank_change", 0)
            star_change = delta.get("star_change", 0)
            heat_change = delta.get("heat_change", 0)
            today_rank = delta.get("today_rank", 0)

            # Rank indicator
            if rank_change > 0:
                rank_html = f'<span class="rank-change rank-up">▲{rank_change}</span>'
            elif rank_change < 0:
                rank_html = f'<span class="rank-change rank-down">▼{abs(rank_change)}</span>'
            else:
                rank_html = '<span class="rank-change rank-same">→</span>'

            # Star change
            star_sign = "+" if star_change >= 0 else ""
            star_cls = "delta-up" if star_change >= 0 else "delta-down"

            # Heat acceleration
            if heat_change > 0:
                heat_html = f'<span class="delta-up">热度 +{heat_change:,}</span>'
            elif heat_change < 0:
                heat_html = f'<span class="delta-down">热度 {heat_change:,}</span>'
            else:
                heat_html = '<span>热度持平</span>'

            repo = today_map.get(name)
            url = repo["url"] if repo else f"https://github.com/{name}"

            lines.append(f'<div class="comparison-item streak-item">')
            lines.append(f'  {rank_html}')
            lines.append(f'  <span class="streak-rank">#{today_rank}</span>')
            lines.append(f'  <a href="{url}">{name}</a>')
            lines.append(f'  <span class="{star_cls}">Stars {star_sign}{star_change:,}</span>')
            lines.append(f'  {heat_html}')
            lines.append(f'  <span class="badge-streak">Day {days}</span>')
            lines.append(f'</div>')
        lines.append("")

    # 5. Top 5 comparison chart
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

    # 6. Growth detail table (collapsible)
    if repo_deltas:
        lines.append("### 增长明细")
        lines.append("")
        lines.append("<details>")
        lines.append("<summary>点击展开增长明细表</summary>")
        lines.append("")
        lines.append('<div class="growth-table-wrapper">')
        lines.append('<table class="growth-table">')
        lines.append("  <thead><tr>")
        lines.append("    <th>项目</th><th>排名</th><th>Star 变化</th>")
        lines.append("    <th>Fork 变化</th><th>热度变化</th><th>连续天数</th>")
        lines.append("  </tr></thead>")
        lines.append("  <tbody>")

        # Sort by today_rank
        sorted_deltas = sorted(
            repo_deltas.items(),
            key=lambda x: x[1].get("today_rank", 99),
        )
        for name, delta in sorted_deltas:
            days = consecutive_days.get(name, 1)
            rank_change = delta.get("rank_change", 0)
            if rank_change > 0:
                rank_indicator = f'▲{rank_change}'
            elif rank_change < 0:
                rank_indicator = f'▼{abs(rank_change)}'
            else:
                rank_indicator = '→'
            star_sign = "+" if delta["star_change"] >= 0 else ""
            fork_sign = "+" if delta["fork_change"] >= 0 else ""
            heat_sign = "+" if delta["heat_change"] >= 0 else ""
            short_name = name.split("/")[-1][:20]
            lines.append(f"  <tr>")
            lines.append(f"    <td>{short_name}</td>")
            lines.append(f"    <td>#{delta['today_rank']} {rank_indicator}</td>")
            lines.append(f"    <td>{star_sign}{delta['star_change']:,}</td>")
            lines.append(f"    <td>{fork_sign}{delta['fork_change']:,}</td>")
            lines.append(f"    <td>{heat_sign}{delta['heat_change']:,}</td>")
            lines.append(f"    <td>Day {days}</td>")
            lines.append(f"  </tr>")
        lines.append("  </tbody>")
        lines.append("</table>")
        lines.append("</div>")
        lines.append("")
        lines.append("</details>")
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

    # Get badge map and delta data from comparison
    repo_badges = comparison["repo_badges"] if comparison else {}
    repo_deltas = comparison.get("repo_deltas", {}) if comparison else {}
    consecutive_days = comparison.get("consecutive_days", {}) if comparison else {}

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

            # Delta tags for repos with comparison data
            name = repo["full_name"]
            delta = repo_deltas.get(name)
            days = consecutive_days.get(name, 0)
            if delta or days >= 2:
                lines.append('  <div class="repo-deltas">')
                if delta:
                    sc = delta.get("star_change", 0)
                    if sc != 0:
                        sc_sign = "+" if sc >= 0 else ""
                        sc_cls = "delta-up" if sc >= 0 else "delta-down"
                        lines.append(
                            f'    <span class="delta-tag {sc_cls}">Stars {sc_sign}{sc:,}</span>'
                        )
                    rc = delta.get("rank_change", 0)
                    if rc != 0:
                        if rc > 0:
                            lines.append(
                                f'    <span class="delta-tag rank-up">Rank ▲{rc}</span>'
                            )
                        else:
                            lines.append(
                                f'    <span class="delta-tag rank-down">Rank ▼{abs(rc)}</span>'
                            )
                if days >= 2:
                    lines.append(
                        f'    <span class="streak-tag">Trending {days} days</span>'
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

    # Load yesterday's snapshot and recent snapshots for comparison
    print("Loading previous snapshot for comparison...")
    previous_snapshot = load_previous_snapshot(date_str, repo_root)
    comparison = None
    if previous_snapshot:
        print(f"Found yesterday's snapshot ({len(previous_snapshot)} repos), computing comparison...")
        recent_snapshots = load_recent_snapshots(date_str, repo_root, days=7)
        print(f"Loaded {len(recent_snapshots)} recent snapshots for streak calculation")
        comparison = compute_comparison(
            repos, previous_snapshot,
            recent_snapshots=recent_snapshots,
            date_str=date_str,
        )
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
