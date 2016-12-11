---
layout: post
title: Java Concurrency Core Tech 笔记
excerpt: Java Concurrency Core Tech
category: Java
---

```java
  Thread thread1 = new Thread();
```


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
