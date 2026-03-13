---
layout: post
title: Effective Java并发编程最佳实践：第10章核心要点解析
excerpt: 深入解读Effective Java第二版并发章节，掌握Java多线程编程的8条黄金法则
category: Java
tags: [Java, Effective Java, 并发编程, 最佳实践, 线程安全]
---

## Executive Summary

### 核心观点（金字塔原理）
> **结论先行**: Java并发编程应遵循8条核心原则：正确同步共享数据、避免过度同步、优先使用高级并发工具、充分文档化线程安全性，以编写出既正确又高效的并发程序。
>
> **支撑论点**:
> 1. 同步访问共享可变数据是并发正确性的基础，但过度同步会导致性能问题和死锁风险
> 2. Executor框架和并发工具类（如CountDownLatch、Semaphore）应优先于底层的Thread和wait/notify
> 3. 延迟初始化需谨慎使用，线程调度器和线程组不应被依赖

### SWOT 分析

| 维度 | 分析 |
|------|------|
| **S** 优势 | 8条法则覆盖并发编程核心要点；从同步基础到高级工具形成完整知识体系 |
| **W** 劣势 | 第二版基于Java 6，部分内容需结合新版本特性更新理解 |
| **O** 机会 | 适用于Java并发编程入门到进阶；代码审查的检查清单 |
| **T** 威胁 | 过度依赖规则可能忽视具体场景分析；新并发特性（如CompletableFuture）未覆盖 |

### 适用场景
- Java并发编程学习和代码审查
- 多线程应用设计决策参考
- 技术面试并发知识点复习

---

#### 第10章 并发

- **66 同步访问共享的可变数据**：`synchronized` 不仅保证互斥，还保证内存可见性。如果只需要线程间通信而不需要互斥，`volatile` 是更轻量的选择。最安全的做法是不共享可变数据——将可变数据限制在单线程内，或使用不可变对象。
- **67 避免过度同步**：在同步区域内不要调用外部方法（alien method），因为你无法控制外部方法的行为，可能导致死锁或数据损坏。通常应在同步区域内做尽可能少的工作：获取锁，检查共享数据，必要时转换数据，然后释放锁。
- **68 executor和task优先于线程**：`java.util.concurrent.ExecutorService` 提供了灵活的线程池管理。直接创建 Thread 是低级操作，应使用 `Executors.newFixedThreadPool`、`newCachedThreadPool` 等工厂方法，将任务提交（Runnable/Callable）与执行机制分离。
- **69 并发工具优先于wait和notify**：`java.util.concurrent` 提供的高级工具（ConcurrentHashMap, CountDownLatch, Semaphore, BlockingQueue）几乎总是优于直接使用 `wait/notify`。如果必须使用 wait，务必在 while 循环中调用（防止虚假唤醒），并优先使用 `notifyAll` 而非 `notify`。
- **70 线程安全性的文档化**：类必须在文档中清楚地说明其线程安全级别：不可变（immutable）、无条件线程安全（unconditionally thread-safe）、有条件线程安全（conditionally thread-safe）、非线程安全（not thread-safe）、线程对立（thread-hostile）。
- **71 慎用延迟初始化**：大多数字段应正常初始化而非延迟初始化。如果需要延迟初始化静态字段，使用 lazy initialization holder class 模式；如果需要延迟初始化实例字段，使用双重检查锁定（double-check locking）模式。
- **72 不要依赖于线程调度器**：正确的程序不应依赖线程调度器的行为。线程不应忙等（busy-wait）——反复检查共享对象等待状态变化。`Thread.yield` 没有可测试的语义，不要用它来"修复"并发问题。
- **73 避免使用线程组**：`ThreadGroup` API 已经过时且功能薄弱，异常处理功能已被 `Thread.UncaughtExceptionHandler` 取代。使用线程池（ExecutorService）代替线程组来管理线程的逻辑分组。

