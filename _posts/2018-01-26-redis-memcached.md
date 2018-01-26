---
layout: post
title: Redis VS Memcached 
excerpt: Cache
category: Destributed
---

###### 问题
1. Redis/Memcached 是什么？
2. 网络模型？
3. 数据类型？
4. 数据存储及持久化？
5. 内存管理？
6. 数据一致性？
6. 集群管理？
7. 使用，如何区分两者的使用场景？以及使用过程中的问题？

###### Redis/Memcached 是什么? 


###### 网络模型？

|Memcached | Redis |
|----------|-------|
|1. 多线程，非阻塞IO复用网络模型 
 2. Master主线程/Worker子线程，多线程能更好利用多核带来数据一致性，
   与锁同步问题比如stats命令需要加锁,性能损耗
  |
  1. 单线程的IO复用模型. 
封装AeEvent事件处理框架，
主要实现了epoll, kqueue和select.
单线程性能高效,redis也提供了一些简单的
计算功能，比如排序、聚合等，对于这些操作，
单线程模型施加会严重影响整体吞吐量，
CPU计算过程中，整个IO调度都是被阻塞的
|

###### 数据类型？

|Memcached | Redis |
|----------|-------|

###### 数据存储及持久化？

|Memcached | Redis |
|----------|-------|

###### 内存管理？

|Memcached | Redis |
|----------|-------|

###### 数据一致性？

|Memcached | Redis |
|----------|-------|

###### 集群管理？

|Memcached | Redis |
|----------|-------|

###### 使用，如何区分两者的使用场景？以及使用过程中的问题？

|Memcached | Redis |
|----------|-------|
