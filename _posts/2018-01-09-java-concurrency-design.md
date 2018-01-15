---
layout: post
title: Java-concurrency-design
excerpt: Java-concurrency-design
category: Java
---

##### 内容
- 使用线程的经验:设置名称、响应中断、使用ThreadLocal
- Executor :ExecutorService和Future ☆ ☆ ☆
- 阻塞队列 : put和take、offer和poll、drainTo 
- 线程间的协调手段:lock、condition、wait、notify、notifyAll ☆ ☆ ☆ 
- Lock-free: atomic、concurrentMap.putIfAbsent、CopyOnWriteArrayList ☆ ☆ ☆ 
- 关于锁使用的经验介绍
- 并发流程控制手段:CountDownlatch、Barrier
- 定时器: ScheduledExecutorService、大规模定时器TimerWheel 
- 并发三大定律:Amdahl、Gustafson、Sun-Ni
- 总结 

###### 启动线程的注意事项

```java
  public static void main(String[] args) {
      //1
      Thread thread1 = new Thread("threadName1"){
          @Override
          public void run() {
              // do xxx
          }
      };
      //2
      MyThread thread2 = new MyThread();
      thread2.start();
      //3
      Thread thread3 = new Thread() {
          @Override
          public void run() {
              //do xxx
          }
      };
      thread3.setName("threadName3");
      thread3.start();
      //4
      Thread thread4 = new Thread(new Runnable() {
          @Override
          public void run() {
              // do xxx
          }
      });
      thread4.setName("threadName4");
      thread4.start();
      //5
      Thread thread5 = new Thread(new Runnable() {
          @Override
          public void run() {
              //do xxx
          }
      }, "threadName5");
      thread5.start();
  }
  static class MyThread extends Thread {
      public MyThread() {
          super("threadNmae2");
      }

      @Override
      public void run() {
          //do xxx
      }
  }
```

- 无轮何种方式，启动一个线程，都要给它一个名字，这对排错诊断系统监控很有帮助。否则诊断问题时，无法直观知道某个线程的用途。

##### 响应中断 Thread.interrupt()

```java
  public static void main(String[] args) {
      //1
      Thread threadInterrupted1 = new Thread("interrupt test1"){
          @Override
          public void run() {
              for (;;) {
                  //do xxx
                  if (Thread.interrupted()){
                      break;
                  }
              }
          }
      };
      threadInterrupted1.start();
  }
  //2
  public void foo() throws InterruptedException {
      if(Thread.interrupted()) {
          throw new InterruptedException();
      }
  }
```

- 程序应该对线程中断作出恰当的响应

##### ThreadLocal

```js
 //结构
 ThreadLocal<T>
 initalValue(): T
 get(): T
 set(T value)
 remove()
```

- ThreadLocal顾名思义它是local variable(线程局部变量)。它的功用非常简单，就是为每一个使用该变量的线程都提供一个变量值
的副本，是每一个线程都可以独立地改变自己的副本，而不会和其他线程的副本冲突。从线程的角度看，就好像每一个线程都完全拥有该变量。
- 使用场景：
  1. To keep state with a thrad (user-id, transaction-id, logging-id)
  2. To cache objects which you need frequently
  3. 隐式传参数
#### 注意⚠️使用ThreadLocal，一般都声明在静态变量中，如果不断的创建ThreadLocal而且没有调用remove方法，将导致`内存泄漏`,同时请注意，如果是static的ThreadLocal一般不需要调用remove。

##### 任务的提交者和执行者

- 为了方便并发执行任务，出现了一种专门用来执行任务的实现，就是`Executor`.由此，任务提交者不需要再创建管理线程，
使用更方便，也减少了开销。
- `java.util.concurrent.Executors`是Executor的工厂类，通过`Executors`可以创建你所需要的`Executor`
- 有两种任务: `Runnable`, `Callable` Callable是需要返回值的任务

```js
 Future<T>
 cancel(boolean): boolean
 isCancelled(): boolean
 isDone(): boolean
 get(): T
 get(long, TimeUnit): T
```

```js
  ExecutorService executor = Executors.newSingleThreadExecutor();
  Callable<Object> task = new Callable<Object>() { //Task Executor
      @Override
      public Object call() throws Exception {
          Object result = ".....";
          return  result;
      }
  };
  Future<Object> future = executor.submit(task); //Task Submitter
  try {
      System.out.printf("future:"+future.get());
      future.get(3, TimeUnit.SECONDS);//设置超时时间如果超时则出现 TimeoutException
  } catch (InterruptedException e) {
      e.printStackTrace();
  } catch (ExecutionException e) {
      e.printStackTrace();
  } catch (TimeoutException e) {
      e.printStackTrace();
  }
```

- TaskSubmitter把任务提交给Executor执行，它们之间需要一种通讯手段，这种手段的具体实现，通常叫做`Future`,Future通常包括`get(阻塞至任务完成)`，`cancel`,`get(timeout)`等等。Future也用于异步同步的场景。

##### 阻塞队列

```js
blockingQueue.put(object); //如果队列满则阻塞,生产者
blockingQueue.take(); //如果队列空则阻塞,消费者
//阻塞队列是一种常用的并发数据结构，常用于生产正-消费者模式。有如下阻塞队列
ArrayBlockingQueue  常用
LinkedBlockingQueue  不会满,消耗内存空间
SynchronousQueue  size为0
CompletionService (BlockingQuue + Executor)
TransferQueue(JDK7中更快的SynchronousQueue)
```

```js
//使用阻塞队列
Queue<E>  //使用BlockingQueue时尽量不要使用从Queue继承下来的方法否则就失去了Blocking的特性了。
add(E): boolean
remove(): E
offer(): boolean
poll(): E
element(): E
peek(): E
 ^
 | 继承
BlockingQueue<E> //在BlockingQueue中要使用put和take而非offer和poll。如果要使用offer和poll也是要用带时间参数的offer,poll
put(E)
take(): E
offer(E, long, TimeUnit): boolean
poll(long, TimeUnit): E
remainingCapacity()
drainTo(Collection<? super E): int  //使用drainTo批量获得其中的内容，能够减少锁的次数
drainTo(Collection<? super E, int): int 
```

- ❌

```js
 final BlockingQuue<Object> blockingQ = new ArrayBlockingQueue<Object>(10);
 Thread thread = new Thread("concumer thread") {
   public void run() {
     for (;;) {
       Object object = blockingQ.poll();//❌不等待就会直接返回
       handle(object);
     }
   }
 }
```

- ✅

```js
 final BlockingQuue<Object> blockingQ = new ArrayBlockingQueue<Object>(10);
 Thread thread = new Thread("concumer thread") {
   public void run() {
     for (;;) {
       try {
	  Object object = blockingQ.take();//等到有数据才继续
	  handle(object);
       } catch (InterruptedException e) {
	  break;
       } catch (Exception e) {
	  //handle exception
       }
     }
   }
 }
```

- ✅

```js
 final BlockingQuue<Object> blockingQ = new ArrayBlockingQueue<Object>(10);
 Thread thread = new Thread("concumer thread") {
   public void run() {
     for (;;) {
       try {
	  Object object = blockingQ.poll(1, TimeUnit.SECONDS); //防止死等
	  if (object == null) {
	    continue;// 或者做其他处理
	  }
	  handle(object);
       } catch (InterruptedException e) {
	  break;
       } catch (Exception e) {
	  //handle exception
       }
     }
   }
 }
```

##### 小结: 使用BlockingQueue时要使用`put/take`，如果要使用`offer/poll`需要加上`时间`参数。使用drainTo批量获得数据可以减少锁的次数

- 实现一个简单的阻塞队列

```js
 private Lock lock = new ReentrantLock();
 private Condition notEmpty = lock.newCondition();
 private Condition notFull = lock.newCondition();
 private Queue<Object> linkedList = new LinkedList<Object>();
 private int maxLength = 10;

 public Object take() throws InterruptedException {
     lock.lock();
     try {
         if (linkedList.size() == 0) {
             notEmpty.await();
         }
         if (linkedList.size() == maxLength) {
             notFull.signalAll();
         }
         return linkedList.poll();
     } finally {
         lock.unlock();
     }
 }

 public void offer(Object object) throws InterruptedException{
     lock.lock();
     try {
         if (linkedList.size() == 0) {
             notEmpty.signalAll();
         }
         if (linkedList.size() == maxLength) {
             notFull.await();
         }
         linkedList.add(object);
     } finally {
         lock.unlock();
     }
 }
// ⚠️未锁就直接执行await,signal,signalAll会抛异常
```

- ReentrantLock和Synchronized
  - synchronized是Lock的一种简化实现，一个Lock可以对应多个Condition，而synchronized把Lock和Condition合并了。
  一个synchronized Lock只对应一个Condition，可以说synchronized是Lock的简化版本。在JDK5,synchronized要比Lock慢很多，
  但在JDK6中，它们效率差不多。

```js
Lock
lock();
tryLock();
Unlock();
  ^
  |
Condition
await();  // wait
signal();  // notify
signallAll();  // notifyAll

synchronized
lock();
unlock();
wait();  //await
notify();  //signal
notifyAll();  signalAll
```

- [synchronization](https://en.wikipedia.org/wiki/Monitor_(synchronization))
- `AtomicInteger` 是由硬件提供原子操作指令实现的。在非激烈竞争的情况下，开销更小，速度更快。在`java.util.concurrent`中
实现的原子操作包括:`AtomicBoolean,AtomicInteger,AtomicLong,AtomicReference` 注意 CAS的`ABA`问题

##### Lock-Free算法

```js
 private AtomicInteger max = new AtomicInteger();
 public void set(int value) {
     int current;
     do {
         current = max.get();
         if (value <= current) {
             break;
         }
     } while (!max.compareAndSet(current, value));
 }
```

#### 非阻塞型同步 (Non-blocking Synchronization)

- 如何正确有效的保护共享数据是编写并行程序必须面临的一个难题，通常的手段就是同步。同步分为阻塞型同步(Blocking Synchronization)和非阻塞型同步(Non-blocking Synchronization)
- 阻塞型同步是指当一个线程到达临界区时，因另外一个线程已经持有访问该共享数据的锁，从而不能获取锁资源而阻塞，直到另外一个线程
释放锁。常见的同步原语有 `mutex,semaphore`等。如果同步方案采用不当，会造成死锁(deadlock),活锁(livelock_)和优先级反转(priority inversion)，以及效率低下等现象。
- 为了降低风险程度和提高程序运行效率，业界提出了不采用锁的同步方案，依照这种设计思路的算法称为非阻塞型算法，其本质就是停止
一个线程的执行不会阻碍系统中其他执行实体的运行。
- 有如下三种实现非阻塞型算法：
  1. `Wait-free`: 指任意线程的任何操作都可以在有限步之内结束，而不用关心其它线程的执行速度。Wait-free是基于per-thread的，可以认为是`starvation-free`的，非常遗憾的是实际情况并非如此，采用`wait-free`的程序并不能保证`starvation-free`，同时内存消耗也随线程数量而线性增长，目前只有极少数的非阻塞算法实现了这一点。
  2. `Lock-free`: 是能够确保执行它的所有线程中至少有一个能继续往下执行，由于每个线程不是`starvation-free`的，即有些线程
  可能会被任意地延迟，然后在每一步都至少有一个线程能够往下执行，因此系统作为一个整体是在持续执行的。可以认为是`system-wide`的，所有的`wait-free`算法都是`lock-free`的。
  3.`Obstruction-free`: 指在任何时间点，一个孤立运行线程的每一个操作可以在有限步之内结束。只要没有竞争，线程就可以持续运行。
  一旦共享数据被修改，`Obstruction-free`要求中止已经完成的部分操作，并进行回滚。所有`Lock-free`的算法都是`Obstruction-free`的。


```js
  ⬆️ Wait-Free  |
复| Lock-Free  | 加锁
杂| Obstruction-Free  |
程| Atomic            | 粒度
度| Lockless-based    |
  | Lock-based        ⬇️
```

- `ConcurrentHashMap`并没有实现`Lock-Free`只是使用了分离锁的办法使得能够支持多个Writer并发。ConcurrentHashMap需要使用更多的内存。
- `Lock-Free`算法，可以说是乐观锁如果非激烈竞争的时候，不需要使用锁，从而开销更小，速度更快.

```sql
//乐观锁
update table set value=v1, version=version+1 where id=xx and value=v2 and version=vserion1
//悲观锁
select .... from table where .... for update //默认为RowLock条件是明确指定主键,否则TableLock
```

- `CopyOnWriteArrayList` COW是一种古老的技术类似的并发数据结构有: `ConcurrentSkipListMap, ConcurrentSkipListSet,
CopyOnWriteArrayList, CopyOnWriteArraySet`适当使用CopyOnWriteArrayList能提高读操作的效率。

#### 锁的使用
- 使用支持CAS的数据结构避免使用锁，如：AtomicXXX, ConcurrentMap, CopyOnWriteList, ConcurrentLinkedQueue
- 一定要在使用锁的时候，注意获得锁的顺序，相反顺序获得锁，就容易产生死锁
- 死锁经常是无法完全避免的，`鸵鸟策略`被很多基础框架锁采用
- 通过`Dump`线程的`StackTrace`例如linux下执行命令`kill -3 <pid>` 或者`jstack -l <pid>`或者使用Jconsole连接上查看线程
的StackTrace由此来诊断死锁问题。
- 外部锁常被忽视而导致死锁，例如数据库的锁
- 存在检测死锁的办法
- 存在一些预防死锁的手段，比如Lock的tryLock,JDK7引入的Phaser等。

- 并发流程控制-使用`CountDownLatch`
- `Barrier`实现并发性能测试的聚合点，JDK7中包括一个类似的流程控制手段`Phaser`
- 定时器`ScheduledExecutorService`
- 大规模定时器`TimerWheel`
- JDK7 任务分解工具`Fork/Join`,分而治之，获取问题后，递归后将它分成多个子问题，直到每个子问题足够小，以至于可以高效地串行解决它们。递归过程将会把问题分成两个或者多个子问题，然后把这些问题放入队列中等待处理.(fork步骤),接下来等待所有子问题的结果(join步骤)把多个结果合到一起.
- `Fork/Join`分解主要包含以下几类:
```js
任务分解: 不同的行为分解给不同的线程
数据分解: 多个线程对不同的数据集执行同样的操作
数据流分解: 一个线程的输出是第二个线程的输入
```

- 并发三大定律:`Amdahl`计算机系统架构设计中某个部件的优化对整个架构的优化和改善是有上限的。`Gustafson`随着处理器个数的增加，并行与串行的计算总量也是可以增加的。`Sun-Ni`充分利用存储空间等计算资源尽量增大问题规模以产生更好/更精确的解。

- Donald Knuth说:"在我看来这种现象(并发)或多或少是由于硬件设计者已经无计可施导致的，它们将Moore定律失效的责任推脱给软件开发者"
- `GPU大规模并行计算`并行线程组织结构:Thread并行基本单位,Thread block相互合作的线程组,CTA(Cooperative Thread Array),允许彼此同步,通过快速共享内存交换数据,以1维2维,3维组织,最多包含512个线程; Grid：一组thread block，共享全局内存; Kernel：在GPU上执行的核心程序`One Kernel<->one grid`
- 问题:1 Future是做什么用的？2.Lock与synchronized区别是? 3. CAS? 4 Lock-Free算法三个组成部分？(循环,CAS(CompareAndSet),回退)

- [维基百科并发控制专题](http://en.wikipedia.org/wiki/Category:Concurrency_control)
- [维基百科并行计算专题](http://en.wikipedia.org/wiki/Parallel_computing)
- [维基百科非阻塞同步专题](http://en.wikipedia.org/wiki/Non-blocking_synchronization)
- [Herb Sutter的个人主页](http://www.gotw.ca)
- [Doug Lea的个人主页](http://g.oswego.edu/)
- [非阻塞同步算法论文](http://www.cs.wisc.edu/trans-memory/biblio/swnbs.html)
- [ACE关于并发和网络的指南](http://www.cs.wustl.edu/~schmidt/tutorials-patterns.html)
- [透过 Linux 内核看无锁编程](http://www.ibm.com/developerworks/cn/linux/l-cn-lockfree/)
- [OpenCL官方网站](http://www.khronos.org/opencl/)
