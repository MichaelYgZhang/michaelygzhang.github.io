---
layout: post
title: OAuth2.0笔记
excerpt: OAuth2.0笔记
category: CS
---

##### OAuth2.0笔记

1. Third-party application：第三方应用程序，本文中又称"客户端"（client），即上一节例子中的"云冲印"。
2. HTTP service：HTTP服务提供商，本文中简称"服务提供商"，即上一节例子中的Google。
3. Resource Owner：资源所有者，本文中又称"用户"（user）。
4. User Agent：用户代理，本文中就是指浏览器。
5. Authorization server：认证服务器，即服务提供商专门用来处理认证的服务器。
6. Resource server：资源服务器，即服务提供商存放用户生成的资源的服务器。它与认证服务器，可以是同一台服务器，也可以是不同的服务器。


###### OAuth的作用就是让"客户端"安全可控地获取"用户"的授权，与"服务商提供商"进行互动。

![OAuth2.0流程图](http://image.beekka.com/blog/2014/bg2014051203.png)

1. 用户打开客户端以后，客户端要求用户给予授权。
2. 用户同意给予客户端授权。
3. 客户端使用上一步获得的授权，向认证服务器申请令牌。
4. 认证服务器对客户端进行认证以后，确认无误，同意发放令牌。
5. 客户端使用令牌，向资源服务器申请获取资源。
6. 资源服务器确认令牌无误，同意向客户端开放资源。

新浪微博就是你的家。偶尔你会想让一些人（第三方应用）去你的家里帮你做一些事，或取点东西。你可以复制一把钥匙（用户名和密码）给他们，但这里有三个问题：

1. 别人拿了钥匙后可以去所有的房间
2. 别人拿到你的钥匙后也许会不小心丢到，甚至故Third-party application：第三方应用程序，本文中又称"客户端"（client），即上一节例子中的"云冲印"。
3. 过一段时间你也许会想要回自己的钥匙，但别人不还怎么办？

OAuth 是高级钥匙:

1. 你可以配置不同权限的钥匙。有些只能进大厅（读取你的微博流）。有些钥匙可以进储藏柜（读取你的相片)
2. 钥匙上带着指纹验证的（指纹 = appkey)。 收到钥匙的人只能自己用，不能转让
3. 你可以远程废除之前发出的钥匙

相对来说, OAuth比给出用户名密码安全

###### OAuth是让第三方应用不需要用户名密码读取用户数据的一个认证过程。

*OpenID是Authentication*

*OAuth是Authorization*

前者是网站对用户进行认证，让网站知道“你是你所声称的URL的属主”
后者其实并不包括认证，只不过“只有认证成功的人才能进行授权”，结果类似于“认证+授权”了。OAuth相当于：A网站给B网站一个令牌，然后告诉B网站说根据这个令牌你可以获取到某用户在A网站上允许你访问的所有信息

如果A网站需要用B网站的用户系统进行登录（学名好像叫federated login），它可以
选择OpenID认证，然后通过attribute exchange获取用户的昵称或其他通过OpenID暴露出来的用户属性，或者
选择OAuth认证，获取到token后再用token获取用户昵称或其他允许被访问的信息

关于OAuth的授权，不能说是滥用，是OAuth Service Provider对OAuth的权限没有细分。好比我只需要用户的昵称性别，你却把修改昵称性别的权限也授权给我了（虽然我不一定会去用）。这个错在OAuth Service Provider

[OAuth2.0](https://en.wikipedia.org/wiki/OAuth)
[理解OAuth2.0](http://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html)
[知乎链接1](https://www.zhihu.com/question/19781476/answer/13158282)
[知乎链接2](https://www.zhihu.com/question/19628327/answer/12591409)
