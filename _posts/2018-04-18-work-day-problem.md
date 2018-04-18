---
layout: post
title: Git常用命令
excerpt: 记录积累Git日常命令
category: Tools
---

#### FastJson value为null时不输出结果的处理方法

```java
JSONObject jsonObject = new JSONObject();
jsonObject.put("id", null);
jsonObject.put("abc", 0);
System.out.println(jsonObject.toJSONString());//{"abc":0}
System.out.println(JSONObject.toJSONString(jsonObject, SerializerFeature.WriteMapNullValue));//{"abc":0,"id":null}
```
