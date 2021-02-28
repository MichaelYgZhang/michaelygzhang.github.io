---
layout: post
title: 面试总结2021
excerpt: 面试总结2021
category: Interview
---


* TOC
{:toc}


---

# ChangeLog

|版本 | 备注|
|:-|:-|
|1.0.0|2021-02-15第一个版本，系统化总结面试相关内容，完成大纲|

---

# 面试总结
> 总结内容包括如下几个方面

- [ ] 计算机基础部分
    - [ ] TCP/IP
    - [ ] HTTP
-  [ ] Java
    - [ ] JDK
    - [ ] 多线程
-  [ ] Java框架
    - [ ] Spring
    - [ ] Mybatis
- [ ] 中间件
    - [ ] Zookeeper
    - [ ] Eureka
    - [ ] Nacos
    - [ ] Etcd
    - [ ] kafka
    - [ ] Elasticsearch
- [ ] 存储
    - [ ] MySQL
    - [ ] Redis
    - [ ] HDFS
    - [ ] HBase
    - [ ] 分库分表
- [ ] 分布式架构相关
    - [ ] 2PC, 3PC, TCC
    - [ ] 分布式相关算法
        - [ ] Raft
        - [ ] Paxos
- [ ] 服务设计和服务治理相关
    - [ ] 分布式事务
    - [ ] 幂等问题以及解决方案
    - [ ] 唯一id问题
    - [ ] 熔断
    - [ ] 限流
    - [ ] 服务监控告警
- [ ] 算法相关
- [ ] 工程能力
    - [ ] 代码质量
    - [ ] maven, jar包加载顺序, jar包排包问题
- [ ] 问题排查方面
    - [ ] CPU负载问题
    - [ ] 内存泄漏问题
- [ ] 项目总结
    - [ ] 架构图，分析架构设计原因
    - [ ] 遇到的问题和挑战，如何进行处理和解决的？最后进行总结提炼心得体会或者方法伦？SOP
    - [ ] 系统是否还有什么问题未处理和解决？



# 计算机基础部分

## TCP/IP

## HTTP

# Java

## 面向对象设计
- 封装
- 继承
- 多态
    - 重写（override）和重载（overload）、向上转型。简单说，重写是父子类中相同名字和参数的方法，不同的实现；重载则是相同名字的方法，但是不同的参数，本质上这些方法签名是不一样的
- SOLID
    - 单一职责Single Responsibility
    - 开关原则Open-Close Open for extension Close for modification
    - 里氏替换Liskov Subsitution，进行继承关系抽象时，凡是可以用父类或者基类的地方，都可以用子类替换。
    - 接口分离Interface Segregation
    - 依赖反转Dependency Inversion，实体应该依赖于抽象而不是实现，高层次模块不应该依赖于低层次模块，而应该基于抽象。

## JDK

### Java基础部分
- equals vs ==
    - == 
        1. 用于基本数据类型比较的是值，基础类型（byte, short, int, long, float, double, char,boolean）
        2. 用于包装类型（引用类）比较的是对象内存地址
    - equals
        1. equals方法如果没有重写，比较的是对象内存地址
        2. equals方法如果重写，则根据重写内容进行比较
            - String：重写了equals方法，比较的是内容
    - 扩展：
        - 注意一个基本的原则：重写equals()方法同时需要重写hashcode()方法。
            - 两个对象equals方法相同则hashcode方法一定相同，反之hashcode相同可能为hash冲突equlas方法不一定相同。
            - 如何重写equals？如何重写hashcode？hashcode重写通常质数（31 * 对象的filed hashcode）

        ```java
        @Override
        public boolean equals(Object obj) {
            if(this == obj){
                //地址相等
                return true;
            }

            if(obj == null){
                //非空性：对于任意非空引用x，x.equals(null)应该返回false。
                return false;
            }

            if (getClass() != obj.getClass()) {
                //不是相同的对象
                return false;
            }

            User other = (User) obj;
            //需要比较的字段相等，则这两个对象相等
            return Objects.equals(this.name, other.name) && Objects.equals(this.age, other.age);
        }
        ```

- transient vs serialization vs Externalizable
    - 变量被transient修饰，变量将不再是对象持久化的一部分，该变量内容在序列化后无法获得访问。
    - transient关键字只能修饰变量，而不能修饰方法和类。注意，本地变量是不能被transient关键字修饰的。变量如果是用户自定义类变量，则该类需要实现Serializable接口。
    - 一个静态变量不管是否被transient修饰，均不能被序列化。
    - 对象的序列化可以通过实现两种接口来实现，若实现的是Serializable接口，则所有的序列化将会自动进行，若实现的是Externalizable接口，则没有任何东西可以自动序列化，需要在writeExternal方法中进行手工指定所要序列化的变量，这与是否被transient修饰无关

- 字符串不变性的好处/不变性编程 常量池
    - 谈到了不可变类和String，大意就是 他会更倾向于使用不可变类，它能够缓存结果，当你在传参的时候，使用不可变类不需要去考虑谁可能会修改其内部的值，这个问题不存在的。如果使用可变类的话，可能需要每次记得重新拷贝出里面的值，性能会有一定的损失。
    - 迫使String类设计成不可变的另一个原因是安全，当你在调用其他方法，比如调用一些系统级操作之前，可能会有一系列校验，如果是可变类的话，可能在你校验过后，其内部的值被改变了，可能引起严重的系统崩溃问题，这是迫使String类设计成不可变类的重要原因。
    1. 效率高，字符串池可复用节约内存高效
    2. 安全性(因为字符串是不可变的，所以它的值是不可改变的，否则黑客们可以钻到空子，改变字符串指向的对象的值，造成安全漏洞。)
    3. 因为字符串是不可变的，所以是多线程安全的，同一个字符串实例可以被多个线程共享。这样便不用因为线程安全问题而使用同步。字符串自己便是线程安全的。
    4. hashcode在字符串生成时就计算好了比如作为map的key值更高效
    5. 因为字符串是不可变的，所以在它创建的时候hashcode就被缓存了，不需要重新计算。这就使得字符串很适合作为Map中的键，字符串的处理速度要快过其它的键对象。这就是HashMap中的键往往都使用字符串。

- 异常
    - ![java-exception-error](https://raw.githubusercontent.com/MichaelYgZhang/michaelygzhang.github.io/master/images/java-exception-error.png)
    - Exception VS Error
        - Exception 和 Error 都是继承了 Throwable 类，在 Java 中只有 Throwable 类型的实例才可以被抛出（throw）或者捕获（catch），它是异常处理机制的基本组成类型。
        - Exception 和 Error 体现了 Java 平台设计者对不同异常情况的分类。Exception 是程序正常运行中，可以预料的意外情况，可能并且应该被捕获，进行相应处理。
        - Error 是指在正常情况下，不大可能出现的情况，绝大部分的 Error 都会导致程序（比如 JVM 自身）处于非正常的、不可恢复状态。既然是非正常情况，所以不便于也不需要捕获，常见的比如 OutOfMemoryError 之类，都是 Error 的子类。
        - Exception 又分为可检查（checked）异常和不检查（unchecked）异常，可检查异常在源代码里必须显式地进行捕获处理，这是编译期检查的一部分。前面我介绍的不可查的 Error，是 Throwable 不是 Exception。
        - 不检查异常就是所谓的运行时异常，类似 NullPointerException、ArrayIndexOutOfBoundsException 之类，通常是可以编码避免的逻辑错误，具体根据需要来判断是否需要捕获，并不会在编译期强制要求。
    - 异常处理: 主要在异常时最后关闭回收资源，定期分析异常日志找到问题处理问题，具体明确是那类异常提早抛出延迟捕获？
    - 异常处理准则
        - 第一，尽量不要捕获类似 Exception 这样的通用异常，而是应该捕获特定异常
        - 第二，不要生吞（swallow）异常。这是异常处理中要特别注意的事情，因为很可能会导致非常难以诊断的诡异情况。
    ```java
    try { 
        // 业务代码 
        // … 
        Thread.sleep(1000L);
    } catch (Exception e) { //这里存在2个错误，Thread.sleep() 抛出的 InterruptedException。
        // Ignore it
    }
    ```
    - try-catch 代码段会产生额外的性能开销，或者换个角度说，它往往会影响 JVM 对代码进行优化，所以建议仅捕获有必要的代码段，尽量不要一个大的 try 包住整段的代码；与此同时，利用异常控制代码流程，也不是一个好主意，远比我们通常意义上的条件语句（if/else、switch）要低效。
    - Java 每实例化一个 Exception，都会对当时的栈进行快照，这是一个相对比较重的操作。如果发生的非常频繁，这个开销可就不能被忽略了。
    - NoClassDefFoundError VS ClassNotFoundException
        - NoClassDefFoundError 是个Error，是指一个class在编译时存在，在运行时找不到了class文件了；ClassNotFoundException 是个Exception，是使用类似Class.foName()等方法时的checked exception。
        - NoClassDefFoundError是一个错误(Error)，而ClassNOtFoundException是一个异常，在Java中对于错误和异常的处理是不同的，我们可以从异常中恢复程序但却不应该尝试从错误中恢复程序。
        - ClassNotFoundException的产生原因主要是：
            - Java支持使用反射方式在运行时动态加载类，例如使用Class.forName方法来动态地加载类时，可以将类名作为参数传递给上述方法从而将指定类加载到JVM内存中，如果这个类在类路径中没有被找到，那么此时就会在运行时抛出ClassNotFoundException异常。解决该问题需要确保所需的类连同它依赖的包存在于类路径中，常见问题在于类名书写错误。另外还有一个导致ClassNotFoundException的原因就是：当一个类已经某个类加载器加载到内存中了，此时另一个类加载器又尝试着动态地从同一个包中加载这个类。通过控制动态类加载过程，可以避免上述情况发生。
        - NoClassDefFoundError产生的原因在于：
            - 如果JVM或者ClassLoader实例尝试加载（可以通过正常的方法调用，也可能是使用new来创建新的对象）类的时候却找不到类的定义。要查找的类在编译的时候是存在的，运行的时候却找不到了。这个时候就会导致NoClassDefFoundError.造成该问题的原因可能是打包过程漏掉了部分类，或者jar包出现损坏或者篡改。解决这个问题的办法是查找那些在开发期间存在于类路径下但在运行期间却不在类路径下的类。

- final、finally、finalize
    - final
        - 可以用来修饰类、方法、变量，分别有不同的意义，final 修饰的 class 代表不可以继承扩展，final 的变量是不可以修改的，而 final 的方法也是不可以重写的（override）。
        - 并发安全性
        - 提高性能？
    - finally 
        - 是 Java 保证重点代码一定要被执行的一种机制。我们可以使用 try-finally 或者 try-catch-finally 来进行类似关闭 JDBC 连接、保证 unlock 锁等动作。
        - 扩展思考：栈帧（Stack Frame）是用于支持虚拟机进行方法调用和方法执行的数据结构。它存储了方法的局部变量表、操作数栈、动态链接和方法返回地址等信息。每一个方法从调用开始至执行完成的过程，都对应着一个栈帧在虚拟机栈里面从入栈到出栈的过程。
        - 因为finally的出现，导致return的时候，需要先执行finally，所以需要在局部变量表指定一个位置存放要返回的结果信息。当finally执行完，再把结果取出来。所以finally中执行的语句不会改变局部变量表已存储的结果内容。
        - 测试题目：如下结果为：30，finally执行时是在 return a; 之前执行的。
        ```java
        public static int getInt() {
            int a = 10;
            try {
                System.out.println(a/0);
                a = 20;
            } catch(Exception e) {
                a = 30;
                return a;
            } finally {
                a = 40;
            }
            return a;
        }
        ```
    - finalize 
        - 是基础类 java.lang.Object 的一个方法，它的设计目的是`保证对象在被垃圾收集前完成特定资源的回收`。finalize 机制现在已经不推荐使用，并且在 JDK 9 开始被标记为 deprecated。
        - java 平台目前在逐步使用 java.lang.ref.Cleaner 来替换掉原有的 finalize 实现。Cleaner 的实现利用了幻象引用（PhantomReference）
        - 阻碍JVM进行垃圾回收
- 强引用、软引用、弱引用、幻象引用
    - 不同的引用类型，主要的区别是：对象不同的可达性状态和对垃圾收集器的影响
    - 强引用StrongReference：普通的对象的引用，只要还有一个强引用存在则垃圾收集器不会进行回收。如果可以释放则可以进行赋值为 null，具体何时回收要看垃圾收集器的策略。
    - 软引用SoftReference：当JVM认为内存不足时可以试图回收软引用对象。JVM会在抛出OutOfMemoryError之前清理软引用对象。软引用通常可以用来实现内存敏感的缓存。
    - 弱引用WeakReference：弱引用的生命周期比软引用短。在垃圾回收器线程扫描它所管辖的内存区域的过程中，一旦发现了具有弱引用的对象，不管当前内存空间足够与否，都会回收它的内存。
    - 幻象引用，虚引用：提供一种确保对象被finalize以后，做某些事情的机制，比如利用幻象引用监控对象的创建和销毁。
    - 可达性状态流转图
        - ![可达性状态流转图](https://raw.githubusercontent.com/MichaelYgZhang/michaelygzhang.github.io/master/images/java-ssw-reference.png)
    - 资料：<https://blog.csdn.net/OrPis/article/details/80852184>
- String、StringBuffer、StringBuilder
    - String：Immutable类，不可变性，线程安全，多线程情况下高性能
        - intern() 方法可以字符串进行缓存，以备重复使用。风险：被缓存的字符串存在于“永久代”，基本不会被FullGC之外的垃圾收集器回收，所以如果使用不当，会造成OOM问题。
    - StringBuffer：char[] 数组实现，初始值：16，利用arraycopy进行扩容，线程安全，性能开销大
    - StringBuilder：char[] 数组实现，初始值：16，利用arraycopy进行扩容，线程不安全，性能开销相对小
- Java反射机制，动态代理基于什么原理？
    - 反射机制是 Java 语言提供的一种基础功能，赋予程序在运行时自省（introspect，官方用语）的能力。通过反射我们可以直接操作类或者对象，比如获取某个对象的类定义，获取类声明的属性和方法，调用方法或者构造对象，甚至可以运行时修改类定义。资料：<https://docs.oracle.com/javase/tutorial/reflect/index.html>
        - AccessibleObject.setAccessible​(boolean flag)。它的子类也大都重写了这个方法，这里的所谓 accessible 可以理解成修饰成员的 public、protected、private，这意味着我们可以在运行时修改成员访问限制！
    - 静态代理：事先写好代理类，可以手工编写，也可以用工具生成。缺点是每个业务类都要对应一个代理类，非常不灵活。如果类方法数量越来越多的时候，代理类的代码量是十分庞大的。

    ```java
    public interface Subject   
    {   
        public void doSomething();   
    }
    
    public class RealSubject implements Subject   
    {   
        public void doSomething()   
        {   
            System.out.println( "call doSomething()" );   
        }   
    }

    public class SubjectProxy implements Subject
    {
        Subject subimpl = new RealSubject();
        public void doSomething()
        {
            subimpl.doSomething();
        }
    }

    public class TestProxy 
    {
        public static void main(String args[])
        {
            Subject sub = new SubjectProxy();
            sub.doSomething();
        }
    }
    ```

    - 动态代理是一种方便运行时动态构建代理、动态处理代理方法调用的机制，很多场景都是利用类似机制做到的，比如用来包装 RPC 调用、面向切面的编程（AOP）日志、用户鉴权、全局性异常处理、性能监控，甚至事务处理等。动态代理：运行时自动生成代理对象。缺点是生成代理代理对象和调用代理方法都要额外花费时间。
    - 实现动态代理的方式很多，比如 JDK 自身提供的动态代理，就是主要利用了上面提到的反射机制。还有其他的实现方式，比如利用传说中更高性能的字节码操作机制，类似 ASM、cglib（基于 ASM）、Javassist 等。
        - JDK动态代理 JDK Proxy：必须有个接口interface Hello，需要实现接口：implements InvocationHandler 重写invoke。JDK动态代理：基于Java反射机制实现，必须要实现了接口的业务类才能用这种办法生成代理对象。新版本也开始结合ASM机制。
            - Proxy类的代码量被固定下来，不会因为业务的逐渐庞大而庞大；
            - 可以实现AOP编程，实际上静态代理也可以实现，总的来说，AOP可以算作是代理模式的一个典型应用；
            - 解耦，通过参数就可以判断真实类，不需要事先实例化，更加灵活多变。
        
        ```java
        public interface Subject   
        {   
            public void doSomething();   
        }

        public class RealSubject implements Subject   
        {   
            public void doSomething()   
            {   
                System.out.println( "call doSomething()" );   
            } 
        }


        import java.lang.reflect.InvocationHandler;  
        import java.lang.reflect.Method;  
        import java.lang.reflect.Proxy;  

        public class ProxyHandler implements InvocationHandler
        {
            private Object tar;

            //绑定委托对象，并返回代理类
            public Object bind(Object tar)
            {
                this.tar = tar;
                //绑定该类实现的所有接口，取得代理类 
                return Proxy.newProxyInstance(tar.getClass().getClassLoader(), tar.getClass().getInterfaces(), this);
            }    

            public Object invoke(Object proxy , Method method , Object[] args)throws Throwable
            {
                Object result = null;
                //这里就可以进行所谓的AOP编程了
                //在调用具体函数方法前，执行功能处理
                result = method.invoke(tar,args);
                //在调用具体函数方法后，执行功能处理
                return result;
            }
        }

        public static void main(String args[])
        {
            ProxyHandler proxy = new ProxyHandler();
            //绑定该类实现的所有接口
            Subject sub = (Subject) proxy.bind(new RealSubject());
            sub.doSomething();
        }
        ```
        
        - cglib：cglib 动态代理采取的是创建目标类的子类的方式，因为是子类化，我们可以达到近似使用被调用者本身的效果。在 Spring 编程中，框架通常会处理这种情况，当然我们也可以显式指定。cglib动态代理：基于ASM机制实现，通过生成业务类的子类作为代理类。资料：<https://cliffmeyers.com/blog/2006/12/29/spring-aop-cglib-or-jdk-dynamic-proxies.html>
        - JDK Proxy 的优势：
            - 最小化依赖关系，减少依赖意味着简化开发和维护，JDK 本身的支持，可能比 cglib 更加可靠。
            - 平滑进行 JDK 版本升级，而字节码类库通常需要进行更新以保证在新版 Java 上能够使用。
            - 代码实现简单。
        - 基于类似 cglib 框架的优势：
            - 有的时候调用目标可能不便实现额外接口，从某种角度看，限定调用者实现接口是有些侵入性的实践，类似 cglib 动态代理就没有这种限制。
            - 只操作我们关心的类，而不必为其他相关类增加工作量。
            - 高性能。
- int vs Integer
    - 源码: <http://hg.openjdk.java.net/jdk/jdk/file/26ac622a4cab/src/java.base/share/classes/java/lang/Integer.java>

- static: 无论是变量，方法，还是代码块，只要用static修饰，就是在类被加载时就已经"准备好了",也就是可以被使用或者已经被执行，都可以脱离对象而执行。反之，如果没有static，则必须要依赖于对象实例。
    - 执行步骤：静态代码块 > 成员变量初始化 > 构造方法，双亲委派机制


## IO; Netty
![java-io](https://raw.githubusercontent.com/MichaelYgZhang/michaelygzhang.github.io/master/images/java-io.png)
### IO/BIO/NIO/AIO Netty
- 同步 VS 异步 ；阻塞  VS 非阻塞
    - 同步 vs 异步： 关注点在于消息通知的机制。
    - 阻塞 vs 非阻塞：侧重点在于程序（线程）等待消息的状态。
    - https://www.zhihu.com/question/19732473
    - https://michaelygzhang.github.io/architecture/2020/10/11/concept.html
- NIO最底层与操作系统是如何交互的？ 最底层 ！ 或者是AIO 最底层是与操作系统交互的？？
- [IBM-NIO](https://www.ibm.com/developerworks/cn/education/java/j-nio/j-nio.html)
- [NIO-1](https://juejin.im/entry/58e116f1da2f60005fd09881)
- Netty 框架模块. NIO ？[Netty-1](http://blog.csdn.net/linxcool/article/details/7771952)

### Netty长链接和短链接 ：
基本思路：netty服务端通过一个Map保存所有连接上来的客户端SocketChannel,客户端的Id作为Map的key。每次服务器端如果要向某个客户端发送消息，只需根据ClientId取出对应的SocketChannel,往里面写入message即可。心跳检测通过IdleEvent事件，定时向服务端放送Ping消息，检测SocketChannel是否终断。Netty自带心跳检测功能，IdleStateHandler,客户端在写空闲时主动发起心跳请求，服务器接受到心跳请求后给出一个心跳响应。当客户端在一定时间范围内不能够给出响应则断开链接。
 心跳 机制. 心跳机制的工作原理是: 在服务器和客户端之间一定时间内没有数据交互时, 即处于 idle 状态时, 客户端或服务器会发送一个特殊的数据包给对方, 当接收方收到这个数据报文后, 也立即发送一个特殊的数据报文, 回应发送方, 此即一个 PING-PONG 交互. 自然地, 当某一端收到心跳消息后, 就知道了对方仍然在线, 这就确保 TCP 连接的有效性.
在 Netty 中, 实现心跳机制的关键是 IdleStateHandler,
1. 使用 Netty 实现心跳机制的关键就是利用 IdleStateHandler 来产生对应的 idle 事件.
2. 一般是客户端负责发送心跳的 PING 消息, 因此客户端注意关注 ALL_IDLE 事件, 在这个事件触发后, 客户端需要向服务器发送 PING 消息, 告诉服务器"我还存活着".
3. 服务器是接收客户端的 PING 消息的, 因此服务器关注的是 READER_IDLE 事件, 并且服务器的 READER_IDLE 间隔需要比客户端的 ALL_IDLE 事件间隔大(例如客户端ALL_IDLE 是5s 没有读写时触发, 因此服务器的 READER_IDLE 可以设置为10s)
4. 当服务器收到客户端的 PING 消息时, 会发送一个 PONG 消息作为回复. 一个 PING-PONG 消息对就是一个心跳交互.
- [资料](https://segmentfault.com/a/1190000006931568)
- [资料IO](https://yq.aliyun.com/articles/75397?spm=a2c4e.11153940.blogrightarea75403.22.118338cc05ruap)

### 零拷贝zero-copy


### JCF（Java Collections Framework）
- <http://java-performance.com/>
- <https://docs.oracle.com/javase/8/docs/technotes/guides/collections/overview.html>
![JCF](https://upload-images.jianshu.io/upload_images/2243690-9cd9c896e0d512ed.gif?imageMogr2/auto-orient/strip%7CimageView2/2/w/643)
![java.util.Collection class and interface hierarchy](https://upload.wikimedia.org/wikipedia/commons/a/ab/Java.util.Collection_hierarchy.svg)
![Java's java.util.Map class and interface hierarchy](https://upload.wikimedia.org/wikipedia/commons/7/7b/Java.util.Map_hierarchy.svg)

#### List
- Vector
    - 顺序存储，线程安全数组，扩容调整1倍，除了尾插元素和删除其他操作往往性能比较差，比如中间插入一个元素需要移动后面的所有元素。
- ArrayList
    - 实现List接口, 底层实现Object[],非线程安全,多线程安全考虑使用Vector/Collections.synchronizedList(List l)
    - 实现RandomAccess接口,可高效进行foreach(:){}
    - 构造集合时若不设置initialCapacity则第一次add操作时将开辟DEFAULT_CAPACITY = 10;的内存数组空间
    - 当前数组集合大小若不足时将进行0.5倍的扩容,数组最大值为MAX_ARRAY_SIZE = Integer.MAX_VALUE - 8;即`2^32-1`;注意扩容将调用public static native void arraycopy(Object src, int  srcPos, Object dest, int destPos, int length);性能消耗点.
    - 迭代时fail-fast; 如有修改 the iterator will throw a ConcurrentModificationException.
    - 缩容机制：trimToSize
 - `API简介`
    - public boolean add(E e) {};最后一位数组下标插入;
    - public void add(int index, E element) {};指定下表插入需移动index之后的元素,当size比较大时index约小,需要移动数组的元素越多,性能越低.最坏情况是1. 先扩容 2. 调用System.arraycopy(....)移动元素
    - public E set(int index, E element) {}; 替换指定位置元素
    - public E remove(int index) {}; 移除指定位置元素,index约小需要前移动的元素越多,性能消耗越大.注意elementData[--size] = null; // clear to let GC do its work
    - public boolean remove(Object o) {}; 1. 找到元素下标 2.移动元素 3.elementData[--size] = null; // clear to let GC do its work

- LikedList 
    - 实现List<E>, Deque<E>双端队列，非线程安全, `插入/删除`高效,`遍历`性能低, 消耗更多的内存,产生更多对象,增加GC的次数/时间；
    - Collections.synchronizedList(new LinkedList(...));可做到线程安全

- CopyOnWriteArrayList

#### Set
- HashSet
    - 无序,不重复,采用散列的存储方法，所以没有顺序; 其实就是一个hashmap,只是在在添加元素的时候对应的put(k,object),k就是要添加的值,而参数v就是一个final类型的object对象。此处需要注意的是:由于map允许有一个key为null的键值对，所以set也就允许有一个为null的对象，唯一的一个。
- LinkedHashSet
    - 是HashSet的一个子类,只是HashSet底层用的HashMap,而LinkedHashSet底层用的LinkedHashMap; 元素有序.

#### Queue/Deque
- 在这个题目下，自然就会想到优先级队列了，但还需要额外考虑vip再分级，即同等级vip的平权的问题，所以应该考虑除了直接的和vip等级相关的优先级队列优先级规则问题，还得考虑同等级多个客户互相不被单一客户大量任务阻塞的问题，数据结构确实是基础，即便这个思考题考虑的这个场景，待调度数据估计会放在redis里面吧

#### Sort
- 原始数据类型采用的: 双轴快速排序 <http://hg.openjdk.java.net/jdk/jdk/file/26ac622a4cab/src/java.base/share/classes/java/util/DualPivotQuicksort.java>
    - 优化算法 <http://mail.openjdk.java.net/pipermail/core-libs-dev/2018-January/051000.html>
- 引用对象类型：TimSort ， 思路：归并+二分插入，查找数据集中已经排好序的分区，然后合并这些分区来达到排序的目的。 <http://hg.openjdk.java.net/jdk/jdk/file/26ac622a4cab/src/java.base/share/classes/java/util/TimSort.java>
- Java8 引入并行排序parallelSort，数据量大时处理器多核有明显差异，后续验证下。

#### Map
- 哈希
    - 哈希冲突，解决哈希冲突的常用方法有：
        - 开放定址法
            - 基本思想是：当关键字key的哈希地址p=H（key）出现冲突时，以p为基础，产生另一个哈希地址p1，如果p1仍然冲突，再以p为基础，产生另一个哈希地址p2，…，直到找出一个不冲突的哈希地址pi ，将相应元素存入其中。
        - 再哈希法
            - 这种方法是同时构造多个不同的哈希函数：Hi=RH1（key）  i=1，2，…，k，当哈希地址Hi=RH1（key）发生冲突时，再计算Hi=RH2（key）……，直到冲突不再产生。这种方法不易产生聚集，但增加了计算时间。
        - 链地址法
            - 这种方法的基本思想是将所有哈希地址为i的元素构成一个称为同义词链的单链表，并将单链表的头指针存在哈希表的第i个单元中，因而查找、插入和删除主要在同义词链中进行。链地址法适用于经常进行插入和删除的情况。
        - 建立公共溢出区
            - 这种方法的基本思想是：将哈希表分为基本表和溢出表两部分，凡是和基本表发生冲突的元素，一律填入溢出表。
- Hashtable 
    - 线程安全; HashTable基于Dictionary类,HashTable中的key和value都不允许为null,HashMap仅支持Iterator的遍历方式;
- HashMap
    - HashMap 数组的特点是：寻址容易，插入和删除困难；而链表的特点是：寻址困难，插入和删除容易。哈希表结合了两者的优点。哈希表有多种不同的实现方法，可以理解将此理解为“链表的数组”;哈希表是由数组+链表组成;HashMap是基于AbstractMap;HashMap可以允许存在一个为null的key和任意个为null的value; HashMap仅支持Iterator的遍历方式;
    - 高并发情况下可能存在CPU负载高问题？
        - HashMap在并发执行put操作时发生扩容，可能会导致节点丢失，产生环形链表等情况。 节点丢失，会导致数据不准 生成环形链表，会导致get()方法死循环。
        - 在jdk1.7中，由于扩容时使用头插法，在并发时可能会形成环状列表，导致死循环，在jdk1.8中改为尾插法，可以避免这种问题，但是依然避免不了节点丢失的问题。
        - <https://bugs.java.com/bugdatabase/view_bug.do?bug_id=6423457>
    - 为什么总是 2^n次？
        - 原因 `hashcode & (length -1)` 如果length为奇数根据hashmap计算下标的算法则必然导致有一半的数据无法存储数据，空间浪费，所以必须为偶数
    - 资料：<https://juejin.cn/post/6927211419918319630?utm_source=gold_browser_extension>
    - 资料：<https://blog.csdn.net/ns_code/article/details/36034955>
- TreeMap 则是基于红黑树的一种提供顺序访问的 Map，和 HashMap 不同，它的 get、put、remove 之类操作都是 O（log(n)）的时间复杂度，具体顺序可以由指定的 Comparator 来决定，或者根据键的自然顺序来判断。
- LinkedHashMap：重写`removeEldestEntry`方法可以实现简单的淘汰数据的容器

    ```java
    import java.util.LinkedHashMap;
    import java.util.Map;  
    public class LinkedHashMapSample {
        public static void main(String[] args) {
            LinkedHashMap<String, String> accessOrderedMap = new LinkedHashMap<String, String>(16, 0.75F, true){
                @Override
                protected boolean removeEldestEntry(Map.Entry<String, String> eldest) {
                    // 实现自定义删除策略，否则行为就和普遍Map没有区别
                    return size() > 3;
                }
            };
            accessOrderedMap.put("Project1", "Valhalla");
            accessOrderedMap.put("Project2", "Panama");
            accessOrderedMap.put("Project3", "Loom");
            accessOrderedMap.forEach( (k,v) -> {
                System.out.println(k +":" + v);
            });
            // 模拟访问
            accessOrderedMap.get("Project2");
            accessOrderedMap.get("Project2");
            accessOrderedMap.get("Project3");
            System.out.println("Iterate over should be not affected:");
            accessOrderedMap.forEach( (k,v) -> {
                System.out.println(k +":" + v);
            });
            // 触发删除
            accessOrderedMap.put("Project4", "Mission Control");
            System.out.println("Oldest entry should be removed:");
            accessOrderedMap.forEach( (k,v) -> {// 遍历顺序不变
                System.out.println(k +":" + v);
            });
        }
    }
    ```

- PriorityQueue：二叉堆实现的 
- ConcurrentHashMap
    - ConcurrentHashMap JDK1.7 `Segment[] + HashEntry[] + HashEntry单链`
        - 其中Segment在实现上继承了ReentrantLock，这样就自带了锁的功能。数组大小默认16,0.75增长因子,2^n次方大小.
        - `size计算方式`: 先不加锁连续计算元素个数最多3次,如果前后2次一样,则返回;否则给每个Segment进行加锁计算一次;
        - 当执行put方法插入数据时，根据key的hash值，在Segment数组中找到相应的位置，如果相应位置的Segment还未初始化，则通过CAS进行赋值，接着执行Segment对象的put方法通过加锁机制插入数据，实现如下：场景：线程A和线程B同时执行相同Segment对象的put方法
        1. 线程A执行tryLock()方法成功获取锁，则把HashEntry对象插入到相应的位置；
        2. 线程B获取锁失败，则执行scanAndLockForPut()方法，在scanAndLockForPut方法中，会通过重复执行tryLock()方法尝试获取锁，在多处理器环境下，重复次数为64，单处理器重复次数为1，当执行tryLock()方法的次数超过上限时，则执行lock()方法挂起线程B；
        3. 当线程A执行完插入操作时，会通过unlock()方法释放锁，接着唤醒线程B继续执行；
    - ConcurrentHashMap JDK1.8 `Node数组 + CAS + Synchronized 数组+链表+红黑树`
        - volatile类型的变量baseCount计算size值，因为元素个数保存baseCount中，部分元素的变化个数保存在CounterCell数组中，通过累加baseCount和CounterCell数组中的数量，即可得到元素的总个数；
        - 扩容时优先扩容数组(<64时),2倍数组进行扩容; 然后才是当单链>8时转化红黑树；
        - size计算: 通过对 baseCount 和 counterCell 进行 CAS 计算，最终通过 baseCount 和 遍历 CounterCell 数组得出 size。JDK 8 推荐使用mappingCount 方法，因为这个方法的返回值是 long 类型，不会因为 size 方法是 int 类型限制最大值。

- ConcurrentSkipListMap 基于跳跃列表（Skip List）的ConcurrentNavigableMap实现。本质上这种集合可以当做一种TreeMap的线程安全版本来使用。

- ConcurrentSkipListSet：使用 ConcurrentSkipListMap来存储的线程安全的Set。

#### JDK集合总结:
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


## 多线程
- 多线程与并发编程:
  进程: 一个计算机的运行实例，有自己独立的地址空间，包含程序内容和数据，不同进程间相互隔离，拥有各自的各种资源和状态信息，包括打开的文件，子进程和信号处理等。
  线程: 程序的执行流程，CPU调度的基本单位，线程拥有自己的程序计数器，寄存器，栈帧，同一进程中的线程拥有相同的地址空间，同时共享进程中的各种资源
- 多线程开发中应该优先使用高层API，如果无法满足，使用java.util.concurrent.atomic和java.util.concurrent.locks包提供的中层API，
  而synchronized和volatile，以及wait,notify和notifyAll等低层API 应该最后考虑。
- 并发集合容器,线程安全的非线程安全的分别都有哪些?
- 如何看当前线程是否是线程安全的? 特征是什么? 【资料](https://yq.aliyun.com/articles/75403)
- Semphore

- 线程是如何通信的？ 
    ![java-thread-state](https://raw.githubusercontent.com/MichaelYgZhang/michaelygzhang.github.io/master/images/java-thread-state.png)
    - wait()：wait()方法表示当前线程让出执行权
    - notify()：notify()表示唤醒wait()状态的线程。
        - `一个线程如果没有持有对象锁，将不能调用wait()，notify()或者notifyAll()。否则，会抛出IllegalMonitorStateException异常`。
    - notifyAll()：
    - join()：让“主线程”等待“子线程”结束之后才能继续运行，底层实现调用wait方法。

        ```java
        public final native void wait(long timeout) throws InterruptedException;
        ```
        - 举例子说明：

        ```java
        public static void main(String[] args){
            try {
                ThreadA t1 = new ThreadA("t1"); // 新建“线程t1”

                t1.start();                     // 启动“线程t1”
                t1.join();                        // 将“线程t1”加入到“主线程main”中，并且“主线程main()会等待它的完成”
                System.out.printf("%s finish\n", Thread.currentThread().getName());
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        static class ThreadA extends Thread{

            public ThreadA(String name){
                super(name);
            }
            public void run(){
                System.out.printf("%s start\n", this.getName());

                // 延时操作
                for(int i=0; i <1000000; i++)
                    ;

                System.out.printf("%s finish\n", this.getName());
            }
        }
        //输出
        t1 start
        t1 finish
        main finish
        ```

        ![java-thread-join](https://raw.githubusercontent.com/MichaelYgZhang/michaelygzhang.github.io/master/images/java-thread-join.png)

    - CountdownLatch（以下简称 CDL）适用于一个线程去等待多个线程的情况：举例说明：D保护ABC先撤离，D最后撤离

    ```java
    int armyNum = 3;
    final CountDownLatch countDownLatch = new CountDownLatch(armyNum);
        for (char army = 'A'; army <= 'C'; army++) {
            final String name = String.valueOf(army);
            new Thread(new Runnable() {
                @Override
                public void run() {
                    System.out.println(name + "部队正在撤离");
                    try {
                        //模拟耗时
                        Thread.sleep(100);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    System.out.println(name + "部队已经撤离");
                    countDownLatch.countDown();
                }
            }).start();
        }
        new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("D 正在断后（等待其他部队撤离）");
                try {
                    countDownLatch.await();
                    System.out.println("ABC撤离完毕，D可以撤离了");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    //输出
    A部队正在撤离
    B部队正在撤离
    C部队正在撤离
    D 正在断后（等待其他部队撤离）
    A部队已经撤离
    B部队已经撤离
    C部队已经撤离
    ABC撤离完毕，D可以撤离了
    ```

    - CyclicBarrier为了实现线程间互相等待这种需求，我们可以利用 CyclicBarrier：

    ```java
    int runner = 3;
        final CyclicBarrier cyclicBarrier = new CyclicBarrier(runner);
        final Random random = new Random();
        for (char runnerName = 'A'; runnerName <= 'C'; runnerName++) {
            final String rN = String.valueOf(runnerName);
            new Thread(new Runnable() {
                @Override
                public void run() {
                    long prepareTime = random.nextInt(10000) + 100;
                    System.out.println("裁判等了" + prepareTime + "毫秒，" + rN + "选手到了");
                    try {
                        Thread.sleep(prepareTime);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    try {
                        System.out.println(rN + "选手准备好了，在等其他人");
                        cyclicBarrier.await(); // 当前选手准备好，等待其他人
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    } catch (BrokenBarrierException e) {
                        e.printStackTrace();
                    }
                    System.out.println(rN + "比赛开始"); // 人齐开始比赛
                }
            }).start();
        }
    //输出
    裁判等了7075毫秒，A选手到了
    裁判等了5433毫秒，B选手到了
    裁判等了9676毫秒，C选手到了
    B选手准备好了，在等其他人
    A选手准备好了，在等其他人
    C选手准备好了，在等其他人
    C比赛开始
    B比赛开始
    A比赛开始
    ```

    - CyclicBarrier与CountDownLatch比较
        - CountDownLatch: 一个线程(或者多个)，等待另外N个线程完成某个事情之后才能执行；
        - CyclicBarrier: N个线程相互等待，任何一个线程完成之前，所有的线程都必须等待。
        - CountDownLatch: 一次性的；CyclicBarrier:可以重复使用。
        - CountDownLatch基于AQS；CyclicBarrier基于锁和Condition。本质上都是依赖于volatile和CAS实现的
    - 多线程题目: 两个线程交替打印数字，你打印一个我打印一个

    ```java
    class Ticket implements Runnable {
        Object x = "90";
        static int total = 10;
        static Ticket t1 = new Ticket();

        public static void main(String[] args) {
            printMethod();
        }

        static void printMethod() {
            Thread A = new Thread(t1);
            Thread B = new Thread(t1);
            A.setName("A");
            B.setName("B");
            B.start();
            A.start();
        }

        @Override
        public void run() {
            synchronized (x) {
                for (; total < 20; total++) {
                    System.out.println(Thread.currentThread().getName() + "------" + total);
                    x.notify();
                    try {
                        x.wait();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }
            }
        }
    }
    ```

- Semaphore
    - 是一个计数信号量，必须由获取它的线程释放。作用是控制并发的数量。内部实现：AbstractQueuedSynchronizer
- Synchronized
    - synchronized可以保证方法或代码块在运行时，同一时刻只有一个线程可以进入到临界区（互斥性），同时它还保证了共享变量的内存可见性，不公平的锁，可重入锁。
    - monitorenter/monitorexit机制
        - 线程一旦进入到被synchronized修饰的方法或代码块时，指定的锁对象通过某些操作将`类对象头中的LockWord指向Monitor` 的起始地址与之关联，同时monitor 中的Owner存放拥有该锁的线程的唯一标识，确保一次只能有一个线程执行该部分的代码，线程在获取锁之前不允许执行该部分的代码。
    - [synchronized资料](https://www.jianshu.com/p/19f861ab749e)
    - 两个问题：
        - 1、为何所有的任意的对象都可以作为synchronized锁的对象？Java实例对象，包括Java对象头。Java对象头中存储了指向Monitor对象的指针。并且每一个实例对象都存在着一个Monitor对象与之关联。所以每一个对象，都可以作为锁的对象。
        - 2、ObjectMonitor是如何实现同步的？而在Java虚拟机(HotSpot)中，monitor是由ObjectMonitor实现的，ObjectMonitor的结构如下：ObjectMonitor中有两个队列，_WaitSet 和 _EntryList，用来保存ObjectWaiter对象列表( 每个等待锁的线程都会被封装成ObjectWaiter对象)，_owner指向持有ObjectMonitor对象的线程，当多个线程同时访问一段同步代码时，首先会进入 _EntryList 集合，当线程获取到对象的monitor 后进入 _Owner 区域并把monitor中的owner变量设置为当前线程同时monitor中的计数器count加1，若线程调用 wait() 方法，将释放当前持有的monitor，owner变量恢复为null，count自减1，同时该线程进入 WaitSe t集合中等待被唤醒。若当前线程执行完毕也将释放monitor(锁)并复位变量的值，以便其他线程进入获取monitor(锁)。这种就保证了一次，同一个时刻只有一个线程在操作对象。
    - 偏向锁：不占用CPU，线程进入同步块，则为偏向锁，目的是减少同一线程获取锁的代价 CAS(Compare And Swap)，核心思想：如果一个线程获得了锁，那么锁就进入偏向锁，此时Mark Word的结构变为偏向锁结构，当该线程再次请求锁时，无需做任何同步操作，即获取锁的过程，只需要检查Mark Word的锁标记位为偏向锁以及当前线程Id等于Mard Word的ThreadId即可，这样就省去了大量有关锁申请的操作。注意：不适用于锁竞争比较激烈的多线程场合。偏向锁的目的是消除数据在无竞争情况下的同步原语，进一步提高程序的运行性能。如果说轻量级锁是在无竞争的情况下使用CAS操作去消除同步使用的互斥量，那偏向锁就是在无竞争的情况下把整个同步都消除掉，连 CAS 操作都不做了。偏向锁的“偏”，就是偏心的 “偏”、偏袒的 “偏”，它的意思是这个锁会偏向于第一个获得它的线程，如果在接下来的执行过程中，该锁没有被其他的线程获取，则持有偏向锁的线程将永远不需要再进行同步。虚拟机都可以不再进行任何同步操作（例如 Locking 、Unlocking 及对 Mark Word的Update 等）。
    - 轻量级锁：由偏向锁升级而来，偏向锁运行在一个线程进入同步块的情况下，当第二个线程加入锁争用的时候，偏向锁就升级为轻量级锁。比如线程交替执行同步块情况。若存在多个线程同一时间访问同一锁的情况，就会导致轻量锁膨胀为重量级锁。它的本意是在没有多线程竞争的前提下，减少传统的重量级锁使用操作系统互斥量产生的性能消耗。
    - 重量级锁：重量级锁也就是通常说synchronized的对象锁
    - 自选锁：占用CPU资源，锁占用时间短，线程切换不值得，通过线程执行循环等待锁的释放，不让出CPU资源。如果锁竞争激烈，性能开销大。
        - 自适应自选锁：自适应意味着自旋的时间不再固定了，而是由前一次在同一个锁上的自旋时间及锁的拥有者的状态来决定。如果在同一个锁对象上，自旋等待刚刚成功获得过锁，并且持有锁的线程正在运行中，那么虚拟机就会认为这次自旋也很有可能再次成功，进而它将允许自旋等待持续相对更长的时间，比如100个循环。另外，如果对于某个锁，自旋很少成功获得过，那在以后要获取这个锁时将可能省略掉自旋过程，以避免浪费处理部资源。有了自适应自旋，随着程序运行和性能监控信息的不断完善，虚拟机对程序锁的状况预测就会越来越准确。虚拟机就会变得越来越 “聪明” 了。
    - `锁消除`：锁消除是指虚拟机即时编译器在运行时，对一些代码上要求同步，但是被检测到不可能存在共享数据竞争的锁进行消除。锁消除的主要判定依据来源于逃逸分析的数据支持，如果判断在一段代码中，堆上的所有数据都不会逃逸出去从而被其他线程访问到，那就可以把它们当做栈上数据对待，认为它们是线程私有的，同步加锁自然就无须进行。
    - `锁粗化`：扩大加锁的范围，避免反复加锁和解锁。比如在循环内部反复进行加锁和释放锁，则可以进行锁粗化，提高性能。
    - 资料: <https://www.cnblogs.com/softidea/p/12354042.html>
    ![java-lock-state](https://raw.githubusercontent.com/MichaelYgZhang/michaelygzhang.github.io/master/images/java-lock-state.png)
    ![java-lock-synchronized](https://raw.githubusercontent.com/MichaelYgZhang/michaelygzhang.github.io/master/images/java-lock-synchronized.png)
- `ReentrantLock`
    - <https://www.jianshu.com/p/4358b1466ec9>
    - [LOCK](http://www.cnblogs.com/dolphin0520/p/3923167.html)
    - [LOCK-1](https://www.jianshu.com/p/2344a3e68ca9)
    - [LOCK-2](http://www.leocook.org/2017/07/16/Java%E5%B9%B6%E5%8F%91(%E5%85%AD)-ReentrantLock-synchronized/)
- `AQS框架(AbstractQueuedSynchronizer)`
    - 队列同步器AQS是用来构建锁或其他同步组件的基础框架，内部使用一个int成员变量表示同步状态，通过内置的FIFO队列来完成资源获取线程的排队工作，其中内部状态state，等待队列的头节点head和尾节点head，都是通过volatile修饰，保证了多线程之间的可见。
    - static final int CANCELLED =  1;SIGNAL = -1等待触发状态;CONDITION = -2等待条件状态;PROPAGATE = -3状态需要向后传播;
    - 子类重写tryAcquire和tryRelease方法通过CAS指令修改状态变量state。
        - [AQS详解](https://www.jianshu.com/p/d8eeb31bee5c)
    1. 线程A执行CAS执行成功，state值被修改并返回true，线程A继续执行。
    2. 线程A执行CAS指令失败，说明线程B也在执行CAS指令且成功，这种情况下线程A会执行步骤3。
    3. 生成新Node节点node，并通过CAS指令插入到等待队列的队尾（同一时刻可能会有多个Node节点插入到等待队列中），如果tail节点为空，则将head节点指向一个空节点（代表线程B）
    4. node插入到队尾后，该线程不会立马挂起，会进行自旋操作。因为在node的插入过程，线程B（即之前没有阻塞的线程）可能已经执行完成，所以要判断该node的前一个节点pred是否为head节点（代表线程B），如果pred == head，表明当前节点是队列中第一个“有效的”节点，因此再次尝试tryAcquire获取锁
        - 如果成功获取到锁，表明线程B已经执行完成，线程A不需要挂起
        - 如果获取失败，表示线程B还未完成，至少还未修改state值。进行步骤5
    5. 前面我们已经说过只有前一个节点pred的线程状态为SIGNAL时，当前节点的线程才能被挂起。
        1. 如果pred的waitStatus == 0，则通过CAS指令修改waitStatus为Node.SIGNAL。
        2. 如果pred的waitStatus > 0，表明pred的线程状态CANCELLED，需从队列中删除。
        3. 如果pred的waitStatus为Node.SIGNAL，则通过LockSupport.park()方法把线程A挂起，并等待被唤醒，被唤醒后进入步骤6。
    6. 线程每次被唤醒时，都要进行中断检测，如果发现当前线程被中断，那么抛出InterruptedException并退出循环。从无限循环的代码可以看出，并不是被唤醒的线程一定能获得锁，必须调用tryAccquire重新竞争，因为锁是非公平的，有可能被新加入的线程获得，从而导致刚被唤醒的线程再次被阻塞，这个细节充分体现了“非公平”的精髓。
    - 释放锁过程:
        1. 如果头结点head的waitStatus值为-1，则用CAS指令重置为0；
        2. 找到waitStatus值小于0的节点s，通过LockSupport.unpark(s.thread)唤醒线程

- `CAS(Compare and Swap)`
    - ABA问题
    - CAS三个参数，一个当前内存值V、旧的预期值A、即将更新的值B，当且仅当预期值A和内存值V相同时，将内存值修改为B并返回true，否则什么都不做，并返回false。
    - CAS存在一个很明显的问题，即ABA问题。AtomicStampedReference,它可以通过控制变量值的版本来保证CAS的正确性。
    - CAS 可以复用缓存

- 线程有哪些状态,继承thread,创建多个线程,是分别执行自己的任务。实现runnable，创建多个线程是多个线程对某一共同任务的执行。区别。
    - [Thread](https://michaelygzhang.github.io/java/2016/09/25/Java-Thread.html)
- 等待池，锁池
    - 锁池：假设线程A已经拥有了某个对象(注意:不是类)的锁，而其它的线程想要调用这个对象的某个synchronized方法(或者synchronized块)，由于这些线程在进入对象的synchronized方法之前必须先获得该对象的锁的拥有权，但是该对象的锁目前正被线程A拥有，所以这些线程就进入了该对象的锁池中
    - 等待池：假设一个线程A调用了某个对象的wait()方法，线程A就会释放该对象的锁(因为wait()方法必须出现在synchronized中，这样自然在执行wait()方法之前线程A就已经拥有了该对象的锁)，同时线程A就进入到了该对象的等待池中。如果另外的一个线程调用了相同对象的notifyAll()方法，那么处于该对象的等待池中的线程就会全部进入该对象的锁池中，准备争夺锁的拥有权。如果另外的一个线程调用了相同对象的notify()方法，那么仅仅有一个处于该对象的等待池中的线程(随机)会进入该对象的锁池.
    - 如果有个线程执行了objectX.wait()，那么该线程就会被暂停（线程的生命周期状态会被调整为Waiting），并且会释放掉objectX锁，然后被存入objectX的等待池之中。此时，该线程就被称为objectX的等待线程。当其他线程执行了objectX.notify()/notifyAll()时，等待池中的一个（或者多个，取决于被调用的是notify还是notifyAll方法）任意（注意是“任意”，而不一定是等待池中等待时间最长或者最短的）等待线程会被唤醒，这些被唤醒的线程会被放到锁池中，会与锁池中已经存在的线程以及其他（可能的）活跃线程共同参与抢夺objectX。至于代码中到底是使用notify还是notifyAll方法，这个要根据实际情况来分析。等待池中的线程被notify()或者notifyAll()方法唤醒进入到锁池，最后竞争到了锁并且进入了Runnable状态的话，会从wait现场恢复，执行wait()方法之后的代码。
- `volatile`
    - happend-before原则
    - 保证多线程间的可见性, 不保证原子性
    - 避免指令重排序，如何进行避免的？JMM，8个基本操作，lock, read, load, use, assign, store, write
    - volatile修饰long,double可以原子性，内存屏障会将所有写的值更新到缓存，顺序性可见性, 否则出现`伪共享缓存`问题。
- `ThreadLocal`
    - 使用场景？怎么用？使用注意事项，原理是什么？
    - InheritableThreadLocal，重写 childValue，解决父子线程数据传递问题。资料: <https://www.cnblogs.com/gxyandwmm/p/9471507.html>
    - ThreadLocal 内存何时情况有可能发生内存泄漏？ 如何解决？答得是remove? 待核实！！threadlocal使用线程局部变量，注意使用后释放？static修饰？
    - [http://blog.xiaohansong.com/2016/08/06/ThreadLocal-memory-leak/](http://blog.xiaohansong.com/2016/08/06/ThreadLocal-memory-leak/)
- `线程池`
    - 美团Java线程池资料: <https://tech.meituan.com/2020/04/02/java-pooling-pratice-in-meituan.html>
    - ThreadPoolExecutor
    - 原理
    - 参数如何设置
    - CPU密集，IO密集
    - 如何进行监控
    - Callerrunspolicy 风险？交给主线程进行执行，其他线程进行等待，可能拖垮主线程
    - excutorServer接口，继承自executor；提供了对任务的管理：submit()，可以吧Callable和Runnable作为任务提交，得到一个Future作为返回，可以获取任务结果或取消任务。提供批量执行：invokeAll()和invokeAny()，同时提交多个Callable；invokeAll()，会等待所有任务都执行完成，返回一个包含每个任务对应Future的列表；invokeAny()，任何一个任务成功完成，即返回该任务结果。超过时限后，任何尚未完成的任务都会被取消。

## JVM

### JVM原理
- JVM运行时内存
    - heap, java stack, native method stack, PC register, method area; [资料](http://www.cnblogs.com/leesf456/p/5055697.html)
- 对象分配？
- 栈帧？
- 如何将对象直接初始化到老年代？
- 大对象？年轻代配置大小。
- `类加载原理`
    - [资料](https://segmentfault.com/a/1190000002579346)
    - 加载：首先是加载阶段（Loading），它是 Java 将字节码数据从不同的数据源读取到 JVM 中，并映射为 JVM 认可的数据结构（Class 对象），这里的数据源可能是各种各样的形态，如 jar 文件、class 文件，甚至是网络数据源等；如果输入数据不是 ClassFile 的结构，则会抛出 ClassFormatError。加载阶段是用户参与的阶段，我们可以自定义类加载器，去实现自己的类加载过程。
    - 链接：第二阶段是链接（Linking），这是核心的步骤，简单说是把原始的类定义信息平滑地转化入 JVM 运行的过程中。这里可进一步细分为三个步骤：
        1. 验证（Verification），这是虚拟机安全的重要保障，JVM 需要核验字节信息是符合 Java 虚拟机规范的，否则就被认为是 VerifyError，这样就防止了恶意信息或者不合规的信息危害 JVM 的运行，验证阶段有可能触发更多 class 的加载。文件格式/魔术开头
        2. 准备（Preparation），创建类或接口中的静态变量，并初始化静态变量的初始值。但这里的“初始化”和下面的显式初始化阶段是有区别的，侧重点在于分配所需要的内存空间，不会去执行更进一步的 JVM 指令。为类的静态变量分配内存，并将其初始化为默认值
        3. 解析（Resolution），在这一步会将常量池中的符号引用（symbolic reference）替换为直接引用。在Java 虚拟机规范中，详细介绍了类、接口、方法和字段等各个方面的解析。
    - 初始化：最后是初始化阶段（initialization），这一步真正去执行类初始化的代码逻辑，包括静态字段赋值的动作，以及执行类定义中的静态初始化块内的逻辑，编译器在编译阶段就会把这部分逻辑整理好，父类型的初始化逻辑优先于当前类型的逻辑。
    - 双亲委派模型：再来谈谈双亲委派模型，简单说就是当类加载器（Class-Loader）试图加载某个类型的时候，除非父加载器找不到相应类型，否则尽量将这个任务代理给当前加载器的父加载器去做。使用委派模型的目的是避免重复加载 Java 类型。

- JVM常用命令？
    - JVM常用命令： <https://my.oschina.net/feichexia/blog/196575>
- `JVM垃圾回收机制有几种`？工作原理是什么？CMS清理步骤？G1？
- `JVM内存模型类加载机制`？为什么这么设计？
- 堆栈，对象分析？

### GC
- GC算法
    - 引用计数器
        - 存在循环引用问题。
    - 可达性分析算法
        - `GCRoot`：JVM 会把虚拟机栈和本地方法栈中正在引用的对象、静态属性引用的对象和常量，作为 GC Roots。
    - 复制（Copying）算法，我前面讲到的`新生代 GC，基本都是基于复制算法`，过程就如专栏上一讲所介绍的，将活着的对象复制到 to 区域，拷贝过程中将对象顺序放置，就可以避免内存碎片化。这么做的代价是，既然要进行复制，既要提前预留内存空间，有一定的浪费；另外，对于 G1 这种分拆成为大量 region 的 GC，复制而不是移动，意味着 GC 需要维护 region 之间对象引用关系，这个开销也不小，不管是内存占用或者时间开销。
        - -XX:MaxTenuringThreshold=<N>  对象年计数阀值设置
    - 标记 - 清除（Mark-Sweep）算法，首先进行标记工作，标识出所有要回收的对象，然后进行清除。这么做除了标记、清除过程效率有限，另外就是不可避免的出现碎片化问题，这就导致其不适合特别大的堆；否则，一旦出现 Full GC，暂停时间可能根本无法接受。
    - 标记 - 整理（Mark-Compact），类似于标记 - 清除，但为避免内存碎片化，它会在清理过程中将对象移动，以确保移动后的对象占用连续的内存空间。    
- 垃圾收集器
    - Serial GC：
        - 它是最古老的垃圾收集器，“Serial”体现在其收集工作是单线程的，并且在进行垃圾收集过程中，会进入臭名昭著的“Stop-The-World”状态。当然，其单线程设计也意味着精简的 GC 实现，无需维护复杂的数据结构，初始化也简单，所以一直是 Client 模式下 JVM 的默认选项。从年代的角度，通常将其老年代实现单独称作 Serial Old，它采用了标记 - 整理（Mark-Compact）算法，区别于新生代的复制算法。Serial GC 的对应 JVM 参数是：-XX:+UseSerialGC
        - 串行运行；作用于新生代；复制算法；响应速度优先；适用于单CPU环境下的client模式。
    - ParNew GC：
        - 很明显是个新生代 GC 实现，它实际是 Serial GC 的多线程版本，最常见的应用场景是配合老年代的 CMS GC 工作，下面是对应参数：-XX:+UseConcMarkSweepGC -XX:+UseParNewGC
        并行运行；作用于新生代；复制算法；响应速度优先；多CPU环境Server模式下与CMS配合使用。
    - CMS（Concurrent Mark Sweep） GC：
        - 基于标记 - 清除（Mark-Sweep）算法，设计目标是尽量减少停顿时间，这一点对于 Web 等反应时间敏感的应用非常重要，一直到今天，仍然有很多系统使用 CMS GC。但是，CMS 采用的标记 - 清除算法，存在着内存碎片化问题，所以难以避免在长时间运行等情况下发生 full GC，导致恶劣的停顿。另外，既然强调了并发（Concurrent），CMS 会占用更多 CPU 资源，并和用户线程争抢。
        - 并发运行；作用于老年代；标记-清除算法；响应速度优先；适用于互联网或B/S业务。
    - Parallel GC：
        - 在早期 JDK 8 等版本中，它是 server 模式 JVM 的默认 GC 选择，也被称作是`吞吐量优先的 GC`。它的算法和 Serial GC 比较相似，尽管实现要复杂的多，其特点是`新生代和老年代 GC 都是并行进行的`，在常见的服务器环境中更加高效。开启选项是：-XX:+UseParallelGC，另外，Parallel GC 引入了开发者友好的配置项，我们可以直接设置暂停时间或吞吐量等目标，JVM 会自动进行适应性调整，例如下面参数：-XX:MaxGCPauseMillis=value，-XX:GCTimeRatio=N // GC时间和用户时间比例 = 1 / (N+1)
    - G1 GC ：

        ![G1](https://raw.githubusercontent.com/MichaelYgZhang/michaelygzhang.github.io/master/images/java-gc-g1.png)

        - 在新生代，G1 采用的仍然是并行的复制算法，所以同样会发生 Stop-The-World 的暂停。
        - 在老年代，大部分情况下都是并发标记，而整理（Compact）则是和新生代 GC 时捎带进行，并且不是整体性的整理，而是增量进行的。
        - 这是一种兼顾吞吐量和停顿时间的 GC 实现，是 Oracle JDK 9 以后的默认 GC 选项。G1 可以直观的设定停顿时间的目标，相比于 CMS GC，G1 未必能做到 CMS 在最好情况下的延时停顿，但是最差情况要好很多。G1 GC 仍然存在着年代的概念，但是其内存结构并不是简单的条带式划分，而是类似棋盘的一个个 region。Region 之间是复制算法，但整体上实际可看作是标记 - 整理（Mark-Compact）算法，可以有效地避免内存碎片，尤其是当 Java 堆非常大的时候，G1 的优势更加明显。G1 吞吐量和停顿表现都非常不错，并且仍然在不断地完善，与此同时 CMS 已经在 JDK 9 中被标记为废弃（deprecated），所以 G1 GC 值得你深入掌握。
        - 并发运行；可作用于新生代或老年代；标记-整理算法+复制算法；响应速度优先；面向服务端应用。
        - g1垃圾为啥时间可控的？
            - 可以有计划地避免在Java堆的进行全区域的垃圾收集；G1跟踪各个Region获得其收集价值大小，在后台维护一个优先列表；每次根据允许的收集时间，优先回收价值最大的Region（名称Garbage-First的由来）；这就保证了在有限的时间内可以获取尽可能高的收集效率；  
        - [资料](http://www.cnblogs.com/wxw7blog/p/7221725.html)
        - [资料-2](http://zhaoyanblog.com/archives/397.html)

- 如何主动进行GC？
    - system.gc()



### JMM
- `JMM内存模型`？
    - JMM内存模型: <https://juejin.cn/post/6926715555760046087>
- 线程安全 与 JVM内存模型之间的关系？
    - 如果你的代码所在的进程中有多个线程在同时运行，而这些线程可能会同时运行这段代码。如果每次运行结果和单线程运行的结果是一样的，而且其他的变量的值也和预期的是一样的，就是线程安全的。    

### JVM调优

![Linux Opt](https://raw.githubusercontent.com/MichaelYgZhang/michaelygzhang.github.io/master/images/computer-opt.png)

- JVM调优思路：
    - 基本的调优思路可以总结为：
        - 理解应用需求和问题，确定调优目标。假设，我们开发了一个应用服务，但发现偶尔会出现性能抖动，出现较长的服务停顿。评估用户可接受的响应时间和业务量，将目标简化为，希望 GC 暂停尽量控制在 200ms 以内，并且保证一定标准的吞吐量。
        - 掌握 JVM 和 GC 的状态，定位具体的问题，确定真的有 GC 调优的必要。具体有很多方法，比如，通过 jstat 等工具查看 GC 等相关状态，可以开启 GC 日志，或者是利用操作系统提供的诊断工具等。例如，通过追踪 GC 日志，就可以查找是不是 GC 在特定时间发生了长时间的暂停，进而导致了应用响应不及时。
        - 这里需要思考，选择的 GC 类型是否符合我们的应用特征，如果是，具体问题表现在哪里，是 Minor GC 过长，还是 Mixed GC 等出现异常停顿情况；如果不是，考虑切换到什么类型，如 CMS 和 G1 都是更侧重于低延迟的 GC 选项。
        - 通过分析确定具体调整的参数或者软硬件配置。
        - 验证是否达到调优目标，如果达到目标，即可以考虑结束调优；否则，重复完成分析、调整、验证这个过程。

- `项目中JVM调优都调整那些参数`？回收器？内存大小？CMS分代比例？日志打印信息？压缩针？
- [资料-Java优化](https://michaelygzhang.github.io/java/2018/02/09/java-%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96.html)    
- 问题排除 jvm内存溢出？CPU100%？堆内存溢出？栈异常死锁？涉及哪些Linux命令？机器负载高，怎么办，用那些命令可以解决。
    - [资料](http://masutangu.com/2017/02/linux-performance-monitor/)   

#### ClassLoader?比如根ClassLoader？JVM级别的ClassLoader？系统扩展级别的ClassLoader？要非常具体和详细的描述？
- Bootstrap class loader(负责加载虚拟机的核心类库，如 java.lang.* ,JAVA_HOME\lib 目录中的，或通过-Xbootclasspath参数指定路径中的，且被虚拟机认可（按文件名识别，如rt.jar）的类。)C/C++编写 
-> Extension class loader:这个加载器加载出了基本 API 之外的一些拓展类,JAVA_HOME\lib\ext 目录中的，或通过java.ext.dirs系统变量指定路径中的类库。
-> AppClass Loader: 应用/程序自定义类加载器,负责加载用户路径（classpath）上的类库。
- 双亲委派机制: 系统类防止内存中出现多份同样的字节码; 保证Java程序安全稳定运行;

#### Class.forName()和ClassLoader.loadClass()区别
- Class.forName()：将类的.class文件加载到jvm中之外，还会对类进行解释，执行类中的static块；
- ClassLoader.loadClass()：只干一件事情，就是将.class文件加载到jvm中，不会执行static中的内容,只有在newInstance才会去执行static块。
- Class.forName(name, initialize, loader)带参函数也可控制是否加载static块。并且只有调用了newInstance()方法采用调用构造函数，创建类的对象 。

#### ClassNotFoundException 与 NoClassDeFoundError 的区别
- [资料-1](http://blog.csdn.net/bryantlmm/article/details/78118763)
- [资料-2](https://www.cnblogs.com/hnucdj/p/4288369.html)

# Java框架

## Spring
- `事务传播机制`
    - 原理
    - `回滚机制`？回滚异常都有那些？如何进行处理？
- Spring中用到的设计模式
- Interceptor，filter各自的使用场景
- `Spring启动流程`
    - Spring启动流程: <https://www.cnblogs.com/shamo89/p/8184960.html>
- Spring注解声明和xml方式声明的区别？
- `AOP的实现原理`？
    - 2种动态代理模式？
    - 资料：<https://cliffmeyers.com/blog/2006/12/29/spring-aop-cglib-or-jdk-dynamic-proxies.html>
    - 动态代理: <https://www.zhihu.com/question/20794107>
- `如何解决循环依赖问题？如果是构造方法注入能解决循环引用吗`？
    - 3级缓存？
- `大事务优化`？
- `AOP/IOC`
- `Spring Bean创建过程`？
- spring容器启动原理？ [资料](http://www.majunwei.com/view/201708231840127244.html)
- Spring AOP两种实现方式？
- SprintBoot与SpringMVC的区别?


## SpringCloud


### Ribbon 负载均衡
- `负载均衡策略`
    - 轮训，随机。。TODO


## Mybatis
- `$ vs # 区别`？
    - https://www.cnblogs.com/williamjie/p/11188716.html

## Tomcat
- tomcat与spring容器关联的点？ web.xml?

## HttpClient
- HttpClient 连接池实现？连接池原理，设计时的注意事项？连接池中连接都是在发起请求的时候建立，并且都是长连接
    1. 降低延迟：如果不采用连接池，每次连接发起Http请求的时候都会重新建立TCP连接(经历3次握手)，用完就会关闭连接(4次挥手)，如果采用连接池则减少了这部分时间损耗，别小看这几次握手，本人经过测试发现，基本上3倍的时间延迟
    2. 支持更大的并发：如果不采用连接池，每次连接都会打开一个端口，在大并发的情况下系统的端口资源很快就会被用完，导致无法建立新的连接
- 连接池中连接都是在发起请求的时候建立，并且都是长连接;
- 连接池内的连接数其实就是可以同时创建多少个 tcp 连接，httpClient 维护着两个 Set，leased(被占用的连接集合) 和 avaliabled(可用的连接集合) 两个集合，释放连接就是将被占用连接放到可用连接里面。


> Java相关资料库
- https://mp.weixin.qq.com/s?__biz=MzkwMDE1MzkwNQ==&mid=2247495973&idx=1&sn=a18538bc3d9a3e92db729b4d347efb84&chksm=c04ae67bf73d6f6d6381cd21f164f5c9192215040f91f7403e20acb8d54976bc033e7c5dda05&token=549878447&lang=zh_CN#rd
- https://www.cnblogs.com/williamjie/p/11139302.html


# 中间件

## Zookeeper
### zookeeper节点类型，选主机制? 主从怎么做？有何问题？
- [资料](https://michaelygzhang.github.io/destributed/2017/01/18/paxos-to-zookeeper.html)

## Eureka
- TODO

## Nacos

## Etcd

## MQ
- MQ如何实现延迟队列？
- 死信的使用场景？
- `幂等消费问题`

### mq如何保证幂等
- a,mq,落地db,b。a生成一个业务相关全局唯一biz_id,a发给mq,mq落地db,返回给a说成功了，若失败a重试,mq生成内部一个唯一msg_id业务无关的,这样保证b接受的幂等,会有定时删除重复的数据。b接受消息时，根据a生成的id,判断以此保证b幂等，mq重复策略，可以是1s,3s,5s重复发送机制。

### 环行队列实现延迟消息，可以很好避免定时任务的扫库的效率低的问题? RingBuffer?

- [资料-cache](https://timyang.net/data/cache-failure/)


### kafka
- kafka <https://www.cnblogs.com/williamjie/p/11102282.html>
- `顺序消息是如何实现的？局部顺序？全局顺序`？
- `消费挤压如何处理`
- `如何保证消息不丢失`
    - 怎么做？参数是什么？
- `Rebalance过程`
- `消费失败处理，消息积压问题处理`？
- Leader选举机制？
    - https://honeypps.com/mq/deep-interpretation-of-kafka-data-reliability/
    - https://www.infoq.cn/article/depth-interpretation-of-kafka-data-reliability


## Elasticsearch
- 常见ES问题？
- `ES设计时，索引如何设计的`？
- 索引的存储和查询原理和步骤？
- 如何进行优化慢查询？深度分页问题如何解决？


## LeafId
### 设计一个全局ID生成器，怎么设计？性能/有序性/?
- <http://vesta.cloudate.net/vesta/doc/%E7%BB%9F%E4%B8%80%E5%8F%91%E5%8F%B7%E5%99%A8(Vesta)%20-%20%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1.html>

## RPC
- 框架

### 设计一个RPC框架需要关注哪些？ 比如像Dubbo？
- [资料-DongFangHongRpc](https://github.com/MichaelYgZhang/DongFangHongRpc)

- `RPC原理`？
- `负载均衡`？
- `容错策略`？
- Pigeon
- Dubbo
- GRPC
- `序列化`

### Google Protocol Buffer 高性能原因？ 
- [资料-protobuf-1](https://www.ibm.com/developerworks/cn/linux/l-cn-gpb/index.html)
- [资料-protobuf-2](http://masutangu.com/2016/09/talk-about-protobuf/)
- [资料-protobuf-3](https://yq.aliyun.com/wenji/article_2594-page_3)

- thirft

# 存储

## MySQL
- https://mp.weixin.qq.com/s?__biz=MzAxNTM4NzAyNg==&mid=2247491894&idx=1&sn=05e52c044f20aeda15d6e0d046ffda4d&chksm=9b8671cbacf1f8ddffd0759eb69f7fe39e466273b1c895ac1620eada69c9fafcf46c8cb344f7&scene=132#wechat_redirect
- https://mp.weixin.qq.com/s?__biz=MzU3MTAzNTMzMQ==&mid=2247485938&idx=1&sn=1a3525cb38e97f67f513dbbbf6cbd732&chksm=fce7125ecb909b48135cf8fc0be669cbbaedddb00965fd2aac17c18533a516d4004f26efba62&token=1066766011&lang=zh_CN#rd
- http://blog.codinglabs.org/articles/theory-of-mysql-index.html
- https://www.cnblogs.com/williamjie/p/11081592.html
- https://www.cnblogs.com/williamjie/p/11080893.html
- https://www.cnblogs.com/williamjie/p/11081081.html
- https://baijiahao.baidu.com/s?id=1598257553176708891&wfr=spider&for=pc
- http://neoremind.com/2020/01/inside_innodb_file/
- https://www.cnblogs.com/yyjie/p/7486975.html
- 架构
- 聚集索引 vs 非聚聚索引？
- filesort？
- `索引数据结构`
    - Hash, 精确匹配查询
    - B Tree, 数据在中间节点和叶子节点，内存一页可以加载的数据比较少
    - B+Tree, 数据只存储在叶子节点, 内存可以加载比较多的中间节点数据, 从而可以减少磁盘IO, 可以支持范围查询
    - 为什么这么设计？
- mysql InnoDB为什选择自增主键做主键？
    - 聚簇索引每个页面装载因子（innodb 默认为 15/16）
- 双写机制？
- `redolog，undolog，binlog`这几个文件都有什么用？
- `MVCC` Multi-Versioning Concurrency Control
    - InnoDB 的 MVCC, 是通过在每行记录后面保存两个隐藏的列来实现的, 这两个列，分别保存了这个行的创建时间，一个保存的是行的删除时间。这里存储的并不是实际的时间值, 而是系统版本号 (可以理解为`事务的ID`)，每次开始一个新的事务，系统版本号就会自动递增；当删除一条数据的时候，该数据的删除时间列就会存上当前事务的版本号 ；事务开始时刻的系统版本号会作为事务的 ID；
    - SELECT InnoDB会根据以下两个条件检查每条记录：
        - InnoDB只会查找版本早于当前事务版本的数据行（创建时间系统版本号小于或等于当前事务版本号），这样可以确保事务读取到的数据要么是本次事务开始之前就已经存在的，要么是当前事务本身做的修改；
        - 行的删除版本要么是未定义，要么大于当前事务的版本号，这样确保了事务读取到的行，在事务开始之前未被删除；
        - 以上两个条件同时满足的情况下，才能作为结果返回；
        - InnoDB 执行 UPDATE,实际上是新插入的一行数据 ，并保存其创建时间（事务ID）为当前事务的系统版本号，同时保存当前事务系统版本号到需要UPDATE的行的删除时间(事务ID） 
    - 当前读
        - 像select lock in share mode(共享锁), select for update ; update, insert ,delete(排他锁)这些操作都是一种当前读，为什么叫当前读？就是它读取的是记录的最新版本，读取时还要保证其他并发事务不能修改当前记录，会对读取的记录进行加锁
    - 快照读
        - 像不加锁的select操作就是快照读，即不加锁的非阻塞读；快照读的前提是隔离级别不是串行级别，串行级别下的快照读会退化成当前读；之所以出现快照读的情况，是基于提高并发性能的考虑，快照读的实现是基于多版本并发控制，即MVCC,可以认为MVCC是行锁的一个变种，但它在很多情况下，避免了加锁操作，降低了开销；既然是基于多版本，即快照读可能读到的并不一定是数据的最新版本，而有可能是之前的历史版本ßßß
    - 说白了MVCC就是为了实现读-写冲突不加锁，而这个读指的就是快照读, 而非当前读，当前读实际上是一种加锁的操作，是悲观锁的实现
- `ACID`
    - ACID是什么？
    - InnoDB引擎如何保障ACID？
- `事务隔离`

    |事务隔离级别|说明|问题|
    |:--|:--|:--|
    |未提交读 Read UnCommitted| 如果一个事务读到了另一个未提交事务修改过的数据称为未提交读。这种读到另一个未提交事务修改的数据场景称为`脏读`|脏读，不可重复读，幻读|
    |读已提交 Read Committed| 如果一个事务只能读到另一个已经提交的事务修改过的数据，并且其他事务每对该数据进行一次修改并提交后，该事务都能查询得到最新值，那么这种隔离级别就称之为已提交读。每次事务A提交之后都能被事务B读到最新的值，这种现象称为`不可重复读`|不可重复读，幻读|
    |`可重复读 Repeatable Read`默认隔离级别| 一个事务只能读到另一个已经提交的事务修改过的数据，但是第一次读过某条记录后，即使其他事务修改了该记录的值并且提交，该事务之后再读该条记录时，读到的仍是第一次读到的值，而不是每次都读到不同的数据。那么这种隔离级别就称之为可重复读|幻读，但在Mysql实现的Repeatable read配合gap锁不会出现幻读！|
    |串行化Serializable|以上3种隔离级别都允许对同一条记录进行读-读、读-写、写-读的并发操作，如果我们不允许读-写、写-读的并发操作，可以使用SERIALIZABLE隔离级别|避免所有情况|

    - 幻读：幻读仅专指“新插入的行”。通过 next-key lock解决。(1)产生幻读的原因是，行锁只能锁住行，但是新插入记录这个动作，要更新的是记录之间的“间隙”。因此，为了解决幻读，InnoDB引入间隙锁。(2)Gap lock间隙锁在可重复读级别下才有效 (3)间隙锁和行锁合称 next-key lock，每个 next-key lock 是前开后闭区间。
        - 事务A 按照一定条件进行数据读取， 期间事务B 插入了相同搜索条件的新数据，事务A再次按照原先条件进行读取时，发现了事务B 新插入的数据 称为幻读
        - 注意区别：如果事务A 按一定条件搜索， 期间事务B 删除了符合条件的某一条数据，导致事务A 再次读取时数据少了一条。这种情况归为 不可重复读
    - 当前读就是读取最新版本的数据。如果事务中都使用快照读，那么就不会产生幻读现象，但是快照读和当前读混用就会产生幻读。
        - 什么情况下使用的是快照读：（快照读，不会加锁）
            - 一般的 select * from .... where ... 语句都是快照读；
        - 什么情况下使用的是当前读：（当前读，会在搜索的时候加锁）
            - select * from .... where ... for update 
            - select * from .... where ... lock in share mode 
            - update .... set .. where ... 
            - delete from. . where ..
        - 当前读可以解决幻读问题，当前读为什么会阻塞新数据的插入，主要是间隙锁的加锁机制。
    
    - 默认什么隔离级别？
        - `可重复读 Repeatable Read`
    - RR，每一种隔离级别为解决什么问题？
    - [DB-事务](https://michaelygzhang.github.io/db/2016/09/25/mysql-transaction.html)
- `锁`
    - 锁种类？
    - 乐观锁，共享锁，悲观锁，排他锁？
    - 记录锁
    - 间隙锁grap锁
        - 将两行记录间的空隙加上锁，阻止新记录的插入；这个锁称为间隙锁。
    - 表锁
    - 意向锁？
    - 死锁
    - 间隙锁插入意向锁？
    - `死锁分析`？死锁解决处理？
    - 场景举例？
    - 2PL，两段锁，两阶段加锁协议:主要用于单机事务中的一致性与隔离性。在对记录更新操作或者(select for update、lock in share model)时，会对记录加锁(有共享锁、排它锁、意向锁、gap锁、nextkey锁等等),
        - 资料1: <https://blog.csdn.net/qq4165498/article/details/76855139>
        - 资料2: <https://segmentfault.com/a/1190000012513286>
- `索引失效举例`？
    - 非最左匹配
    - not in 
    - 函数
    - 运算 加减乘除
- limit分页慢？
    - 原因是什么？
    - 如何解决？
- update 过程分析如下？update T set c=c+1 where ID=2;

```
1.首先客户端通过tcp/ip发送一条sql语句到server层的SQL interface
2.SQL interface接到该请求后，先对该条语句进行解析，验证权限是否匹配
3.验证通过以后，分析器会对该语句分析,是否语法有错误等
4.接下来是优化器器生成相应的执行计划，选择最优的执行计划
5.之后会是执行器根据执行计划执行这条语句。在这一步会去open table,如果该table上有MDL，则等待。
如果没有，则加在该表上加短暂的MDL(S)
(如果opend_table太大,表明open_table_cache太小。需要不停的去打开frm文件)
6.进入到引擎层，首先会去innodb_buffer_pool里的data dictionary(元数据信息)得到表信息
7.通过元数据信息,去lock info里查出是否会有相关的锁信息，并把这条update语句需要的
锁信息写入到lock info里(锁这里还有待补充)
8.然后涉及到的老数据通过快照的方式存储到innodb_buffer_pool里的undo page里,并且记录undo log修改的redo
(如果data page里有就直接载入到undo page里，如果没有，则需要去磁盘里取出相应page的数据，载入到undo page里)
9.在innodb_buffer_pool的data page做update操作。并把操作的物理数据页修改记录到redo log buffer里
由于update这个事务会涉及到多个页面的修改，所以redo log buffer里会记录多条页面的修改信息。
因为group commit的原因，这次事务所产生的redo log buffer可能会跟随其它事务一同flush并且sync到磁盘上
10.同时修改的信息，会按照event的格式,记录到binlog_cache中。(这里注意binlog_cache_size是transaction级别的,不是session级别的参数,
一旦commit之后，dump线程会从binlog_cache里把event主动发送给slave的I/O线程)
11.之后把这条sql,需要在二级索引上做的修改，写入到change buffer page，等到下次有其他sql需要读取该二级索引时，再去与二级索引做merge
(随机I/O变为顺序I/O,但是由于现在的磁盘都是SSD,所以对于寻址来说,随机I/O和顺序I/O差距不大)
12.此时update语句已经完成，需要commit或者rollback。这里讨论commit的情况，并且双1
13.commit操作，由于存储引擎层与server层之间采用的是内部XA(保证两个事务的一致性,这里主要保证redo log和binlog的原子性),
所以提交分为prepare阶段与commit阶段
14.prepare阶段,将事务的xid写入，将binlog_cache里的进行flush以及sync操作(大事务的话这步非常耗时)
15.commit阶段，由于之前该事务产生的redo log已经sync到磁盘了。所以这步只是在redo log里标记commit
16.当binlog和redo log都已经落盘以后，如果触发了刷新脏页的操作，先把该脏页复制到doublewrite buffer里，把doublewrite buffer里的刷新到共享表空间，然后才是通过page cleaner线程把脏页写入到磁盘中

二阶段提交理解:
1 prepare阶段 2 写binlog 3 commit
当在2之前崩溃时
重启恢复：后发现没有commit，回滚。备份恢复：没有binlog 。
一致
当在3之前崩溃
重启恢复：虽没有commit，但满足prepare和binlog完整，所以重启后会自动commit。备份：有binlog. 一致

redo是物理的，binlog是逻辑的；现在由于redo是属于InnoDB引擎，所以必须要有binlog，因为你可以使用别的引擎
保证数据库的一致性，必须要保证2份日志一致，使用的2阶段式提交；其实感觉像事务，不是成功就是失败，不能让中间环节出现，也就是一个成功，一个失败
如果有一天mysql只有InnoDB引擎了，有redo来实现复制，那么感觉oracle的DG就诞生了，物理的速度也将远超逻辑的，毕竟只记录了改动向量
binlog几大模式，一般采用row，因为遇到时间，从库可能会出现不一致的情况，但是row更新前后都有，会导致日志变大
最后2个参数，保证事务成功，日志必须落盘，这样，数据库crash后，就不会丢失某个事务的数据了
其次说一下，对问题的理解
备份时间周期的长短，感觉有2个方便
首先，是恢复数据丢失的时间，既然需要恢复，肯定是数据丢失了。如果一天一备份的话，只要找到这天的全备，加入这天某段时间的binlog来恢复，如果一周一备份，假设是周一，而你要恢复的数据是周日某个时间点，那就，需要全备+周一到周日某个时间点的全部binlog用来恢复，时间相比前者需要增加很多；看业务能忍受的程度
其次，是数据库丢失，如果一周一备份的话，需要确保整个一周的binlog都完好无损，否则将无法恢复；而一天一备，只要保证这天的binlog都完好无损；当然这个可以通过校验，或者冗余等技术来实现，相比之下，上面那点更重要

Binlog有两种模式，statement 格式的话是记sql语句， row格式会记录行的内容，记两条，更新前和更新后都有。
```


- SQL执行过程
    - 查询器
    - 优化器，缓存
    - 执行引擎
        - Innodb
        - MyISAM
- `SQL优化`
    - 慢SLQ分析步骤？
    - 慢SQL优化案例？
    - `explain`  参数
    - 资料1 <https://zhuanlan.zhihu.com/p/76494612>
    - 资料2 <https://tech.meituan.com/>

- 大数据量如何做分布式存储？分库分表？如何分怎么设计？还是利用HDFS？
- 分库分表查询，业务拼装，多线程查询，热点数据放一起，冗余数据，防止攻击接口幂等，分库分表事务？
- 比如找第200页数据每页5条，三个库，怎么查？如果查询维度很多该怎么办?

```html
1 order by time offset x limit y 改写为offset 0 limit x+y 内存中排序，少可以多性能差
2 禁止跳页，只能顺序翻页，记录maxtime, order by time where time
> maxtime, limit y 每次只返回一页数据
3 二次查询法
offset x\n limit y ,n 数据个数,
找到mintime,order by time betwwen mintime and maxtime,第一次取出的，设置虚拟mintime,找到全局offset,因为本来就按时间排序，得到全局offset,
```

```sql
悲观锁：
悲观锁的实现，往往依靠数据库提供的锁机制（也只有数据库层提供的锁机制才能真正保证数据访问的排他性，否则，即使在本系统中实现了加锁机制，也无法保证外部系 
统不会修改数据）。例如： 
select * from table_name where id = ‘xxx’ for update; 
这样查询出来的这一行数据就被锁定了,在这个update事务提交之前其他外界是不能修改这条数据的，但是这种处理方式效率比较低，一般不推荐使用。
```

## Redis
- `redis高性能原因`？
- `数据一致性问题`
    - 监听binlong
- `缓存中的问题以及解决方案`
    - 穿透
    - 击穿: 更新DB加互斥锁，其他线程等待。
    - 雪崩？不过期，随机，降级
- `redis持久化`
    - RDB
    - AOF
- `Redis数据结构和使用场景`
- `redis扩容机制`？
- `锁`
    - 分布式锁实现，有什么问题？是否有更好的解决方案？
    - setnx, px
    - 正确使用锁姿势 <https://www.cnblogs.com/williamjie/p/9395659.html>
    - 锁续租问题？
- `集群`
    - `主从 + 哨兵`
        - 如何选主？如何调度？
    - 集群
    - 公司集群方式？几主几丛？
    - 主从同步机制？
- `缓存击穿应急方案`？
- `大key大value问题`
- 原子命令？
- `布隆过滤器`？
- `zset`？
- 资料1: <https://www.cnblogs.com/williamjie/p/11080889.html>

### Redis VS Memcached 优缺点？ 如何选型？
- [redisVSMemcached](https://michaelygzhang.github.io/destributed/2018/01/26/redis-memcached.html)

### redis高效点？redis数据结构？Redis为什么高效,原理是什么，为什么使用跳表结构存储？持久化实现方式？
- [redis源码](https://github.com/menwengit/redis_source_annotation)



## HDFS

## HBase

## 分库分表
- 如何进行？
- 解决什么问题？
- 怎么改造的？
- `Zebra`
- 分库分表使用场景，解决什么问题？
- 如何进行分库分表
- 分库分表一般都是跟随者业务量来进行的，改造过程会有什么坑吗？

# 分布式架构相关

## 分布式原理
- 分布式系统的思想
    - [资料](https://coolshell.cn/articles/10910.html)
- `BASE`
- `CAP`

## 分布式事务 2PC, 3PC, TCC
- 2PC，3PC，阿里的TCC？是否还有？核心思想如何实现的？分布式事务中的关键点有哪些？ 2PC，3PC，TCC分别都有哪些优缺点？ 底层如何实现？看源码？ 是否还有更优秀的分布式事务框架？
- 2PC
- 3PC
- TCC
- [资料](http://www.infoq.com/cn/articles/solution-of-distributed-system-transaction-consistency)

## 分布式相关算法

### `Raft`

### Paxos

### `一致性Hash`

# 服务设计和服务治理
- processOn总结: <https://www.processon.com/view/5990ed4ee4b06df72659f1fd#map>

## 服务设计

## DDD
- 读多写少
- 读少写多
- 抽象思维
- 可扩展性
- 微服务架构
- `服务性能度量和优化思考`
- 常见架构问题
    - 服务出现大量接口超市的问题排查和处理？
    - 分布式锁问题？分布式锁怎么实现的？锁的各种使用场景？需要注意什么问题？
- `系统高可用`
    - 事前
    - 事中
    - 事后
    - 设计时考虑如果当前业务出现错误如何更好恢复？自动恢复能力？
    - 服务降级，容错，号码运营商降级，服务本身降级，如果所有运营商都出现问题，反真实号码，imc出现问题，走本地缓存，最后是服务恢复。
    - 隔离，幂等，异步，超时，服务降级？
    - 高可用服务，请求限流器表每分钟每个用户的请求量，并发请求限流器，抛弃非关键api,处理关键api机制，令牌算法，注意可随时调控。限流器不应该影响到正常的业务，被限流的请求注意文案，可开启或关闭限流器。
    - 重试时注意重试次数？并发量与QPS之间的关联关系？
- `系统高性能`
- 系统可扩展
- `系统可伸缩`

## 服务治理

### 分布式链路追踪
- Mtrace

### `幂等问题以及解决方案`
#### 接口幂等事如何实现的？
- [API接口设计安全性](http://www.jianshu.com/p/c6518a8f4040)

```java
幂等：
Bool  withdraw(account_id, amount)
 ——>
 int create_ticket(); //创建唯一id  
bool idempotent_withdraw(ticket_id, account_id, amount);
幂等设计：服务端确保生成唯一标识符。
```



### 唯一id问题

### `分布式锁`

#### Redis实现

#### ZK实现

#### MySQL实现

### `熔断`

#### `资源隔离之术`
- Hystrix
    - 信号量隔离 VS 线程池隔离

### `限流`
- 常见限流算法和优缺点？
    - 令牌桶，等 <https://xie.infoq.cn/article/32606ec229eb96f3bb4b295ee>
- 布隆过滤器

### 多级缓存
- TODO


### `压测`
- 为什么做？目的？怎么做？事前准备什么？中间过程是什么？事后总结？
- 压测工具？


### `服务监控告警`
- 服务稳定性保障？
- 巡检？


### 大数据
- Hadoop
- Hive
- Spark


### DevOps
- Docker
- Kubernetes
- jekines


# `设计模式`
- 创建型模式，是对对象创建过程的各种问题和解决方案的总结，包括5种：
    - 工厂模式（Factory）
    - 抽象工厂模式（Abstract Factory）
    - 单例模式（Singleton）
    - 构建器模式（Builder）
    - 原型模式（ProtoType）
- 结构型模式，是针对软件设计结构的总结，关注于类、对象继承、组合方式的实践经验。常见的结构型模式，包括7种：
    - 桥接模式（Bridge）
    - 适配器模式（Adapter）
    - 装饰者模式（Decorator）
    - 代理模式（Proxy）
    - 组合模式（Composite）
    - 外观模式（Facade）
    - 享元模式（Flyweight）
- 行为型模式，是从类或对象之间交互、职责划分等角度总结的模式。比较常见的行为型模式有
    - 策略模式（Strategy）
    - 解释器模式（Interpreter）
    - 命令模式（Command）
    - 观察者模式（Observer）
    - 迭代器模式（Iterator）
    - 模板方法模式（Template Method）
    - 访问者模式（Visitor）
    - 责任链模式（Chain of Responsibility）
    - 状态模式（State）
    - 中介模式（Mediator）
    - 备忘录（Memento）

# 工程能力

## 代码质量

## maven, jar包加载顺序, jar包排包问题
- Maven-jar包冲突如何处理？
    - 子pom > 父pom
    - 浅层依赖 > 深层依赖
    - 声明前 > 声明后

## Git
- git rebase vs git merge

# `问题排查方面`

## CPU负载问题
- CPU负载高如何排查？  遇到的case：服务注册与发现 + 服务器本身可能性能不足导致
    - CPU负载定义是什么？哪些因素可能导致CPU负载变高？
    - 如何找到CPU占用最高的线程？ 
        - 资料: <https://juejin.cn/post/6927291610732429325>
    - top 得到cpu使用率最高的进程 pid
    - top -H -p$pid 在进程下找到使用率比较高的线程号
    - top -Hp pid shift +p 按cpu使用情况排序 
    - shift +m 按照内存使用情况排序
    - Printf %x $tid  输出 十六进制 线程id
    - jstack $pid | grep $tip 十六进制数据，ps：如果线上没有权限需要申请sudo 权限


## 内存泄漏问题
- 如何使用dump内存
    - jmap -dump:format=b,file=dumpFileName pid
    - 举例子：jmap -dump:format=b,file=/tmp/dump.dat 21711 
- 内存泄漏问题？


## 问题排查工具
- MAT <https://juejin.cn/post/6911624328472133646>
- 火焰图 <http://neoremind.com/2017/09/%e4%bd%bf%e7%94%a8%e7%81%ab%e7%84%b0%e5%9b%be%e5%81%9a%e6%80%a7%e8%83%bd%e5%88%86%e6%9e%90/>


# 项目总结

## 项目介绍, 架构图,分析架构设计原因
- 框架分层
- 框架思考
- 框架总结
- 数据层面
- 监控告警


## 遇到的问题和挑战,如何进行处理和解决的？最后进行总结提炼心得体会或者方法伦？SOP

## 系统是否还有什么问题未处理和解决？

# 经验教训
- 服务迁移的坑？服务注册与发现Zookeeper目前只发现到 service，不到方法层面，导致服务打错服务调用自己的服务了。


--- 

技术问题套路：原理是什么？可以解决什么问题？怎么用的？为什么这么用？是否还有其他更好的方案？

沟通能力
详细描述负责项目的功能和服务，主要解决业务场景和解决的问题，是否熟悉上下游的业务。
思辩能力
针对当前的业务现状的反思，性能的瓶颈，业务的瓶颈。针对瓶颈的解决方案是什么？举一反三说。
专业能力
java基础，线上问题排查经验，踩过什么坑，如何进行发现，解决的？
项目中使用什么中间件（zk，redis，kafka，es）进行深入研究？技术深度和学习能力如何？
数据相关，慢sql排查，索引等
工程质量，稳定性保障工作，如何进行，能否从事前，事中，事后维度进行考虑？


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



# `算法相关`
- 常见笔试题 <https://blog.csdn.net/ym123456677/article/details/112260079>

## 优化题: 
```js
规则:
1, A,B,C
2, C,D
3, E,F
....

输入: ACD -> true; ACEF -> true; 任意命中一个规则返回true/false;
TODO
```



## 算法
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

## 笔试题

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


- 二叉树的遍历，深度/广度/查找

```java

static class TreeNode{
        Object val = null;
        TreeNode left = null;
        TreeNode right = null;
        public TreeNode(Object val) {
            this.val = val;
        }

        public TreeNode(TreeNode left, TreeNode right, Object val) {
            this.left = left;
            this.right = right;
            this.val = val;
        }
    }
    /**
    *   🌲结构
    *                   A
    *           B             C
    *      D        E
    *         F
    *      G    H   
    */
    static TreeNode builderTree(){
        TreeNode G = new TreeNode(null, null, 'G');
        TreeNode H = new TreeNode(null, null, 'H');
        TreeNode F = new TreeNode(G, H, 'F');
        TreeNode D = new TreeNode(null, F, 'D');
        TreeNode E = new TreeNode(null, null, 'E');
        TreeNode B = new TreeNode(D, E, 'B');
        TreeNode C = new TreeNode(null, null, 'C');
        TreeNode A = new TreeNode(B, C, 'A');
        return A;
    }
    
    /**
    *   ->A->B->D->F->G->H->E->C
    */
    static void 深度优先遍历(TreeNode root) {
        Stack<TreeNode> stack = new Stack<>();//为什么用栈？先进后出特点
        if (root != null){
            stack.push(root);
        } else {
            return;
        }
        while (!stack.empty()) {
            TreeNode treeNode = stack.pop();
            System.out.print("->"+  treeNode.val);

            if (treeNode.right != null) { //注意是先右边,为什么？因为栈先进后出
                stack.push(treeNode.right);
            }

            if (treeNode.left != null) {
                stack.push(treeNode.left);
            }
        }
    }
    /** 
    * ->A->B->C->D->E->F->G->H 
    */
    static void 广度优先遍历(TreeNode root) {
        Queue<TreeNode> queue = new ArrayBlockingQueue<TreeNode>(10);//先进先出特点
        if (root != null) {
            queue.add(root);
        } else {
            return;
        }
        while (!queue.isEmpty()) {
            TreeNode treeNode = queue.poll();
            System.out.print("->"+ treeNode.val);
            if (treeNode.left != null) {
                queue.add(treeNode.left);
            }
            if (treeNode.right != null) {
                queue.add(treeNode.right);
            }
        }

    }

    //二叉树查询就很简单了，在遍历的基础上，加判断条件就可以了，比如:
    static TreeNode 深度优先遍历_查询(TreeNode root, Object target) {
        Stack<TreeNode> stack = new Stack<>();//为什么用栈？先进后出特点
        if (root != null){
            stack.push(root);
        } else {
            return null;
        }
        while (!stack.empty()) {
            TreeNode treeNode = stack.pop();
            if (treeNode.val.equals(target)) {
                System.out.println("找到了!!");
                return treeNode;
            }
            if (treeNode.right != null) { //注意是先右边,为什么？因为栈先进后出
                stack.push(treeNode.right);
            }

            if (treeNode.left != null) {
                stack.push(treeNode.left);
            }
        }
        return null;
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


## cat xx.log.2017-09-20 | awk -F '(txt=|&client)' '{print $2}'| sort | uniq -c | sort -nr| head -10 > testfile


# 其他资料
- [Java面试极客学院](http://wiki.jikexueyuan.com/project/java-interview-bible/basic-concept.html)
- [资料-1](http://www.bieryun.com/1733.html?spm=a2c4e.11153940.blogcont495584.15.4f1b1491F2IviJ)
- [源码相关-杂](http://www.iocoder.cn/)
- [资料-面试](http://blog.csdn.net/sinat_35512245/article/details/59056120)
- [Google Interview University 一套完整的学习手册帮助自己准备 Google 的面试](https://github.com/jwasham/coding-interview-university/blob/master/translations/README-cn.md)
- [technology-talk](https://github.com/aalansehaiyang/technology-talk)
- [Interview-Notebook](https://github.com/CyC2018/Interview-Notebook)

# 资料
- XXL开源社区项目：<https://www.xuxueli.com/page/projects.html>
- [x] md文档资料: <https://www.jianshu.com/p/8c1b2b39deb0/>

## 临时存储面试资料
- 割肉机面试题目: <https://www.cnblogs.com/williamjie/category/1485042.html>
- Java面试题: <https://www.cnblogs.com/williamjie/p/12532685.html>
- Java面试题: <https://www.cnblogs.com/williamjie/p/11139302.html>
