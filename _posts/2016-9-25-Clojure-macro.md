---
layout: post
title: Clojure macro
excerpt: Clojure 宏
category: Clojure
---

#### 宏

```clojure
(defmacro dbg [x] `(let [x# ~x] (println '~x "=" x#) x#))
(defn tt [x] (dbg (+ x 1)))

;user> (tt 1)
;(+ x 1) = 2
;2
```

可以看到我们用defmacro定义了一个dbg的宏，这个宏的作用就是先实现代码喝代码执行的结果，并将结果 返回回去。在clojure的宏里我们主要会用到以下几个符号。

- ' (quote) :表示被quote不求值
- ` (syntax quote) :把变量变成有namespace的形势

```clojure
user> 'x
x
user> `x
user/x
```

- ~ (unquote):⚠️`~`和点搭配使用时，`~`必须在其的后面，并且`~`的数量不能超过点的数量，`~`是用来将变量的值替换到相应位置，比如

```clojure
user> (def a 123)
#'user/a
user> `(def b ~a)
(def user/b 123)
```

可以看到`~a`被替换为a的值123了，而`~@`的作用和`~`类似，不过`~@`不但会替换掉值而且会把括号去掉。

- ~@ (unquote splicing)

```clojure
user> (def c [1 2 3])
#'user/c
user> `(def d [~@c])
(def user/d [1 2 3])
```

```clojure
(defmacro t1 [] (let [a1 (+ 1 1)] `(defn cc [] println ~a1)))

;user> (t1)
;#'user/cc
;user> (cc)
;2
```

传递给宏的代码是不会求值的，这点和函数非常不同，函数传的参数都是先做函数运算，如下例子所示:

```clojure
(defn aa [] (println "aa") 1)
(defn bb [] (println "bb") 2)
(defn cc [c a b] (if c a b))
(defmacro dd [c a b] (if c a b))

;user> (cc true (aa) (bb))
;aa
;bb
;1
;user> (dd true (aa) (bb))
;aa
;1
;⚠️结果的区别，因为行数的参数是先求值的，所以调用cc的时候bb也被运行了，这不是我们希望看到的，我们希望看到的是像dd那样只执行aa函数，这时候我们就需要宏了。
;宏是在编译代码的时候运行的，运行一次之后就会把宏的返回值替换到代码的相应位置，所以宏更像是元编程一类的东西，用代码去生成代码。
```

[Clojure宏](http://www.isnowfy.com/clojure-macro/)
