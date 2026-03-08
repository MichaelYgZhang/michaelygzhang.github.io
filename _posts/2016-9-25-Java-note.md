---
layout: post
title: Java单元测试与事务控制实战笔记
excerpt: 深入解析Java单元测试中的SQL返回值陷阱、try-finally返回值机制及Spring事务@Transactional的正确使用方式
category: Java
tags: [Java, 单元测试, Spring, 事务, Transactional]
---

## Executive Summary

### 核心观点（金字塔原理）
> **结论先行**: Java开发中需要正确理解SQL执行返回值、try-finally执行机制以及Spring事务控制的代理原理，才能避免常见的测试和事务失效问题。
>
> **支撑论点**:
> 1. SQL UPDATE返回值是matched行数而非changed行数，单测断言需注意
> 2. try-finally中return的值在finally执行前已保存到栈帧slot，基本类型不受finally修改影响
> 3. Spring @Transactional失效的根本原因是内部方法调用绕过了AOP代理

### SWOT 分析
| 维度 | 分析 |
|------|------|
| **S** 优势 | 通过具体代码示例揭示了三个容易被忽视的Java陷阱，实战性强 |
| **W** 劣势 | 示例场景相对独立，缺乏系统性的最佳实践总结 |
| **O** 机会 | 适用于代码审查、新人培训、单测规范制定 |
| **T** 威胁 | 不理解这些细节可能导致测试用例误判、事务失效引发数据不一致 |

### 适用场景
- Java单元测试编写与调试
- Spring事务配置与问题排查
- 代码审查中的细节把控

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



```java
public class Test {
	public static void main(String[] args) {
		System.out.println("result=" + new Test().test());;
	}
	static int test()
	{
	    int x = 1;
      System.out.println("1111");
	    try{
	    	  System.out.println("222");
	        return x;
	    }
	    finally{
	    	  System.out.println("333");
	        ++x;
	    }
	}
}
`111
 222
 333
 result=1`
```

注意:这里涉及到一个栈帧的问题。
在catch中执行的时候，return之前是需要去执行finally的。执行finally之前，把当前要返回的值的引用保存到一个slot【槽】中，也就是说return已经执行，但是还没返回（debug模式下可以看的很清楚），把当前要返回的值保存起来了。 然后执行finally，执行完finally，再从slot中取出要返回的值进行返回。如果返回的是一个对象的引用的话，那么将是finally执行后的值。如果是一个基本类型的话，那么返回的就只是那个基本类型的值了。
【在这里需要注意一点的是，引用类型修改会反映到返回值中，是因为存储在slot中的是对象的引用。在finally中修改的时候，修改的内容已经保存到堆中的对象了。此时return，会反映出修改后的结果。】






##### Transactional 使用
> mysql的表是有事务安全( 比如：InnoDB)和非事务安全(比如：ISAM、MyISAM)之分的 注意
###### 情况1: 不加事务控制,都成功
```java
public void a() {
        System.out.println("a:" + epsxSupplierMapper.insertTest("a", 1)); //入库成功
	b();
    }

    public void b() throws Exception{
        System.out.println("b:" + epsxSupplierMapper.insertTest("b", 2)); //入库成功
       int x = 10/0;
    }
```


###### 情况2: b()加失效,原因是动态代理控制事务切面在a()上
```java
    public void a() {
        System.out.println("a:" + epsxSupplierMapper.insertTest("a", 1)); //入库成功
	b();
    }
    @Transactional	// `失效`
    public void b() throws Exception{
        System.out.println("b:" + epsxSupplierMapper.insertTest("b", 2)); //入库成功
       int x = 10/0;
    }
```

###### 情况3:
```java
    @Transactional
    public void a() {
        System.out.println("a:" + epsxSupplierMapper.insertTest("a", 1)); //入库回滚
	b();
    }

    public void b() throws Exception{
        System.out.println("b:" + epsxSupplierMapper.insertTest("b", 2)); //入库回滚
       int x = 10/0;
    }
```

###### 情况4  `正确方式, 注意: spring.aop.proxy-target-class=true; @EnableTransactionManagement`
```java
    public void a() {
        System.out.println("a:" + epsxSupplierMapper.insertTest("a", 1)); //入库成功
	Test aTest = (Test) AopContext.currentProxy();   // 注意这里
        aTest.b();
    }

    @Transactional
    public void b() throws Exception{
        System.out.println("b:" + epsxSupplierMapper.insertTest("b", 2)); // 入库回滚
       int x = 10/0;
    }
```

###### 情况5
```java
    @Transactional	//只要这里加上,不论b()是否增加@Transactional,只要b失败,a就回滚
    public void a() {
        System.out.println("a:" + epsxSupplierMapper.insertTest("a", 1)); // 入库回滚
	Test aTest = (Test) AopContext.currentProxy();   // 注意这里
        aTest.b();

    @Transactional
    public void b() throws Exception{
        System.out.println("b:" + epsxSupplierMapper.insertTest("b", 2)); // 入库回滚
       int x = 10/0;
    }
```

