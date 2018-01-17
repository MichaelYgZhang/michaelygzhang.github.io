---
layout: post
title: Netty 权威指南
excerpt: Netty
category: Java
---

#### 基础篇 走进Java NIO

##### 第1章 Java的I/O演进之路

- Linux网络I/O模型简介
  - 阻塞I/O模型
  - 非阻塞I/O模型
  - I/O复用模型：select/poll
  - 信号驱动I/O模型
  - 异步I/O：与信号驱动模型区别是：信号驱动I/O由内核通知我们何时开始一个I/O操作，异步I/O模型由内核通知我们I/O何时已经完成。
- I／O多路复用技术：目前支持I/O多路复用的系统调用有select、pselect、poll、epoll由于select有一些缺点，所以epoll作了很大改进，总结如下：
  1. 支持一个进程打开的socket描述符(FD)不受限制(仅受限于操作系统的最大文件句柄数)。`cat /proc/sys/fs/file-max` 可以进行察看，这个值跟系统的内存关系比较大。
  2. I／O效率不会随着FD数目的增加而线性下降。
  3. 使用mmap加速内核与用户空间的消息传递。
  4. epoll的API更加简单。
- Java的I/O演进。
  - JDK1.4推出NIO之前都是BIO，BIO简单，性能和可靠性有巨大瓶颈。
  - JDK1.7 NIO2.0

##### 第2章 NIO入门

- 传统的BIO编程。
- 伪异步I/O编程
  - 弊端分析：读写IO都是同步阻塞的，只是对BIO线程模型进行了简单的优化，无法从跟不上解决同步I/O导致的通信线程阻塞问题。
- NIO(Non-block I/O): 以下是NIO类库和相关概念
  - 缓冲区Buffer：包含了一些要写入或者要写出的数据。本质就是字节数组，提供了对数据的结构化访问以及维护读写位置等信息。
    ByteBuffer、CharBuffer、ShortBuffer、IntBuffer、LongBuffer、FloatBuffer、DoubleBuffer。
  - 通道Channel：通过它来读取和写入数据，网络数据通过Channel读取和写入，通道与流的不同之处在于通道是双工的，流只有一个方向。通道可以用于读、写或者同时读写。分为两大类：用于网络读写的SelectableChannel和文档操作FileChannel。
  - 多路复用器Selector：简单来讲，Selector会不断地轮训注册在其上的Channel，如果某个Channel上面有新的TCP连接接入、读写事件，这个Channel就处于就绪状态，会被Selector轮训出来，然后通过SelectionKey可以获取就绪Channel的集合，进行后续的I/O操作。一个多路复用器Selector可以同时轮训多个Channel，由于JDK采用了epoll()代替了传统的select实现，所以它并没有最大连接句柄1024/2048的限制，意味着只需要一个线程负责Selector的轮询就可以接入成千上万的客户端。
- NIO服务端序列图
  1. 打开ServerSocketChannel
  2. 绑定监听地址InetSocketAddress
  3. 创建Selector启动线程
  4. 将ServerSocketChannel注册到Selector，监听
  5. Selector轮询就绪的Key
  6. handleAccept()处理新的客户端接入
  7. 设置新的客户端连接的Socket参数
  8. 向Selector注册监听读操作SelectionKey.OP_READ
  9. handleRead()异步请求消息到ByteBuffer
  10. decode请求消息
  11. 异步写ByteBuffer到SocketChannel

- NIO客户端序列图
  1. 打开SocketChannel
  2. 设置SocketChannel为非阻塞模式，同时设置TCP参数
  3. 异步连接服务端
  4. 判断连接结果，如果成功则调到步骤10，否则5
  5. 向Reactor线程的多路复用器注册OP_CONNECT事件
  6. 创建Selector启动线程
  7. Selector轮询就绪的Key
  8. handerConnect()
  9. 判断连接是否完成，完成步骤10
  10. 向多路复用器注册读事件OP_READ
  11. HandleRead()异步请求消息到ByteBuffer
  12. decode请求消息
  13. 异步写ByteBuffer到SocketChannel

- AIO编程
 - TODO

- 选择Netty而直接使用JDK的NIO类库开发的理由
  1. NIO的类库和API繁杂，使用麻烦，需要熟练掌握Selector,ServerSocketChannel,SocketChannel,ByteBuffer等
  2. 需要具备其他额外的技能做铺垫，例如熟悉Java多线程编程，这是因为NIO编程涉及到Reactor模式，你必须对多线程和网络编程非常熟悉，才能写出高质量的NIO程序。
  3. 可靠性能补齐，工作量和难度都非常大。如客户端面临断链重连，网络闪断，半包读写，失败缓存，网络拥塞和异常码流的处理等问题，NIO编程的特点是功能开发相对容易，但可靠性能力的工作量和难度都非常大。
  4. JDK NIO的BUG。例如epoll bug，导致Selector空轮询，最终导致CPU 100%

- Netty优点：
  1. API简单，开发门槛低
  2. 功能强大，预置了多种编解码功能，支持多种主流协议
  3. 定制能力强，可以通过ChannelHandler对通信框架进行灵活扩展。
  4. 性能高，成熟稳定，修复了以发现的所有JDK NIO bug，不需要再为NIO的bug烦恼
  5. 社区活跃，版本迭代周期短,发现的bug能即时修复，以及更多的新功能加入。
  6. 经历了大规模的商业应用考验，质量得到验证。


#### 入门篇 Netty NIO开发指南

##### 第3章 Netty入门应用

- DEOM

##### 第4章 TCP粘包／拆包问题的解决之道

- TCP粘包／拆包：TCP是个流协议，没有界限的一串数据，没有分界线，TCP底层并不了解上层业务数据的具体含义，它根据TCP缓冲区的实际情况进行包的划分，所以一个完成的包可能会被TCP拆分成多个包发送，也有可能把多个小包封装在一个大的数据包发送，这就是所谓的粘包和拆包问题。

- TCP粘包／拆包发生原因：
  1. 应用程序write写入的字节大小大于套接口发送缓冲区的大小。
  2. 进行MSS大小的TCP分段。
  3. 以太网帧payload大于MTU进行IP分片
- 粘包解决策略：
  1. 消息定长，例如每个报文大小固定长度200字节，如果不够空位补空格。
  2. 在包尾增加回车换行符进行分割，例如FTP协议。
  3. 将消息分为消息头和消息体，消息头中包含表示消息总长度的字段，通常设计思路为消息头的第一个字段使用int32来表示消息的总长度。
  4. 更复杂的应用层协议。

- Netty利用LineBasedFrameDecoder、StringDecoder解决TCP粘包问题。Netty提供了多种编解码器用于处理半包问题。
- LineBasedFrameDecoder的工作原理是它依次遍历ByteBuf中的可读字节，判断是否有'\n'或者'\r\n'，如果有，就以此位置为结束位置，从可读索引到结束位置区间的字节就组成了一行，它是支持配置单行的最大长度。如果连续读取到最大长度后仍然没有发现换行符，就抛出异常，同时忽略之前读到的异常码流。
- StringDecoder的功能非常简单，就是将接收到的对象转换成字符串，然后继续调用后面的handler，LineBasedFrameDecoder+StringDecoder组合就是按行切换的文本解码器。

##### 第5章 分隔符和定长解码器的应用  

- DelimiterBasedFrameDecoder和FixedLengthFramerDecoder前者可以自动完成分隔符做结束标志的消息的解码，后者可以自动完成对定长消息的解码，它们都能解决TCP粘包／拆包导致的半读问题。
- 使用指南：只要将DelimiterBasedFrameDecoder或FixedLengthFramerDecoder添加到对应的ChannelPipeline的起始位置即可。

```java
Bootstrap b = new Bootstrap();
b.group(group).channel(NioSocketChannel.class)
      .option(ChannelOption.TCP_NODELAY, true)
      .handler(new ChannelInitializer<SocketChannel>() {
        @Override
        protected void initChannel(SocketChannel socketChannel) throws Exception {
          ByteBuf delimiter = Unpooled.copiedBuffer("$_".getBytes());
          socketChannel.pipeline().addLast(
            new DelimiterBasedFrameDecoder(1024, delimiter));
          socketChannel.pipeline().addLast(new StringDecoder());
          socketChannel.pipeline().addLast(new EchoClientHandler());  
        }
      });
ChannelFuture f = b.connect(host, port).sync();
f.channel().closeFuture().sync();
```

#### 中级篇 Netty编解码开发指南

##### 第6章 编解码技术

- Java序列化，实现 java.io.Serializable并生成序列ID即可，缺点如下：
  1. 无法跨语言最致命的问题，不同的服务可能语言不同。Java序列化后的字节数组，别的语言无法进行反序列化，事实上目前几乎所有流行的RPC通信框架都没有使用Java序列化作为编解码框架，原因就是无法跨语言。
  2. 序列化后的码流太大。导致存储占空间更大成本就越高，传输更占带宽，导致系统吞吐量低。
  3. 序列化性能低。
  4.

```java
//java序列化 info对象  java.io.ObjectInput或java.io.ObjectOutput进行反序列化和序列化
ByteArrayOutputStream bos = new ByteArrayOutputStream();
ObjectOutputStream os = new ObjectOutputStream(bos);
os.writeObject(info);
os.flush();
os.close;
```

- 评判一个编解码框架主要考虑以下因素：
  1. 是否支持跨语言
  2. 编码后的码流大小
  3. 编解码的性能
  4. 类库是否小巧API使用是否方便
  5. 使用者需要手工开发的工作量和难度

- Protobuf(Google Protocol Buffers):特点如下:
  1. 结构化数据存储(XML, JSON等)，二进制编码
  2. 高效编解码性能
  3. 语言无关、平台无关、扩展性好。
  4. 官方支持Java、C++、Python三种语言
- Protobuf优点如下：
  1. 文本化数据结构，语言和平台无关，适合做异构系统间的集成。
  2. 通过标识字段的顺序，可以实现协议的前向兼容
  3. 自动代码生成，不要手工编写同样数据结构的C++和Java版本
  4. 方便后续管理和维护

- Thrift／JBoss Marshalling

##### 第7章 Java序列化

- 通过使用Netty的Java序列化编解码handler，可以完成POJO的序列化和反序列化。

##### 第8章 Google Protobuf编解码

- 优点：
  1. Google内部长期使用，产品成熟度高；
  2. 跨语言，C++，Java，Python
  3. 编码后的消息更小，更加有利于存储和传输
  4. 编解码性能高
  5. 支持不同协议版本的前后兼容
  6. 支持定义可选和必选字段


##### 第9章 JBoss Marshalling编解码

- 略。

#### 高级篇 Netty多协议开发和应用

##### 第10章 HTTP协议开发应用

- HTTP协议主要特点：
  1. 支持Client/Server模式
  2. 简单--客户向服务器请求服务时，只需指定服务URL，携带必要的请求参数或者消息体
  3. 灵活--HTTP允许传输任意类型的数据对象，传输的内容类型由HTTP消息头中的Content-Type加以标记
  4. 无状态--HTTP协议是无状态协议。
- P232  TODO   

##### 第11章 WebSocket协议开发

##### 第12章 UDP协议开发

##### 第13章 文件传输

##### 第14章 私有协议栈开发

#### Netty高性能之道

- 传统RPC调用采用BIO即阻塞IO，线程模型问题：由于采用同步阻塞IO，会导致每个TCP连接都占用一个线程，由于线程资源是JVM虚拟机非常宝贵的资源，当IO读写阻塞导致无法及时释放时，会导致系统性能急剧下降，严重的甚至会导致虚拟机无法创建新的线程。
- 高性能RPC三个主题
  1. 传输:用什么样的通道将数据传输给对方，BIO、NIO、AIO，IO模型很大程度上决定了框架的性能。
  2. 协议：采用什么样的通信协议，HTTP或者内部私有自定义协议，协议的不同，性能也有不同。相比公有协议，内部私有协议的性能通常可以被设计的更优。
  3. 线程:数据报如何读取，读取后编解码在那个线程进行，编解码后的消息如何派发，Reactor线程模型的不同，对性能影响也非常大。
- 零拷贝。
  1. Netty的接收和发送ByteBuffer采用Direct Buffers，使用堆外直接内存进行Socket读写，不需要进行字节缓冲区的二次拷贝。如果使用传统的堆内存(Heap Buffers)进行Socket读写，JVM会将堆内存Buffer拷贝一份到直接内存中，然后才写入Socket中。相比堆外直接内存，消息在发送过程中多了一次缓冲区的内存拷贝。
  2. Netty提供了组合Buffer对象，可以聚合多个ByteBuffer对象，用户可以像操作一个Buffer那样方便的对组合Buffer进行操作，避免了传统通过内存拷贝的方式将几个小Buffer合并成一个大Buffer。
  3. Netty的文件传输采用了transferTo方法，它可以直接将文件缓冲区数据发送到目标Channel，避免了传统通过循环write方式导致的内存拷贝问题。
- 高效的Reactor线程模型: 有三种。
  1. Reactor单线程模型
  2. Reactor多线程模型
  3. 主从Reactor多线程模型.
    - Reactor单线程模型，指的是所有IO操作都在同一个NIO线程上面完成，NIO线程职责如下:
      1. 作为NIO服务端，接受客户端的TCP连接。
      2. 作为NIO客户端，向服务端发起TCP连接。
      3. 读取通信对端的请求或者应答。
      4. 向通信对端发送消息请求或者应答消息。
    - 单线程模型缺点:
      1. 一个NIO线程同时处理成百上千的链路，性能上无法支撑，即便NIO线程的CPU负荷达到100%，也无法满足海量消息的编码、解码、读取和发送；
      2. 当NIO线程负载过重之后，处理速度变慢，导致大量客户端连接超时，超时后往往会进行重发，这更加重了NIO线程的负载，最终导致大量消息积压和处理超时，NIO线程会成为系统的性能瓶颈。
      3. 可靠性问题：一旦NIO线程意外跑飞，或者死循环，导致整个系统通信模块不可用，不能接收和处理外部消息，造成节点故障。
    - Reactor多线程模型：
      1. 有专门一个NIO线程Acceptor线程用于监听服务端，接收客户端的TCP连接请求。
      2. 网络IO操作读、写等由一个NIO线程池负责，线程池可以采用标准的JDK线程池实现，它包含一个任务队列和N个可用线程，由这些NIO线程负责消息的读取、解码、编码和发送。
      3. 1个NIO线程可以同时处理N条链路，但是1个链路只对应1个NIO线程，防止并发操作问题。
    - 主从Reactor多线程模型：解决了1个服务端监听线程无法有效处理所有客户端连接的性能不足问题。
    - Netty的线程模型并非固定不变，通过在启动辅助类中创建不同的EventLoopGroup实例并通过适当的参数配置，就可以支持上述三种Reactor线程模型。正是因为Netty 对Reactor线程模型的支持提供了灵活的定制能力，所以可以满足不同业务场景的性能诉求。
- Netty无锁化的串行设计。
- 高效的并发编程:主要体现在如下几点。
  1. volatile的大量且正确使用。
  2. CAS和原子累的广泛使用。
  3. 线程安全容器的使用。
  4. 通过读写锁提升并发性能。
- 高性能的序列化框架:
  1. 序列化后的码流大小(网络带宽的占用)
  2. 序列化&反序列化的性能(CPU资源占用)
  3. 是否支持跨语言(异构系统的对接口和开发语言的切换)
  - Netty默认提供了堆Google Protobuf的支持，通过扩展Netty的编解码接口，可以实现其他高性能序列化框架。由于Java原生的序列化性能太差才催生了各种高性能开源序列化技术和框架。以及跨语言、IDL定义等其他原因。
- Netty灵活的TCP参数配置能力，合理设置TCP参数在某些场景下对性能的提升可以起到显著地效果。
