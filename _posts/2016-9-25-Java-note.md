---
layout: post
title: Java work note
excerpt: Java work note
category: Java
---

###### Java单测注意事项

**SQL:**

```sql
update user set name = 'a' where age = 1;
```

**数据库-user**

 |ID  |name|age|
 |----|----|---|
 | 1  | a  | 1 |
 | 2  | b  | 2 |

`以上SQL执行结果是:
Query OK, 1 row affected (0.00 sec)
Rows matched:2 Changed:1 Warnings:0`

⚠️ matched:2,changed:1

而在代码做单测时若测试如下接口:

```java
public interface UserMapper{
    @Update("update user set name = 'a' where age = 1")
    int updateUser();
}
```

⚠️ 结果返回2,指的是matched结果,而不是实际changed的数量
⚠️使用mock做单测时，serviceImpl的实现类使不允许有`@Transactional`注释的，否则无法通过测试，事务控制应该在Dao层处理。
