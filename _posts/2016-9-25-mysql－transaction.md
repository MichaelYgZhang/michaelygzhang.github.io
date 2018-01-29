---
layout: post
title: MySQL Transaction
excerpt: MySQL 事务
category: DB
---

##### 事务基本要素 `ACID`

- `Atomicity`原子性:一个事务必须被视为一个不可分割的最小工作单元，整个事务中的所有操作要么全部提交成功，要么全部失败回滚，对一个事务来说，不可能只执行其中的一部分操作，这就是事务的原子性。
- `Consistency`一致性:事务开始前和结束后，数据库的完整性没有遭到破坏。
- `Isolation`隔离性:在同一时间，只允许一个事务请求同一数据。
- `Durability`持久性:事务完成以后，该事务对数据库所做的操作持久化在数据库中，并不会被会滚。

##### 事务隔离级别`Transaction Isolation Level`

1. READ_UNCOMMITTED(未提交读)

> 事务中的修改，即使没有提交，对其他事务也都是可见的。事务可以读取未提交的数据，这也被称为脏读(Dirty Read)。这个级别会导致很多问题，从性能上来说，READ_UNCOMMITTED不会比其他级别好太多，但却会缺乏其他级别的很多好处，除非真的非常有必要的理由，在实际应用中一般很少使用

2. READ_COMMITTED(提交读)

> 大多数据库系统的默认隔离级别都是READ_COMMITTED(但MySQL不是)。READ_COMMITTED满足前面提到的隔离性的简单定义:一个事务开始时，只能"看见"已经提交的事务所做的修改。话句话说，一个事物从开始直到提交之前，所做的任何修改对其他事务都是不可见的。这个级别有时候也叫做不可重复读(nonrepeatable read)，因为两次执行同样的查询，可能会得到不一样的结果。

3. REPEATABLE_READ(可重复读)

> 解决了脏读的问题，该级别保证了在同一个事务中多次读取同样记录的结果是一致的。但是理论上，可重复读隔离级别还是无法解决另一个幻读(Phantom Read)的问题。所谓幻读，指的是某个事务在读取某个范围内的记录时，另一个事务又在该范围内插入了新的记录，当之前的事务再次读取该范围的记录时，会产生幻行(Phantom Row)。InnoDB和XtraDB存储引擎通过多版本并发控制(MVCC, Multiversion Concurrency Control)解决了幻读的问题。可重复读是MySQL的默认事务隔离级别。

4. SERIALIZABLE(可串行化)

> 最高的隔离级别。通过强制事务串行执行，避免了前面说的幻读的问题。简单来说SERIALIZABLE会在读取的每一行数据上都加锁，所以可能导致大量的超时和锁的竞争问题，实际应用中也很少用到这个隔离级别，只有在非常需要确保数据的一致性而且可以接受没有并发的情况下，才考虑该级别

⚠️*REPEATABLE READ:在mysql中，不会出现幻读。mysql的实现和标准定义的RR隔离级别有差别。*

⚠️*由上往下，级别越来越高，并发性越来越差，安全性越来越高，反之则反。*

|--------隔离级别--------|脏读可能性|不可重复读可能性|幻读可能性|加锁读|
|--------|----------|----------------|----------|------|
|READ_UNCOMMITTED|Yes|Yes|Yes|No|
|READ_COMMITTED|No|Yes|Yes|No|
|REPEATABLE_READ|No|No|Yes|No|
|SERIALIZABLE|No|No|No|Yes|

##### 事务中常出现的并发问题

- 脏读:一个事务读取了另一个事务操作但未提交的数据。
- 可重复读:一个事务中的多个相同的查询返回了不同数据。
- 幻读:事务并发执行时，其中一个事务对另一个事务中操作的结果集

##### 死锁问题

T1

```sql
start transaction;
update user set age=15 where id=1;
update user set age=10 where id=2;
commit;
```

T2

```sql
start transaction;
update user set age=12 where id=2;
update user set age=10 where id=1;
commit;
```

如果T1,T2都执行了第一条update语句，更新了一行，同时也锁定了该行数据，接着每个事务都尝试去执行第二条update语句，却发现改行已经被对方锁定，然后两个事务都等待对方释放锁，同时又持有对方需要的锁，则陷入死循环，除非由外部因素介入才可能解除死锁。

为了解决这个问题，数据库系统引入了各种死锁检测和死锁超时机制。


##### 设置事务级别

```sql
set session transaction isolation level read committed;
````

##### 查看事务级别

```sql
select @@tx_isolation;
```

##### 查看是否自动提交

```sql
select @@autocommit;
```

|@@autocommit|
|------------|
|   1        |

结果1表示自动提交，设置为禁用自动提交`set autocommit=0;`

![事务管理](http://static.oschina.net/uploads/space/2013/0909/011829_pKHp_223750.png)

##### 原文

[探索数据库的事务隔离级别](http://blog.jobbole.com/99774/)

[Transaction](http://blog.jobbole.com/103211/)
