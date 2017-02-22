---
layout: post
title: JVM Optimize Practice
excerpt: JVM Optimize Practice
category: Java
---

- JVM堆内存的分代: 虚拟机的堆内存共划分为三个代：年轻代（Young Generation）、年老代（Old Generation）和持久代（Permanent Generation）。其中持久代主要存放的是Java类的类信息，与垃圾收集器要收集的Java对象关系不大。所以，年轻代和年老代的划分才是对垃圾 收集影响比较大的。
- 年轻代: 所有新生成的对象首先都是放在年轻代的。年轻代的目标就是尽可能快速的收集掉那些生命周期短的对象。年轻代分三个区。一个Eden区，两个 Survivor区(一般而言)。大部分对象在Eden区中生成。当Eden区满时，还存活的对象将被复制到Survivor区（两个中的一个），当一个Survivor区满 时，此区的存活对象将被复制到另外一个Survivor区，当另一个Survivor区也满了的时候，从前一个Survivor区复制过来的并且此时还存 活的对象，将被复制“年老区”。需要注意，两个Survivor区是对称的，没先后关系，所以同一个Survivor区中可能同时存在从Eden区复制过来对象，和从另一个Survivor区复制过来的对象；而复制到年老区的只有从前一个Survivor区（相对的）过来的对象。而且，Survivor区总有一个是空的。特殊的情况下，根据程序需要，Survivor区是可以配置为多个的（多于两个），这样可以增加对象在年轻代中的存在时间，减少被放到年老代的可能。
- 年老代: 在年轻代中经历了N（可配置-XX:MaxTenuringThreshold）次垃圾回收后仍然存活的对象，就会被放到年老代中。因此，可以认为年老代中存放的都是一些生命周期较长的对象。
- 持久代: 用于存放静态数据，如 Java Class, Method 等。持久代对垃圾回收没有显著影响，但是有些应用可能动态生成或者调用一些Class，例如 Hibernate 等，在这种时候需要设置一个比较大的持久代空间来存放这些运行过程中动态增加的类型。持久代大小通过 -XX:MaxPermSize进行设置。

##### 常用命令

###### jps(Java Virtual Machine Process Status Tool)jps主要用来输出JVM中运行的进程状态信息

```js
jps [options] [hostid]
-q 不输出类名、Jar名和传入main方法的参数
-m 输出传入main方法的参数
-l 输出main类或Jar的全限名
-v 输出传入JVM的参数
```

###### jstack  如果是在64位机器上，需要指定选项"-J-d64"， 输出 jvm自身线程、用户线程等

```js
jstack [ option ] pid
jstack [ option ] executable core
jstack [ option ] [server-id@]remote-hostname-or-IP
-F当jstack [-l] pid没有相应的时候强制打印栈信息
-l 长列表. 打印关于锁的附加信息,例如属于java.util.concurrent的ownable synchronizers列表.
-m 打印java和native c/c++框架的所有栈信息.
-h | -help打印帮助信息
pid 需要被打印配置信息的java进程id,可以用jps查询.
-线程状态
死锁，Deadlock（重点关注）
等待资源，Waiting on condition（重点关注）
等待获取监视器，Waiting on monitor entry（重点关注）
阻塞，Blocked（重点关注）
执行中，Runnable
暂停，Suspended
对象等待中，Object.wait() 或 TIMED_WAITING
停止，Parked
```

###### jmap 查看内存

```js
jmap [option] pid
jmap [option] executable core
jmap [option] [server-id@]remote-hostname-or-IP
-dump:[live]format=b,file=<filename> 使用hprof二进制形式,输出jvm的heap内容到文件，假如指定live选项,那么只输出活的对象到文件.
-finalizerinfo 打印正等候回收的对象的信息.
-heap 打印heap的概要信息，GC使用的算法，heap的配置及wise heap的使用情况.
-histo[:live] 打印每个class的实例数目,内存占用,类全名信息. 如果live子参数加上后,只统计活的对象数量.
-permstat 打印classload和jvm heap持久层的信息. 包含每个classloader的名字,活泼性,地址,父classloader和加载的class数量. 另外,内部String的数量和占用内存数也会打印出来.
-h | -help 打印辅助信息
-J 传递参数给jmap启动的jvm.
pid 需要被打印配相信息的java进程id,可以用jps查看

jmap -histo pid  每个class的实例数目,内存占用,类全名信息
jmap -histo 4939 > a.txt
jmap -dump:format=b,file=fileName pid
```

###### jstat 性能分析

```js
jstat [option] [pid]
-class	用于查看类加载情况的统计
-compiler	用于查看HotSpot中即时编译器编译情况的统计
-gc	用于查看JVM中堆的垃圾收集情况的统计
-gccapacity	用于查看新生代、老生代及持久代的存储容量情况
-gccause	用于查看垃圾收集的统计情况（这个和-gcutil选项一样），如果有发生垃圾收集，它还会显示最后一次及当前正在发生垃圾收集的原因。
-gcnew	用于查看新生代垃圾收集的情况
-gcnewcapacity	用于查看新生代的存储容量情况
-gcold	用于查看老生代及持久代发生GC的情况
-gcoldcapacity	用于查看老生代的容量
-gcpermcapacity	用于查看持久代的容量
-gcutil	用于查看新生代、老生代及持代垃圾收集的情况
-printcompilation	HotSpot编译方法的统计

jstat -gcutil [pid]
-gcutil  新生代、老生代及持代垃圾收集的情况

列名	说明
S0	Heap上的 Survivor space 0 区已使用空间的百分比
S1	Heap上的 Survivor space 1 区已使用空间的百分比
E	Heap上的 Eden space 区已使用空间的百分比
O	Heap上的 Old space 区已使用空间的百分比
P	Perm space 区已使用空间的百分比
YGC	从应用程序启动到采样时发生 Young GC 的次数
YGCT	从应用程序启动到采样时 Young GC 所用的时间(单位秒)
FGC	从应用程序启动到采样时发生 Full GC 的次数
FGCT	从应用程序启动到采样时 Full GC 所用的时间(单位秒)
GCT	从应用程序启动到采样时用于垃圾回收的总时间(单位秒)，它的值等于YGC+FGC
```

###### 堆内存 = 年轻代 + 年老代 + 永久代     年轻代 = Eden区 + 2Sourvivor区(From/To)

##### JVM 参数设置

###### 堆设置

```js
-Xmx3550m：设置JVM最大堆内存为3550M。
-Xms3550m：设置JVM初始堆内存为3550M。此值可以设置与-Xmx相同，以避免每次垃圾回收完成后JVM重新分配内存。
-Xss128k： 设置每个线程的栈大小。JDK5.以后每个线程栈大小为1M，之前每个线程栈大小为256K。
        应当根据应用的线程所需内存大小进行调整。在相同物理内存下，减小这个值能生成更多的线程。
        但是操作系统对一个进程内的线程数还是有限制的，不能无限生成，经验值在 3000~5000 左右。
-Xmn2g：设置堆内存年轻代大小为2G。整个堆内存大小 = 年轻代大小 + 年老代大小 + 持久代大小 。
        持久代一般固定大小为64m，所以增大年轻代后，将会减小年老代大小。此值对系统性能影响较大，Sun官方推荐配置为整个堆的3/8。
-XX:PermSize=256M：设置堆内存持久代 初始值为256M。(貌似是Eclipse等IDE的初始化参数)
-XX:MaxNewSize=size：新生成的对象能占用内存的最大值。
-XX:MaxPermSize=512M：设置持久代最大值为512M。
-XX:NewRatio=4：设置堆内存年轻代（包括Eden和两个Survivor区）与堆内存年老代的比值（除去持久代） 。
        设置为4，则年轻代所占与年老代所占的比值为1:4。
-XX:SurvivorRatio=4：设置堆内存年轻代中Eden区与Survivor区大小的比值 。
        设置为4，则两个Survivor区（JVM堆内存年轻代中默认有2个Survivor区）与一个Eden区的比值为2:4，
        一个Survivor区占 整个年轻代的1/6。
-XX:MaxTenuringThreshold=7：表示一个对象如果在救助空间（Survivor区）移动7次还没有被回收就放入年老代。
        如果设置为0的话，则年轻代对象不经过Survivor区，直接进入年老代，对于年老代比较多的应用，这样做可以提高效率。
        如果将此值设置为一个较大值，则年轻代对象会在Survivor区进行多次复制，这样可以增加对象在年轻代存活时间，
        增加对象在年轻代即被回收的概率。
```

##### 回收器选择

###### 串行收集器

-XX:+UseSerialGC：设置串行收集器

###### 并行收集器(吞吐量优先)

```js
-XX:+UseParallelGC：选择垃圾收集器为并行收集器。此配置仅对年轻代有效。即上述配置下，年轻代使用并发收集，而年老代仍旧使用串行收集。
-XX:ParallelGCThreads=20：配置并行收集器的线程数，即：同时多少个线程一起进行垃圾回收。此值最好配置与处理器数目相等。
-XX:+UseParallelOldGC：配置年老代垃圾收集方式为并行收集。JDK6.0支持对年老代并行收集。
-XX:MaxGCPauseMillis=100：设置每次年轻代垃圾回收的最长时间（单位毫秒），如果无法满足此时间，JVM会自动调整年轻代大小，以满足此值。
-XX:+UseAdaptiveSizePolicy：设置此选项后，并行收集器会自动选择年轻代区大小和相应的Survivor区比例，
          以达到目标系统规定的最低响应时间或者收集频率等。此参数建议使用并行收集器时，一直打开。
```

###### 并发收集器(响应时间优先)

```js
-XX:+UseParNewGC：设置年轻代为并发收集。可与CMS收集同时使用。JDK5.0以上，JVM会根据系统配置自行设置，所以无需再设置此值。
          CMS， 全称Concurrent Low Pause Collector，是jdk1.4后期版本开始引入的新gc算法，在jdk5和jdk6中得到了进一步改进，
          它的主要适合场景是对响应时间的重要性需求 大于对吞吐量的要求，能够承受垃圾回收线程和应用线程共享处理器资源，
          并且应用中存在比较多的长生命周期的对象的应用。CMS是用于对tenured generation的回收，也就是年老代的回收，
          目标是尽量减少应用的暂停时间，减少FullGC发生的几率，利用和应用程序线程并发的垃圾回收线程来 标记清除年老代。
-XX:+UseConcMarkSweepGC：设置年老代为并发收集。
          测试中配置这个以后，-XX:NewRatio=4的配置失效了。所以，此时年轻代大小最好用-Xmn设置。
-XX:CMSFullGCsBeforeCompaction=：由于并发收集器不对内存空间进行压缩、整理，
          所以运行一段时间以后会产生“碎片”，使得运行效率降低。此参数设置运行次FullGC以后对内存空间进行压缩、整理。
-XX:+UseCMSCompactAtFullCollection：打开对年老代的压缩。可能会影响性能，但是可以消除内存碎片。
-XX:+CMSIncrementalMode：设置为增量收集模式。一般适用于单CPU情况。
-XX:CMSInitiatingOccupancyFraction=70：表示年老代空间到70%时就开始执行CMS，确保年老代有足够的空间接纳来自年轻代的对象。
注：如果使用 throughput collector 和 concurrent low pause collector 这两种垃圾收集器，需要适当的挺高内存大小，为多线程做准备。

其它
-XX:+ScavengeBeforeFullGC：新生代GC优先于Full GC执行。
-XX:-DisableExplicitGC：禁止调用System.gc()，但JVM的gc仍然有效。
-XX:+MaxFDLimit：最大化文件描述符的数量限制。
-XX:+UseThreadPriorities：启用本地线程优先级API，即使 java.lang.Thread.setPriority() 生效，反之无效。
-XX:SoftRefLRUPolicyMSPerMB=0：“软引用”的对象在最后一次被访问后能存活0毫秒（默认为1秒）。
-XX:TargetSurvivorRatio=90：允许90%的Survivor空间被占用（默认为50%）。提高对于Survivor的使用率——超过就会尝试垃圾回收。
```

###### 辅助信息

```js
-XX:-CITime：打印消耗在JIT编译的时间
-XX:ErrorFile=./hs_err_pid.log：保存错误日志或者数据到指定文件中
-XX:-ExtendedDTraceProbes：开启solaris特有的dtrace探针
-XX:HeapDumpPath=./java_pid.hprof：指定导出堆信息时的路径或文件名
-XX:-HeapDumpOnOutOfMemoryError：当首次遭遇内存溢出时导出此时堆中相关信息
-XX:OnError=";"：出现致命ERROR之后运行自定义命令
-XX:OnOutOfMemoryError=";"：当首次遭遇内存溢出时执行自定义命令
-XX:-PrintClassHistogram：遇到Ctrl-Break后打印类实例的柱状信息，与jmap -histo功能相同
-XX:-PrintConcurrentLocks：遇到Ctrl-Break后打印并发锁的相关信息，与jstack -l功能相同
-XX:-PrintCommandLineFlags：打印在命令行中出现过的标记
-XX:-PrintCompilation：当一个方法被编译时打印相关信息
-XX:-PrintGC：每次GC时打印相关信息
-XX:-PrintGC Details：每次GC时打印详细信息
-XX:-PrintGCTimeStamps：打印每次GC的时间戳
-XX:-TraceClassLoading：跟踪类的加载信息
-XX:-TraceClassLoadingPreorder：跟踪被引用到的所有类的加载信息
-XX:-TraceClassResolution：跟踪常量池
-XX:-TraceClassUnloading：跟踪类的卸载信息
-XX:-TraceLoaderConstraints：跟踪类加载器约束的相关信息
```

###### JVM服务调优实战

```js
服务器：8 cup, 8G mem
java -Xmx3550m -Xms3550m -Xss128k -XX:NewRatio=4 -XX:SurvivorRatio=4 -XX:MaxPermSize=16m -XX:MaxTenuringThreshold=0
调优方案：
-Xmx5g：设置JVM最大可用内存为5G。
-Xms5g：设置JVM初始内存为5G。此值可以设置与-Xmx相同，以避免每次垃圾回收完成后JVM重新分配内存。
-Xmn2g：设置年轻代大小为2G。整个堆内存大小 = 年轻代大小 + 年老代大小 + 持久代大小 。持久代一般固定大小为64m，
        所以增大年轻代后，将会减小年老代大小。此值对系统性能影响较大，Sun官方推荐配置为整个堆的3/8。
-XX:+UseParNewGC：设置年轻代为并行收集。可与CMS收集同时使用。JDK5.0以上，JVM会根据系统配置自行设置，所以无需再设置此值。
-XX:ParallelGCThreads=8：配置并行收集器的线程数，即：同时多少个线程一起进行垃圾回收。此值最好配置与处理器数目相等。
-XX:SurvivorRatio=6：设置年轻代中Eden区与Survivor区的大小比值。根据经验设置为6，则两个Survivor区与一个Eden区的比值为2:6，
        一个Survivor区占整个年轻代的1/8。
-XX:MaxTenuringThreshold=30： 设置垃圾最大年龄（次数）。如果设置为0的话，则年轻代对象不经过Survivor区直接进入年老代。
        对于年老代比较多的应用，可以提高效率。如果将此值 设置为一个较大值，则年轻代对象会在Survivor区进行多次复制，
        这样可以增加对象再年轻代的存活时间，增加在年轻代即被回收的概率。设置为30表示
        一个对象如果在Survivor空间移动30次还没有被回收就放入年老代
-XX:+UseConcMarkSweepGC：设置年老代为并发收集。测试配置这个参数以后，参数-XX:NewRatio=4就失效了，
        所以，此时年轻代大小最好用-Xmn设置，因此这个参数不建议使用。
```

###### 堆溢时会将堆栈信息输出到文件中的配置

- -XX:+HeapDumpOnOutOfMemoryError-XX:HeapDumpPath=/path/to/heap/dump
