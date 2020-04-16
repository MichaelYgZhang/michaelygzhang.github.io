---
layout: post
titile: 高性能MySQL
excerpt: 高性能MySQL
category: DB
---

##### 表设计指南
- 业务合理情况下通常约小约好，考虑长远性。
- 整数类型

|类型  | 存储占用空间  |
|:---|:-----|
|TINYINT | 1Byte|
|SMALLINT| 2Byte|
|MEDIUMINT| 3Byte|
|INT| 4Byte|
|BIGINT| 8Byte|

- 实数类型

|类型| 存储占用空间|


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


