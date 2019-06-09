---
layout: post
title: 工作日常问题记录
excerpt: 日常工作小问题记录
category: Experience
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