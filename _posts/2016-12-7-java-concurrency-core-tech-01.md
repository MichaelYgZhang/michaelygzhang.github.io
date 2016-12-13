---
layout: post
title: Java Concurrency Core Tech 笔记
excerpt: Java Concurrency Core Tech
category: Java
---

- println()内部是同步的。

```java
public void println(String x){
  synchronized (this){
    print(x);
    newLine();
  }
}
```

- 停止线程方式
  1. 使用退出标志，使线程正常退出，也就是当run方法完成后线程终止。
  2. 使用stop方法强制终止线程，但是不推荐使用这个方法，因为stop和suspend及resume一样，都是作废过期的方法，使用他们可能产生不可预料的结果。
  3. 使用interrupt方法中断线程。

- this.interrupted()：测试当前线程是否已经是中断状态，执行后具有将状态标志置清除为false的功能；
  this.isInterrupted()：测试线程Thread对象是否已经是中断状态，但不清除状态标志。
- yield方法：作用是放弃当前CPU资源，将它让给其他任务去占用CPU执行时间。但放弃的时间不确定，有可能刚刚放弃，马上又获得CPU时间片。
- 线程优先级setPriority()分为1～10个等级小于1或大于10抛出异常throw IllegalArgumentException()。
- 线程优先级具有继承特性。
- 线程优先级具有随机性，就是说优先级高的线程大多数会先执行，但并不一定每次都先执行完。
- 守护线程：java中有两种线程一种用户线程，一种守护线程。只要当前JVM实例中存在任何一个非守护线程没有结束，守护线程就在工作。
只有当最后一个非守护线程结束时，守护线程才随着JVM一同结束工作。Daemon的作用就是为其他线程的运行提供便利服务，守护线程的典型就是GC，他就是一个很称职的守护者。Thread.setDaemon(true);设置守护线程。

- 多个线程访问多个对象则JVM会创建多个锁。
- A线程先持有object对象的Lock锁，B线程可以以异的方式调用object对象中的非synchronized类型的方法。
- A线程先持有object对象的Lock锁，B线程如果在这时调用object对象中的synchronized类型方法则需要等待，就是同步。

- 脏读一定会出现操作实例变量的情况下，这就是不同县城“争抢”实例变量的结果。
- `synchronized`锁重入，在使用`synchronized`时，当一个线程得到一个对象的锁后，再次请求此对象锁时是可以再次得到
  该对象的锁的。这也证明了一个`synchronized`方法/块的内部调用本类的其他`synchronized`方法/块时，是可以得到这个对象的锁的，
  从而避免了死锁。
- 当存在父子类继承关系时，子类完全可以通过"可重入锁"调用父类的同步方法的。
- 当一个现层呢执行的代码出现异常时，其所持有的锁会自动释放。
- 同步不具有继承性。
- 和`synchronized`方法一样，`synchronized(this)`代码块也是锁定当前对象的。
- 多个线程调用同一个对象中的不同名称的`synchronized`同步方法或`synchronized(this)`同步代码块时，调用的效果就是按
  顺序执行，也是同步的，阻塞的。
- 锁非this对象具有一定的优点：如果在一个类中有很多个`synchronized`方法，这时虽然能实现同步，但会收到阻塞，所以影响效率；
  但如果使用同步代码块非this对象，则`synchronized(非this)`代码中的程序对同步方法是异步的，不与其他锁this同步方法争抢this锁，
  则可以大大提高运行效率。
- `synchronized`关键字加在`static`方法上是给`Class`类上锁，而`synchronized`关键字加到非`static`方法上是给对象上锁。而`Class`锁可以对类的所有对象实例起作用，注意两者的区别。
- `synchronized(class)`代码块的作用其实和`synchronized static`方法的作用一样。

- JVM中具有String常量池缓存功能。所以如果`synchronized(String)`则可能会造成多个线程同步时错误的情况。可以采用new Object()
  实例化一个Object对象，`synchronized(object)`这种方式。
-  volatile使变量在多线程间可见，只能修饰变量，不保证原子性。
- `synchronized`可以保证在同一时刻，只有一个线程可以执行某一个方法或某一个代码块。它包含两个特性：互斥性和可见性。同步`synchronized`不仅可以解决一个线程看到对象处于不一致的状态，还可以保证进入同步方法或者同步代码块的每个线程，都看到由`同一个锁`
保护之前所有的修改效果。


###### 线程间通信

[线程](https://michaelygzhang.github.io/java/2016/09/25/Java-Thread.html)

- wait()方法可以使用调用该方法的线程释放共享资源的锁，然后从运行状态退出，进入等待队列，直到再次唤醒。调用该方法后，该线程后续的代码
  不执行。
- notify()方法可以随机唤醒等待队列中等待同一个共享资源的一个线程，并使该线程退出等待队列，进入就绪可运行状态，也就是notify()方法仅通知一个线程。在制定notify()方法后，当前线程不会马上释放该对象的线程，呈wait状态的线程也并不能马上获取该对象的锁，要等到执行notify()方法的线程将程序执行完，也就是退出synchronized代码块后，当前线程才会释放锁，而wait状态所在的线程才可以获取该对象锁。
- notifyAll()方法可以使所有正在等待队列中等待同一个共享资源的全部线程从等待状态退出，进入可运行状态，此时，优先级最高的那个线程最先执行，但也有可能是随机执行，这取决与JVM虚拟机的实现。
- 每个锁对象都有两个队列，一个就绪队列，一个阻塞队列。就绪队列存储了将要获得锁的线程，阻塞队列存储了被阻塞的线程。一个线程被唤醒后
，才会进入就绪队列，等待CPU的调度；反而一个线程被wait后，就会进入阻塞队列，等待下一次被唤醒。
注意这里针对的是同一个共享资源锁对象。
- sleep()方法不释放锁资源对象。
- 当线程呈wait()状态时，调用线程对象的interrupt()方法会出现InterruptedException异常。
- 在执行同步代码块的过程中，遇到异常而导致线程终止，锁也会被释放。
- 若在阻塞队列中有若干个等待同一个共享资源的线程，调用一个notify后将会随机一个唤醒。
- wait(long)等待某一时间内是否有线程对锁进行唤醒，如果超过这个时间则自动唤醒。
- 若notify没有需要唤醒的阻塞线程，则此命令被忽略。
- C/P 设计
- 通过管道进行线程间通信：字节流
- join()的作用是等待线程对象销毁，使所属的线程对象x正常执行run()方法中的任务，而使当前线程z进行无限期的阻塞，等待线程x销毁后再继续执行线程z后面的代码。方法join具有使线程排队运行的作用，有些类似同步的运行效果。join与synchronized的区别是:join在内部使用
wait()方法进行等待，而synchronized关键字使用的是"对象监视器"原理作为同步。
- join(long)与sleep(long)的区别：join(long)的功能在内部是使用wait(long)方法实现的，所以具有释放锁的特点。而sleep(long)不释放锁。
- ThreadLocal主要解决的就是每个线程绑定自己的值，可以将ThreadLocal类比喻成全局存放数据的盒子，盒子中可以存储每个线程的私有数据。
- 类InheritableThreadLocal的使用可以在子线程中取得父线程继承下来的值。注意如果子线程在取得值的同时，主线程将InheritableThreadLocal中的值进行更改，那么子线程取到的值还是旧值。



###### Lock的使用
- ReentrantLock: lock()获取锁，unlock()释放锁；lock.lock()代码的线程持有“对象监视器”其他线程只有等待锁被释放时再次
  争抢，效果和使用synchronized关键字一样，线程之前还是顺序执行。
- Condition实现等待／通知，在使用notify/notifyAll方法进行通知时，被通知的线程是由JVM随机选择的，所有线程都注册在它一个
对象身上，线程开始notifyAll时，需要通知所有的WAITING线程，没有选择全，会出现相当大的效率问题。使用ReentrantLock结合
Condition类可以实现“选择性通知”，这个功能非常重要，而且在Condition类中默认提供的。Condition.await()/Condition.signal()；
- 公平锁与非公平锁，公平锁即先到先得FIFO先进先出顺序，而非公平锁就是一中获取锁的抢占机制，时随机获取锁的。这个方式可能造成
某些线程一直拿不到锁，结果也就时不公平的了。
- ReentrantLock:方法，getHoldCount()查询当前线程保持此锁定的个数，也就是调用lock()方法的次数；getQueueLength()返回正等待获取此锁定的线程数； getWaitQueueLength()返回等待与此锁定相关的给定条件Condition的线程估计数。
- ReentrantReadWriteLock加快效率，一个时读锁，也称为共享锁；另一个是写操作相关的锁，也叫排他锁。就是多个读锁之间不互斥，
读锁与写锁互斥，写锁与写锁互斥。



总结： java多线程编程核心技术 这本书主要是入门，更多的是简单的示例，基本API的使用。
