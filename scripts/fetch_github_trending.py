#!/usr/bin/env python3
"""
Fetch GitHub Trending repositories and generate a Jekyll blog post.

Scrapes github.com/trending, classifies repos into tech categories,
picks top 5 directions, and outputs a Markdown post to _posts/.
"""

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


def generate_markdown(top_directions, date_str):
    """Generate a Jekyll-compatible Markdown blog post."""
    direction_names = [d[0] for d in top_directions]
    tags_str = ", ".join(["GitHub Trending", "开源"] + direction_names)

    lines = [
        "---",
        "layout: post",
        f"title: GitHub Trending 技术趋势 ({date_str})",
        f"excerpt: 每日GitHub热门项目精选，覆盖{'、'.join(direction_names)}等方向",
        "category: AI",
        f"tags: [{tags_str}]",
        "---",
        "",
        "## Executive Summary",
        "",
        "### 核心观点",
        f"> 今日 GitHub Trending 热门项目覆盖以下 {len(direction_names)} 大技术方向：",
        ">",
    ]
    for i, name in enumerate(direction_names, 1):
        count = len(top_directions[i - 1][1])
        lines.append(f"> {i}. **{name}** ({count} 个项目)")
    lines.append("")

    for category, repos in top_directions:
        lines.append(f"## {category}")
        lines.append("")
        # Deduplicate repos within this category
        seen = set()
        for repo in repos:
            if repo["full_name"] in seen:
                continue
            seen.add(repo["full_name"])
            lines.append(f"### [{repo['full_name']}]({repo['url']})")
            lines.append(f"> {repo['description']}")
            lines.append("")
            meta_parts = [f"**语言**: {repo['language']}"]
            if repo["stars"]:
                meta_parts.append(f"**Stars**: {repo['stars']}")
            if repo["forks"]:
                meta_parts.append(f"**Forks**: {repo['forks']}")
            if repo["today_stars"]:
                meta_parts.append(f"**今日**: {repo['today_stars']}")
            lines.append(" | ".join(meta_parts))
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

    print("Generating blog post...")
    markdown = generate_markdown(top_directions, date_str)

    os.makedirs(posts_dir, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Generated: {output_file}")


if __name__ == "__main__":
    main()
