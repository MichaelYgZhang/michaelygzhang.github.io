---
layout: post
title: 性能分析工具-火焰图
excerpt: 火焰图
category: Architecture
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