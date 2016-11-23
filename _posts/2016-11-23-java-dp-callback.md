---
layout: post
title: CallBack
excerpt: CallBack Demo
category: DP
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
