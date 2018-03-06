---
layout: post
title: Interview-2018
excerpt: Interview-2018
category: Interview
---

- 写在最前面: 问题主要从这几个方面来讲what？how？why？是什么？怎么用说一下使用场景？为什么这么样用？对比其它方案是否有更好的方案？

##### 自我介绍 5min

###### 比如说项目的时候，要说的是项目中技术难点！！！！！！技术难点！！！！！！而不是业务的痛点！！！！

- 项目简介:1. 核心业务流程 2. 技术架构3.技术难点亮点
- 说的越多越好？不一定，先理解好题目，是否还有更好的方案可以代替呢？
- 所做系统的难点？ 如何发现，解决的？ 是否有更好的解决方案 ？是否可以自己想一个难点去说呢？ 
- 简历中的核心点多聊聊关于技术的。系统技术框架是怎么样的？为何采用这种技术方案？ 是否有更好的技术方案？
- 项目技术技术技术难点？ 如何解决的？   
- 动态检测模块？为啥不融合到业务中？
- 做过的事情需要总结成一句话来说，心得！！！！
- 监控告警，有误报率？比如话单量下降20%的告警？节假日如何处理的？ 等等。。可以展开思路多思考。。

##### JavaCore
- final／static？
- ThreadLocal 内存何时情况有可能发生内存泄漏？ 如何解决？答得是remove? 待核实！！threadlocal使用线程局部变量，注意使用后释放？static修饰？
- 线程安全 与 JVM内存模型之间的关系？
- 并发集合容器,线程安全的非线程安全的分别都有哪些?
- NIO最底层与操作系统是如何交互的？ 最底层 ！ 或者是AIO 最底层是与操作系统交互的？？
- 线程是如何通信的？ awrit/notify? 是吗？还是阻塞队列？ 还是主内存共享？CSP？Java的线程通信与Gorutine最根本的区别是什么？
- 同步锁
- 线程有哪些状态
- 线程池子,每一种线程池子的优缺点,比如fix，cache....
- 分布式的中间件，使用场景，遇到的问题，优缺点
- Redis为什么高效,原理是什么，为什么使用跳表结构存储
- 数据库分表怎么分的，为什么这么分？如果查询维度很多该怎么办
- 总结：多思考什么场景适合用什么技术，以及是否有更好的技术方案。
- aqs，threadlocal,aqs,cas,ThreadLocal，AQS，CAS，
- synchorized两个方法同时被访问，是否等待阻塞方法? synchronized、lock、volatile
    - https://www.jianshu.com/p/2344a3e68ca9
    - http://www.leocook.org/2017/07/16/Java%E5%B9%B6%E5%8F%91(%E5%85%AD)-ReentrantLock-synchronized/
- 线程有哪些状态，线程池子？
- cannable,future,futuretask,runable区别
- 字符串不变性的好处，效率高，字符串池可复用节约内存高效，安全性，多线程安全，hashcode在字符串生成时就计算好了比如作为map的key值更高效
- volitile修饰long,double可以原子性，内存屏障会将所有写的值更新到缓存，顺序性可见性, 否则出现`伪共享缓存`问题。
- 死锁情况，多线程交替执行？
- hashmap,currenyhhashmap,volitile,缓存场景
- 异常处理，主要在异常时最后关闭回收资源，定期分析异常日志找到问题处理问题，具体明确是那类异常提早抛出延迟捕获？
- 继承thread,创建多个线程,是分别执行自己的任务。实现runnable，创建多个线程是多个线程对某一共同任务的执行。区别。
- HttpClient 连接池实现？连接池原理，设计时的注意事项？
- list,map循环,反射API练习，多个while循环,如何跳出,并发练习.
- 多线程与并发编程:
  进程: 一个计算机的运行实例，有自己独立的地址空间，包含程序内容和数据，不同进程间相互隔离，拥有各自的各种资源和状态信息，包括打开的文件，子进程和信号处理等。
  线程: 程序的执行流程，CPU调度的基本单位，线程拥有自己的程序计数器，寄存器，栈帧，同一进程中的线程拥有相同的地址空间，同时共享进程中的各种资源
- excutorServer接口，继承自executor；提供了对任务的管理：submit()，可以吧Callable和Runnable作为任务提交，得到一个Future作为返回，可以获取任务结果或取消任务。
  提供批量执行：invokeAll()和invokeAny()，同时提交多个Callable；invokeAll()，会等待所有任务都执行完成，返回一个包含每个任务对应Future的列表；
  invokeAny()，任何一个任务成功完成，即返回该任务结果。超过时限后，任何尚未完成的任务都会被取消。
 - 多线程开发中应该优先使用高层API，如果无法满足，使用java.util.concurrent.atomic和java.util.concurrent.locks包提供的中层API，
  而synchronized和volatile，以及wait,notify和notifyAll等低层API 应该最后考虑。
- JDK集合框架 https://www.cnblogs.com/jing99/p/7057245.html
- ConcurrentyHashMap  http://www.cnblogs.com/ITtangtang/p/3948786.html
- Netty 框架模块. NIO ？http://blog.csdn.net/linxcool/article/details/7771952
- Netty拆包粘包处理方式？http://blog.csdn.net/sicexpn/article/details/45365041

```html
Netty长链接和短链接 ：
基本思路：netty服务端通过一个Map保存所有连接上来的客户端SocketChannel,客户端的Id作为Map的key。每次服务器端如果要向某个客户端发送消息，只需根据ClientId取出对应的SocketChannel,往里面写入message即可。心跳检测通过IdleEvent事件，定时向服务端放送Ping消息，检测SocketChannel是否终断。Netty自带心跳检测功能，IdleStateHandler,客户端在写空闲时主动发起心跳请求，服务器接受到心跳请求后给出一个心跳响应。当客户端在一定时间范围内不能够给出响应则断开链接。
 心跳 机制. 心跳机制的工作原理是: 在服务器和客户端之间一定时间内没有数据交互时, 即处于 idle 状态时, 客户端或服务器会发送一个特殊的数据包给对方, 当接收方收到这个数据报文后, 也立即发送一个特殊的数据报文, 回应发送方, 此即一个 PING-PONG 交互. 自然地, 当某一端收到心跳消息后, 就知道了对方仍然在线, 这就确保 TCP 连接的有效性.
在 Netty 中, 实现心跳机制的关键是 IdleStateHandler,
1. 使用 Netty 实现心跳机制的关键就是利用 IdleStateHandler 来产生对应的 idle 事件.
2. 一般是客户端负责发送心跳的 PING 消息, 因此客户端注意关注 ALL_IDLE 事件, 在这个事件触发后, 客户端需要向服务器发送 PING 消息, 告诉服务器"我还存活着".
3. 服务器是接收客户端的 PING 消息的, 因此服务器关注的是 READER_IDLE 事件, 并且服务器的 READER_IDLE 间隔需要比客户端的 ALL_IDLE 事件间隔大(例如客户端ALL_IDLE 是5s 没有读写时触发, 因此服务器的 READER_IDLE 可以设置为10s)
4. 当服务器收到客户端的 PING 消息时, 会发送一个 PONG 消息作为回复. 一个 PING-PONG 消息对就是一个心跳交互.
 https://segmentfault.com/a/1190000006931568

```






#### 框架
- springmvc,boot，mybatis框架
- tomcat与spring容器关联的点？ web.xml?
- spring容器启动原理？
- Spring AOP两种实现方式？
- SprintBoot与SpringMVC的区别?





####JVM
###### JVM 类加载的整个过程

```html
jvm,加载，链接，初始化，使用，卸载。
加载，加载class文件
链接，验证，准备阶段，静态变量初始化，解析，符合引用变直接引用。
初始化，双亲委派机制，主动被动引用
，使用，卸载。
```

- 方法区，常量池，堆，栈，计数器，本地方法区。JNI,优化重复使用的代码段。
###### ClassLoader?比如根ClassLoader？JVM级别的ClassLoader？系统扩展级别的ClassLoader？要非常具体和详细的描述？
###### ClassNotFoundException 与 NoClassDeFoundError 的区别
- http://blog.csdn.net/bryantlmm/article/details/78118763
- https://www.cnblogs.com/hnucdj/p/4288369.html
###### 问题排除 jvm内存溢出？CPU100%？堆内存溢出？栈异常死锁？涉及哪些Linux命令？机器负载高，怎么办，用那些命令可以解决。
- http://masutangu.com/2017/02/linux-performance-monitor/
###### g1垃圾为啥时间可控的？






#### 中间件
###### Redis VS Memcached 优缺点？ 如何选型？https://kb.cnblogs.com/page/69074/
###### redis高效点？redis数据结构？跳表？Redis数据结构，持久化实现方式？
###### 分布式锁都用哪些？ Memcached ? Redis ? Zookeeper?  
###### 优缺点是什么？什么场景下用那种，还有底层内部实现是什么？ 具体实现锁调用的API是什么？
###### Google Protocol Buffer 高性能原因？ 
- https://www.ibm.com/developerworks/cn/linux/l-cn-gpb/index.html
- http://masutangu.com/2016/09/talk-about-protobuf/
- https://yq.aliyun.com/wenji/article_2594-page_3
###### 异步的httpclient？使用场景？
###### zookeeper节点类型，选主机制? 主从怎么做？有何问题？
- https://michaelygzhang.github.io/destributed/2017/01/18/paxos-to-zookeeper.html
###### mq如何保证幂等
- a,mq,落地db,b。a生成一个业务相关全局唯一biz_id,a发给mq,mq落地db,返回给a说成功了，若失败a重试,mq生成内部一个唯一msg_id业务无关的,这样保证b接受的幂等,会有定时删除重复的数据。b接受消息时，根据a生成的id,判断以此保证b幂等，mq重复策略，可以是1s,3s,5s重复发送机制。
###### 环行队列实现延迟消息，可以很好避免定时任务的扫库的效率低的问题? RingBuffer?






#### DB
###### mysql的存储数据结构，b树与b+数的区别，mysql是否indexia索引？有哪些索引方式？
###### 大数据量如何做分布式存储？分库分表？如何分怎么设计？还是利用HDFS？
###### mysql优化？MySQL数据存储？MySQL数据结构存储方式以及读写锁？
###### 分库分表查询，业务拼装，多线程查询，热点数据放一起，冗余数据，防止攻击接口幂等，分库分表事务？
###### 比如找第200页数据每页5条，三个库，怎么查？

```html
1 order by time offset x limit y 改写为offset 0 limit x+y 内存中排序，少可以多性能差
2 禁止跳页，只能顺序翻页，记录maxtime, order by time where time
> maxtime, limit y 每次只返回一页数据
3 二次查询法
offset x\n limit y ,n 数据个数,
找到mintime,order by time betwwen mintime and maxtime,第一次取出的，设置虚拟mintime,找到全局offset,因为本来就按时间排序，得到全局offset,
```

###### DB事务隔离级别？ 
- https://michaelygzhang.github.io/db/2016/09/25/mysql-transaction.html

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
- http://www.infoq.com/cn/articles/solution-of-distributed-system-transaction-consistency
###### 分布式系统的思想
- http://blog.hebiace.net/other/428.html#





#### 服务容器化
###### Docker底层框架架构？ 





#### CS
###### B树与B+树区别？
###### 跳表?






#### 其他
###### 开源代码阅读过哪些框架，Spring是否阅读过？JDK核心的有哪些比较了解？
###### 想问的问题？
###### 你有哪些优点？有哪些缺点？ 有哪些这次面试过程中没表现出来的？
###### 对公司是否有些诉求？比如期待未来进入什么样的团队？






#### 算法
- 一致性hash算法? 





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
public static int binSearch(int srcArray[], int key) {   
 int mid = srcArray.length / 2;   
 if (key == srcArray[mid]) {   
     return mid;   
 }   

 int start = 0;   
 int end = srcArray.length - 1;   
 while (start <= end) {   
     mid = (end - start) / 2 + start;   
     if (key < srcArray[mid]) {   
        end = mid - 1;   
     } else if (key > srcArray[mid]) {   
         start = mid + 1;   
     } else {   
         return mid;   
     }   
 }   
 return -1;   
} 
        
```

- 写一个死锁的例子。
- 实现令牌限流/ 另一种方式限流{漏桶,令牌桶算法(Guava中的Ratelimiter来实现控制速率),信号量(Semaphore)};
- wait/notify 实现生产者/消费之模式
- Linux命令查询, 比如 nginx日志，过滤 xxx.do请求的前十名的IP倒序排列

