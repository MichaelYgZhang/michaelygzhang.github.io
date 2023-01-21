---
layout: post
title: Alfred Workflows使用总结
excerpt: tools
category: tools
---

### Alfred
- 特点：收费，提高工作效率的工具，可以自定义工作流提高工作效率
- WorkFlow，支持/bin/bash; /python等；

### Workflow 开发流程
1. 创建脚本
2. script 填写 /usr/bin/python script.py "{query}"；此处选择python开发，需要先学习一下python简单的语法
3. 使用python开发工作流需要再工作流实例的根目录下安装python的依赖
4. 选中对应的工作流右键，在 finder 中打开
```html
Your Workflow/
    info.plist
    icon.png
    workflow/
        __init__.py
        background.py
        notify.py
        Notify.tgz
        update.py
        util.py
        version
        web.py
        workflow.py
        workflow3.py
    yourscript.py
    etc.
```
5. 安装依赖， 在上面打开的目录中执行；`pip install --target=. Alfred-Workflow`，
6. 执行后：workflow 目录上面安装的依赖包，youscript.py是我们下面需要介绍的
7. 可以先安装部分依赖: `pip install browsercookie; pip install requests`
8. 开发youscript.py脚本；脚本内容：使用http接口查询{yourWebSite}上面查询配置信息，然后解析成Alfred的下拉框选项，组装{yourWebSite}的跳转连接，使用arg属性传输到下一步
9. 空白处右键，创建 action --> openUrl，URL录入{query}或者采用其他方式

```python
#!/usr/bin/env python
# coding:utf-8

import requests
import json
import browsercookie
import sys
import time
from workflow import Workflow, ICON_WEB, web

url = 'https://xxx.xxx.com/api/xxx?_search='
cookies = browsercookie.chrome()
icon='/item.ico' #show your icon

def send_request(query): # 发送http请求获取数据
    params = {"key": query} # 拼接请求参数
    r = requests.get(url=url, cookies=cookies, params=params)
    return json.loads(r.text)

def main(wf): # 获取输入框中的参数，查询接口，将放回信息放到 Workflow 中（会自动转换成 XML），alfred 选中对应item 回车会将 arg 作为参数传递到下一个操作对象
    if len(wf.args):
        query = wf.args[0]
    else:
        query = None #使用缓存加速# result = send_request(query)
    result = wf.cached_data(query, lambda :send_request(query), max_age=60)
    wf.logger.info(result) # logger，在debug console中显示，可以进行调试
    for item in result['data']:
        name = item['key']
        path = str(name).replace(".", "/")
        linkUrl = 'https://xxx.xxx.com/' + path  # 跳转链接
        wf.add_item(title=name, icon=icon, arg=linkUrl, valid=True)
    wf.send_feedback()

if __name__ == '__main__': # 构造 Workflow 对象，运行完退出
    wf = Workflow()
    sys.exit(wf.run(main))
```

##### 其他注意事项
- 导入安装可能遇到的问题
1. 由于脚本使用的python开发需要对应的python环境。alfred 的工作流依赖 python 2.7，不支持python3
2. 脚本中使用到了一些python的包，所以需要安装下。使用 pip install 进行安装就行，pip 没有安装的可以在网上查下
3. 脚本中使用requests模块去请求接口，这里接口大部分是不要登录才能访问的，所以这里使用了一个包（browsercookie）来获取本地的浏览器 cookies。
4. 在第一次发送请求的时候会提示授权，输入密码点击始终允许。
5. `查看alfred工作的运行情况可以通过debug日志查看`

#### 资料
- 官网：https://www.alfredapp.com/
- workflows：https://www.alfredworkflows.store/
- 中英文翻译：https://github.com/xfslove/alfred-google-translate

