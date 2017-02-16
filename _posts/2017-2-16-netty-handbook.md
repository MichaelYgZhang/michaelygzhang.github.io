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
- 
