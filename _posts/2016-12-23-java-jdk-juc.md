---
layout: post
title: JUC(Java Util Concurrency)
excerpt: JUC
category: Java
---

##### ConcurrentHashMap

##### ConcurrentLinkedQueue


##### 线程池的分析和使用

- 为什么要使用线程池？
  1. 降低资源消耗。通过重复利用已创建的线程降低线程创建和销毁造成的消耗。
  2. 提高响应速速。当任务到达时，任务可以不需要等到线程创建就能执行。
  3. 提高线程的可管理性。线程时稀缺资源，如果无限制的创建，不仅会消耗系统资源，还会降低系统的稳定性，使用线程池可以进行
    统一的分配，调优和监控。

- 线程的创建:
`new ThreadPoolExecutor(corePoolSize, maximumPoolSize, keepAliveTime, milliseconds,runnableTaskQueue, handler);`
    1. corePoolSize:线程池的基本大小。
    2. runnableTaskQueue:任务队列。

- 线程池的监控

- 阻塞队列

- Fork/Join框架

-     
