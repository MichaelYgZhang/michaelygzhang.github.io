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

```
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

```
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

```
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

