#!/usr/bin/env python3
"""
Generate daily AI technology blog posts using DeepSeek API.
Reads topic schedule from topic_schedule.yaml, generates Jekyll blog posts.
"""
import os
import re
import sys
import time
import yaml
from datetime import datetime, timezone, timedelta
from openai import OpenAI

BEIJING_TZ = timezone(timedelta(hours=8))
POSTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_posts")
SCHEDULE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "topic_schedule.yaml")


REQUIRED_TOPIC_KEYS = {"id", "title", "slug", "phase", "tags", "key_areas"}


def load_schedule():
    """Load and return the topics list from topic_schedule.yaml."""
    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    topics = data["topics"]
    for i, topic in enumerate(topics):
        missing = REQUIRED_TOPIC_KEYS - set(topic.keys())
        if missing:
            raise ValueError(f"Topic #{i+1} missing required keys: {missing}")
    return topics


def find_existing_slugs():
    """Scan _posts/ for ai-daily articles and return a set of their slugs."""
    slugs = set()
    if not os.path.isdir(POSTS_DIR):
        return slugs
    for filename in os.listdir(POSTS_DIR):
        match = re.search(r"-ai-daily-(.+)\.md$", filename)
        if match:
            slugs.add(match.group(1))
    return slugs


def build_prompts(topic):
    """Build system_prompt and user_prompt from the given topic."""
    system_prompt = """你是一位拥有 10 年经验的 AI 架构师和技术博主。你的读者是有 5-7 年经验的 Java/后端工程师，正在系统学习 AI 技术栈。

写作要求：
1. 文章结构：AI Summary HTML 区块 → 引言 → 核心概念 → 实战代码 → 对比表格 → 最佳实践 → 总结 → 参考资料
2. 字数：3000-4000 中文字符
3. 从 ## 开始，不要输出 YAML front matter
4. 代码示例使用 Python，确保可运行
5. 包含至少一个 Markdown 对比表格
6. 技术深度：不停留在概念层面，要有架构图描述和生产级考量

AI Summary 区块必须作为文章开头第一个内容，使用以下固定 HTML 模板（替换其中内容）：

<div style="background: linear-gradient(135deg, #e8f4f8 0%, #f0e6ff 100%); border-left: 4px solid #7c3aed; border-radius: 8px; padding: 20px 24px; margin: 20px 0;">
<div style="display: flex; align-items: center; margin-bottom: 12px;">
<span style="background: #7c3aed; color: white; font-size: 12px; font-weight: bold; padding: 2px 8px; border-radius: 4px; margin-right: 8px;">AI Summary</span>
<span style="font-size: 18px; font-weight: bold;">核心观点总结</span>
</div>

<p style="margin: 8px 0;"><strong>结论先行：</strong>（一句话总结文章核心观点）</p>

<p style="margin: 8px 0;"><strong>关键要点1：</strong>（要点描述）</p>

<p style="margin: 8px 0;"><strong>关键要点2：</strong>（要点描述）</p>

<p style="margin: 8px 0;"><strong>关键要点3：</strong>（要点描述）</p>

<p style="margin: 8px 0; color: #666; font-size: 13px;">本摘要由 AI 自动生成，基于文章核心内容提炼</p>
</div>"""

    key_areas_list = "\n".join(
        f"{i+1}. {area}" for i, area in enumerate(topic["key_areas"])
    )

    user_prompt = f"""请撰写一篇关于「{topic['title']}」的深度技术博文。

本文属于「{topic['phase']}」阶段的学习内容。

需要覆盖的关键领域：
{key_areas_list}

请严格按照系统提示中的写作要求和文章结构进行撰写。"""

    return system_prompt, user_prompt


def call_deepseek_api(system_prompt, user_prompt):
    """Call DeepSeek API with retry logic. Return the generated content string."""
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=8192,
                temperature=0.7,
                top_p=0.9,
            )
            return response.choices[0].message.content
        except Exception as e:
            wait_time = (2 ** attempt) * 5
            print(f"API call failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise


def post_process(content):
    """Clean up LLM-generated content for Jekyll compatibility."""
    # Remove any YAML front matter (between --- markers) if the LLM accidentally generates it
    content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, count=1, flags=re.DOTALL)

    # Fix H1 headings (# ) to H2 (## ) outside of fenced code blocks
    parts = re.split(r"(```.*?```)", content, flags=re.DOTALL)
    for i in range(0, len(parts), 2):  # Only process non-code-block parts
        parts[i] = re.sub(r"^# (?!#)", "## ", parts[i], flags=re.MULTILINE)
    content = "".join(parts)

    # Ensure all <div> tags have matching </div> closures
    open_divs = len(re.findall(r"<div[\s>]", content, re.IGNORECASE))
    close_divs = len(re.findall(r"</div>", content, re.IGNORECASE))
    if open_divs > close_divs:
        content += "\n</div>" * (open_divs - close_divs)

    # Strip leading/trailing whitespace
    content = content.strip()

    return content


def build_front_matter(topic, date_str):
    """Return YAML front matter string for the blog post."""
    tags_str = "[" + ", ".join(topic["tags"]) + "]"
    front_matter = f"""---
layout: post
title: "{topic['title']}"
date: {date_str}
excerpt: "AI 每日技术博文：{topic['title']} — 系统学习 AI 技术栈"
category: AI
tags: {tags_str}
---"""
    return front_matter


def validate_article(content):
    """Validate the generated article content.
    Return (bool, list_of_errors)."""
    errors = []

    if len(content) < 2000:
        errors.append(f"Content too short: {len(content)} characters (minimum 2000)")

    if "AI Summary" not in content:
        errors.append("Missing AI Summary section")

    if "```" not in content:
        errors.append("Missing code block (no ``` found)")

    if "## " not in content:
        errors.append("Missing ## heading")

    valid = len(errors) == 0
    return valid, errors


def main():
    today = datetime.now(BEIJING_TZ).strftime("%Y-%m-%d")
    topics = load_schedule()
    existing_slugs = find_existing_slugs()

    # Find the first topic whose slug has not been generated yet
    topic = None
    for t in topics:
        if t["slug"] not in existing_slugs:
            topic = t
            break

    if topic is None:
        print(f"All {len(topics)} topics completed!")
        sys.exit(0)

    filename = f"{today}-ai-daily-{topic['slug']}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    if os.path.exists(filepath):
        print(f"Already exists: {filename}")
        sys.exit(0)

    print(f"Generating topic {topic['id']}/{len(topics)}: {topic['title']}")

    system_prompt, user_prompt = build_prompts(topic)
    content = call_deepseek_api(system_prompt, user_prompt)
    content = post_process(content)

    valid, errors = validate_article(content)
    if not valid:
        print(f"WARNING: Validation issues: {errors}")
        # Continue anyway - partial content is better than no content

    front_matter = build_front_matter(topic, today)
    full_content = front_matter + "\n" + content + "\n"

    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"Generated: {filename}")
    print(f"  Phase: {topic['phase']}")
    print(f"  Length: {len(content)} characters")


if __name__ == "__main__":
    main()
