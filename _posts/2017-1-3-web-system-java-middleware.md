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

- 分布式事务；X/Open: Application Program, Resource Manager, Transaction Manager
- CAP (Consistency, Availability, Partition-Tolerance)
- BASE (Basically Available, Soft state, Eventually consistent)
- 一般选择CAP中的A和P对于C策略就是保证最终一致性
- Paxos协议：少数服从多数原则
- 集群内数据一致性的算法
  1. Quorum,用来权衡分布式系统中数据一致性和可用性
  2. 补偿重试机制
- 多机器的Sequence问题与处理
  1. 唯一性
  2. 连续性
  - ID集中管理问题：1 性能问题  2 生成器的稳定性问题 3 存储问题
- 分布式查询问题
  1. 跨库join问题，在服务层分多次查询数据库或者数据冗余，借助外部系统比如搜索引擎解决一些跨库问题。
  2. 外键约束。
- SQL解析-->规则处理-->SQL改写-->数据源选择-->SQL执行-->结果集返回合并处理
- 读写分离，主/备库分库方式不同的数据复制，非对称复制，引入数据变更平台
- 数据平滑迁移，添加增量日志

##### 第六层 消息中间件

- MOM(Message-oriented middleware)
- 如何确定消息发送一致性
- JMS
  1. Destination, 指消息所走通道的目标定义，也就是用来定义消息从发送端发出后要走的通道，而不是最终接收方，它属于管理类的对象。
  2. ConnectionFactory，指用于创建连接的对象，属于管理类的对象。
  3. Connnection，连接接口，所负责的重要工作是创建Session
  4. Seesion，会话接口，消息的发送者，接收者以及消息对象本身，都是由这个会话对象创建的。
  5. MessageConsumer，消息的消费者，订阅消息并处理消息的对象
  6. MessageProducer，消息的生产者，用来发送消息的对象
  7. XXXMessage，指各种类型的消息对象，包括BytesMessage、MapMessage、ObjectMessage、StreamMessage和TextMessage 5种。
  8. XA系列接口为了实现分布式事务的支持
- 解决一致性的方案
  1. 发送消息给消息中间件
  2. 消息中间件入库消息
  3. 消息中间件返回结果
  4. 业务操作
  5. 发送业务操作结果给消息中间件
  6. 更改存储中消息状态

```java
//伪代码
Result postMessage(Message m, PostMessageCallback pmc) {
  //发送消息给消息中间件
  //获取返回结果
  //如果失败，返回失败
  //进行业务操作
  //获取业务操作结果
  //发送业务操作结果给消息中间件
  //返回处理结果
}
```

- 解决消息中间件与使用者的强依赖问题
  1. 提供消息中间件系统的可靠性，但没办法保证百分百可靠。
  2. 对于消息中间件系统中影响业务操作进行的部分，使其可靠性与业务自身的可靠性相同。
  3. 可以提供弱依赖的支持，能够较好地保证一致性。
- 消息模型对消息接收的影响
  1. JMS Queue模型 只有一个应用会去消费某一条消息，所以JMS Queue模型也被称为PeerToPeer(PTP)方式
  2. JMS Topic模型 可以独立收到所有到达Topic的消息，所以也被称为Pub/Sub方式
- 消息订阅者订阅消息方式
  1. 持久订阅和非持久订阅。
- 消息系统的扩容处理，给每一条消息增加一个server标识字段，当有新加入的消息中间件时，会使用新的server标识。
- 消息存储的扩容处理，？
- 应对消息重复的办法时，使消息接收端的处理是一个幂等操作，这样做降低了消息中间件的整体复杂度，同时给消息中间件
  接收端应用带来一定的限制和门槛。
- 保证顺序的消息队列设计
- 消息中间件Push和Pull方式

##### 第七章 软负载中心与集中配置管理

- 软负载中心基础职责。聚合地址信息，生命周期感知。
- 

##### 第八章 构建大型网站的其他要素
