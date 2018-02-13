---
layout: post
title: Go并发原理
excerpt: Go并发
category: Go
---

#### Goroutine

##### 协程Coroutine

- 轻量级"线程"
- 非抢占式多任务处理，由协程主动交出控制权
- 编译器／解释器／虚拟机层面的多任务
- 多个协程可以在一个或多个线程上运行
- `runtime.Gosched()`协程主动交出控制权
- 子程序是协程的一个特例

###### goroutine的定义

- 任何函数只需要加上go就能送给调度器运行
- 不需要在定义时区分是否是异步函数
- 调度器在合适的点进行切换,切换点如下:
  - I/O,select
  - channel
  - 等待锁
  - 函数调用有时
  - runtime.Gosched()
  - 只是参考不能保证切换不能保证在其他地方不切换
- 使用 `-race`来检测数据访问冲突
- channel,buffered channel range 由发送方进行close() channel操作，理论基础`Communication Sequential Process CSP`
- `sync.WaitGroup`等待channel完成通信

- `不要通过共享内存来通信，要通过通信来共享内存`


