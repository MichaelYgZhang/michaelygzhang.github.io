---
layout: post
title: Interview-2018
excerpt: Interview-2018
category: Interview
---

- 写在最前面: 问题主要从这几个方面来讲what？how？why？是什么？怎么用说一下使用场景？为什么这么样用？对比其它方案是否有更好的方案？
- 总结：多思考什么场景适合用什么技术，以及是否有更好的技术方案。做过的事情需要总结成一句话来说，心得！！！！

##### 自我介绍 5min

- 项目简介:1.核心业务流程 2.技术架构 3.技术难点亮点,解决过哪些系统难点问题? 如何发现,解决的,收获是什么? 现有系统是否还能进一步优化?
- 简历中的核心点多聊聊关于技术的。系统技术框架是怎么样的？为何采用这种技术方案？ 是否有更好的技术方案？ 

- 计算机专业,写了点儿博客记录学习历程以及技术的积累
- 架构采用RPC通信, 站点: 参数及帖子校验header,refer等,IP拉黑,动态验证码...反作弊,反爬虫策略,简称流量过滤. 
服务层: 号码资源管理模块(分配/绑定/释放)号码资源隔离以及降级策略; 运营商服务故障监测模块; 业务/性能监控模块; 查询模块;
JOB,ThreadPoll, HttpClient, ESB, 分布式锁,线程池子隔离措施.灵活配置等,做了服务重构的事,开发测试效率提升约20%;缓存,IP名单,锁.. 
    - 故障检测: 类心跳监测,下号 + 短信/邮件告警, 上号码 做系统高可用
    - 监控告警，有误报率？比如话单量下降20%的告警？节假日如何处理的？
    - 系统遇到的难点: 
    - 网络超时造成A,B系统号码状态不一致问题. 
    - 反爬虫,观测,分析,对症下药,比如不返回错误,而是返回假号码,让对方以为一切正常...等
    - 慢SQL优化,分析找到问题SQL,优化,效果验证?
 - 个人总结: 
    1. 技术选型时适合就好, 变化与不变性的东西隔离开,
    2. 不相信任何第三方服务做好容错降级处理,系统做到小步快跑,做好测试用例方便今后的扩展
    3. 提高内存使用率,减少IO, 指数级调用减少常量级调用
    4. 流量激增增加副本, 数据激增分库分表或者引入大数据HDFS


##### JavaCore 以下JDK版本1.9

###### Java Collections Framework（JCF）  

- [http://java-performance.com/](http://java-performance.com/)
- [https://docs.oracle.com/javase/8/docs/technotes/guides/collections/overview.html](https://docs.oracle.com/javase/8/docs/technotes/guides/collections/overview.html)

![JCF](https://upload-images.jianshu.io/upload_images/2243690-9cd9c896e0d512ed.gif?imageMogr2/auto-orient/strip%7CimageView2/2/w/643)
![java.util.Collection class and interface hierarchy](https://upload.wikimedia.org/wikipedia/commons/a/ab/Java.util.Collection_hierarchy.svg)
![Java's java.util.Map class and interface hierarchy](https://upload.wikimedia.org/wikipedia/commons/7/7b/Java.util.Map_hierarchy.svg)

- `ArrayList` 
    - 实现List接口, 底层实现Object[],非线程安全,多线程安全考虑使用Vector/Collections.synchronizedList(List l)
    - 实现RandomAccess接口,可高效进行foreach(:){}
    - 构造集合时若不设置initialCapacity则第一次add操作时将开辟DEFAULT_CAPACITY = 10;的内存数组空间
    - 当前数组集合大小若不足时将进行1.5倍的扩容,数组最大值为MAX_ARRAY_SIZE = Integer.MAX_VALUE - 8;即`2^32-1`;
    注意扩容将调用public static native void arraycopy(Object src, int  srcPos, Object dest, int destPos, int length);性能消耗点.
    - 迭代时fail-fast; 如有修改 the iterator will throw a ConcurrentModificationException.
 - `API简介`
    - public boolean add(E e) {};最后一位数组下标插入;
    - public void add(int index, E element) {};指定下表插入需移动index之后的元素,当size比较大时index约小,需要移动数组的元素越多,性能越低.
    最坏情况是1. 先扩容 2. 调用System.arraycopy(....)移动元素
    - public E set(int index, E element) {}; 替换指定位置元素
    - public E remove(int index) {}; 移除指定位置元素,index约小需要前移动的元素越多,性能消耗越大.注意elementData[--size] = null; // clear to let GC do its work
    - public boolean remove(Object o) {}; 1. 找到元素下标 2.移动元素 3.elementData[--size] = null; // clear to let GC do its work

- `LikedList` 
    - 实现List<E>, Deque<E>双端队列，非线程安全, `插入/删除`高效,`遍历`性能低, 消耗更多的内存,产生更多对象,增加GC的次数/时间；
    - Collections.synchronizedList(new LinkedList(...));可做到线程安全

- `HashSet`无序,不重复,采用散列的存储方法，所以没有顺序; 其实就是一个hashmap,只是在在添加元素的时候对应的put(k,object),k就是要添加的值,而参数v就是一个final类型的object对象。
此处需要注意的是:由于map允许有一个key为null的键值对，所以set也就允许有一个为null的对象，唯一的一个。

- `LinkedHashSet`LinkedHashSet是HashSet的一个子类,只是HashSet底层用的HashMap,而LinkedHashSet底层用的LinkedHashMap; 元素有序.

- `HashMap` 数组的特点是：寻址容易，插入和删除困难；而链表的特点是：寻址困难，插入和删除容易。哈希表结合了两者的优点。
哈希表有多种不同的实现方法，可以理解将此理解为“链表的数组”;哈希表是由数组+链表组成;HashMap是基于AbstractMap;
HashMap可以允许存在一个为null的key和任意个为null的value; HashMap仅支持Iterator的遍历方式;

- `TreeMap` 对象必须实现equals方法和Comparable/Comparator 

- `Hashtable`线程安全; HashTable基于Dictionary类,HashTable中的key和value都不允许为null,HashMap仅支持Iterator的遍历方式;

###### 并发集合

- `CopyOnWriteArrayList：list`
- `ConcurrentLinkedDeque / ConcurrentLinkedQueue`

###### ConcurrentHashMap JDK1.7 Segment[] + HashEntry[] + HashEntry单链
其中Segment在实现上继承了ReentrantLock，这样就自带了锁的功能。
数组大小默认16,0.75增长因子,2^n次方大小.size计算方式:1不加锁连续计算元素个数最多3次,如果前后2次一样,则返回;否则给每个Segment进行加锁计算一次.
;

- 当执行put方法插入数据时，根据key的hash值，在Segment数组中找到相应的位置，如果相应位置的Segment还未初始化，则通过CAS进行赋值，接着执行Segment对象的put方法通过加锁机制插入数据，实现如下：
场景：线程A和线程B同时执行相同Segment对象的put方法
1. 线程A执行tryLock()方法成功获取锁，则把HashEntry对象插入到相应的位置；
2. 线程B获取锁失败，则执行scanAndLockForPut()方法，在scanAndLockForPut方法中，会通过重复执行tryLock()方法尝试获取锁，在多处理器环境下，重复次数为64，单处理器重复次数为1，当执行tryLock()方法的次数超过上限时，则执行lock()方法挂起线程B；
3. 当线程A执行完插入操作时，会通过unlock()方法释放锁，接着唤醒线程B继续执行；

###### ConcurrentHashMap JDK1.8 Node数组 + CAS + Synchronized | 数组+链表+红黑树
volatile类型的变量baseCount计算size值，因为元素个数保存baseCount中，部分元素的变化个数保存在CounterCell数组中，通过累加baseCount和CounterCell数组中的数量，即可得到元素的总个数；
- 扩容时优先扩容数组(<64时),2倍数组进行扩容; 然后才是当单链>8时转化红黑树；

- `ConcurrentSkipListMap` 基于跳跃列表（Skip List）的ConcurrentNavigableMap实现。本质上这种集合可以当做一种TreeMap的线程安全版本来使用。
- ConcurrentSkipListSet：使用 ConcurrentSkipListMap来存储的线程安全的Set。


###### JDK集合总结:
- 选择合适的集合，使用泛型避免出现ClassCastException
- 数组查询高效,插入删除移动元素,每次add到最后一个下标,容量不够则扩容复制元素`System.arraycopy()`; 
- 链表每次新建Entry对象需要更多的内存空间,增加GC,插入删除高效遍历耗时.
- 重写equals & hashcode方法,注意:equals相等必定hashcode相同; 若hashcode相同equals不等则造成hash冲突,导致单链/rehash等操作
- 可以设置初始容量来避免重新计算hash值或者是扩容，Map的key尽量采用不可变对象比如String
- tree相关Comparable/Comparator 
- 实现了RandomAccess接口的类可以通过foreach遍历高效,否则采用Iterator迭代器遍历,Iterator可以进行remove操作.
- 编程的时候接口优于实现，底层的集合实际上是空的情况下，返回长度是0的集合或者是数组，不要返回 null。
- [集合](http://wiki.jikexueyuan.com/project/java-interview-bible/collection.html)
- [集合面试题](http://www.importnew.com/15980.html)
- [Java7/8 中的 HashMap 和 ConcurrentHashMap 全解析](http://www.importnew.com/28263.html)
- [集合相关runoob](http://www.runoob.com/java/java-collections.html)
- [JCF-github](https://github.com/CarpenterLee/JCFInternals/blob/master/markdown/0-Introduction.md)
- [集合-](https://www.cnblogs.com/jing99/p/7057245.html)

- final／static？TODO

##### AQS (AbstractQueuedSynchronizer) 
队列同步器AQS是用来构建锁或其他同步组件的基础框架，内部使用一个int成员变量表示同步状态，
通过内置的FIFO队列来完成资源获取线程的排队工作，其中内部状态state，等待队列的头节点head和尾节点head，
都是通过volatile修饰，保证了多线程之间的可见。
- static final int CANCELLED =  1;SIGNAL = -1等待触发状态;CONDITION = -2等待条件状态;PROPAGATE = -3状态需要向后传播;
- 子类重写tryAcquire和tryRelease方法通过CAS指令修改状态变量state。
- [AQS详解](https://www.jianshu.com/p/d8eeb31bee5c)

1. 线程A执行CAS执行成功，state值被修改并返回true，线程A继续执行。
2. 线程A执行CAS指令失败，说明线程B也在执行CAS指令且成功，这种情况下线程A会执行步骤3。
3. 生成新Node节点node，并通过CAS指令插入到等待队列的队尾（同一时刻可能会有多个Node节点插入到等待队列中），
如果tail节点为空，则将head节点指向一个空节点（代表线程B）
4. node插入到队尾后，该线程不会立马挂起，会进行自旋操作。因为在node的插入过程，线程B（即之前没有阻塞的线程）
可能已经执行完成，所以要判断该node的前一个节点pred是否为head节点（代表线程B），如果pred == head，
表明当前节点是队列中第一个“有效的”节点，因此再次尝试tryAcquire获取锁
    - 如果成功获取到锁，表明线程B已经执行完成，线程A不需要挂起
    - 如果获取失败，表示线程B还未完成，至少还未修改state值。进行步骤5
5. 前面我们已经说过只有前一个节点pred的线程状态为SIGNAL时，当前节点的线程才能被挂起。
   1. 如果pred的waitStatus == 0，则通过CAS指令修改waitStatus为Node.SIGNAL。
   2. 如果pred的waitStatus > 0，表明pred的线程状态CANCELLED，需从队列中删除。
   3. 如果pred的waitStatus为Node.SIGNAL，则通过LockSupport.park()方法把线程A挂起，并等待被唤醒，被唤醒后进入步骤6。
6. 线程每次被唤醒时，都要进行中断检测，如果发现当前线程被中断，那么抛出InterruptedException并退出循环。
从无限循环的代码可以看出，并不是被唤醒的线程一定能获得锁，必须调用tryAccquire重新竞争，
因为锁是非公平的，有可能被新加入的线程获得，从而导致刚被唤醒的线程再次被阻塞，这个细节充分体现了“非公平”的精髓。

- 释放锁过程:
    1. 如果头结点head的waitStatus值为-1，则用CAS指令重置为0；
    2. 找到waitStatus值小于0的节点s，通过LockSupport.unpark(s.thread)唤醒线程


##### CAS(Compare and Swap)
- CAS三个参数，一个当前内存值V、旧的预期值A、即将更新的值B，当且仅当预期值A和内存值V相同时，将内存值修改为B并返回true，否则什么都不做，并返回false。
- CAS存在一个很明显的问题，即ABA问题。AtomicStampedReference,它可以通过控制变量值的版本来保证CAS的正确性。
- CAS 可以复用缓存

##### synchronized 
- synchronized可以保证方法或代码块在运行时，同一时刻只有一个线程可以进入到临界区（互斥性），同时它还保证了共享变量的内存可见性
- monitorenter/monitorexit
- [synchronized资料](https://www.jianshu.com/p/19f861ab749e)

##### ReentrantLock Synchronized 
- [资料](https://www.jianshu.com/p/4358b1466ec9)
- [LOCK](http://www.cnblogs.com/dolphin0520/p/3923167.html)
- [LOCK-1](https://www.jianshu.com/p/2344a3e68ca9)
- [LOCK-2](http://www.leocook.org/2017/07/16/Java%E5%B9%B6%E5%8F%91(%E5%85%AD)-ReentrantLock-synchronized/)
- volitile修饰long,double可以原子性，内存屏障会将所有写的值更新到缓存，顺序性可见性, 否则出现`伪共享缓存`问题。

##### 线程池 [资料](https://www.jianshu.com/p/87bff5cc8d8c)  场景?优势/缺点是什么?

- ThreadLocal 内存何时情况有可能发生内存泄漏？ 如何解决？答得是remove? 待核实！！threadlocal使用线程局部变量，注意使用后释放？static修饰？
    - [http://blog.xiaohansong.com/2016/08/06/ThreadLocal-memory-leak/](http://blog.xiaohansong.com/2016/08/06/ThreadLocal-memory-leak/)
    
- 线程安全 与 JVM内存模型之间的关系？
    - 如果你的代码所在的进程中有多个线程在同时运行，而这些线程可能会同时运行这段代码。如果每次运行结果和单线程运行的结果是一样的，而且其他的变量的值也和预期的是一样的，就是线程安全的。
    - 
- 并发集合容器,线程安全的非线程安全的分别都有哪些?
- 如何看当前线程是否是线程安全的? 特征是什么? 【资料](https://yq.aliyun.com/articles/75403)

##### IO/BIO/NIO/AIO Netty
- NIO最底层与操作系统是如何交互的？ 最底层 ！ 或者是AIO 最底层是与操作系统交互的？？
- [IBM-NIO](https://www.ibm.com/developerworks/cn/education/java/j-nio/j-nio.html)
- [NIO-1](https://juejin.im/entry/58e116f1da2f60005fd09881)
- Netty 框架模块. NIO ？[Netty-1](http://blog.csdn.net/linxcool/article/details/7771952)
###### Netty长链接和短链接 ：
基本思路：netty服务端通过一个Map保存所有连接上来的客户端SocketChannel,客户端的Id作为Map的key。每次服务器端如果要向某个客户端发送消息，只需根据ClientId取出对应的SocketChannel,往里面写入message即可。心跳检测通过IdleEvent事件，定时向服务端放送Ping消息，检测SocketChannel是否终断。Netty自带心跳检测功能，IdleStateHandler,客户端在写空闲时主动发起心跳请求，服务器接受到心跳请求后给出一个心跳响应。当客户端在一定时间范围内不能够给出响应则断开链接。
 心跳 机制. 心跳机制的工作原理是: 在服务器和客户端之间一定时间内没有数据交互时, 即处于 idle 状态时, 客户端或服务器会发送一个特殊的数据包给对方, 当接收方收到这个数据报文后, 也立即发送一个特殊的数据报文, 回应发送方, 此即一个 PING-PONG 交互. 自然地, 当某一端收到心跳消息后, 就知道了对方仍然在线, 这就确保 TCP 连接的有效性.
在 Netty 中, 实现心跳机制的关键是 IdleStateHandler,
1. 使用 Netty 实现心跳机制的关键就是利用 IdleStateHandler 来产生对应的 idle 事件.
2. 一般是客户端负责发送心跳的 PING 消息, 因此客户端注意关注 ALL_IDLE 事件, 在这个事件触发后, 客户端需要向服务器发送 PING 消息, 告诉服务器"我还存活着".
3. 服务器是接收客户端的 PING 消息的, 因此服务器关注的是 READER_IDLE 事件, 并且服务器的 READER_IDLE 间隔需要比客户端的 ALL_IDLE 事件间隔大(例如客户端ALL_IDLE 是5s 没有读写时触发, 因此服务器的 READER_IDLE 可以设置为10s)
4. 当服务器收到客户端的 PING 消息时, 会发送一个 PONG 消息作为回复. 一个 PING-PONG 消息对就是一个心跳交互.
- [资料]( https://segmentfault.com/a/1190000006931568)
- [资料IO](https://yq.aliyun.com/articles/75397?spm=a2c4e.11153940.blogrightarea75403.22.118338cc05ruap)


##### 线程是如何通信的？ 
`wait()、notify()` 还是阻塞队列？ 还是主内存共享？CSP？Java的线程通信与Gorutine最根本的区别是什么？ [线程通信](http://www.importnew.com/26850.html)
- CountDownLatch 适用于一个线程去等待多个线程的情况。
- 为了实现线程间互相等待这种需求，我们可以利用 CyclicBarrier

- 线程有哪些状态,继承thread,创建多个线程,是分别执行自己的任务。实现runnable，创建多个线程是多个线程对某一共同任务的执行。区别。
    - [Thread](https://michaelygzhang.github.io/java/2016/09/25/Java-Thread.html)



#### 字符串不变性的好处/不变性编程 常量池
- 谈到了不可变类和String，大意就是 他会更倾向于使用不可变类，它能够缓存结果，当你在传参的时候，使用不可变类不需要去考虑谁可能会修改其内部的值，这个问题不存在的。如果使用可变类的话，可能需要每次记得重新拷贝出里面的值，性能会有一定的损失。
- 迫使String类设计成不可变的另一个原因是安全，当你在调用其他方法，比如调用一些系统级操作之前，可能会有一系列校验，如果是可变类的话，可能在你校验过后，其内部的值被改变了，可能引起严重的系统崩溃问题，这是迫使String类设计成不可变类的重要原因。
    
1. 效率高，字符串池可复用节约内存高效
2. 安全性(因为字符串是不可变的，所以它的值是不可改变的，否则黑客们可以钻到空子，改变字符串指向的对象的值，造成安全漏洞。)
3. 因为字符串是不可变的，所以是多线程安全的，同一个字符串实例可以被多个线程共享。这样便不用因为线程安全问题而使用同步。字符串自己便是线程安全的。
4. hashcode在字符串生成时就计算好了比如作为map的key值更高效
5. 因为字符串是不可变的，所以在它创建的时候hashcode就被缓存了，不需要重新计算。这就使得字符串很适合作为Map中的键，字符串的处理速度要快过其它的键对象。这就是HashMap中的键往往都使用字符串。

- 异常处理，主要在异常时最后关闭回收资源，定期分析异常日志找到问题处理问题，具体明确是那类异常提早抛出延迟捕获？

###### HttpClient
- HttpClient 连接池实现？连接池原理，设计时的注意事项？连接池中连接都是在发起请求的时候建立，并且都是长连接
    1. 降低延迟：如果不采用连接池，每次连接发起Http请求的时候都会重新建立TCP连接(经历3次握手)，用完就会关闭连接(4次挥手)，如果采用连接池则减少了这部分时间损耗，别小看这几次握手，本人经过测试发现，基本上3倍的时间延迟
    2. 支持更大的并发：如果不采用连接池，每次连接都会打开一个端口，在大并发的情况下系统的端口资源很快就会被用完，导致无法建立新的连接
- 连接池中连接都是在发起请求的时候建立，并且都是长连接;
- 连接池内的连接数其实就是可以同时创建多少个 tcp 连接，httpClient 维护着两个 Set，leased(被占用的连接集合) 和 avaliabled(可用的连接集合) 两个集合，释放连接就是将被占用连接放到可用连接里面。
###### 异步的httpclient？使用场景？


- 多线程与并发编程:
  进程: 一个计算机的运行实例，有自己独立的地址空间，包含程序内容和数据，不同进程间相互隔离，拥有各自的各种资源和状态信息，包括打开的文件，子进程和信号处理等。
  线程: 程序的执行流程，CPU调度的基本单位，线程拥有自己的程序计数器，寄存器，栈帧，同一进程中的线程拥有相同的地址空间，同时共享进程中的各种资源
- excutorServer接口，继承自executor；提供了对任务的管理：submit()，可以吧Callable和Runnable作为任务提交，得到一个Future作为返回，可以获取任务结果或取消任务。
  提供批量执行：invokeAll()和invokeAny()，同时提交多个Callable；invokeAll()，会等待所有任务都执行完成，返回一个包含每个任务对应Future的列表；
  invokeAny()，任何一个任务成功完成，即返回该任务结果。超过时限后，任何尚未完成的任务都会被取消。
 - 多线程开发中应该优先使用高层API，如果无法满足，使用java.util.concurrent.atomic和java.util.concurrent.locks包提供的中层API，
  而synchronized和volatile，以及wait,notify和notifyAll等低层API 应该最后考虑。


#### 框架
- springmvc,boot，mybatis框架
- tomcat与spring容器关联的点？ web.xml?
- spring容器启动原理？ [资料](http://www.majunwei.com/view/201708231840127244.html)
- Spring AOP两种实现方式？
- SprintBoot与SpringMVC的区别?


#### JVM
###### JVM 类加载的整个过程
- [资料](https://segmentfault.com/a/1190000002579346)

```html
加载-> 验证 -> 准备 -> 解析 -> 初始化 -> 使用 - > 卸载
双亲委派 -> 验证:文件格式/魔术开头.. -> 准备: 为类的静态变量分配内存，并将其`初始化为默认值`
 -> 解析: 把类中的符号引用转换为直接引用 -> 初始化: 为类的静态变量`赋予正确的初始值`
验证，准备阶段，静态变量初始化，解析，符合引用变直接引用。
初始化，双亲委派机制，主动被动引用
，使用，卸载。
```

- heap, java stack, native method stack, PC register, method area; [资料](http://www.cnblogs.com/leesf456/p/5055697.html)

###### ClassLoader?比如根ClassLoader？JVM级别的ClassLoader？系统扩展级别的ClassLoader？要非常具体和详细的描述？
- Bootstrap class loader(负责加载虚拟机的核心类库，如 java.lang.* ,JAVA_HOME\lib 目录中的，或通过-Xbootclasspath参数指定路径中的，且被虚拟机认可（按文件名识别，如rt.jar）的类。)C/C++编写 
-> Extension class loader:这个加载器加载出了基本 API 之外的一些拓展类,JAVA_HOME\lib\ext 目录中的，或通过java.ext.dirs系统变量指定路径中的类库。
-> AppClass Loader: 应用/程序自定义类加载器,负责加载用户路径（classpath）上的类库。
- 双亲委派机制: 系统类防止内存中出现多份同样的字节码; 保证Java程序安全稳定运行;

###### Class.forName()和ClassLoader.loadClass()区别
- Class.forName()：将类的.class文件加载到jvm中之外，还会对类进行解释，执行类中的static块；
- ClassLoader.loadClass()：只干一件事情，就是将.class文件加载到jvm中，不会执行static中的内容,只有在newInstance才会去执行static块。
- Class.forName(name, initialize, loader)带参函数也可控制是否加载static块。并且只有调用了newInstance()方法采用调用构造函数，创建类的对象 。

###### ClassNotFoundException 与 NoClassDeFoundError 的区别
- [资料-1](http://blog.csdn.net/bryantlmm/article/details/78118763)
- [资料-2](https://www.cnblogs.com/hnucdj/p/4288369.html)

###### 问题排除 jvm内存溢出？CPU100%？堆内存溢出？栈异常死锁？涉及哪些Linux命令？机器负载高，怎么办，用那些命令可以解决。
- [资料](http://masutangu.com/2017/02/linux-performance-monitor/)

###### g1垃圾为啥时间可控的？
- [资料](http://www.cnblogs.com/wxw7blog/p/7221725.html)
- [资料-2](http://zhaoyanblog.com/archives/397.html)
- 可以有计划地避免在Java堆的进行全区域的垃圾收集；G1跟踪各个Region获得其收集价值大小，在后台维护一个优先列表；
每次根据允许的收集时间，优先回收价值最大的Region（名称Garbage-First的由来）；这就保证了在有限的时间内可以获取尽可能高的收集效率；
###### GC算法？JVM优化手段？常见的优化场景？
- [资料-Java优化](https://michaelygzhang.github.io/java/2018/02/09/java-%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96.html)

###### Tomcat/Netty Server相关
- TODO


#### 中间件
###### Redis VS Memcached 优缺点？ 如何选型？
- [redisVSMemcached](https://michaelygzhang.github.io/destributed/2018/01/26/redis-memcached.html)
###### redis高效点？redis数据结构？Redis为什么高效,原理是什么，为什么使用跳表结构存储？持久化实现方式？
- [redis源码](https://github.com/menwengit/redis_source_annotation)
###### 分布式锁都用哪些？ Memcached ? Redis ? Zookeeper?  
###### 优缺点是什么？什么场景下用那种，还有底层内部实现是什么？ 具体实现锁调用的API是什么？
###### Google Protocol Buffer 高性能原因？ 
- [资料-protobuf-1](https://www.ibm.com/developerworks/cn/linux/l-cn-gpb/index.html)
- [资料-protobuf-2](http://masutangu.com/2016/09/talk-about-protobuf/)
- [资料-protobuf-3](https://yq.aliyun.com/wenji/article_2594-page_3)



###### zookeeper节点类型，选主机制? 主从怎么做？有何问题？
- [资料](https://michaelygzhang.github.io/destributed/2017/01/18/paxos-to-zookeeper.html)
###### mq如何保证幂等
- a,mq,落地db,b。a生成一个业务相关全局唯一biz_id,a发给mq,mq落地db,返回给a说成功了，若失败a重试,mq生成内部一个唯一msg_id业务无关的,这样保证b接受的幂等,会有定时删除重复的数据。b接受消息时，根据a生成的id,判断以此保证b幂等，mq重复策略，可以是1s,3s,5s重复发送机制。
###### 环行队列实现延迟消息，可以很好避免定时任务的扫库的效率低的问题? RingBuffer?

- [资料-cache](https://timyang.net/data/cache-failure/)

#### DB
###### mysql的存储数据结构，b树与b+数的区别，mysql是否indexia索引？有哪些索引方式？
###### 大数据量如何做分布式存储？分库分表？如何分怎么设计？还是利用HDFS？
###### mysql优化？MySQL数据存储？MySQL数据结构存储方式以及读写锁？
###### 分库分表查询，业务拼装，多线程查询，热点数据放一起，冗余数据，防止攻击接口幂等，分库分表事务？
###### 比如找第200页数据每页5条，三个库，怎么查？如果查询维度很多该怎么办?

```html
1 order by time offset x limit y 改写为offset 0 limit x+y 内存中排序，少可以多性能差
2 禁止跳页，只能顺序翻页，记录maxtime, order by time where time
> maxtime, limit y 每次只返回一页数据
3 二次查询法
offset x\n limit y ,n 数据个数,
找到mintime,order by time betwwen mintime and maxtime,第一次取出的，设置虚拟mintime,找到全局offset,因为本来就按时间排序，得到全局offset,
```

###### DB事务隔离级别？ 
- [DB-事务](https://michaelygzhang.github.io/db/2016/09/25/mysql-transaction.html)

```sql
悲观锁：
悲观锁的实现，往往依靠数据库提供的锁机制（也只有数据库层提供的锁机制才能真正保证数据访问的排他性，否则，即使在本系统中实现了加锁机制，也无法保证外部系 
统不会修改数据）。例如： 
select * from table_name where id = ‘xxx’ for update; 
这样查询出来的这一行数据就被锁定了,在这个update事务提交之前其他外界是不能修改这条数据的，但是这种处理方式效率比较低，一般不推荐使用。
```
###### Mysql 乐观锁，共享锁，悲观锁，排他锁？



#### 分布式服务架构设计
###### 设计一个RPC框架需要关注哪些？ 比如像Dubbo？
- [资料-DongFangHongRpc](https://github.com/MichaelYgZhang/DongFangHongRpc)
###### 序列化？都有哪些对象的序列化方式以及优缺点是什么？ 
###### RPC通信，Netty？ 怎么做通信的？ 
###### 编码器，解码器？ 什么来实现？ 那种更好些？
###### 服务的注册与发现？用什么实现，那种实现方式更好？Zookeeper, Eruk…?
###### 设计一个全局ID生成器，怎么设计？性能/有序性/?
- http://vesta.cloudate.net/vesta/doc/%E7%BB%9F%E4%B8%80%E5%8F%91%E5%8F%B7%E5%99%A8(Vesta)%20-%20%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1.html
###### 接口幂等事如何实现的？

```java
幂等：
Bool  withdraw(account_id, amount)
 ——>
 int create_ticket(); //创建唯一id  
bool idempotent_withdraw(ticket_id, account_id, amount);
幂等设计：服务端确保生成唯一标识符。
```
- [API接口设计安全性](http://www.jianshu.com/p/c6518a8f4040)


###### 怎样理解微服务？
###### 设计时考虑如果当前业务出现错误如何更好恢复？自动恢复能力？


#### 如何做到系统高可用？
###### 服务降级，容错，号码运营商降级，服务本身降级，如果所有运营商都出现问题，反真实号码，imc出现问题，走本地缓存，最后是服务恢复。
###### 隔离，幂等，异步，超时，服务降级？
- 高可用服务，请求限流器表每分钟每个用户的请求量，并发请求限流器，抛弃非关键api,处理关键api机制，
  令牌算法，注意可随时调控。限流器不应该影响到正常的业务，被限流的请求注意文案，可开启或关闭限流器。
###### 重试时注意重试次数？并发量与QPS之间的关联关系？



#### 分布式事务
###### 2PC，3PC，阿里的TCC？是否还有？核心思想如何实现的？分布式事务中的关键点有哪些？ 
###### 2PC，3PC，TCC分别都有哪些优缺点？ 底层如何实现？看源码？ 是否还有更优秀的分布式事务框架？
###### 数据一致性问题？分布式注意的点，prosx原理？raft？Paxos原理，2PC，3PC原理
- [资料](http://www.infoq.com/cn/articles/solution-of-distributed-system-transaction-consistency)
###### 分布式系统的思想
- [资料](https://coolshell.cn/articles/10910.html)


#### 服务容器化
###### Docker底层框架架构？ 



#### CS
###### TODO 复习数据结构
###### B树与B+树区别？
###### 跳表?




#### 其他
###### 开源代码阅读过哪些框架，Spring是否阅读过？JDK核心的有哪些比较了解？
###### 想问的问题？
###### 你有哪些优点？有哪些缺点？ 有哪些这次面试过程中没表现出来的？
###### 对公司是否有些诉求？比如期待未来进入什么样的团队？
###### 优化题: 
```js
规则:
1, A,B,C
2, C,D
3, E,F
....

输入: ACD -> true; ACEF -> true; 任意命中一个规则返回true/false;
TODO
```



#### 算法
- 一致性hash算法? 
-  [算法-1](http://www.cnblogs.com/gxbk629/p/3587562.html)
- [算法-2](http://www.jfox.info/459.html)
- [算法-3](http://www.cnblogs.com/lan-writenbook/p/5487265.html)
- [算法-4](http://blog.csdn.net/u012403290/article/details/73845263)
- [算法-5](https://www.cnblogs.com/fanling999/p/7810558.html)
- [算法-6](https://www.cnblogs.com/wxisme/p/5243631.html)
- [算法-7](http://www.jfox.info/java-classical-algorithm-interview-40-questions-and-answer.html)
- [算法-8](http://blog.csdn.net/star535X/article/details/50936919)
- [算法-9](http://blog.csdn.net/DUANJIEFEI/article/details/46461049)
- [算法-0](http://blog.csdn.net/zyx520ytt/article/details/72466255)

#### 笔试题

- 请用jdk7实现以下shell脚本的功能, 注意异常处理及输出格式(alibaba)

```jshelllanguage
cat /home/admin/logs/webx.log | grep "login" | awk '{print $6}' | sort | uniq -c | sort -k 2r
  ------------------
   902 www.taobao.com
    20 s.taobao.com
     9 i.taobao.com
```

- 二分查找(dd)

```java
// 二分查找递归实现   
    public static int binSearch(int srcArray[], int start, int end, int key) {   
        int mid = (end - start) / 2 + start;   
        if (srcArray[mid] == key) {   
            return mid;   
        }   
         if (start >= end) {   
             return -1;   
         } else if (key > srcArray[mid]) {   
             return binSearch(srcArray, mid + 1, end, key);   
         } else if (key < srcArray[mid]) {   
             return binSearch(srcArray, start, mid - 1, key);   
         }   
         return -1;   
    } 

// 二分查找普通循环实现   
// Like public version, but without range checks.
    private static int binarySearch0(int[] a, int fromIndex, int toIndex, int key) {
        int low = fromIndex;
        int high = toIndex - 1;

        while (low <= high) {
            int mid = (low + high) >>> 1;
            int midVal = a[mid];
            if (midVal < key)
                low = mid + 1;
            else if (midVal > key)
                high = mid - 1;
            else
                return mid; // key found
        }
        return -(low + 1);  // key not found.
    }
        
```

- 写一个死锁的例子。
- 实现令牌限流/ 另一种方式限流{漏桶,令牌桶算法(Guava中的Ratelimiter来实现控制速率),信号量(Semaphore)};
- wait/notify 实现生产者/消费之模式
- Linux命令查询, 比如 nginx日志，过滤 xxx.do请求的前十名的IP倒序排列

```js
统计xx.log某字符串出现前10名输出到testfile中
sdate=2017-09-20 23:59:32&txt=com.ford.fordmobile&client_id=x
切割后:
sdate=2017-09-20 23:59:32&
com.ford.fordmobile
_id=x
```

###### cat xx.log.2017-09-20 | awk -F '(txt=|&client)' '{print $2}'| sort | uniq -c | sort -nr| head -10 > testfile


#### 其他资料
- [Java面试极客学院](http://wiki.jikexueyuan.com/project/java-interview-bible/basic-concept.html)
- [资料-1](http://www.bieryun.com/1733.html?spm=a2c4e.11153940.blogcont495584.15.4f1b1491F2IviJ)
- [源码相关-杂](http://www.iocoder.cn/)
- [资料-面试](http://blog.csdn.net/sinat_35512245/article/details/59056120)
- [Google Interview University 一套完整的学习手册帮助自己准备 Google 的面试](https://github.com/jwasham/coding-interview-university/blob/master/translations/README-cn.md)
- [technology-talk](https://github.com/aalansehaiyang/technology-talk)
- [Interview-Notebook](https://github.com/CyC2018/Interview-Notebook)