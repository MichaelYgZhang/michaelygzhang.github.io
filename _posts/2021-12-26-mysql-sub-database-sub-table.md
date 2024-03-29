---
layout: post
title: MySQL分库分表
excerpt: MySQL分库分表
category: Architecture
---

### 问题 & 解决方案
#### IO瓶颈
- 磁盘IO：大量慢SQL
  - 解决方案：分库，垂直分表
- 网络IO
  - 解决方案：分库

#### CPU瓶颈
- SQL问题，比如SQL中有join，group by等，条件查询多，函数多，增加CPU运算
  - 解决方案：SQL优化，建立合适的索引，service中运算；索引注意最左匹配原则
- 单表数据量太大，扫描行多，SQL效率低
  - 解决方案：水平分表

### 水平分表
- 按照某一字段一定的路由规则（hash，range等），将一个表的数据拆分到N个表中
- 结果：表结构一致，数据没有交集，所有表数据并集为全量数据
- 场景：系统并发量较小，只是单表数据量太大，影响SQL效率，CPU成为瓶颈。表数据量小了，SQL效率提高，CPU负担小；

### 水平分库
- 按照某一字段一定的路由规则（hash，range等），将一个库的数据拆分到N个库中
- 结果：库结构一致，数据没有交集，所有库数据并集为全量数据
- 场景：系统并发量较高，分表不能解决问题，IO/CPU压力较大时，可以采用此方案


### 垂直分库
- 一般以大表为依据，按照业务归属不同，拆分到不同的库中
- 结果：库结构不一样，库数据不一样，没有交集，所有库并集为全量数据。
- 场景：可以理解为服务化

### 垂直分表
- 以字段为依据，将字段拆分不同的表中，比如冷热数据拆分，主/次表
- 结果：表结构不一样，一般至少有一列交集一般为主键，用于关联数据，所有表数据并集为全量数据
- 场景：系统绝对并发量并没有上来，表的记录并不多，但是字段多，并且热点数据和非热点数据在一起，单行数据所需的存储空间较大。以至于数据库缓存的数据行减少，查询时会去读磁盘数据产生大量的随机读IO，产生IO瓶颈。可以理解为列表页和详情页的关系

### 工具
- sharding-sphere：jar，前身是sharding-jdbc；
- TDDL：jar，Taobao Distribute Data Layer；
- Mycat：中间件。
- spring提供的分库方案

### 分库分表引入的问题
- 主键全局唯一问题？雪花算法？
- 非partitionKey的查询问题
  - 解决方案：ES
- 非partitionKey跨库表分页查询问题
  - 解决方案：ES
- 扩容问题
  - 双写？Redis增加节点方案处理？





