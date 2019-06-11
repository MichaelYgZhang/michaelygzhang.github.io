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
###### 情况1
```java
public void a() {
        try {
            System.out.println("a:" + epsxSupplierMapper.insertTest("a", 1)); //入库成功
	     b();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void b() throws Exception{
        try {
            System.out.println("b:" + epsxSupplierMapper.insertTest("b", 2)); //入库成功
            int x = 10/0;
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
```


###### 情况2
```java

    public void a() {
        try {
            System.out.println("a:" + epsxSupplierMapper.insertTest("a", 1)); //入库成功
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
    @Transactional
    public void b() throws Exception{
        try {
            System.out.println("b:" + epsxSupplierMapper.insertTest("b", 2));//入库成功
            int x = 10/0;
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
```

###### 情况2
```java
    @Transactional
    public void a() {
        try {
            System.out.println("a:" + epsxSupplierMapper.insertTest("a", 1)); //入库成功
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
    
    public void b() throws Exception{
        try {
            System.out.println("b:" + epsxSupplierMapper.insertTest("b", 2));//入库成功
            int x = 10/0;
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
```

###### 情况4
```java
@Transactional(rollbackFor = Exception.class)
    public void a() {
        try {
            System.out.println("a:" + epsxSupplierMapper.insertTest("a", 1)); //入库成功
            b();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    @Transactional(rollbackFor = Exception.class)
    public void b() throws Exception{
        try {
            System.out.println("b:" + epsxSupplierMapper.insertTest("b", 2)); //入库成功
            int x = 10/0;
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
```

###### 情况5

```java
@Transactional(propagation = Propagation.REQUIRED)
    public void a() {
        try {
            System.out.println("a:" + epsxSupplierMapper.insertTest("a", 1)); //入库成功
            TransTest a = (TransTest) AopContext.currentProxy();
            a.b();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
    @Transactional(propagation = Propagation.REQUIRED)
    public void b() throws Exception{
        try {
            System.out.println("b:" + epsxSupplierMapper.insertTest("b", 2));  // 入库成功
            int x = 10/0;
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
```

###### 情况6  `正确方式, 注意: spring.aop.proxy-target-class=true`
```java
@Transactional(propagation = Propagation.REQUIRED)
    public void a() {
        try {
            System.out.println("a:" + epsxSupplierMapper.insertTest("a", 1)); //入库成功
            TransTest a = (TransTest) AopContext.currentProxy();
            a.b();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void b() throws Exception{
        try {
            System.out.println("b:" + epsxSupplierMapper.insertTest("b", 2));  // `入库失败`
            int x = 10/0;
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
```

