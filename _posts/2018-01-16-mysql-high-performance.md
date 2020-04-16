---
layout: post
titile: 高性能MySQL开发
excerpt: 高性能MySQL开发
category: DB
---

##### 表设计指南
- 业务合理情况下通常约小约好，考虑长远性。

|类型  | 存储占用空间  |
|:---|:-----|
|TINYINT | 1Byte|
|SMALLINT| 2Byte|
|MEDIUMINT| 3Byte|
|INT| 4Byte|
|BIGINT| 8Byte|
|VARCHAR(n)| 可变长度,支持到65535B，需要额外补充1-2字节记录长度，原数据位置更细切可变，易产生碎片，使用场景，字符串的最大长度比平均长度大很对，比如评价，字段更新少，碎片化问题不严重。|
|CHAR(n)| 定长，支持到255B， 无需额外空间，定长不易产生碎片问题。使用场景，存储固定长度数据，比如MD5值，身份证ID，经常变更数据，也不易产生碎片，对于短的列，CHAR比VARCHAR在存储上更有效率|

- 表设计范式需要平衡
1. 没有绝对的对于错，只有适不适合
2. 高性能反范式，适当保留聚合字段，冗余字段

- 表设计-字段少而精
  - 拆分前
    - 字段多，40多个字段甚至更多字段混在一张表中。
    - IO非常低效，返回很多无用的字段。
    - 索引不好复用
    - 耦合严重，读写，变更字段分不开，无法按照字段本身的特点做针对性的优化。
    - 体积大，单表数据大。

- 表设计-分库分表
  - 保留充分的读写拓展能力
    - 分表
      - 分库的数据结构准备
      - 提升读写效率
    - 分库
      - 数据库写能力水平拓展

- 表设计-缓存表（异构表）结合业务场景使用缓存数据异构。比如，userId, orderId, poiId...等组合为一张表。

##### 索引设计指南
- B+Tree，最主要是减少IO操作。
  - 平衡m叉 + 叶子节点才存储数据
    - 增大页内数据量提升预读有效性，减少磁盘IO。操作系统局部性原理。
    - 极大减少树的度，减少磁盘IO。
    - 单页16KB，两int的联合索引8B，4层可存80亿数据。
    - 叶子节点直接绑定数据，减少磁盘IO。
  - 有序 + 叶子节点 双向链表
    - 快速的定位，范围查询，排序
- InnoDB 索引组织表
  - 聚簇索引叶子节点保存完整数据
    - 如果定义了PK，则PK就是作为聚簇索引。
    - 如果没有PK，则第一个非空unique列作为聚簇索引。
    - 否则InnoDB会创建一个隐藏的row-id作为聚簇索引。
  - 辅助索引叶子节点村聚簇索引的值
    - 先查通过普通索引查PK，再由PK查数据，回表操作，如果当前索引存在数据，那么是索引覆盖。
    
- InnoDB主键设计规范
  - 主键设计规范
    - 要有主键，且是顺序增长的。
    - 强烈建议使用int/bigint作为自增id作为主键
    - 避免使用 md5/uuid 等无序散列的数据作为主键
  - 为什么一定要有顺序？
    - 


  
  
  

##### 查询设计指南


##### 应用及运维相关指南

#### MySQL 查询处理

```java
(7) SELECT (8) DISTINCT <select_list>
(1) FROM <left_table>
(3) <join_type> JOIN <right_type>
(2) ON <join_condition>
(4) WHERE <where_condition>
(5) GROUP BY <group_by_list>
(6) HAVING <having_condition>
(9) ORDER BY <order_by_list>
(10) LIMIT <number>
```

#### 执行计划 [explain](https://dev.mysql.com/doc/refman/5.5/en/explain-output.html#explain-extra-information)

```java
局限：
1）不考虑触发器，存储过程和自定义函数。
2）不考虑Cache。
3）不显示优化过程。
4）统计信息是估算。 
最主要的优化方式：
慢查询日志 + 执行计划分析
```


