---
layout: post
title: Java并发编程艺术-读书笔记
excerpt: Java并发编程艺术
category: Java
---

##### 1 并发编程的挑战

- 上下文切换，减少上下文切换的方法有无锁并发编程、CAS算法、使用最少线程和使用协程。
- 死锁，避免死锁的常见方法，避免一个线程同时获取多个锁；避免一个线程在锁内同时占用多个资源，尽量
  保证每个锁只占用一个资源；尝试使用定时锁，使用lock.tryLock(timeout)来替代使用内部锁机制；
  对于数据库锁，加锁和解锁必须在一个数据库连接里，否则会出现解锁失败的情况。
- 资源限制，可以通过增加集群解决，具体问题具体分析

##### 2 Java并发机制的底层实现原理

- `volatile` 多线程共享变量的可见性，不保证原子性。比`synchronized`的执行成本更低，因为它不会引起线程上下文的切换和调度。实现机制：1. volatile变量生成字节码中，在写之前有lock，lock前缀指令会引起处理器缓存回写到内存，
并且有会有个称为“缓存锁定”的操作，这个缓存一致性机制会阻止同时修改由两个以上处理器缓存的内存区域数据。2. 一个处理器缓存回写到内存会导致其他处理器的缓存无效。
- `synchronized`的实现原理与应用。每个对象对应会有一对Monitor，monitorenter/monitorexit
  1. 普通同步方法，锁的是当前实例对象。
  2. 对于静态同步方法，锁是当前类的Class对象。
  3. 对于同步方法块，锁的是'synchronized'括号里的对象。

锁 | 优点| 缺点| 使用场景 |
:--|:---|:----|:--------|
偏向锁|加锁和解锁不需要额外的消耗，和执行非同步方法相比仅存在纳秒级差距|线程存在锁竞争带来额外的锁撤销的消耗|适用于只有一个线程访问同步块场景。|
轻量级锁| 竞争的线程不会阻塞，提高程序的响应速度|如果程序始终得不到锁竞争的线程使用自旋会消耗CPU|追求响应时间同步块执行速度非常快|
重量级锁|线程竞争不使用自旋,不会消耗CPU|线程阻塞，响应时间缓慢|追求吞吐量同步块执行速度较长|

- 原子操作的实现原理
  1. 使用总线锁保证原子性。
  2. 使用缓存锁保证原子性。

- Java如何实现原子操作。
  1. 锁
  2. CAS
    - ABA问题(`AtomicStampedReference`)
    - 自旋CAS如果长时间不成功，循环时间长开销大
    - 自能保证一个共享变量的原子操作，可以合并共享变量然后JDK 1.5开始可以使用`AtomicReference`类保证引用对象之前的原子性。


##### 3 Java内存模型 JMM

- Java内存模型的基础，共享内存模型。
  1. 在执行程序时，为了提高性能，编译器和处理器常常会对执行做重排序，分3中类型。
    - 编译器优化的重排序。
    - 指令级并行的重排序，如果不存在数据依赖性，处理器可以改变语句对应机器指令的执行顺序。
    - 内存系统的重排序，由于处理器使用缓存和读／写缓冲区，使得家在和存储操作看上去可能是乱序执行。
    - 从源码到最终实际执行的指令序列。源码-->1编译器优化冲排序-->2指令级并行重排序-->3内存系统重排序-->最终执行的指令序列。1为编译器重排序23为处理器重排序。通过内存屏障指令可以禁止特定类型的处理器重排序。
  2. happens-before原则

- 重排序，是指编译器和处理器为了优化程序性能而对指令序列进行重排序的一种手段。
  1. 数据依赖；如果两个操作访问一个变量，且这两个操作中有一个写操作，此时这个两个操作之前就存在数据依赖，3中情况，写后读，写后写，读后写，只要重排序两个操作的执行顺序，程序结果就会被改变。编译器和处理器不会改变存在数据依赖关系的两个操作的执行顺序。
  2. as-if-serial语义；不管怎么重排序，程序的执行结果不能被改变。
  3. 程序顺序规则。

- 顺序一致性。

- volatile 的内存语义

- 锁的内存语义

- final域的内存语义

- happens-before

- Java编译器在生成字节码时，会在执行指令序列的适当位置插入内存屏障来限制处理器的重排序。

###### 4 Java并发编程基础

- JMX 查看一个Java程序包含那些线程

```java
public class MultiThread {
    public static void main(String[] args) {
        ThreadMXBean threadMXBean = ManagementFactory.getThreadMXBean();
        ThreadInfo[] threadInfos = threadMXBean.dumpAllThreads(false, false);
        for (ThreadInfo threadInfo : threadInfos){
            System.out.println("[" + threadInfo.getThreadId() + ":" + threadInfo.getThreadName() + "]");
        }
    }
}
/** Mac JDK1.8
[7:JDWP Command Reader]
[6:JDWP Event Helper Thread]
[5:JDWP Transport Listener: dt_socket]
[4:Signal Dispatcher]
[3:Finalizer]
[2:Reference Handler]
[1:main]
*/
```

- 使用多线程的原因：利用多核，更快的响应时间，更好的编程模型
- 线程优先级setPriority(int);默认5，范围1～10.
- 线程的状态:NEW;RUNNABLE;BLOCKED;WAITING;TIME_WAITING;TERMINATED;
- Daemon线程Thread.setDaemon(true);线程启动前设置，不能在启动后设置。
- 启动和终止线程
- 线程间通信
- 线程应用实例

#### 5 Java中的锁

- 
