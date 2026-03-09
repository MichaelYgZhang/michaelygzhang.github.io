---
layout: post
title: Netflix---Hystrix文档翻译--01
excerpt: Netflix---Hystrix文档翻译--01
category: Distributed
---

## Executive Summary

### 核心观点（金字塔原理）
> **结论先行**: Hystrix是Netflix开源的容错库，通过Command模式封装服务调用，支持同步、异步和响应式三种执行方式，实现服务降级和熔断保护。
>
> **支撑论点**:
> 1. Command模式封装：通过HystrixCommand和HystrixObservableCommand两种方式封装远程调用逻辑
> 2. 多种执行方式：支持execute()同步执行、queue()异步执行、observe()/toObservable()响应式执行
> 3. 线程隔离：通过HystrixCommandGroupKey进行命令分组，实现资源隔离和监控

### SWOT 分析
| 维度 | 分析 |
|------|------|
| **S** 优势 | Netflix大规模生产验证；API设计简洁优雅；支持多种执行模式；与RxJava深度集成 |
| **W** 劣势 | 项目已进入维护模式；学习曲线较陡；Observable模式理解成本高 |
| **O** 机会 | 微服务架构的服务容错；分布式系统的弹性设计；服务降级和熔断场景 |
| **T** 威胁 | Resilience4j等新一代容错库的竞争；Spring Cloud Circuit Breaker抽象层的出现 |

### 适用场景
- 微服务架构中的服务间调用保护
- 需要实现服务降级和熔断的分布式系统
- 对第三方依赖调用的容错处理

---

[Hystrix wiki ](https://github.com/Netflix/Hystrix/wiki/How-To-Use)

[How-To-Use](https://github.com/Netflix/Hystrix/wiki/How-To-Use)


#### Hello World!

```java
public class CommandHelloWorld extends HystrixCommand<String> {

    private final String name;

    public CommandHelloWorld(String name) {
        super(HystrixCommandGroupKey.Factory.asKey("ExampleGroup"));
        this.name = name;
    }

    @Override
    protected String run() {
        // a real example would do work like a network call here
        return "Hello " + name + "!";
    }
}

//另一种方式，使用HystrixObservableCommand替代HystrixCommand需要覆盖其构造方法。
public class CommandHelloWorld extends HystrixObservableCommand<String> {

    private final String name;

    public CommandHelloWorld(String name) {
        super(HystrixCommandGroupKey.Factory.asKey("ExampleGroup"));
        this.name = name;
    }

    @Override
    protected Observable<String> construct() {
        return Observable.create(new Observable.OnSubscribe<String>() {
            @Override
            public void call(Subscriber<? super String> observer) {
                try {
                    if (!observer.isUnsubscribed()) {
                        // a real example would do work like a network call here
                        observer.onNext("Hello");
                        observer.onNext(name + "!");
                        observer.onCompleted();
                    }
                } catch (Exception e) {
                    observer.onError(e);
                }
            }
         } ).subscribeOn(Schedulers.io());
    }
}
```

#### 同步执行  Synchronous Execution
- 使用HystrixCommand的方式时，可以运行execute()方法,以及对应的测试用例
```java
String s = new CommandHelloWorld("World").execute();
@Test
public void testSynchronous() {
  assertEquals("Hello World!", new CommandHelloWorld("World").execute());
  assertEquals("Hello Bob!", new CommandHelloWorld("Bob").execute());
}
```
##### HystrixObservableCommand Equivalent
- There is no simple equivalent to execute for a HystrixObservableCommand, but if you know that the Observable produced by such a command must always produce only a single value, you can mimic the behavior of execute by applying .toBlocking().toFuture().get() to the Observable.

#### 异步执行 Asynchronous Execution
- 使用HystrixCommand的方式时，queue()方法执行。

```java
Future<String> fs = new CommandHelloWorld("World").queue();
String s = fs.get();//获取结果
@Test
public void testAsynchronous1() throws Exception {
    assertEquals("Hello World!", new CommandHelloWorld("World").queue().get());
    assertEquals("Hello Bob!", new CommandHelloWorld("Bob").queue().get());
}

@Test
public void testAsynchronous2() throws Exception {

    Future<String> fWorld = new CommandHelloWorld("World").queue();
    Future<String> fBob = new CommandHelloWorld("Bob").queue();

    assertEquals("Hello World!", fWorld.get());
    assertEquals("Hello Bob!", fBob.get());
}
```

- 两种执行方式结果相同
```java
String s1 = new CommandHelloWorld("World").execute();
String s2 = new CommandHelloWorld("World").queue().get();
```

###### HystrixObservableCommand Equivalent
- There is no simple equivalent to queue for a HystrixObservableCommand, but if you know that the Observable produced by such a command must always produce only a single value, you can mimic the behavior of queue by applying the RxJava operators .toBlocking().toFuture() to the Observable.

#### 非阻塞方式执行 Reactive Execution
