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
- p46
