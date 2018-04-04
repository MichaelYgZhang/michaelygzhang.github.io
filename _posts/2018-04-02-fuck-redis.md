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

```jshelllanguage
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

#### 事件处理 select/epoll/kqueue

##### 事件处理概述:

- Redis采用Reactor模式来处理事件，Redis会将所有待处理的事件放入事件池，然后挨个取出其中的事件，
调用该事件的回调函数对其进行处理，这样的模式就称为Reactor模式。
- Redis的事件分为文件事件和时间事件两种。其中，文件事件采用I/O多路复用技术，监听I/O事件，
例如读、写事件等，当事件的描述符变为可读或可写时，就将该事件放入待处理事件池，Redis在事件循环的时候会对其进行一一处理。
而时间事件则是维护一个定时器，每当满足预设的时间要求，就将该时间事件标记为待处理，然后在Redis的事件循环中进行处理。
Redis对于这两种事件的处理优先级是，文件事件优先于时间事件。
- 文件事件(fileEvent):Redis通过套接字与客户端进行连接，而文件事件就是服务器对套接字操作的抽象。
- 时间事件: Redis一些操作需要在给定的事件点执行，而时间事件就是服务器对这类定时操作的抽象。

```cgo
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

```cgo
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

```cgo
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

```cgo
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

- aeProcessEvents(eventLoop, AE_ALL_EVENTS); 核心逻辑:

1. 查找最早的时间事件，判断是否需要执行，如需要，就标记下来，等待处理
2. 获取已准备好的文件事件描述符集
3. 优先处理读事件
4. 处理写事件
5. 如有时间事件，就处理时间事件

##### 第三部分: 内部数据结构源码分析； 
#### SDS(Simple Dynamic String)
- sds 代替了C默认的`char*`类型,因为char*功能单一,抽象层次低，并且不能高效地支持一些Redis常见操作，比如
追加操作和长度计算，所以在redis内部，大多数使用sds而不是char*表示字符串；
- 在C中，字符串以`\0`结尾的char数组来表示，缺点是，每次计算字符串的长度(strlen(s))复杂度O(n);
对字符串进行N次追加，必定需要对字符串进行N次内存重分配(realloc); 由于对字符串的追加APPEND和长度计算STRLEN
操作很频繁，所以不应该成为性能瓶颈。以及Redis字符串还应该是`二进制安全的`数据可以以任意结尾不一定就是`\0`;
归结以上原因所以替换了C默认的`char*`;

```cgo
#define SDS_MAX_PREALLOC (1024*1024)    //预先分配内存的最大长度1MB
typedef char *sds;  //sds兼容传统C风格字符串，所以起了个别名叫sds，并且可以存放sdshdr结构buf成员的地址
struct sdshdr {
    unsigned int len;   //buf中已占用空间的长度
    unsigned int free;  //buf中剩余可用空间的长度,惰性释放,在做释放操作时并不会马上减少SDS所占内存，而是free增加,同时对外提供真正释放的API,被调用时才真正释放
    char buf[];         //初始化sds分配的数据空间
};

```

```cgo
//举例
struct sdshdr {
    len = 11; // O(1) 计算长度
    free = 0; 
    buf = "hello world\0"; //buf 实际长度为len+1
}
//当操作 `append msg " again!"` 则
struct sdshdr {
    len = 18;
    free = 18; // 这里做了扩容操作，小于SDS_MAX_PREALLOC则2倍扩容否则分配SDS_MAX_PREALLOC大小；
    buf = "hello world again!\0";
}
```

- 扩容逻辑

```cgo
/* Enlarge the free space at the end of the sds string so that the caller
 * is sure that after calling this function can overwrite up to addlen
 * bytes after the end of the string, plus one more byte for nul term.
 *
 * Note: this does not change the *length* of the sds string as returned
 * by sdslen(), but only the free buffer space we have. */
sds sdsMakeRoomFor(sds s, size_t addlen) {
    struct sdshdr *sh, *newsh;
    size_t free = sdsavail(s);  //获得s的未使用空间长度
    size_t len, newlen;
    if (free >= addlen) return s;   //free的长度够用不用扩展直接返回
    //free长度不够用，需要扩展
    len = sdslen(s);    //获得s字符串的长度
    sh = (void*) (s-(sizeof(struct sdshdr)));
    newlen = (len+addlen);  //扩展后的新长度
    if (newlen < SDS_MAX_PREALLOC)  //新长度小于“最大预分配长度”，就直接将扩展的新长度乘2
        newlen *= 2;
    else
        newlen += SDS_MAX_PREALLOC; //新长度大于“最大预分配长度”，就在加上一个“最大预分配长度”
    newsh = zrealloc(sh, sizeof(struct sdshdr)+newlen+1);   //获得新的扩展空间的地址
    if (newsh == NULL) return NULL;

    newsh->free = newlen - len; //更新新空间的未使用的空间free
    return newsh->buf;
}

```

#### 小结: 
- Redis字符串表示为sds，不是C字符串以`\0`结尾的char*;
- sds做了如下改进
- 1. 高效执行长度计算(strlen)
- 2. 高效进行追加操作(append)
- 3. 二进制安全? 怎么理解,简单讲不以任何特殊格式为结尾就是二进制安全的，比如C以`\0`就不是二进制安全的。
- ![二进制安全](http://www.cnblogs.com/Alight/p/4123043.html)  ![wiki-binary-safe](https://en.wikipedia.org/wiki/Binary-safe)
- sds可能会在做APPEND操作时进行扩容操作，从而加快追加操作速度，并降低内存分配次数，代价时多占用了些内存。

#### 双端链表 
- 操作:RPUSH, LPOP, LLEN...
- Redis列表使用两种数据结构作为底层实现；1. 双端链表 2. 压缩列表； 由于双端链表占用的内存比压缩列表要多，
所以当创建新的列表键时，列表会优先考虑使用压缩列表作为底层实现，并且在有需要的时候，才从压缩列表实现转换到
双端链表实现。
- 除了实现列表类型以外，双端链表还被很多 Redis 内部模块所应用:

```html
 • 事务模块使用双端链表来按顺序保存输入的命令;
 • 服务器模块使用双端链表来保存多个客户端;
 • 订阅/发送模块使用双端链表来保存订阅模式的多个客户端;
 • 事件模块使用双端链表来保存时间事件(time event)
```

- 具体数据结构，以及对应的特点

```cgo
typedef struct listNode {
    struct listNode *prev;  //前驱节点，如果是list的头结点，则prev指向NULL
    struct listNode *next;  //后继节点，如果是list尾部结点，则next指向NULL
    void *value;    //万能指针，能够存放任何信息 ⚠️
} listNode;

typedef struct listIter {
    listNode *next;     //迭代器当前指向的节点（名字叫next有点迷惑）
    int direction;      //迭代方向，可以取以下两个值：AL_START_HEAD和AL_START_TAIL
} listIter;

typedef struct list {
    listNode *head;         //链表头结点指针
    listNode *tail;         //链表尾结点指针

    //下面的三个函数指针就像类中的成员函数一样
    void *(*dup)(void *ptr);    //复制链表节点保存的值
    void (*free)(void *ptr);    //释放链表节点保存的值
    int (*match)(void *ptr, void *key); //比较链表节点所保存的节点值和另一个输入的值是否相等
    unsigned long len;          //链表长度计数器 时间复杂度O(1)
} list;
```

#### 字典 dictionary

```cgo
typedef struct dictEntry {
    void *key;          //key
    union {
        void *val;
        uint64_t u64;
        int64_t s64;
        double d;
    } v;                //value
    struct dictEntry *next; //指向下一个hash节点，用来解决hash键冲突（collision）
} dictEntry;
```

```cgo
typedef struct dictType {
    unsigned int (*hashFunction)(const void *key);  //计算hash值的函数
    void *(*keyDup)(void *privdata, const void *key);   //复制key的函数
    void *(*valDup)(void *privdata, const void *obj);   //复制value的函数
    int (*keyCompare)(void *privdata, const void *key1, const void *key2);//比较key的函数
    void (*keyDestructor)(void *privdata, void *key);   //销毁key的析构函数
    void (*valDestructor)(void *privdata, void *obj);   //销毁val的析构函数
} dictType;
```

```cgo
/* This is our hash table structure. Every dictionary has two of this as we
 * implement incremental rehashing, for the old to the new table. */
typedef struct dictht { //哈希表
    dictEntry **table;  //存放一个数组的地址，数组存放着哈希表节点dictEntry的地址。
    unsigned long size; //哈希表table的大小
    unsigned long sizemask; //用于将哈希值映射到table的位置索引。它的值总是等于(size-1)。
    unsigned long used; //记录哈希表已有的节点（键值对）数量。
} dictht;

typedef struct dict {
    dictType *type; //指向dictType结构，dictType结构中包含自定义的函数，这些函数使得key和value能够存储任何类型的数据。
    void *privdata; //私有数据，保存着dictType结构中函数的参数。
    dictht ht[2];   //两张哈希表。只是用ht[0],当发生rehash时,ht[1]才被使用; 
    long rehashidx; //rehash的标记，rehashidx==-1，表示没在进行rehash
    int iterators; //正在迭代的迭代器数量
} dict;
```

- TODO 什么情况下发生rehash? key发生碰撞次数过多？怎么rehash?

- ![Redis-Rehash](https://raw.githubusercontent.com/MichaelYgZhang/michaelygzhang.github.io/master/images/redis-rehash.png)

#### 核心流程
1. 计算key的hash值，找到hash映射到table数组的下标。
2. 如果key已经存在，则hash碰撞，链表处理
3. 如果key多次发生碰撞，链表将越来越长，查询速度越来越慢，为了维持正常的负载，Redis将会进行`渐进式rehash`操作，增加table数组长度。步骤如下:
- 1. 根据ht[0]的数据和操作的类型(扩容/缩小)，分配ht[1]大小,并修改rehashidx值
- 2. 将ht[0]的数据rehash到ht[1]上
- 3. rehash完成以后,将ht[1]设置为ht[0],并生成一个新的ht[1]以备下次使用
4. 考虑到key数量可能千万级别，一次rehash将会是一个相对较长的时间，所以为了在rehash期间能继续对外提供服务，Redis采用渐进式rehash.
- 1. 分配ht[1]空间,字典同时持有ht[0]和ht[1].
- 2. 在字典中维护一个rehashidx，设置为0，表示字典正在进行rehash操作。
- 3. 在rehash期间，每次对字典的操作除了进行指定的操作外，都会根据ht[0]的在rehashidx上对应的键值对rehash到ht[1]
- 4. 随着多次操作ht[0]的数据将会全部rehash到ht[1]上，设置ht[0]的rehashidx=-1表示rehash过程结束
5. 在进行rehash过程中，如果进行了delete和update等操作，会在两个哈希表上进行，如果是查询则优先在ht[0]上积习难改，如果没有，再去ht[1]中查找。如果是insert则只会在ht[1]中插入数据，这样保证了ht[1]的数据只增不减，ht[0]的数据不增。
> 思考: 1. rehash触发有哪些情况? 3. 如果扩容的时候，rehash还未结束，有发生了rehash会怎么样? 







##### 第四部分: 分布式锁，事务，持久化；
##### 第五部分: Redis集群研究；
##### 第六部分: Redis整体设计思考, 优缺点分析，是否有更好方案替代?



