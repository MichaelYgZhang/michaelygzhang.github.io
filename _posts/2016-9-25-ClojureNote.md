---
layout: post
title: Clojure note
excerpt: Clojure note
category: Clojure
---

#### `:or` 与 `or` 的区别

```clojure
(let [{opt1 :opt} {:opt false} opt1 :or {opt1 true}] (println opt1))
;true
;nil
(let [{opt1 :opt :or {opt1 true}} {:opt false}] (println opt1))
;false
;nil
```

> 总结:`:or`区分到底是没有赋值还是赋值为逻辑false(nil或者false)

#### `recur`
```clojure
(defn countdown
  [x]
  (if (zero? x)
    :blastoff!
    (do (println x)
        (recur (dec x)))))

;user> (countdown 3)
;3
;2
;1
;:blastoff!
```

> recur能够在不消耗堆栈空间的情况下把程序执行转到离本地上下文最近的loop头那里去


#### 引用 var  与#'

```clojure
(def x 5)
;#'user/x
;user> x
;5
;user> (var x)
;#'user/x
;user> #'x
;#'user/x
```
