---
layout: post
title: Interview-2017
excerpt: Interview-2017
category: Interview
---

####  2016-10-12
Java 8种基本数据类型

```js
基本类型 -> 数值类型 -> 整数类型: byte、short、int、long
                   -> 浮点数据类型: float、double
                   -> 字符类型: char  
基本类型 -> boolean

引用类型 -> 引用 -> 类类型
                -> 接口类型
                -> 数组类型

1byte = 8bits
计算机存储为补码，java也是如此，byte = 8bits, short = 16bits, int = 32bits, long = 64bits , char = 16bits, float = 32bits, double = 64bits, boolean = 8bits
java采用Unicode字符编码，所谓字符编码就是用一串二进制数据来表示特定的字符。
数据需要高精度的场景需要采用java.math.BigDecimal

类的成员变量默认值:byte,short,int,long:0; float:0.0f; double:0.0d; char:"\u0000"; boolean:false; 引用类型:null
注意:局部变量JVM不会自动初始化为默认值，所以必须先显式初始化，才能使用。
当类型低于int时，比如char，则会按照int进行计算;比如String s = '1' + '2' + "abc";
s = 99abc;// 1 = 49; 2 = 50;
```

转义字符 |描述|
:-------|:----|
`\n`      |换行符，将光标定位到下一行的开头|
`\t`|垂直制表符，将光标移动到下一个制表符的位置|
`\r`|回车，将光标定位在当前行的开头，不会跳到下一行|
`\\`|代表反斜杠|
`\'`|代表单引号字符|
`\"`|代表双引号|

##### 变量作用域
- 成员变量: 在类中声明，作用域为整个类
- 局部变量: 在一个方法内部或者代码块的内部声明，作用域为方法内或代码块内。
- 方法参数: 作用域为整个方法内部。
- 异常处理参数: 比如catch(Exception e)异常参数e，它的作用域就是紧跟着后面的代码块

*静态变量和实例变量的生命周期*
- 成员变量有两种: 被static修饰的称为静态变量；另一种没有被static修饰的称为实例变量；
静态变量内存中只有一个，JVM加载类的过程中为静态变量分配内存，静态变量位于方法区，被类的所有实例共享，可以直接通过类名访问，它的生命周期取决于类的生命周期。当加载类时，静态变量被创建并分配内存，当卸载类时，静态变量被销毁并撤销所占内存。
- 类的每一个实例都有相应的实例变量，每创建一个类的实例，JVM就会为实例变量分配一次内存，实例变量位于堆区中，它的生命周期取决于类的实例。


- String底层为private final char value[] + 对这个数组的操作
- StringBuilder JDK1.5 非线程安全; StringBuffer JDK1.0 线程安全在每个方法上加了`synchronized`, 它们都继承与 AbstractStringBuilder

[常见排序算法以及jdk集合源码分析](https://michaelygzhang.github.io/home/)

[Oracle-Collection](http://docs.oracle.com/javase/8/docs/technotes/guides/collections/overview.html)

https://en.wikipedia.org/wiki/Java_(programming_language)


#### 锁

- 单数据库, 乐观锁
- memcached的add()
- redis的setnx(), expire(), get(), getset()
- 思考宕机情况如何解决
- 跨表垮裤事务问题
- 分库分表

- RPC？底层？服务注册、获取？
- JVM, jmap, jstat, jps, jstack...
- ConcurrencyHashMap, safe why? AQS, CAS, HashMap


###### 并发指标：

- PV(Page view)PV是指页面的访问次数，每打开或刷新一次页面，就算做一个pv
- 计算模型：
- 每台服务器每秒处理请求的数量=((80%总PV量)/(24小时*60分*60秒*40%)) / 服务器数量 。
其中关键的参数是80%、40%。表示一天中有80%的请求发生在一天的40%的时间内。24小时的40%是9.6小时，有80%的请求发生一天的9.6个小时当中（很适合互联网的应用，白天请求多，晚上请求少）。
- 注意机房的网络带宽
- QPS - Queries Per Second  每秒处理的查询数（如果是数据库，就相当于读取）
- TPS - Transactions Per Second  每秒处理的事务数(如果是数据库，就相当于写入、修改)
- IOPS，每秒磁盘进行的I/O操作次数

- 设计后端接口时，注意思考这样的几个状态：成功、失败、是否幂等、超时、异常、每个状态如何处理、是否做到了请求次数的最少设计。
  1. 接口设计还应该注意几端接入时扩展性，高并发，稳定性问题。
  2. TODO

- 连接池：
  - 优点: 复用避免重复创建销毁，很好的控制资源，稳定系统性能，其核心思想：连接复用。
  - 关键点: 并发问题，数据库连接池设计时考虑多库多用户问题，事务问题。
  - 关键参数: corePoolSize, maximumPoolSize, keepAliveTime, workQueue阻塞队列; worker, job
    - 核心处理:
      1. works数量低于corePoolSize则创建一个worker处理job
      2. works高于corePoolSize则将job放入待处理队列，若成功则结束。
      3. 若2放入队列失败，则再次检查works是否还是处于高于corePoolSize，如果是小于则创建一个worker处理job
      4. 拒绝处理。

- ThreadLocal：该类提供了线程局部 (thread-local) 变量。这些变量不同于它们的普通对应物，因为访问某个变量（通过其 get 或 set 方法）的每个线程都有自己的局部变量，它独立于变量的`初始化副本`。ThreadLocal 实例通常是类中的 private static 字段，它们希望将状态与某一个线程（例如，用户 ID 或事务 ID）相关联。

- 分布式最终一致性方案:
  - 基于消息队列+定时补偿机制
  - 引入异步回调机制，通知机制
  - TODO

- 用户权限相关做法：
  -  以用户菜单为例，不同角色的用户拥有不同的菜单权限。
  1. 菜单表: id, topid,menu_name,link,status ;编号key,菜单的上一级就是说这里只支持2级菜单，菜单对应的请求路径，状态
  2. 角色表:id,role_name,create_time ;编号key,角色名称比如超期管理员，管理员，经理，员工等,创建时间
  3. 角色菜单表,意思就是那个角色分配哪些菜单,以id关联，字段为:id,role_id,menu_id    ;编号key,角色编号,菜单编号  
  4. 用户表: id,account,pwd,name,sex,status,roles,create_time ;编号key,账号,密码,姓名,性别,状态,
  - 所属角色[1];[1,2]比如可能只有一个角色，也可能有多个角色
- 总结:当一个用户登录时，先在用户表中获得所属角色，然后根据所属角色在角色菜单表中获得相应的菜单，然后再去菜单表中得到需要展现的数据。

- 修改代码时要先取理解原有代码的含义，以及设计的目的，如果不明白，要及时了解沟通，不要随意修改他人代码。
- 编写模块前一定先搞清模块的业务，然后多思考，设计合适的方案，最后才是写代码。
