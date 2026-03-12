---
layout: post
title: 垃圾回收算法手册：标记-清扫算法详解
excerpt: 深入解析标记-清扫回收算法的实现原理，包含伪代码实现与三色标记抽象
category: GC
tags: [GC, 垃圾回收, 标记-清扫, 算法, 内存管理]
---

## Executive Summary

### 核心观点（金字塔原理）
> **结论先行**: 标记-清扫是最基础的垃圾回收算法，通过标记存活对象、清扫未标记对象两个阶段实现内存回收。
>
> **支撑论点**:
> 1. 分配阶段（New）：先尝试分配，失败则触发GC后重试
> 2. 标记阶段（markFromRoots）：从GC Roots出发，遍历标记所有可达对象
> 3. 清扫阶段（sweep）：线性扫描堆空间，回收未标记对象

### SWOT 分析

| 维度 | 分析 |
|------|------|
| **S** 优势 | 算法原理清晰，伪代码实现便于理解，是学习GC的基础 |
| **W** 劣势 | 内容较简短，仅涵盖标记-清扫算法，未涉及其他算法 |
| **O** 机会 | 适合理解GC基本原理，为学习复制算法、G1等奠定基础 |
| **T** 威胁 | 标记-清扫会产生内存碎片，实际生产中常需配合压缩算法 |

### 适用场景
- GC算法入门学习
- 理解三色标记抽象（黑、灰、白）的工作机制
- 分析标记-清扫算法的实现细节

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
