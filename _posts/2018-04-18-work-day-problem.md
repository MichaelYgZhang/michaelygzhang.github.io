---
layout: post
title: Java开发日常问题速查手册
excerpt: FastJson、Mybatis、HDFS等常见技术问题的解决方案记录
category: Experience
tags: [Java, FastJson, Mybatis, HDFS, 问题排查]
---

## Executive Summary

### 核心观点（金字塔原理）
> **结论先行**: 开发过程中常见技术问题需要及时记录，形成可复用的问题解决方案库
>
> **支撑论点**:
> 1. FastJson序列化null值需使用SerializerFeature.WriteMapNullValue配置
> 2. Mybatis缓存问题可通过flushcache="true"强制刷新解决
> 3. HDFS HQL查询需注意数据类型转换，字符串需cast为整数

### SWOT 分析
| 维度 | 分析 |
|------|------|
| **S** 优势 | 问题记录简洁明了，包含可直接复用的代码示例 |
| **W** 劣势 | 问题覆盖面较窄，缺少问题产生的根因分析 |
| **O** 机会 | 可扩展为团队共享的问题知识库 |
| **T** 威胁 | 技术版本更新可能导致解决方案失效 |

### 适用场景
- Java后端开发日常问题快速排查
- FastJson、Mybatis、HDFS技术栈的常见坑点规避

---

#### FastJson value为null时不输出结果的处理方法

```java
JSONObject jsonObject = new JSONObject();
jsonObject.put("id", null);
jsonObject.put("abc", 0);
System.out.println(jsonObject.toJSONString());//{"abc":0}
System.out.println(JSONObject.toJSONString(jsonObject, SerializerFeature.WriteMapNullValue));//{"abc":0,"id":null}
```

##### Mybatis
- Session, Cache问题解决: `<select ... flushcache="true">`


##### HDFS HQL查询注意事项
- 注意字符串还是整数,如果是字符串类型则需要转化为整数 cast(xxxx)
