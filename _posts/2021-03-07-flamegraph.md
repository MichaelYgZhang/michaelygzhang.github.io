---
layout: post
title: JVM性能分析利器：火焰图实战指南
excerpt: 使用async-profiler生成火焰图，直观定位Java应用CPU性能瓶颈
category: Architecture
tags: [性能优化, 火焰图, JVM, async-profiler, 性能分析]
---

## Executive Summary

### 核心观点（金字塔原理）
> **结论先行**: 火焰图通过可视化调用栈采样数据，能够快速定位Java应用的CPU性能热点
>
> **支撑论点**:
> 1. 工具选型：async-profiler是JVM性能分析的高效工具，支持生成SVG格式火焰图
> 2. 使用流程：下载工具 -> 获取目标进程PID -> 执行profiler命令生成火焰图
> 3. 分析方法：火焰图横轴表示采样比例，纵轴表示调用栈深度，宽度越大表示CPU占用越高

### SWOT 分析

| 维度 | 分析 |
|------|------|
| **S** 优势 | 提供完整的示例代码和命令，可快速上手实践 |
| **W** 劣势 | 未深入讲解火焰图的解读技巧和优化策略 |
| **O** 机会 | 适用于生产环境性能问题的快速诊断 |
| **T** 威胁 | profiler采样可能对线上应用产生轻微性能影响 |

### 适用场景
- Java应用CPU占用过高的问题排查
- 性能优化前的热点代码定位分析

---

##### 性能分析工具-火焰图

- 采用 <https://github.com/jvm-profiling-tools/async-profiler> 进行性能分析

- 实现步骤:
    1. 下载: <https://github.com/jvm-profiling-tools/async-profiler>
    2. 自动解压

    ```java
    public class CpuAsyncProfilerTest {
        public static void main(String[] args) throws InterruptedException {
            while (true) {
                CpuAsyncTask cpuAsyncTask = new CpuAsyncTask();
                cpuAsyncTask.run();
            }
        }

        public static void aTest() throws InterruptedException {
            Thread.sleep(10);
            bTest();
            cTest();
        }

        public static void bTest() throws InterruptedException {
            Thread.sleep(10);
            cTest();
        }
        public static void cTest() throws InterruptedException {
            Thread.sleep(10);
        }
    }
    class CpuAsyncTask implements Runnable {

        @Override
        public void run() {
            try {
                while (true) {
                    aTest();
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
```

    3. jps 找到程序的运行pid
    4. 生产火焰图命令 `./profiler.sh -d 30 -f flamegraph.svg 43619`

- ![flamegraph](https://raw.githubusercontent.com/MichaelYgZhang/michaelygzhang.github.io/master/images/flamegraph.svg)

- 资料
    - <http://www.ruanyifeng.com/blog/2017/09/flame-graph.html>
    - <https://queue.acm.org/detail.cfm?id=2927301>
    - <http://www.brendangregg.com/flamegraphs.html>
    - <http://www.brendangregg.com/>
    - <https://github.com/jvm-profiling-tools/async-profiler>
