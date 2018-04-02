---
layout: post
title: Redis系统总结研究
excerpt: Redis系统总结研究
category: Destributed
---

- [Redis命令参考](http://doc.redisfans.com/)
- [Redis命令参考2](http://redisdoc.com/)
- 注意: 源码版本3.2.8

##### 总结Redis使用以及底层实现原理

##### 第一部分: Redis安装

```js
//Mac 安装brew
brew install redis
redis-server
redis-cli
```

##### 第二部分: Redis整体架构；

1. 初始化Server相关参数设置默认值
2. 读取配置文件，覆盖默认值选项
3. 初始化服务器功能模块;
 - 1. 注册信号实践
 - 2. 初始化客户端链表
 - 3. 初始化共享对象
 - 4. 检测设置最大客户端连接数
 - 5. 初始化数据库
 - 6. 初始化网络连接
 - 7. 是否初始化AOF重写
 - 8. 初始化服务器实时统计数据
 - 9. 初始化后台计划任务
 - 10. 初始化慢查询日志
 - 11. 初始化后台线程任务
4. 从RDB或AOF重载数据(如果开启了AOF,优先AOF恢复数据.否则从RDB恢复数据.如果恢复数据失败,则直接退出)
5. 网络监听启动前的准备工作
6. 进入循环开启事件监听，接受客户端请求.

#### 事件处理
> 文件事件(fileEvent):Redis通过套接字与客户端进行连接，而文件事件就是服务器对套接字操作的抽象。时间事件: Redis一些操作需要在给定的事件点执行，而时间事件就是服务器对这类定时操作的抽象。

```java
/* File event structure */
typedef struct aeFileEvent {
    // 文件时间类型：AE_NONE，AE_READABLE，AE_WRITABLE
    int mask; /* one of AE_(READABLE|WRITABLE) */
    // 可读处理函数
    aeFileProc *rfileProc;
    // 可写处理函数
    aeFileProc *wfileProc;
    // 客户端传入的数据
    void *clientData;
} aeFileEvent;  //文件事件
```

```java
/* Time event structure */
typedef struct aeTimeEvent {
    // 时间事件的id
    long long id; /* time event identifier. */
    // 时间事件到达的时间的秒数
    long when_sec; /* seconds */
    // 时间事件到达的时间的毫秒数
    long when_ms; /* milliseconds */
    // 时间事件处理函数
    aeTimeProc *timeProc;
    // 时间事件终结函数
    aeEventFinalizerProc *finalizerProc;
    // 客户端传入的数据
    void *clientData;
    // 指向下一个时间事件
    struct aeTimeEvent *next;
} aeTimeEvent;  //时间事件
```

```java
/* State of an event based program */
typedef struct aeEventLoop {
    // 当前已注册的最大的文件描述符
    int maxfd;   /* highest file descriptor currently registered */
    // 文件描述符监听集合的大小
    int setsize; /* max number of file descriptors tracked */
    // 下一个时间事件的ID
    long long timeEventNextId;
    // 最后一次执行事件的时间
    time_t lastTime;     /* Used to detect system clock skew */
    // 注册的文件事件表
    aeFileEvent *events; /* Registered events */
    // 已就绪的文件事件表
    aeFiredEvent *fired; /* Fired events */
    // 时间事件的头节点指针
    aeTimeEvent *timeEventHead;
    // 事件处理开关
    int stop;
    // 多路复用库的事件状态数据
    void *apidata; /* This is used for polling API specific data */
    // 执行处理事件之前的函数
    aeBeforeSleepProc *beforesleep;
} aeEventLoop;  //事件轮询的状态结构
```

```java
// 事件轮询的主函数
void aeMain(aeEventLoop *eventLoop) {
    eventLoop->stop = 0;
    // 一直处理事件
    while (!eventLoop->stop) {
        // 执行处理事件之前的函数
        if (eventLoop->beforesleep != NULL)
            eventLoop->beforesleep(eventLoop);
        //处理到时的时间事件和就绪的文件事件
        aeProcessEvents(eventLoop, AE_ALL_EVENTS);
    }
}
```


##### 第三部分: 内部数据结构源码分析； 
##### 第四部分: 分布式锁，事务，持久化；
##### 第五部分: Redis集群研究；
##### 第六部分: Redis整体设计思考, 优缺点分析，是否有更好方案替代?



