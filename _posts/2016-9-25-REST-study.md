---
layout: post
title: RESTful note
excerpt: RESTful note
category: CS
---

#### RESTful架构风格
- `REST`即`Representational State Transfer`的缩写，可译为"表现层状态转化”。`REST`最大的几个特点为：资源、统一接口、`URI`和无状态。

**RESTful架构就是用URI定位资源，用HTTP方法描述操作。**

##### 资源
- 资源常见的载体为json、面向用户的一组数据集，

###### 综合上面的解释，总结一下什么是RESTful架构：
1. 每一个URI代表一种资源；
2. 客户端和服务器之间，传递这种资源的某种表现层；
3. 客户端通过几个HTTP动词，对服务器端资源进行操作，实现"表现层状态转化"。

###### RESTful设计误区
- 最常见的一种设计错误，就是URI包含动词。因为"资源"表示一种实体，所以应该是名词，且为复数形式，URI不应该有动词，动词应该放在HTTP协议中。

###### 举例:
- GET /collection：返回资源对象的列表（数组）
- GET /collection/resource：返回单个资源对象
- POST /collection：返回新生成的资源对象
- PUT /collection/resource：返回完整的资源对象
- PATCH /collection/resource：返回完整的资源对象
- DELETE /collection/resource：返回一个空文档

[理解RESTful](http://www.ruanyifeng.com/blog/2011/09/restful.html)
