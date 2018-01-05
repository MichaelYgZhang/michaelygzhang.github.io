---
layout: post
title: 垃圾回收算法手册-笔记
excerpt: The Garbage Collection Handbook
category: GC
---

##### 第2章 标记-清扫回收

- 具体算法。以下为伪代码`<-`表示赋值。

```C
  `New`():      /* 分配过程*/
  ref <- allocate()
  if ref = null     /*堆中无可用空间*/
    collect()
    ref <- allocate()
    if ref = null     /*堆中仍然无可用空间*/
      error "Out of memory"
  return ref

atomic collect():     /* 注意此处是原子操作*/
  markFromRoots()
  sweep(HeapStart, HeapEnd)  

markFromRoots():      /*标记过程*/
  initialise(worklist)
  for each fld in Roots
    ref <- *fld
    if ref != null && not isMarked(ref)
      setMarked(ref)
      add(worklist, ref)
      mark()

initialise(worklist):
  worklist <- empty

mark():
  while not isEmpty(worklist)
    ref <- remove(worklist)     /* ref已经标记过*/
    for each fld in Pointers(ref)
      child <- *fld
      if child != null && not isMarked(child)
        setMarked(child)
        add(worklist, child)

/* 清扫阶段*/
sweep(start, end):
  scan <- start
  while scan < end
    if isMarked(scan)
      unsetMarked(scan)
    else free(scan)
      scan <- nextObject(scan)

```

- 三色抽象:描述了追踪式回收器的一种有效方法，黑色表示存活，灰色表示回收器已处理但对象尚未完成处理，白色表示回收器稍微扫描到的对象(某些对象可能永远无法扫描到)，一个标记栈。
