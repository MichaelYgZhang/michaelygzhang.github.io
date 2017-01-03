---
layout: post
title: 大型网站系统与Java中间件实践
excerpt: WebSystemJavaMiddlewarePractice
category: Java
---

##### 第一章 分布式系统介绍

- A distributed system is one in which components located at networked computers communicate and
  coordinate their actions only by passing messages。 分布式系统的定义。一，组件分布在网络计算机中，二是组件之间
  仅仅通过消息传递来通信并协调行动。
- 组成计算机的基本元素包括输入设备、输出设备、运算器、控制器、存储器。存储器又分为内存和外存。
- 对于线程不安全的容器或对象可以通过加锁或者通过`Copy On Write`的方式控制并发访问。
- 分布式系统的难点：
  1. 缺乏全局时钟
  2. 面对故障独立性
  3. 处理单点故障
    - 单点变集群
    - 给这个单点做好备份，能够在出现问题时进行恢复，并且尽量做到自动恢复，降低恢复需要用的时间。
    - 降低单点故障的影响范围。
  4. 事务的挑战

##### 第二章 大型网站及其架构演进过程
- 分
- session问题
  1. Session Sticky
  2. Session Replication
  3. Session数据集中存储
  4. Cookie Based，长度限制，安全性问题，带宽消耗，性能影响
- 数据库读写压力变大，读写分离
  - 数据复制问题，会出现数据一致性延迟问题
  - 应用对于数据源的选择问题
  - 加速数据读取的利器--缓存
- 页面缓存
- 分布式存储系统
- 库的水平／垂直 拆分
- 数据库拆分的问题
  1. 分布式事务问题
  2. 分页查询问题
- 走服务化的路
- 初识消息中间件
  1. MOM(Message-oriented middleware) is software infrastructure focused on sending and receiving
    message between distributed systems
  2. 异步和解耦

##### 第三章 构件Java中间件

- 远程过程调用和对象访问中间件；主要解决分布式环境下应用的互相访问问题，支撑服务化的基础。
- 消息中间件，解决应用之间的消息传递、解耦、异步的问题。
- 数据访问中间件，主要解决应用访问数据库的共性翁题的组件。

##### 第四章 服务框架

- 服务的拆分
- 服务的粒度
- 优雅和实用的平衡
- 分布式环境中的请求合并
- 分布式锁服务，看情况是否可以根据一定规则把同样的请求分配到同一台服务器上，这样避免了分布式锁的复杂度。
- ESB总线模型，可以更多考虑不同厂商所提供服务的整合。 

##### 第五章 数据访问层

##### 第六层 消息中间件

##### 第七章 软负载中心与集中配置管理

##### 第八章 构建大型网站的其他要素
