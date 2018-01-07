---
layout: post
title: Linux Command
excerpt: Linux Command
category: Linux
---

#### 前言

- 命令格式 ： command -options arguments

###### sort

```js
-b：忽略每行前面开始出的空格字符；
-c：检查文件是否已经按照顺序排序；
-d：排序时，处理英文字母、数字及空格字符外，忽略其他的字符；
-f：排序时，将小写字母视为大写字母；
 -i：排序时，除了040至176之间的ASCII字符外，忽略其他的字符；
 -m：将几个排序号的文件进行合并；
-M：将前面3个字母依照月份的缩写进行排序；
-n：依照数值的大小排序；
-o<输出文件>：将排序后的结果存入制定的文件；
 -r：以相反的顺序来排序；
-t<分隔字符>：指定排序时所用的栏位分隔字符；
+<起始栏位>-<结束栏位>：以指定的栏位来排序，范围由起始栏位到结束栏位的前一栏位。
-n是按照数字大小排序，-r是以相反顺序，-k是指定需要爱排序的栏位，-t指定栏位分隔符为冒号
[root@mail text]# cat sort.txt
AAA:BB:CC
aaa:30:1.6
ccc:50:3.3
ddd:20:4.2
bbb:10:2.5
eee:40:5.4
eee:60:5.1
#将BB列按照数字从小到大顺序排列：
 [root@mail text]# sort -nk 2 -t: sort.txt
AAA:BB:CC
bbb:10:2.5
ddd:20:4.2
aaa:30:1.6
eee:40:5.4
ccc:50:3.3
eee:60:5.1
#将CC列数字从大到小顺序排列：
 [root@mail text]# sort -nrk 3 -t: sort.txt
eee:40:5.4
eee:60:5.1
ddd:20:4.2
ccc:50:3.3
bbb:10:2.5
aaa:30:1.6
AAA:BB:CC
```

##### uniq

```js
从输入文件或者标准输入中筛选相邻的匹配行并写入到输出文件或标准输出。
-c, --count            //在每行前加上表示相应行目出现次数的前缀编号  
-d, --repeated         //只输出重复的行  
-D, --all-repeated     //只输出重复的行，不过有几行输出几行  
-f, --skip-fields=N    //-f 忽略的段数，-f 1 忽略第一段   
-i, --ignore-case      //不区分大小写  
-s, --skip-chars=N      //根-f有点像，不过-s是忽略，后面多少个字符 -s 5就忽略后面5个字符  
-u, --unique           	//去除重复的后，全部显示出来，根mysql的distinct功能上有点像  
-z, --zero-terminated   end lines with 0 byte, not newline  
-w, --check-chars=N     //对每行第N 个字符以后的内容不作对照  
--help              	//显示此帮助信息并退出  
--version              	//显示版本信息并退出  
```

##### ls

##### 在VI中使用Linux命令

```js
//文本数据
2
1
3
4
:1,$!sort 含义:从第一行到最后一行`$`, `!`可以执行后面跟command,格式: `:1,$!command`
结果:
1
2
3
4
```
