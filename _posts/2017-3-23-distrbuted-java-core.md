---
layout: post
title: 分布式Java应用基础与实践
excerpt: 分布式Java应用基础与实践
category: Destributed
---

#### 第1章 分布式Java应用

- 分布式Java应用通常有两种典型的方式来实现
  1. 基于消息方式实现系统间的通信
  2. 基于远程调用方式实现系统间的通信

#### 第2章 大型分布式Java应用与SOA

- SOA平台的挑战
  - 服务多级调用带来的延时
  - 调试跟踪困难
  - 更高的安全、监测的要求
  - 现有应用移植
  - QoS的支持(Quality of Service)
  - 高可用和高度可伸缩
  - 多版本和依赖管理

#### 第3章 深入理解JVM

- Java源码编译机制。
  1. 分析和输入到符号表，词法语法分析，生成抽象语法树
  2. 注解处理
  3. 语法分析和生成class文件
- JVM类加载过程分为三个步骤：装载、链接、初始化。装载和链接过程完成后，即将二进制的字节码转换为Class对象，初始化过程不是加载类时必须触发的，但最迟必须在初次主动使用对象前执行，其所作的动作为给静态变量赋值、调用<clinit>()等

#### 第4章 分布式Java应用与Sun JDK类库

- Collection存放多个单对象，Map接口用于存放Key-Value形式的键值对
- ArrayList:容量默认10，Object[]数组方式存放对象的。1.5倍扩容，add(int,E)指将对象插入指定位置，原来元素往后移动。set(int,E)指替换指定位置上的对象。remove(E)先找到元素然后删除，最后把其后的元素前移一位，最后一个元素设置null。remove(int)删除指定位置的对象多了一次范围的检测，少了对象位置的查找，因此性能更高。删除多个元素使用iterator()对象的it的remove()方法。查找更快，插入删除效率低，插入时可能扩容，删除时不会减少数组容量，如果希望缩小可调用trimToSize()，非线程安全。
- LinkedList:双向链表机制，内部有Entry对象(element,next,previous),get(int)判断参数是否小于0或大于LinkedList的size值，然后判断是否小于LinkedList的size值的一半，如果小从头开始找，否则从队列的尾部往前找。插入删除效率高，耗内存更多，非线程安全。
- Vector:默认大小10的Objcet[].capacityIncrement=0默认。扩容时如果capacityIncrement大于0则将现有size+capacityIncrement，否则扩大为现有size的两倍。线程安全。其它与ArrayList一样。
- Stack:继承于Vector。先进后出。push,pop调用peek获取元素并删除数组的最后一个元素,peek获取当前Object数组的大小并获取数组上的最后一个元素.
- HashSet:不允许元素重复基于HashMap实现。非线程安全。
- TreeSet:可排序基于TreeMap实现，非线程安全。
- HashMap:loadFactor=0.75,threshold=12,大小为16的Entry对象数组。扩容时为当前容量的两倍。rehash操作。非线程安全。
- TreeMap:支持排序Map，可以自定义Comparator参数的构造器，红黑树实现，非线程安全。

- 并发包(java.util.concurrent)
- ConcurrentHashMap:16并发量Segment[]，扩容时当前Segment*2，rehash，锁分段技术，put，remove时先加锁最后释放锁。voliate的HashEntry[]保证读时多线程并发,HashEntry对象中的hash,key,next属性都是final，这样保证next属性构建的链表不会发生变化。线程安全。
- CopyOnWriteArrayList:线程安全读操作时无锁的ArrayList，默认大小为0的数组。add(E)通过ReentrantLock保证线程安全。每次添加元素都创建一个新的比之前数组大小多1的Object[],将之前数组中的内容复制到新数组中，并将新增加的对象放到数组末尾，最后做引用的切换将新创建的数组对象赋值给全局的数组对象。
remove(E)，首先创建一个比当前数组小1的数组，遍历比较，并引用切换，找到返回true否则false。get(int)未加锁，可能会读到脏数据。适合读多写少的并发场景。
- Atomic原子类型CAS原子操作是CPU原语所以性能高于锁机制。
- ThreadPoolExecutor:
- Executors: new FixedThreadPool(int); new SigleThreadExecutor(); new CachedThreadPool(int); new ScheduledThreadPool(int);
- FutureTask
- Semaphore:用于控制某个资源同时被访问的个数的类。比如数据库链接池。
- CountDownLatch:可用于控制多个线程同时开始某动作的类。减计数的方式，当计数减到零时，位于latch.await后的代码才会被执行。
- CyclicBarrier
- ReentrantLock
- Condition 在同一个锁的情况夏可以根据不同的情况执行等待或唤醒动作。
- ReentrantReadWriteLock

- 序列化／反序列化

#### 第5章 性能调优

- 寻找性能瓶颈
  1. CPU消耗分析，CPU主要用于终端、内核以及用户进程的任务处理，优先级为终端>内核>用户进程；上下文切换，可运行队列，利用率。使用`-top`查看CPU的消耗情况
  2. 文件IO消耗分析，pidstat,iostat
  3. 网络IO消耗分析，sar
  4. 内存消耗分析jmap,jstat,mat,visualvm,vmstat
- 程序执行慢原因分析
  1. 锁竞争激烈
  2. 未充分使用硬件资源
  3. 数据量增长
- 调优
  1. JVM调优
  - 代大小的调优关键参数:-Xms-Xmx-Xmn-XX:SurvivorRation -XX:MaxTenuringThreashold ; -Xms和-Xmx通常相同避免运行时扩展JVM内存空间
  - 避免新生代大小设置过小，否则minorGC次数频繁，可能对象进入老年代然后触发FullGC
  - 避免新生代设置过大，老年代小了FullGC，minorGC耗时增加，推荐设置新生代占JVMHeap区大小的33%
  - 避免Survivor区过小或过大
  - 合理设置新生代存活周期-XX:MaxTenuringThreshold默认15次
  2. 程序调优
  - CPU消耗严重的解决方法,CPU us高的解决方法 Thread.sleep
  - CPU sy高的解决方法减少线程运行切换，最简单的方法就是减少线程数量。
  - 文件IO消耗严重的解决方法：异步写文件，批量读写，限流
  - 网络IO消耗严重的解决方法：限流发送packet的频率
  - 释放不必要的引用
  - 使用对象缓存池，采用合理的缓存失效算法FIFO、LRU、LFU等
  - 合理使用SoftReference和WeakReference
- 对资源消耗不多，但程序执行慢的情况，主要原因是锁竞争以及未充分发挥硬件资源
  - 锁竞争激烈导致CPU sy上升
  - 使用并发包中的类
  - 尽可能少用锁
  - 拆分锁
  - 去除读写操作的互斥锁CopyOnWrite
- 未充分使用硬件资源
  - 未充分使用CPU ，fork-join框架可以充分利用CPU
- 未充分使用内存


#### 第6章 构建高可用的系统

- 避免系统中出现单点
  1. 如果均衡地访问到提供业务功能的机器
  2. 如何保证当机器出现问题时，用户不会访问到这些机器
- 负载均衡技术(硬件/软件)
  - 选择实际业务处理器的方式
    1. 随机从地址列表中进行选择，简单，性能高
    2. Hash选择
    3. Round-Robin选择根据地址列表按顺序选择
    4. 按权重选择，根据每个地址的权重进行选择静态或动态权重两种
    5. 按负载选择
    6. 按连接选择
  - 响应返回方式
    1. 响应通过负载均衡机器返回。
    2. 响应直接返回至请求发送方
  - 硬件负载设备
    1. 负载设备的流量
    2. 长连接
- 软件负载方案
  - LVS Linux Virtual Server + Keepalived
  - p253

#### 构建可伸缩的系统
