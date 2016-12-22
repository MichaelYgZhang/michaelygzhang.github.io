---
layout: post
title: Java Concurrency in Paractice 第四部分 高级主题
excerpt: Java Concurrency in Paractice 第十三章 显示锁 第十四章 构建自定义的同步工具 第十五章 原子变量与非阻塞同步机制 第十六章 Java内存模型
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

- 将与条件队列相关联的条件谓词以及在这些条件谓词上等待的操作都写入文档。
- 每一次wait调用都会隐式地与特定的条件谓词关联起来。当调用某个特定条件谓词的wait时，调用者必须已经持有与条件队列相关的锁，并且这个锁必须保护者构成条件谓词的状态变量。
- 当使用条件谓词时(例如：Objcet.wait或 Condition.await)
  1. 通常都有一个条件谓词---包括一些对象状态的测试，线程在执行前必须首先通过这些测试。
  2. 在调用wait之前测试条件谓词，并且从wait中返回时再次测试。
  3. 在一个循环中调用wait。
  4. 确保使用与条件队列相关的锁来保护构成条件谓词的各个状态变量
  5. 当调用wait、notify、notifyAll等方法时，一定要持有与条件相关的锁。
  6. 在检查条件谓词之后以及开始执行相应的操作之前，不要释放锁。

- 每当在等待一个条件时，一定要确保在条件谓词变为真时通过某种方式发出通知。
- 只有同时满足以下两个条件时，才能使用单一的notify而不是notifyAll。
  1. 所有等待线程的类型都相同。只有一个条件谓词与条件队列相关，并且每个线程在从wait返回后将执行相同的操作。
  2. 单进单出，在条件变量上的每次通知，最多只能唤醒一个线程来执行。

- 特别注意：在Condition对象中，与wait、notify、notifyAll方法对应的分别是await、signal、signalAll。但是，Condition对Object进行了扩展，因而它也包含wait和notify方法。一定要确保使用正确的版本---await和signal。
- 要实现一个依赖状态的类---如果没有满足依赖状态的前提条件，那么这个类的方法必须阻塞，那么最好的方式是基于现有的库类来构建，例如Semaphore.BlockingQueue或CountDownLatch，
  有时候现有的类库不能提供足够的功能，在这种情况下，可以使用内置的条件队列，显式的Condition对象或者AbstractQueuedSynchronizer来构建自己的同步器。内置条件队列与内置锁是
    紧密绑定在一起的，这时因为管理状态依赖性机制必须与确保状态一致性机制关联起来。同样，显式的Condition与显式Lock也是紧密地绑定到一起的，并且与内置条件队列相比，还提供了一个扩展的功能集，
    包括每个锁对应与多个等待线程集，可中断或不可中断的条件等待，公平或非公平队列操作，以及基于时限的等待。

##### 原子变量与非阻塞同步机制

- CAS 包含了3个操作数，需要读写的内存位置V，进行比较的值A和拟写入的新值B，当且仅当V的值等于A时，CAS才会通过原子方式用新值B来更新V的值，否则不会
执行任何操作，无论位置V的值是否等于A，都将返回V原有的值。乐观控制。

```java
@ThreadSafe
public class ConcurrentStack<E> {
    AtomicReference<Node<E>> top = new AtomicReference<Node<E>>();

    public void push(E item){
        Node<E> newHead = new Node<E>(item);
        Node<E> oldHead = top.get();
        do {
            oldHead = top.get();
            newHead.next = oldHead;
        } while (!top.compareAndSet(oldHead, newHead));
    }

    public E pop () {
        Node<E> oldNode;
        Node<E> newNode;
        do {
            oldNode = top.get();
            if (oldNode == null)
                return null;
            newNode = oldNode.next;
        } while (!top.compareAndSet(oldNode, newNode));
        return oldNode.item;
    }

    private static class Node<E>{
        public final E item;
        public Node<E> next;
        public Node(E item){
            this.item = item;
        }
    }
}
```

- ABA问题：V值从A变B，然后又由B变A，仍然被认为是发生了变化。解决方案：不是更新某个引用的值，而是更新两个值，包括一个引用和一个版本号。AtomicStampedReference！
- 非阻塞算法通过底层的并发原语（例如比较并交换而不是锁）来维持线程的安全性，这些底层的原语通过原子变量类向外公开，这些类也用做一种“更好的volatile变量”从而为整数和
对象引用提供原子的更新操作。
- 非阻塞算法在设计和实现时非常困难，但通常能够提供更高的可伸缩性，并能更好地防止活跃性故障的发生。在JVM从一个版本升级到下一个版本的过程中，并发性的主要提升都来自于
（在JVM内部以及平台类库中）对非阻塞算法的使用。


##### Java内存模型

-  Happens-Before的规则包括：
  1. 程序顺序规则。如果程序中操作A在操作B之前，那么在线程中A操作将在B操作之前执行。
  2. 监视器锁规则。在监视器上的解锁操作必须在同一个监视器锁上的加锁操作之前执行。
  3. volatile变量规则。对volatile变量的写入操作必须在对该变量的读操作之前执行。
  4. 线程启动规则。在线程上对Thread.Start的调用必须在该线程中执行任何操作之前执行。
  5. 线程结束规则。线程中的任何操作都必须在其他线程检测到该线程已经结束之前执行，或者从Thread.join中成功返回，或者在调用Thread.isAlive时返回false。
  6. 中断规则。当一个线程在另一个线程上调用interrupt时，必须在被中断线程检测到interrupt调用之前执行(通过抛出InterruptedException，或者调用isInterrupted和interrupted)
  7. 终结器规则。对象的构造函数必须在启动该对象的终结器之前执行完成。
  8. 传递性。如果操作A在操作B之前执行，并且操作B在操作C之前执行， 那么操作A必须在操作C之前执行。
