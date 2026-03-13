---
layout: post
title: 从Paxos到Zookeeper：分布式一致性原理与实践详解
excerpt: 深入解析分布式一致性协议演进，从2PC/3PC到Paxos再到ZAB协议的核心原理与工程实践
category: Distributed
tags: [分布式系统, Paxos, Zookeeper, ZAB协议, 一致性, CAP理论]
---

## Executive Summary

### 核心观点（金字塔原理）
> **结论先行**: 分布式系统的核心挑战在于一致性保证，从2PC/3PC到Paxos再到ZAB协议，是一个不断优化容错性和可用性的演进过程，Zookeeper基于ZAB协议实现了高可用的分布式协调服务。
>
> **支撑论点**:
> 1. 分布式系统面临通信异常、网络分区、节点故障等固有问题，需要在CAP理论框架下做权衡
> 2. 2PC存在同步阻塞和单点问题，3PC虽降低阻塞但仍有数据不一致风险，Paxos提供了更完善的一致性保证
> 3. Zookeeper采用ZAB协议（崩溃恢复+消息广播），通过Leader选举和过半投票机制实现高可用分布式协调

### SWOT 分析

| 维度 | 分析 |
|------|------|
| **S** 优势 | ZAB协议结合了Paxos的一致性优点，增加同步阶段保证事务完整性；Leader/Follower/Observer架构灵活扩展读性能 |
| **W** 劣势 | 2PC/3PC存在阻塞和单点问题；ZAB协议在网络分区时参与者可能错误提交导致数据不一致 |
| **O** 机会 | 适用于配置中心、分布式锁、Master选举、服务注册发现等分布式协调场景 |
| **T** 威胁 | 网络分区场景下的脑裂风险；协调者单点故障需要快速恢复机制 |

### 适用场景
- 需要强一致性保证的分布式事务处理系统
- 分布式配置管理、服务注册发现、分布式锁等协调服务
- 对高可用和数据一致性有较高要求的微服务架构

---

##### 第1章 分布式架构

- 1-从集中式到分布式
- 分布式系统是一个硬件或软件组件分布在不同的网络计算机上，彼此之间仅仅通过消息传递进行通信和协调的系统。
- 分布式系统特性：`分布性`、`对等性`、`并发性`、`缺乏全局时钟`、`故障总是会发生`。
- 分布式环境中的问题：`通信异常`、`网络分区`、三态(`成功`、`失败`、`超时`)、`节点故障`
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
  - 2PC:

 ```
1. 提交事务请求(投票阶段)
 1. 事务询问
 2. 执行事务,各参与者节点执行事务操作并将Undo和Redo信息记入事务日志中
 3. 各参与者向协调者反馈事务询问的响应

2. 执行事提交(根据阶段一的反馈情况决定最终是否可以进行事务提交操作)
    	1. 执行事务(阶段一都返回Yes响应)
        1. 发送提交请求，协调者向所有参与者发出Commit请求
        2. 事务提交，参与者接收到Commit请求后，会正式执行事务提交操作，并在完成提交之后释放整个事务执行期间占用的事务资源。
        3. 反馈事务结果,参与者在事务完成后向协调者发送Ack消息
        4. 完成事务，协调者接收到所有参与者反馈的Ack消息后，完成事务。
    	2. 中断事务，任何一个参与者向协调者反馈了No响应或者等待超时后，协调者无法接收到所有参与者的反馈响应，就中断事务
      	1. 发送回滚请求，协调者向所有参与者发出Rollback请求
      	2.事务回滚，参与者接收到Rollback请求后，会利用阶段一中记录的Undo信息来执行事务回滚操作，并在完成回滚之后释放整个事务执行期间的资源
      	3. 反馈事务回滚结果，参与者完成事务回滚后向协调者发送Ack消息
      	4. 中断事务，协调者接收到所有参与者反馈的Ack消息，完成事务中断。
```

- 优缺点:优点，`原理简单`、`实现方便`。缺点:`同步阻塞`、`单点问题`、`数据不一致`比如commit阶段一部分成功一部分网络问题无法提交产生数据不一致、`太过保守容错机制差`。

- 3PC: 将2PC协议的第二个阶段过程一分为二，形成由`CanCommit`、`PreCommit`和`do Commit`三个阶段组成的事务处理协议。


```
1. CanCommit
	1. 事务询问
      	2. 各参与者向协调者反馈事务询问的响应

2. PreCommit
      	1. 执行事务预提交(所有参与者反馈Yes)
		1. 发送预提交请求
		2. 事务预提交
		3. 各参与者向协调者反馈事务执行的响应
      	2. 中断事务(所有参与者有任意一个反馈No，或者等待超时无法接收到参与者的反馈)
		1. 发送中断请求
		2. 中断事务，无论是来自协调者的abort请求还是出现等待超时参与者都中断事务

3. doCommit
	1. 执行事务
	  	1. 发送提交请求，参与者从预提交状态转到提交状态，并向所有参与者发送doCommit请求
	  	2. 事务提交，提交事务并在之后释放事务执行期间占用的事务资源
	  	3. 反馈事务提交结果，参与者向协调者发送Ack消息
	  	4. 完成事务，协调者接收到所有参与者反馈的Ack消息后完成事务

	2. 中断事务
	  	1. 发送中断请求
	  	2. 事务回滚
	  	3. 反馈事务回滚结果
	  	4. 中断事务
```

- 一旦进入阶段三，可能存在以下问题
  1. 协调者出现问题
  2. 协调者和参与者之间的网络故障

- 无论出现那种情况，都导致参与者无法及时接收到来自协调者的doCommit或者abort请求，针对这种异常，参与者都会在等待超时后，继续进行事务提交。

- 三阶段优缺点：
  - 优点：相比二阶段降低参与者的阻塞范围，并能在出现单点故障后达成一致
  - 缺点：三阶段去除阻塞的同时引入了新的问题，就是在参与者接收到preCommit消息后如果网络出现分区，此时协调者所在的节点和参与者都无法正常网络通信，这种情况下，参与者依然会进行事务提交，必然导致数据的不一致性

- Paxos算法  莱斯利-兰伯特 LeslieLamport
  - "拜占庭将军问题", 为解决这个问题提出了 Paxos理论。核心算法是一致性算法。
  - Paxos算法中有三种角色：**Proposer**（提案者，负责提出提案）、**Acceptor**（接受者，负责对提案进行投票表决）、**Learner**（学习者，不参与投票，只学习已达成一致的提案结果）
  - Paxos算法分为两个阶段：**Prepare阶段**，Proposer选择一个提案编号n并向超过半数的Acceptor发送Prepare(n)请求，Acceptor收到后如果n大于其已响应的所有提案编号，则承诺（Promise）不再接受编号小于n的提案，并返回已接受过的编号最大的提案；**Accept阶段**，Proposer收到超过半数Acceptor的Promise响应后，向这些Acceptor发送Accept(n, v)请求（v为响应中编号最大的提案值，若无则可自由提议），Acceptor收到后如未违反承诺则接受该提案
  - **过半机制（Majority）**：一个提案只有被超过半数的Acceptor接受后才被视为被选定（Chosen），这保证了在任意时刻最多只有一个提案值被选定，从而实现一致性
  - **Multi-Paxos优化**：在工程实践中，当Leader稳定时可以跳过Prepare阶段，直接进入Accept阶段，将消息轮次从两轮减少到一轮，大幅提升性能
  - Paxos算法保证了**Safety**（安全性，即一致性不被破坏），但**Liveness**（活性）需要通过Leader选举机制来保证——若多个Proposer交替提案可能形成活锁（live-lock），因此实践中通常选举一个Leader来统一发起提案

##### 第3章 Paxos的工程实践

- Google Chubby是一个基于Paxos算法的分布式锁服务，提供粗粒度的分布式锁和小文件存储功能，是Google基础设施的核心组件之一
- **架构设计**：Chubby集群由5个副本（Replica）组成一个Chubby Cell，通过Paxos协议在副本间选举一个Master，所有的读写请求都由Master处理，其他副本作为热备进行数据复制，Master通过租约（Lease）机制维持其Leader身份
- **核心功能**：提供Advisory Lock（建议性锁）用于分布式协调；提供小文件存储（文件大小不超过256KB）用于元数据管理；提供Event Notification（事件通知）机制，客户端可以注册监听锁状态和文件内容的变化
- **设计理念**：Chubby的设计优先保证可靠性和可用性，而非高吞吐量。典型应用场景包括GFS中Master的选举、BigTable中元数据（Tablet Location）的管理、以及Google内部各种分布式系统的命名服务和配置管理

##### 第4章 ZooKeeper与Paxos

- Zookeeper并未采用Paxos算法,而是采用了一种ZAB(Zookeeper Atomic Broadcast)的一致性协议
- Zookeeper保证如下分布式一致性特征,`顺序一致性`,`原子性`,`单一视图`，`可靠性`,`实时性`
- Zookeeper四个设计目标: 简单的数据模型，可以构建集群，顺序访问，高性能
- Zookeeper集群角色，没有沿用传统的Master/Slave概念，采用Leader,Follower,Observer三种角色。Leader提供`读写`服务,Follower、Observer都提供`读`服务，区别在于，`Observer不参与Leader的选举过程,也不参与写操作的，"写过半成功"策略`,因此Observer在不影响写性能的情况提升了集群的读性能。
- 会话Session,客户端和服务器创建TCP的长连接开始即会话开始，只要网络断开时间小于sessionTimeout时间值能重新连接上集群中的任意一台服务器，则之前的会话仍然有效。
- 数据节点Znode,分为持久节点和临时节点。Watcher，ACL(Access Control Lists)

###### ZAB协议
- ZAB核心是定义了对于那些会改变Zookeeper服务器数据状态的事务请求的处理方式,即:

> 所有事务请求必须由一个全局唯一的服务器来协调处理，这样的服务器被称为Leader服务器，而余下的其他服务器则称为Follower服务器。Leader服务器负责将一个客户端事务请求转换成一个事务Proposal提议，并将该Proposal分发给集群中所有的Follower服务器，之后Leader服务器需要等待所有Follower服务器的反馈，一旦超过半数Follower服务器进行正确的反馈后，那么Leader就会再次向所有的Follower服务器分发Commit消息，要求其将前一个Proposal进行提交

- ZAB两种基本模式:崩溃恢复和消息广播

> 恢复模式: 当整个服务框架在启动过程中，或是当Leader服务器出现网络中断，崩溃退出或重启等异常情况，ZAB协议就进入恢复模式并选举产生新的Leader服务器，然后同步数据状态给所有Follower，当集群中有过半的机器与Leader完成状态同步则ZAB退出恢复模式，从而进入消息广播模式。

- 超过半数投票机制,指自己也算一票。比如3台，一台挂了，是可以产生Leader的。
- 消息广播,可以类比2PC阶段
- ZAB协议规定:任何时候都需要保证只有一个主进程负责进行消息广播，而如果主进程崩溃了，就需要选举出一个新的主进程，主进程的选举机制和消息广播机制是紧密相关的。
- ZAB协议主要包括消息广播和崩溃恢复两个过程。进一步可以细分为三个阶段，发现Discovery,同步Synchronization和广播Broadcast阶段，组成ZAB协议的每一个分布式进程会循环地执行这三个阶段，我们将这样一个循环称为一个主进程周期。
- ZAB协议的设计中，每一个进程都有可能处于以下三种状态之一。

```
LOOKING: Leader选举阶段，启动的初始状态
FOLLOWING: Follower服务器和Leader保持同步状态
LEADING: Leader服务器作为主进程领导状态
```

- ZAB与Paxos算法的联系与区别

```
两者的联系:
1. 都存在一个类似Leader进程的角色，由其负责协调多个Follower进程的运行
2. Leader进程都会等待超过半数的Follower做出正确的反馈后，才会将一个提案进行提交
3. 在ZAB协议中，每个Proposal中都包含了一个epoch值，用来代表当前的Leader周期，在Paxos算法中，同样存在这样一个标识，名字Ballot
```

- 两者的区别:

> 1. 在Paxos算法中，一个新选举产生的主进程会进行两个阶段的工作。第一阶段被称为读阶段，这个阶段中新的主进程会通过和所有其他进程进行通信的方式收集上一个主进程提出的提案并将它们提交。第二阶段被称为写阶段，这个阶段，当前主进程开始提出它自己的提案。在Paxos算法设计的基础上，ZAB协议额外添加了一个同步阶段，有效保证Leader在新的周期中提出事务Proposal之前，所有进程都已经完成了对之前所有事务Proposal的提交，一旦完成同步阶段后，那么ZAB就会执行和Paxos算法类似的写阶段。

> 2. ZAB协议主要用来构建一个高可用的分布式数据主备系统，比如Zookeeper。而Paxos算法则用于构建一个分布式的一致性状态系统。

##### 第5章 使用Zookeeper

```
zoo.cfg
集群配置:
server.id=host:port:port //id标识集群机器序号,范围1~255
```

- ZK节点ACL权限，CREATE,READ,WRITE,DELETE,ADMIN。注意删除，指对子节点的删除权限，其他4中指对自身节点的操作权限
- 身份认证,world,auth,digest(用户名:密码),ip
- 其他需要多练习,开源客户端，ZkClient, Curator

##### 第6章 Zookeeper的典型应用场景

- 数据发布/订阅，即配置中心

```
特点:
1. 数据量通常比较小
2. 数据内容在运行时会发生变化
3. 集群各机器共享，配置一致
```

- 负载均衡(Load Balance)
- 命名服务(Name Service)
- 分布式协调/通知
- 心跳监测
- 工作进度汇报
- 系统调度
- 利用客户端Zookeeper的Watcher监听与Zookeeper上创建临时节点可以监测机器存活性监控的系统
- 分布式日志收集系统
- Master选举
- 分布式锁
- 分布式队列
- 分布式屏障


##### 第7章 Zookeeper技术内幕

- **系统模型**：ZK的数据模型是一棵树（ZNode Tree），类似文件系统的层级结构。节点类型分为持久节点（Persistent）、临时节点（Ephemeral）、持久顺序节点（Persistent Sequential）和临时顺序节点（Ephemeral Sequential）。每个节点维护一个Stat结构，包含version（数据版本）、cversion（子节点版本）和aversion（ACL版本）用于乐观锁控制
- **序列化**：ZK使用Jute作为序列化/反序列化框架，通过Record接口的serialize和deserialize方法实现节点数据的编解码，所有协议通信和数据持久化都依赖Jute进行数据序列化
- **会话管理**：客户端与服务端之间通过TCP长连接维持会话（Session）。会话状态机包含CONNECTING（连接中）、CONNECTED（已连接）、RECONNECTING（重连中）、CLOSE（已关闭）等状态。服务端通过分桶策略（ExpirationInterval）管理会话超时检测，将会话按过期时间归入不同的桶中批量检查
- **Leader选举算法**：ZK默认使用FastLeaderElection算法，每个服务器启动时处于LOOKING状态。选举基于两个核心指标：ZXID（事务ID，越大说明数据越新）和myid（服务器ID）。优先选择ZXID最大的服务器，ZXID相同则选择myid最大的。当某个服务器获得超过半数投票后成为Leader
- **请求处理链**：ZK采用责任链模式处理请求。Leader服务器的处理链为：PrepRequestProcessor（请求预处理、创建事务）-> ProposalRequestProcessor（事务投票）-> CommitProcessor（等待过半确认）-> FinalRequestProcessor（应用到内存数据树并返回响应）。Follower的处理链有所不同，通过FollowerRequestProcessor将写请求转发给Leader
- **数据存储**：ZK数据存储分为内存数据和磁盘数据两部分。内存中使用DataTree维护完整的ZNode树结构，保证高性能读取；磁盘上通过事务日志（Transaction Log）记录每一次事务操作，通过快照（Snapshot）定期对内存数据做全量持久化。恢复时先加载最新快照再重放事务日志，确保数据不丢失

##### 第8章 Zookeeper运维

- **配置管理**：zoo.cfg是ZK的核心配置文件，关键参数包括：`tickTime`（心跳间隔，默认2000ms）、`dataDir`（内存快照存储路径）、`dataLogDir`（事务日志存储路径，建议与dataDir分开配置以提升IO性能）、`clientPort`（客户端连接端口，默认2181）、`initLimit`（Follower初次同步Leader的超时tickTime倍数）、`syncLimit`（Follower与Leader之间心跳超时的tickTime倍数）
- **四字命令（Four Letter Words）**：ZK提供一系列四字命令用于监控和管理集群，包括：`stat`（查看服务器状态和连接信息）、`ruok`（检查服务器是否正常运行，返回imok表示健康）、`dump`（列出未完成的会话和临时节点信息）、`conf`（输出服务器配置详情）、`cons`（列出所有客户端连接的详细信息）、`envi`（输出服务器运行环境信息）
- **最佳实践**：将dataDir和dataLogDir配置在不同的磁盘设备上，避免事务日志写入与快照IO竞争；通过`autopurge.snapRetainCount`配置保留的快照数量（默认3个），`autopurge.purgeInterval`配置自动清理间隔（单位小时，设为0则不开启），防止磁盘被历史日志和快照文件占满
- **监控运维**：ZK支持JMX（Java Management Extensions）集成，可通过JMX暴露的MBean监控关键指标，如节点数量（znode count）、Watch数量、延迟统计、Leader/Follower角色状态等。生产环境建议结合监控系统（如Prometheus + Grafana）对集群健康状态进行持续监控和告警
