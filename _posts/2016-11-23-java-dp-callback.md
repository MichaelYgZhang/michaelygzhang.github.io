---
layout: post
title: Java回调模式详解：异步编程的核心机制
excerpt: 通过完整代码示例深入理解Java回调模式的实现原理，掌握异步处理中的回调机制设计
category: DP
tags: [Java, 设计模式, 回调模式, 异步编程, CallBack]
---

## Executive Summary

### 核心观点（金字塔原理）
> **结论先行**: 回调模式通过将回调接口传递给被调用者，实现调用者在异步操作完成后获得通知，是Java异步编程的核心机制。
>
> **支撑论点**:
> 1. 三方协作：Calling(调用者)实现CallBack接口、Called(被调用者)执行业务并回调、CallBack接口定义响应方法
> 2. 异步特性：调用者发起请求后立即执行其他方法(otherMethod)，不阻塞等待结果
> 3. 解耦设计：通过接口回调实现调用者与被调用者的松耦合

### SWOT 分析

| 维度 | 分析 |
|------|------|
| **S** 优势 | 实现异步非阻塞调用；调用者与被调用者解耦；代码结构清晰易维护 |
| **W** 劣势 | 回调嵌套过深导致回调地狱；调试困难；异常处理复杂 |
| **O** 机会 | 网络IO操作；耗时任务处理；事件驱动编程；消息队列消费 |
| **T** 威胁 | 回调地狱降低可读性；内存泄漏风险（持有外部引用）；线程安全问题 |

### 适用场景
- 网络请求等耗时操作的异步处理
- 事件监听与响应机制
- 需要在任务完成后执行特定逻辑的场景

---

##### Java CallBack

[回调函数](https://zh.wikipedia.org/wiki/%E5%9B%9E%E8%B0%83%E5%87%BD%E6%95%B0)

- 异步处理中常用的处理方式回调。举个例子，Calling为调用者Called为被调用者以及CallBack接口

```java
  public interface CallBack {
  	void response(String result);
  }
```

```java
  public class Calling implements CallBack{
  	private Called called;
  	public void setCalled(Called called){
  		this.called = called;
  	}

  	public void askQuestion(final String question){
  		new Thread(new Runnable() {
  			@Override
  			public void run() {
  				called.execute(Calling.this, question);
  			}
  		}).start();
  		otherMethod();
  	}

  	private void otherMethod() {
  		System.out.println("Calling other mehtod!");
  	}

  	@Override
  	public void response(String result) {
  		System.out.println("called result:" + result);
  	}
  }
```

```java
  public class Called {
  	public void execute(CallBack callBack, String question){
  		System.out.println("Called question: " + question);
  		try {
  			System.out.println("Called sleep 3s!");//模拟耗时
  			Thread.sleep(3000);
  		} catch (InterruptedException e) {
  			e.printStackTrace();
  		}
  		callBack.response("This is called response!");
  	}
  }
```

```java
  public class CallBackTest {
  	public static void main(String[] args) {
  		Called called = new Called();
  		Calling calling = new Calling();
  		calling.setCalled(called);
  		calling.askQuestion(" who are you");
  	}
  }

  //Calling other mehtod!
  //Called question:  who are you
  //Called sleep 3s!
  //Called result:This is called response!
```
