---
layout: post
title: ConcurrentHashMap源码深度解析：线程安全HashMap的实现原理
excerpt: 深入分析ConcurrentHashMap的底层数据结构、CAS无锁操作、分段锁机制及扩容策略
category: Java
tags: [Java, 并发编程, ConcurrentHashMap, 源码分析, 线程安全]
---

## Executive Summary

### 核心观点（金字塔原理）
> **结论先行**: ConcurrentHashMap通过CAS无锁操作、分段锁技术和volatile保证可见性，实现了高效的线程安全HashMap，在高并发场景下性能远优于Hashtable和同步包装器。
>
> **支撑论点**:
> 1. 底层采用bucket数组+单链表/红黑树结构，延迟初始化策略，链表长度超过8时转为红黑树优化查询
> 2. 空bin插入采用CAS无锁操作，更新操作使用第一个node作为锁实现细粒度同步
> 3. 通过volatile修饰数组引用和Node的val/next属性，保证多线程读取时的可见性

### SWOT 分析

| 维度 | 分析 |
|------|------|
| **S** 优势 | CAS无锁插入空bin性能高；以node为粒度的锁减少竞争；红黑树优化长链表查询；volatile保证读操作无需加锁 |
| **W** 劣势 | 实现复杂度高；扩容时需要处理ForwardingNode；hash冲突严重时退化为锁竞争 |
| **O** 机会 | 适用于读多写少的高并发缓存场景；替代Hashtable和Collections.synchronizedMap |
| **T** 威胁 | 数组长度未达64时频繁扩容影响性能；极端并发写场景下锁竞争仍存在 |

### 适用场景
- 高并发环境下的线程安全Map需求
- 读多写少的缓存实现
- 需要替代Hashtable或synchronizedMap的性能敏感场景

---

- 底层bucket数组形式，Node节点k,v,next,所以是个单链结构,延迟初始化策略,2^n大小bucket数组,put第一个bin时采用CAS操作no lock when adding to empty bin,update(insert,delete,replace)则用锁同步,并且用第一个node作为这个bin的锁，锁住整个bucket,新放入的bin的node总在list末尾，所以以第一个node作为锁。默认如果key的hash值and,key值相等则进行覆盖。当单链大于等于8个node节点时则红黑树。

##### 扩容机制：

- 一旦链表中的元素个数超过了8个，那么可以执行数组扩容或者链表转为红黑树，这里依据的策略跟HashMap依据的策略是一致的。
- 当数组长度还未达到64个时，优先数组的扩容，否则选择链表转为红黑树。
- ForwardingNode
- ConcurrentHashMap对数据的读写都是原子操作。虽然ConcurrentHashMap的读不需要锁，但是需要保证能读到最新数据，所以必须加volatile。即数组的引用需要加volatile，同时一个Node节点中的val和next属性也必须要加volatile。

##### TODO 关键源码分析
