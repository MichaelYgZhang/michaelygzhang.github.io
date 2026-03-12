---
layout: post
title: Java并发工具包JUC核心组件解析
excerpt: 深入解析Java Util Concurrency并发包核心组件，包括ConcurrentHashMap、线程池原理及Fork/Join框架
category: Java
tags: [Java, JUC, 并发编程, 线程池, ConcurrentHashMap, Fork/Join]
---

## Executive Summary

### 核心观点（金字塔原理）
> **结论先行**: JUC是Java并发编程的核心工具包，通过线程池复用线程、并发容器保证线程安全、Fork/Join实现任务分治，有效提升多线程程序的性能与可维护性。
>
> **支撑论点**:
> 1. 线程池通过复用线程降低创建销毁开销，提高响应速度，实现统一的线程管理与监控
> 2. ConcurrentHashMap/ConcurrentLinkedQueue提供线程安全的高性能并发容器
> 3. Fork/Join框架支持分治算法的并行执行，适合递归任务场景

### SWOT 分析

| 维度 | 分析 |
|------|------|
| **S** 优势 | 明确了线程池使用的三大核心价值：降耗、提速、可管理 |
| **W** 劣势 | 部分内容（阻塞队列、监控、Fork/Join）待补充完善 |
| **O** 机会 | 可作为深入学习JUC源码和并发编程实践的基础 |
| **T** 威胁 | 线程池参数配置不当可能导致OOM或线程饥饿 |

### 适用场景
- 高并发服务端程序开发
- 线程池配置与调优
- 并发数据结构选型

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

- 线程池参数详解：

| 参数 | 含义 | 建议 |
|------|------|------|
| corePoolSize | 核心线程数，即使空闲也不会被回收 | CPU 密集型：N+1；IO 密集型：2N |
| maximumPoolSize | 最大线程数，核心线程满且队列满时创建非核心线程 | 根据压测结果调整 |
| keepAliveTime | 非核心线程空闲存活时间 | 一般 60s |
| workQueue | 任务等待队列 | 见下方阻塞队列 |
| handler | 拒绝策略，队列满且线程数达最大值时触发 | 根据业务选择 |

- 线程池执行流程：
  1. 提交任务 → 核心线程数未满 → 创建核心线程执行
  2. 核心线程满 → 任务放入队列等待
  3. 队列已满 → 创建非核心线程执行（不超过 maximumPoolSize）
  4. 线程数已达上限且队列满 → 执行拒绝策略

- 拒绝策略：
  - `AbortPolicy`（默认）：抛出 RejectedExecutionException
  - `CallerRunsPolicy`：由提交任务的线程执行，注意可能拖慢主线程
  - `DiscardPolicy`：静默丢弃任务
  - `DiscardOldestPolicy`：丢弃队列中最旧的任务

- 线程池的监控

  监控是线程池调优的基础，ThreadPoolExecutor 提供了以下监控方法：

| 方法 | 说明 |
|------|------|
| `getActiveCount()` | 当前活跃线程数 |
| `getCompletedTaskCount()` | 已完成任务总数 |
| `getTaskCount()` | 已提交任务总数（含已完成） |
| `getQueue().size()` | 当前等待队列中的任务数 |
| `getLargestPoolSize()` | 线程池历史峰值线程数 |

  实践建议：通过定时任务采集以上指标，接入监控系统（如 Prometheus + Grafana），设置告警阈值：
  - 队列堆积 > 阈值 → 告警（任务处理不过来）
  - 活跃线程数持续等于最大线程数 → 告警（可能需要扩容）

- 阻塞队列

| 队列类型 | 特点 | 适用场景 |
|----------|------|----------|
| `ArrayBlockingQueue` | 有界数组队列，FIFO | 限制队列大小防止 OOM，最常用 |
| `LinkedBlockingQueue` | 可选有界链表队列，默认 Integer.MAX_VALUE | Executors.newFixedThreadPool 使用，注意设置容量 |
| `SynchronousQueue` | 不存储元素，直接交付 | Executors.newCachedThreadPool 使用，高吞吐 |
| `PriorityBlockingQueue` | 无界优先级队列 | 需要按优先级执行任务的场景 |
| `DelayQueue` | 延迟队列，元素需实现 Delayed 接口 | 定时任务、延迟执行 |

  **注意**：Executors 工厂方法创建的线程池存在 OOM 风险：
  - `newFixedThreadPool` / `newSingleThreadExecutor`：LinkedBlockingQueue 无界，任务堆积导致 OOM
  - `newCachedThreadPool`：maximumPoolSize 为 Integer.MAX_VALUE，可能创建大量线程
  - 阿里规约建议通过 `ThreadPoolExecutor` 手动创建线程池

- Fork/Join 框架

  Fork/Join 是 JDK 7 引入的并行计算框架，核心思想是**分治**：将大任务拆分（Fork）为小任务并行执行，然后合并结果（Join）。

  **核心组件**：
  - `ForkJoinPool`：执行 ForkJoinTask 的线程池，使用 Work-Stealing 算法平衡负载
  - `ForkJoinTask`：可拆分的任务基类
    - `RecursiveAction`：无返回值的任务
    - `RecursiveTask<V>`：有返回值的任务

  **Work-Stealing 算法**：每个工作线程维护一个双端队列（Deque），线程从自己队列的头部取任务执行；当自己队列为空时，从其他线程队列的尾部"窃取"任务执行，减少线程空闲时间。

```java
// Fork/Join 示例：并行求和
public class SumTask extends RecursiveTask<Long> {
    private static final int THRESHOLD = 10000;
    private long[] array;
    private int start, end;

    public SumTask(long[] array, int start, int end) {
        this.array = array;
        this.start = start;
        this.end = end;
    }

    @Override
    protected Long compute() {
        if (end - start <= THRESHOLD) {
            long sum = 0;
            for (int i = start; i < end; i++) sum += array[i];
            return sum;
        }
        int mid = (start + end) / 2;
        SumTask left = new SumTask(array, start, mid);
        SumTask right = new SumTask(array, mid, end);
        left.fork();  // 异步执行左半部分
        Long rightResult = right.compute();  // 当前线程执行右半部分
        Long leftResult = left.join();  // 等待左半部分完成
        return leftResult + rightResult;
    }
}
// 使用: ForkJoinPool pool = new ForkJoinPool();
//       long result = pool.invoke(new SumTask(array, 0, array.length));
```

  **适用场景**：计算密集型的可递归拆分任务，如大数组排序/求和、树/图遍历、文件搜索等。Java 8 的并行流（parallelStream）底层即使用 ForkJoinPool。
