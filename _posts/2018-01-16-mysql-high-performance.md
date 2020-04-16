---
layout: post
titile: 高性能MySQL开发
excerpt: 高性能MySQL开发
category: DB
---

##### 表设计指南
- 业务合理情况下通常约小约好，考虑长远性。
- 数据类型

|类型  | 存储占用空间  |
|:---|:-----|
|TINYINT | 1Byte|
|SMALLINT| 2Byte|
|MEDIUMINT| 3Byte|
|INT| 4Byte|
|BIGINT| 8Byte|
|VARCHAR(n)| 可变长度,支持到65535B，需要额外补充1-2字节记录长度，原数据位置更细切可变，易产生碎片，使用场景，字符串的最大长度比平均长度大很对，比如评价，字段更新少，碎片化问题不严重。|
|CHAR(n)| 定长，支持到255B， 无需额外空间，定长不易产生碎片问题。使用场景，存储固定长度数据，比如MD5值，身份证ID，经常变更数据，也不易产生碎片，对于短的列，CHAR比VARCHAR在存储上更有效率|

- 表设计范式平衡
1. 没有绝对的对于错，只有适不适合




##### 索引设计指南
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


