---
layout: post
title: 大规模分布式存储系统原理解析与架构实战 读书笔记
excerpt: Analysis of the principle and architecture of large scale distributed storage system
category: Java
---

##### 第1章  概述

- 分布式存储概念
  0. 分布式存储的几个特性
  1. 可扩展
  2. 低成本
  3. 高性能
  4. 易用
- 分布式系统以及数据库技术
  1. 数据分布
  2. 一致性
  3. 容错
  4. 负载 均衡
  5. 事务与并发控制
  6. 易用性
  7. 压缩/解压缩
- 分布式存储分类
  1. 非结构化数据
  2. 结构化数据
  3. 半结构化数据
- 不同的分布式存储系统适合处理不同类型的数据，共分为四类分布式存储系统：分布式文件系统，分布式键值系统，分布式表格系统，分布式数据库。

###### 第一篇 基础篇

##### 第2章 单机存储系统

- 存储系统的性能主要包括两个维度：吞吐量和访问延时，磁盘和SSD的访问延时差别很大，但带宽差别不大，因此，磁盘适合大块顺序访问的存储系统，SSD适合随机访问较多或者对延时比较敏感的关键系统，二者也常常组合在一起进行混合存储，热数据（访问频繁）存储到SSD中，冷数据（访问不频繁）存储到磁盘中。
- 单机存储引擎
  1. 哈希存储引擎
  2. B树存储引擎
  3. LSM树存储引擎
- 数据模型：文件、关系、键值模型
- 事务与并发控制
  1. 为了提高读事务性能，可以采用写时复制(Copy-On-Write COW)或者多版本并发控制(Multi-Version Concurrency Control MVCC)技术避免写事务阻塞读事务。
  2. ACID
  3. SQL的隔离级别 Read Uncommitted, Read Committed, Repeatable Read, Serializable, Lost Update, Dirty Reads,Non-Repeatable Reads, Second Lost Updates problem, Phantom Reads
  4. 并发控制, 数据库锁
    - 解决死锁的思路主要有两种：1 每个事务设置一个超时时间，超时后自动回滚。2 死锁检测，检测到死锁后可以通过回滚其中某些事务来消除循环依赖。
- 故障恢复
  1. 操作日志
  2. 重做日志
  3. 优化手段
    - 成组提交
    - 检查点
- 数据压缩    
  1. 压缩算法
    - Huffman算法，找到一种前缀编码方式使得编码长度最短
    - LZ系列压缩算法，是一种动态创建字典的压缩算法，压缩工程中动态创建字典并保存在压缩信息里面。
    - BMDiff与Zippy
    - 列式存储

##### 第3章 分布式系统
