---
layout: post
title: Alfred Workflow 开发实战指南
excerpt: 通过Python开发Alfred自定义工作流，实现API查询、项目快速打开等效率提升场景
category: Tools
tags: [Alfred, Workflow, Python, 效率工具]
---

## Executive Summary

### 核心观点（金字塔原理）

> **结论先行**: Alfred Workflow是macOS上极具价值的效率提升工具，通过Python脚本可快速开发自定义工作流，将日常重复操作从多步骤简化为一次键盘触发。
>
> **支撑论点**:
> 1. **低门槛开发**：支持Bash/Python等多种脚本语言，alfred-workflow库提供完整的开发框架
> 2. **高度可定制**：可对接任意HTTP API、读取本地文件、调用系统命令
> 3. **即时反馈**：内置缓存机制和调试日志，开发调试效率高

### SWOT 分析

| 维度 | 分析 |
|------|------|
| **S** 优势 | 键盘驱动零鼠标操作、支持多种脚本语言、丰富的社区Workflow资源 |
| **W** 劣势 | 付费软件（Powerpack）、仅限macOS平台、Python 2.7兼容性问题 |
| **O** 机会 | 可集成内部API/工具链、统一团队工作流、替代重复性GUI操作 |
| **T** 威胁 | macOS系统更新可能影响兼容性、Python 2.7已停止维护 |

### 适用场景

- **API快速查询**：配置中心、文档系统、内部工具的快速检索与跳转
- **项目快速打开**：一键搜索并用IDE打开指定目录下的项目
- **日常效率提升**：翻译、计算、格式转换等高频操作

---

## Alfred 简介

Alfred是macOS平台上的效率启动器工具，核心特点：
- 收费软件（Powerpack授权解锁Workflow功能）
- 支持自定义Workflow提高工作效率
- Workflow支持多种脚本语言：`/bin/bash`、`/usr/bin/python`等

---

## Workflow 开发流程

### 步骤一：创建脚本过滤器

1. 打开Alfred Preferences → Workflows
2. 点击 `+` 创建新Workflow
3. 添加 Script Filter：
   - Language：`/bin/bash` 或 `/usr/bin/python`
   - `with input as {query}`

### 步骤二：配置Python环境

在Script中填写：
```bash
/usr/bin/python your_script.py "{query}"
```

### 步骤三：项目目录结构

选中Workflow右键 → 在Finder中打开，目录结构如下：

```
Your Workflow/
├── info.plist          # Workflow配置文件
├── icon.png            # Workflow图标
├── workflow/           # alfred-workflow库
│   ├── __init__.py
│   ├── background.py
│   ├── notify.py
│   ├── web.py
│   ├── workflow.py
│   └── workflow3.py
└── yourscript.py       # 自定义脚本
```

### 步骤四：安装依赖

在Workflow目录中执行：
```bash
pip install --target=. Alfred-Workflow
pip install --target=. requests browsercookie
```

### 步骤五：开发脚本

### 步骤六：配置Action

右键空白处 → Actions → Open URL，配置 `{query}` 作为跳转链接

---

## 实战案例一：API查询工作流

通过HTTP接口查询配置信息，解析为Alfred下拉选项：

```python
#!/usr/bin/env python
# coding:utf-8

import requests
import json
import browsercookie
import sys
from workflow import Workflow

url = 'https://xxx.xxx.com/api/xxx?_search='
cookies = browsercookie.chrome()
icon = '/item.ico'

def send_request(query):
    """发送HTTP请求获取数据"""
    params = {"key": query}
    r = requests.get(url=url, cookies=cookies, params=params)
    return json.loads(r.text)

def main(wf):
    """主函数：获取输入、查询接口、返回结果"""
    query = wf.args[0] if len(wf.args) else None

    # 使用缓存加速，60秒过期
    result = wf.cached_data(query, lambda: send_request(query), max_age=60)
    wf.logger.info(result)

    for item in result['data']:
        name = item['key']
        path = str(name).replace(".", "/")
        linkUrl = 'https://xxx.xxx.com/' + path
        wf.add_item(title=name, icon=icon, arg=linkUrl, valid=True)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
```

**核心API说明**：

| 方法 | 说明 |
|------|------|
| `wf.args` | 获取用户输入参数 |
| `wf.cached_data()` | 缓存数据，避免重复请求 |
| `wf.add_item()` | 添加下拉选项 |
| `wf.send_feedback()` | 返回结果给Alfred |
| `wf.logger.info()` | 输出调试日志 |

---

## 实战案例二：IDEA项目快速打开

快速搜索指定目录下的项目并用IDE打开：

### 配置步骤

1. 创建Script Filter，Language：`/usr/bin/python`
2. 配置环境变量：点击右上角 `{X}` → Environment Variables
   - `idea_workspace_path` = `/User/xxx/project`（支持逗号分隔多目录）
3. 添加Action：Launch Apps/Files，选择IDEA

### 脚本代码

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import re

def search(paths, name):
    """查询指定目录下所有匹配的文件夹"""
    data = []
    for path in paths:
        files = os.listdir(path)
        for file_name in files:
            # 忽略大小写匹配，排除文件（含.的项）
            if re.search(name, file_name, re.I) and file_name.find(".") == -1:
                file_path = path + "/" + file_name
                data.append({
                    "uid": file_name,
                    "title": file_name,
                    "subtitle": file_path,
                    "arg": file_path
                })
    print json.dumps({"items": data})

# 读取配置的工作空间路径
path = os.getenv("idea_workspace_path")
if not path:
    print json.dumps({"items": [{"title": "未设置idea工作空间:idea_workspace_path"}]})
else:
    search(path.split(","), '{query}')
```

---

## 常见问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Python版本不兼容 | Alfred Workflow依赖Python 2.7 | 使用系统自带Python或安装pyenv管理版本 |
| 依赖包找不到 | 未安装到Workflow目录 | 使用 `pip install --target=.` 安装 |
| Cookie获取失败 | browsercookie首次需要授权 | 输入系统密码，点击"始终允许" |
| 调试脚本 | 需要查看运行日志 | 打开Alfred Debug Console查看 |

---

## 参考资料

- Alfred官网：https://www.alfredapp.com/
- alfred-workflow文档：https://github.com/deanishe/alfred-workflow
- Workflow资源库：https://www.alfredworkflows.store/
- Google翻译Workflow：https://github.com/xfslove/alfred-google-translate
- Workflow配置指南：https://www.alfredapp.com/help/workflows/workflow-configuration/
