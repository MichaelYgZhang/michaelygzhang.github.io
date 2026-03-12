---
layout: post
title: Go并发原理
excerpt: Go并发
category: Go
---

## Executive Summary

### 核心观点（金字塔原理）
> **结论先行**: Go的并发核心是Goroutine协程机制，基于CSP理论实现"通过通信来共享内存"的设计哲学，而非传统的共享内存通信方式。
>
> **支撑论点**:
> 1. Goroutine是轻量级协程：比线程更省资源，任何函数加go关键字即可异步执行
> 2. 非抢占式调度：协程主动交出控制权，在I/O、channel、锁等待等点自动切换
> 3. Channel通信机制：通过channel安全传递数据，发送方负责close操作

### SWOT 分析

| 维度 | 分析 |
|------|------|
| **S** 优势 | 协程轻量级资源消耗低、Channel提供安全通信、-race可检测数据竞争 |
| **W** 劣势 | 非抢占式调度需要开发者理解切换时机、不当使用可能导致goroutine泄漏 |
| **O** 机会 | CSP模型简化并发编程复杂度，适合I/O密集型高并发场景 |
| **T** 威胁 | 切换点不可完全预测，某些场景可能出现意外的并发问题 |

### 适用场景
- I/O密集型的高并发服务开发
- 需要大量轻量级任务并行处理的场景
- 基于消息传递模式的分布式系统开发

---

#### Goroutine

##### 协程Coroutine

- 轻量级"线程"
- 非抢占式多任务处理，由协程主动交出控制权
- 编译器／解释器／虚拟机层面的多任务
- 多个协程可以在一个或多个线程上运行
- `runtime.Gosched()`协程主动交出控制权
- 子程序是协程的一个特例

###### goroutine的定义

- 任何函数只需要加上go就能送给调度器运行
- 不需要在定义时区分是否是异步函数
- 调度器在合适的点进行切换,切换点如下:
  - I/O,select
  - channel
  - 等待锁
  - 函数调用有时
  - runtime.Gosched()
  - 只是参考不能保证切换不能保证在其他地方不切换
- 使用 `-race`来检测数据访问冲突
- channel,buffered channel range 由发送方进行close() channel操作，理论基础`Communication Sequential Process CSP`
- `sync.WaitGroup`等待channel完成通信

- `不要通过共享内存来通信，要通过通信来共享内存`


