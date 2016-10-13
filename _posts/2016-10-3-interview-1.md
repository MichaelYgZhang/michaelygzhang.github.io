---
layout: post
title: Interview-1
excerpt: Interview-1
category: Interview
---

####  2016-10-12
Java 8种基本数据类型

```js
基本类型 -> 数值类型 -> 整数类型: byte、short、int、long
                   -> 浮点数据类型: float、double
                   -> 字符类型: char  
基本类型 -> boolean

引用类型 -> 引用 -> 类类型
                -> 接口类型
                -> 数组类型

1byte = 8bits
计算机存储为补码，java也是如此，byte = 8bits, short = 16bits, int = 32bits, long = 64bits , char = 16bits, float = 32bits, double = 64bits, boolean = 8bits
java采用Unicode字符编码，所谓字符编码就是用一串二进制数据来表示特定的字符。
数据需要高精度的场景需要采用java.math.BigDecimal

类的成员变量默认值:byte,short,int,long:0; float:0.0f; double:0.0d; char:"\u0000"; boolean:false; 引用类型:null
注意:局部变量JVM不会自动初始化为默认值，所以必须先显式初始化，才能使用。
当类型低于int时，比如char，则会按照int进行计算;比如String s = '1' + '2' + "abc";
s = 99abc;// 1 = 49; 2 = 50;
```

转义字符 |描述|
:-------|:----|
`\n`      |换行符，将光标定位到下一行的开头|
`\t`|垂直制表符，将光标移动到下一个制表符的位置|
`\r`|回车，将光标定位在当前行的开头，不会跳到下一行|
`\\`|代表反斜杠|
`\'`|代表单引号字符|
`\"`|代表双引号|

##### 变量作用域
- 成员变量: 在类中声明，作用域为整个类
- 局部变量: 在一个方法内部或者代码块的内部声明，作用域为方法内或代码块内。
- 方法参数: 作用域为整个方法内部。
- 异常处理参数: 比如catch(Exception e)异常参数e，它的作用域就是紧跟着后面的代码块

*静态变量和实例变量的生命周期*
- 成员变量有两种: 被static修饰的称为静态变量；另一种没有被static修饰的称为实例变量；
静态变量内存中只有一个，JVM加载类的过程中为静态变量分配内存，静态变量位于方法区，被类的所有实例共享，可以直接通过类名访问，它的生命周期取决于类的生命周期。当加载类时，静态变量被创建并分配内存，当卸载类时，静态变量被销毁并撤销所占内存。
- 类的每一个实例都有相应的实例变量，每创建一个类的实例，JVM就会为实例变量分配一次内存，实例变量位于堆区中，它的生命周期取决于类的实例。


- String底层为private final char value[] + 对这个数组的操作
- StringBuilder JDK1.5 非线程安全; StringBuffer JDK1.0 线程安全在每个方法上加了`synchronized`, 它们都继承与 AbstractStringBuilder

[常见排序算法以及jdk集合源码分析](https://michaelygzhang.github.io/home/)

[Oracle-Collection](http://docs.oracle.com/javase/8/docs/technotes/guides/collections/overview.html)

https://en.wikipedia.org/wiki/Java_(programming_language)
