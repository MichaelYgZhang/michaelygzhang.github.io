---
layout: post
title: Zookeeper
excerpt: Zookeeper
category: Architecture
published: true
author: michael
---

#### [Zookeeper](http://zookeeper.apache.org/)

##### Dubbo架构
![Dubbo](https://raw.githubusercontent.com/MichaelYgZhang/michaelygzhang.github.io/master/images/dubbo.png)

- 数据结构+原语+watcher机制(消息通知)
- 问题: 在server挂机时到zookeeper接收到，再到zookeeper通知到client端是有一定的时长的，那么在这段时间内client的服务是不是就丢了？导致全部失败？还是其他什么情况？
- ZooKeeper可以为所有的读操作设置watch，这些读操作包括：exists()、getChildren()及getData()。watch事件是一次性的触发器，当watch的对象状态发生改变时，将会触发此对象上watch所对应的事件。watch事件将被异步地发送给客户端，并且ZooKeeper为watch机制提供了有序的一致性保证。理论上，客户端接收watch事件的时间要快于其看到watch对象状态变化的时间。
