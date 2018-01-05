---
layout: post
title: ConcurrentHashMap
excerpt: ConcurrentHashMap源码分析
category: Java
---

- 底层bucket数组形式，Node节点k,v,next,所以是个单链结构,延迟初始化策略,2^n大小bucket数组,put第一个bin时采用CAS操作no lock when adding to empty bin,update(insert,delete,replace)则用锁同步,并且用第一个node作为这个bin的锁，锁住整个bucket,新放入的bin的node总在list末尾，所以以第一个node作为锁。默认如果key的hash值and,key值相等则进行覆盖。当单链大于等于8个node节点时则红黑树。

##### 扩容机制：

- 一旦链表中的元素个数超过了8个，那么可以执行数组扩容或者链表转为红黑树，这里依据的策略跟HashMap依据的策略是一致的。
- 当数组长度还未达到64个时，优先数组的扩容，否则选择链表转为红黑树。
- ForwardingNode
- ConcurrentHashMap对数据的读写都是原子操作。虽然ConcurrentHashMap的读不需要锁，但是需要保证能读到最新数据，所以必须加volatile。即数组的引用需要加volatile，同时一个Node节点中的val和next属性也必须要加volatile。

##### TODO 关键源码分析
