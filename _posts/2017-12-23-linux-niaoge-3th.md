---
layout: post
title: Linux鸟哥私房菜-3th
excerpt: Linux鸟哥私房菜-3th
category: Linux
---

#### 第3章 主机规划与磁盘分区

- 在Linux系统中，每隔设备都被当成一个文件系统，每隔设备都会有设备文件名
- 磁盘的设备文件名主要分为IDE接口的/dev/hd[a-d]及SATA/SCSI/USB接口的/dev/sd[a-p]两种
- 磁盘的第一个山区主要记录了两个重要的信息，分别是1.主引导分区(Master Boot Record MBR)可以安装引导加载程序的地方，有446bytes;2.分区表(partition table)记录整块磁盘分区的状态有64bytes;
- 磁盘的主分区与扩展分区最多可以有四个，逻辑分区的设备文件名好吗一定由5号开始。
- 开机的流程是：BIOS-->MBR-->boot loader --> 内核文件
- boot loader的功能主要有提供菜单，加载内核，转交控制权给其他loader
- boot loader 可以安装的地点有两个，分别是MBR与boot sector
- Linux操作系统的文件使用目录树系统与磁盘的对应需要有“挂载”的操作才行
- 适合新手的简单分区，建议只要有/以及swap两个分区即可

#### 第4章 安装CentOS 5.X与多重引导小技巧

#### 第5章 首次登陆与在线求助man page

- Ctrl + Alt + [F1~F6] 切换不同的用户
- startx 切换
- date +%Y/%m/%d %H:%M  2017/12/24 23:45
- cal 日历
- bc 默认输出整数如果想输出全部小数必须要执行 scale=number,number就是小数点后的位数，比如 scale=3   1/3  = .333
- man page  比如"DATE(1)"数字代表的含义

代号 | 代表内容
----|--------|
1| 用户在shell环境中可以操作的命令或可执行文件
2|系统内核可调用的函数与工具
3|一些常用的函数与函数库，大部分为C的函数库
4|设备文件的说明，通常在/dev下的文件
5|配置文件或者是某些文件的格式
6|游戏
7|惯例与协议等，例如Linux文件系统，网络协议，ASCII code等说明
8|系统管理员可用的管理命令
9|跟kernel有关文件

- /string 向下查询 ?string 向上查询 n，N 相反方向
- info info enter进入 N下一个节点 P上一个节点 U上一层 ／查询？
- /usr/share/doc/* 帮助文档
- 关机，将数据同步写入硬盘中的命令 `sync` 惯用`shutdown`,重启关机`reboot`,`halt`,`paweroff`

###### shutdown  

- shutdown [-arkhncfF] 时间 [警告信息]
- shutdown -h now 'shutdown system now' //系统的服务停掉后立即关机

参数|含义|
---|---|
-t sec| -t后面加秒杀，即过多少秒后关机的意思
-k| 不是真的关机，只是发出警告消息
`-r`|在将系统的服务停掉之后就重启
`-h`|将系统的服务停掉后，立即关机
-n|不经过init程序直接以shutdown的功能来关机
-f|关机并开机之后强制略过fsck的磁盘检查
-F|系统重启之后强制进行fsck的磁盘检查
`-c`|取消已经进行的shutdown命令

- 系统运作模式 `init`

参数|含义
---|---|
run level 0|关机
run level 3|纯命令行模式
run level 5|含有图形界面模式
run level 6|重启
....TODO|

###### 开机过程中的问题
- `fsck` 文件系统检查命令
- 忘记root密码？

#### 第6章 Linux的文件权限与目录配置

- chgrp : 改变文件所属用户组   -R(Recursive)递归修改
- chown : 改变文件所有者
- chmod : 改变文件的权限 r,w,x=4,2,1 或 chmod u=rwx,go=rx test.txt -rwxr-xr-x ... test.txt
- 注意区分rwx分别对文件以及文件夹的区别。
- 对文件来说,r (read) w(write但不含删除文件) x(eXecute);
- 对文件夹目录,r (read contents in directory)代表有读取目录结构列表的权限，w(modify contents of directory)表示你具有更改该目录结构列表的权限(新建文件与目录，删除已经存在的文件与目录，不论该文件的权限为何，将已经存在的文件或目录重命名，转移该目录内的文件，目录位置)；x(access directory)代表用户是否进入该目录成为工作目录的用户，即 cd 是否允许，即如果没有x权限的目录无法进入目录，提示Permission denied
- 要开放目录给任何人浏览时，至少r+x权限，w不可以随便给予

```js
drwxr-xr-x 1 root root 10 Sep 8 18:00 test  
-rwxr-xr-x 2 root root 10 Sep 8 18:00 test.txt
权限(own,g,other),连接数,文件所有者,用户组,大小,修改日期,文件名。
d:directory,-:文件
```

- Linux默认使用Ext2/Ext3文件系统，文件名长度限制为,单一文件或者目录的最大容许文件名为255个字符，包含完整路径名称及目录的完整文件名为4096个字符
- FHS(Filesystem Hierarchy Standard) 四种目录: shareable,unshareable; static,variable
- FHS三层主目录为: /, /var, /usr(UNIX Software Resource)
- 必须与跟目录放在同一个分区的5个目录:/etc,/bin,/lib,/dev,/sbin
- FHS: http://proton.pathname.com/fhs/

#### 第7章 Linux文件与目录管理
- cd   切换目录
- pwd  显示当前目录 -p: 不以链接文件路径显示
- mkdir  新建一个新目录  -m: 授权限，-p: 递归创建上级目录
- rmdir  删除一个空目录  -p: 连同上级空的目录一起删除

##### ls
```js
-a : 全部文件包括隐藏文件
-A : 全部文件（连同隐藏文件，但不包括.与..这两个目录)
-d : 列出目录本身
-f : 直接列出结果不进行排序(ls默认以文件名排序)
-F : 根据文件，目录等信息给予附加数据结构
-h : 将文件容量以人类较为易读的方式 (GB,KB,等)列出来
-i : 列出inode好吗
-l : 列出文件的属性与权限等数据
-n : 列出UID与GID，而非用户与用户组的名称
-r : 将排序结果反向输出
-R : 连同子目录的内容一起列出来，等于该目录下的所有文件都会显示出来
-S : 以文件大小排序，而不是文件名
-t : 以时间排序而不是用文件名
--color=never : 不要依据文件特性给予颜色显示
--color=always : 显示颜色
--color=auto  : 让系统自行依据设置来判断是否给予颜色
--full-time  : 以完整的时间模式(年月日时分)输出
--time={atime,ctime} : 输出访问时间或者改变权限的时间，而非内容更改时间
```

##### cp (copy)
```js
cp [-adfilprsu] source destination
cp [options] source1 source2 source3 .... directory
-a : 相当于-pdr
-d : 如果源文件为连接文件的属性(link file)则复制连接文件属性，而非文件本身
-f : 为强制(fore)，若目标文件已经存在且无法开启则删除后再尝试一次
-i : 若目标文件已经存在，在覆盖的时候先进行询问操作进行
-l : 进行硬连接(hard link) 的连接文件创建而非复制文件本身
-p : 连同文件的属性一起复制过去，而非使用默认属性
-r : 递归持续复制用于目录的复制行为
-s : 复制成为符号链接文件，即快捷方式文件(symbolic link)
-u : 若destination比source旧才更新 destination
注意若多个源文件最后一个目的文件一定要是“目录”才行
```
##### rm [-fir] 文件或目录
```js
-f : force
-i : 删除前询问
-r : 递归删除，危险⚠️操作
```
##### mv (移动文件与目录或更名)
```js
-f : force
-i : 若目标文件存在，询问是否覆盖
-u : 若目标文件存在，source比较新才更新
```

- 取得路径的文件名与目录名称

```js
basename /XXX/XXX //文件名
dirname /XXX/XXX  //目录名
```

##### 文件内容查阅

```js
cat:
```
