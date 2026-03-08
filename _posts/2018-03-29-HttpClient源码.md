---
layout: post
title: HttpClient源码研究
excerpt: HttpClient源码研究-> 如何使用(同步/异步) -> 如何做到复用连接的?
category: Java
---

## Executive Summary

### 核心观点（金字塔原理）
> **结论先行**: HttpClient是Apache提供的HTTP客户端库，通过连接池复用机制和同步/异步两种调用模式，实现高效的HTTP通信。
>
> **支撑论点**:
> 1. 同步调用模式：阻塞式HTTP请求，适用于简单场景
> 2. 异步调用模式：非阻塞式HTTP请求，适用于高并发场景
> 3. 连接复用机制：通过连接池管理HTTP连接，减少连接建立开销

### SWOT 分析
| 维度 | 分析 |
|------|------|
| **S** 优势 | 成熟稳定的HTTP客户端库；支持连接池复用；同步异步双模式支持 |
| **W** 劣势 | API相对繁琐；配置项较多；学习成本中等 |
| **O** 机会 | 微服务间HTTP通信；第三方API调用；爬虫和数据采集 |
| **T** 威胁 | OkHttp等现代HTTP库竞争；JDK 11+原生HttpClient；WebClient等响应式客户端 |

### 适用场景
- 需要精细控制HTTP请求的Java应用
- 高并发HTTP请求需要连接池管理的场景
- 企业级应用的HTTP通信基础设施

---

#### HttpClient源码研究
##### TODO 同步
##### TODO 异步
##### 如何做到复用连接的?

