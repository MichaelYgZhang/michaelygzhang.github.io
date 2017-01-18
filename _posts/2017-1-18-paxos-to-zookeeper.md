---
layout: post
title: 从Paxos到Zookeeper分布式一致性原理与实践
excerpt: PaxosToZookeeper
category: Destributed
---

##### 第1章 分布式架构

- 1-从集中式到分布式
- 分布式系统是一个硬件或软件组件分布在不同的网络计算机上，彼此之间仅仅通过消息传递进行通信和协调的系统。
- 分布式系统特性：分布性、对等性、并发性、缺乏全局时钟、故障总是会发生。
- 分布式环境中的问题：通信异常、网络分区、三态(成功、失败、超时)、节点故障
- 从ACID到CAP/BASE; Atomicity原子性、Consistency一致性、Isolation隔离性、Durability持久性；
- 标准SQL规范中定义了4个事务隔离级别：
  1. 未授权读取即读未提交允许出现脏读
  2. 授权读取即只允许读取已经被提交的数据
  3. 可重复读取即多次读取同一个数据时，其值和事务开始时刻是一致的，禁止了不可重复读和脏读，可能出现幻影数据
  4. 串行化即最严格事务隔离级别，事务串行执行。
- CAP和BASE理论：
  1. Consistency一致性、Availability可用性、Partition tolerance分区容错性。
  2. BASE：Basically Avaliable基本可用、Soft state软状态和Eventually consistent最终一致性的简写
- 最终一致性存在以下5种变种
  1. 因果一致性
  2. 读已之所写
  3. 会话一致性
  4. 单调读一致性
  5. 单调写一致性

##### 第2章 一致性协议

- 2PC与3PC
- TODO 17p

##### 第3章 Paxos的工程实践
##### 第4章 ZooKeeper与Paxos
##### 第5章 使用Zookeeper
##### 第6章 Zookeeper的典型应用场景
##### 第7章 Zookeeper技术内幕
##### 第8章 Zookeeper运维
