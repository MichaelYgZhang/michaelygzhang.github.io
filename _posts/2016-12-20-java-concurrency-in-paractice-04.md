---
layout: post
title: Java Concurrency in Paractice 第四部分 高级主题
excerpt: Java Concurrency in Paractice 第十三章 显示锁 第十四章 构建自定义的同步工具
category: Java
---

##### 显示锁

```java
Lock lock = new ReenttrantLock();
...
lock.lock();
try {
  //do something
  // catch execption
} finally {
  lock.unlock();
}
```

-  tryLock()实现轮训锁，可以避免锁顺序的死锁情况的发生。
- lockInterruptibly()方法能够在获得锁的同时保持对中断的响应。
- 非块结构的加锁，更加灵活。比如分段锁机制。有更好的竞争性能。锁的实现方式越好，将需要越少的系统调用和上下文切换，并且在共享内存总线上的内存同步通信量也越少，而一些耗时的操作将占用应用程序的计算资源。
- 公平锁／非公平锁(默认)  公平锁：线程将按照它们发出请求的顺序来获得锁。非公平锁：随机。大多数情况下，非公平锁的性能要高于公平锁的性能。
- 在一些内置锁无法满足的情况下，ReenttrantLock可以作为一种高级工具。当需要一些高级功能时才应该使用ReenttrantLock，这些功能包括：可定时的、可轮训的与可中断的锁获取操作，公平队列，以及
  非块结构的锁。否则，还是应该优先使用 synchronized.
- 接口ReadWriteLock, readLock()/writeLock()  一个资源可以被多个读操作访问，或者被一个写操作访问，但两者不能同时进行。实现类ReentantReadWriteLock.
- ReentantReadWriteLock在构造时也可以选择是一个非公平锁（默认）还是一个公平锁。等待时间最长的线程将优先获得锁，如果这个锁由读线程持有，
  而另一个线程请求写入锁，则其他读线程都不能获得读取锁，直到写线程使用完并且释放了写入锁。在非公平的锁中，线程获得访问许可的顺序是不确定的。写线程降级为读线程是可以的，但从读线程升级为
  写线程则是不可以的（会导致死锁）。写锁只能有唯一的所有者。ConcurrentHashMap。

```java
public class ReadWriteMap<K, V> {
  private final Map<K, V> map;
  private final ReadWriteLock lock = new ReentantReadWriteLock();
  private final Lock r = lock.readLock();
  private final Lock w = lock.writeLock();

  public ReadWriteLock(Map<K, V> map) {
    this.map = map;
  }

  public V put (K key, V value) {
    w.lock();
    try {
      return map.put(key, value);
    } finally {
      w.unlock();
    }
  }
  // 对remove(), putAll(), clear()等方法执行相同的操作。

  public V get(Objcet key) {
    r.lock();
    try {
      return map.get(key);
    } finally {
      r.unlock();
    }
  }

  //对其他只读Map方法执行相同的操作。
}  
```

- 与内置锁相比，显示的Lock提供了一些扩展功能，在处理锁的不可用性方面有着更高的灵活性，并且对队列行有着更好的控制，但ReenttrantLock不能完全取代synchronized，只有在它无法满足需求时，
  才应该使  用ReenttrantLock.读-写锁允许多个读线程并发低访问被保护的对象，当访问读取操作为主的数据结构时，它能提高程序的可伸缩性。


##### 构建自定义的同步工具

- 
