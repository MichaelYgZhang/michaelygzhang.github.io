---
layout: post
title: Java Collections HashMap JDK1.7 源码分析
excerpt: Java Collections HashMap JDK1.7 源码分析
category: Java
---

HashMap 和 HashSet 是 Java Collection Framework 的两个重要成员，其中 HashMap 是 Map 接口的常用实现类， 简单来说就是底层一个数组+Entry链来实现的。 下面通过源码来进行分析。

###### HashMap的存储实现

```java
  HashMap map = new HashMap();
  map.put("first" , "michael");
  map.put("last" , "zhang");
```

当程序执行map.put(key,value);方法时。则执行的代码逻辑是:

```java
    public V put(K key, V value){
        // 如果 key 为 null，调用 putForNullKey 方法进行处理
        if (key == null)
            return putForNullKey(value);
        // 根据 key 的 hashCode 计算 Hash 值
        int hash = hash(key.hashCode());
        // 搜索指定 hash 值在对应 table 中的索引
        int i = indexFor(hash, table.length);
        // 如果 i 索引处的 Entry 不为 null，通过循环不断遍历 e 元素的下一个元素
        for (Entry e = table[i]; e != null; e = e.next)
        {
            Object k;
            // 找到指定 key 与需要放入的 key 相等(hash 值相同通过 equals 比较返回 true)则覆盖oldValue(与HashSet不同,HashSet不会覆盖,
            //HashSet调用的方法set.add(Object e);
            //其实就是public boolean add(E e) {
	          // return map.put(e, PRESENT)==null;//注意e,是key值
            // })
            if (e.hash == hash && ((k = e.key) == key || key.equals(k)))
                {
                    V oldValue = e.value;
                    e.value = value;
                    e.recordAccess(this);
                    return oldValue;
                }
        }
        // 如果 i 索引处的 Entry 为 null，表明此处还没有 Entry, modCount记录HashMap中修改结构的次数
        modCount++;
        // 将 key、value 添加到 i 索引处
        addEntry(hash, key, value, i);
        return null;
    }
```

- 根据上面 put 方法的源代码可以看出，当程序试图将一个 key-value 对放入 HashMap 中时，程序首先根据该 key 的 hashCode() 返回值决定该 Entry 的存储位置：如果两个 Entry 的 key 的 hashCode() 返回值相同， 那它们的存储位置相同。如果这两个 Entry 的 key 通过 equals 比较返回 true，新添加 Entry 的 value 将覆盖集合中原有 Entry 的 value，但 key 不会覆盖。 如果这两个 Entry 的 key 通过 equals 比较返回 false，新添加的 Entry 将与集合中原有 Entry 形成 Entry 链，而且新添加的 Entry 位于 Entry 链的头部——具体说明继续看 addEntry() 方法的说明。 当向 HashMap 中添加 key-value 对，由其 key 的 hashCode() 返回值决定该 key-value 对（就是 Entry 对象）的存储位置。当两个 Entry 对象的 key 的 hashCode() 返回值相同时， 将由 key 通过 eqauls() 比较值决定是采用覆盖行为（返回 true），还是产生 Entry 链（返回 false）。

- 程序中调用 indexFor(int h, int length) 方法来计算该对象应该保存在 table 数组的哪个索引处。indexFor(int h, int length) 方法的代码如下：

```java
  static int indexFor(int h, int length) {
    return h & (length-1);
  }
```

- 注解:该方法总是通过 h &(table.length -1) 来得到该对象的保存位置——而 HashMap 底层数组的长度总是 2 的 n 次方，这一点可参看后面关于 HashMap 构造器的介绍。 当 length 总是 2 的倍数时，h & (length-1)将是一个非常巧妙的设计：假设 h=5,length=16, 那么 h & length - 1 将得到 5； 如果 h=6,length=16, 那么 h & length - 1 将得到 6 ……如果 h=15,length=16, 那么 h & length - 1 将得到 15； 但是当 h=16 时 , length=16 时，那么 h & length - 1 将得到 0 了；当 h=17 时 , length=16 时，那么 h & length - 1 将得到 1 了…… 这样保证计算得到的索引值总是位于 table 数组的索引之内。

- put方法中 addEntry 是 HashMap 提供的一个包访问权限的方法，该方法仅用于添加一个 key-value 对。下面是该方法的代码：

```java
    void addEntry(int hash, K key, V value, int bucketIndex)
    {
        // 获取指定 bucketIndex 索引处的 Entry
        Entry e = table[bucketIndex];
        // 将新创建的 Entry 放入 bucketIndex 索引处，并让新的 Entry 指向原来的 Entry,此时将会形成一个Entry链
        table[bucketIndex] = new Entry(hash, key, value, e);
        // 如果 Map 中的 key-value 对的数量超过了极限
        if (size++ >= threshold)
        // 把 table 对象的长度扩充到 2 倍。
        resize(2 * table.length);
    }
```    

##### 存储示意图

![](https://raw.githubusercontent.com/MichaelYgZhang/home/gh-pages/images/hash.jpg)

##### HashMap的读取实现

```java
    public V get(Object key)
    {
        // 如果 key 是 null，调用 getForNullKey 取出对应的 value
        if (key == null)
            return getForNullKey();
        // 根据该 key 的 hashCode 值计算它的 hash 码
        int hash = hash(key.hashCode());
        // 直接取出 table 数组中指定索引处的值，
        for (Entry e = table[indexFor(hash, table.length)];e != null;
                        // 搜索该 Entry 链的下一个 Entr
                        e = e.next)
        {
            Object k;
            // 如果该 Entry 的 key 与被搜索 key 相同
            if (e.hash == hash && ((k = e.key) == key || key.equals(k)))
                return e.value;
        }
        return null;
    }
```

- 总结:HashMap 在底层将 key-value 当成一个整体进行处理，这个整体就是一个 Entry 对象。HashMap 底层采用一个 Entry[] 数组来保存所有的 key-value 对， 当需要存储一个 Entry 对象时，会根据 Hash 算法来决定其存储位置；当需要取出一个 Entry 时，也会根据 Hash 算法找到其存储位置，直接取出该 Entry。 由此可见：HashMap 之所以能快速存、取它所包含的 Entry， 完全类似于,不同的东西要放在不同的位置，需要时才能快速找到它。


##### HashMap中Hash算法的性能控制

- 首先了解HashMap的构造方法： HashMap()：构建一个初始容量为 16，负载因子为 0.75 的 HashMap。HashMap(int initialCapacity)：构建一个初始容量为 initialCapacity，负载因子为 0.75 的 HashMap。HashMap(int initialCapacity, float loadFactor)：以指定初始容量、指定的负载因子创建一个 HashMap。


```java
    // 以指定初始化容量、负载因子创建 HashMap
   public HashMap(int initialCapacity, float loadFactor)
   {
       // 初始容量不能为负数
       if (initialCapacity < 0)
           throw new IllegalArgumentException(
               "Illegal initial capacity: " +
               initialCapacity);
       // 如果初始容量大于最大容量，让出示容量
       if (initialCapacity > MAXIMUM_CAPACITY)
           initialCapacity = MAXIMUM_CAPACITY;
           // 负载因子必须大于 0 的数值
       if (loadFactor <= 0 || Float.isNaN(loadFactor))
           throw new IllegalArgumentException(loadFactor);
       // 计算出大于 initialCapacity 的最小的 2 的 n 次方值。
       int capacity = 1;
       while (capacity < initialCapacity)
           capacity <<= 1;
       this.loadFactor = loadFactor;
       // 设置容量极限等于容量 * 负载因子
       threshold = (int)(capacity * loadFactor);
       // 初始化 table 数组
       table = new Entry[capacity];
       init();
   }
```

- 注解:table 的实质就是一个数组，一个长度为 capacity 的数组。当系统开始初始化 HashMap 时，系统会创建一个长度为 capacity 的 Entry 数组， 这个数组里可以存储元素的位置被称为“桶（bucket）”，每个 bucket 都有其指定索引，系统可以根据其索引快速访问该 bucket 里存储的元素。 无论何时，HashMap 的每个“桶”只存储一个元素（也就是一个 Entry），由于 Entry 对象可以包含一个引用变量（就是 Entry 构造器的的最后一个参数） 用于指向下一个 Entry，因此可能出现的情况是：HashMap 的 bucket 中只有一个 Entry，但这个 Entry 指向另一个 Entry ——这就形成了一个 Entry 链。
- initialCapacity：HashMap的最大容量，即为底层数组的长度。
- loadFactor：负载因子loadFactor定义为：散列表的实际元素数目(n)/ 散列表的容量(m)。
负载因子衡量的是一个散列表的空间的使用程度，负载因子越大表示散列表的装填程度越高，反之愈小。 对于使用链表法的散列表来说，查找一个元素的平均时间是O(1+a)，因此如果负载因子越大，对空间的利用更充分， 然而后果是查找效率的降低；如果负载因子太小，那么散列表的数据将过于稀疏，对空间造成严重浪费。 HashMap的实现中，通过threshold字段来判断HashMap的最大容量：threshold = (int)(capacity * loadFactor); 结合负载因子的定义公式可知，threshold就是在此loadFactor和capacity对应下允许的最大元素数目，超过这个数目就重新resize， 以降低实际的负载因子。默认的的负载因子0.75是对空间和时间效率的一个平衡选择。 当threshold超出此最大容量时， 修改resize后的HashMap容量是容量的两倍。 其实就是对Table数组的扩容，原数组中的数据必须重新计算其在新数组中的位置，并放进去，这就是resize。


##### Key的hashCode()与equals()方法的重写   

在map.put(key,value);中首先是对key进行hashCode()取值,然后通过hash()取值，得到元素在数组中的位置，之后进行key的equals(); 方法，找到该链表中的所需元素。可以看出hashCode(),equals()在put(),get(),方法中都是关键方法。所以为了保证存取对象时的正确性，要修改其 hashCode()以及equals()方法。

##### Fail-Fast策略（速错）

java.util.HashMap不是线程安全的，因此如果在使用迭代器的过程中有其他线程修改了map，那么将抛出ConcurrentModificationException， 这就是所谓fail-fast策略（速错），这一策略在源码中的实现是通过modCount域，modCount顾名思义就是修改次数， 对HashMap内容的修改都将增加这个值，那么在迭代器初始化过程中会将这个值赋给迭代器的expectedModCount。

```java
    private abstract class HashIterator implements Iterator {
        Entry next;        // next entry to return
        int expectedModCount;   // For fast-fail
        int index;              // current slot
        Entry current;     // current entry

        HashIterator() {//Hash迭代
            expectedModCount = modCount;
            if (size > 0) { // advance to first entry
                Entry[] t = table;
                while (index < t.length && (next = t[index++]) == null)
                ;
            }
        }

        public final boolean hasNext() {
            return next != null;
        }

        final Entry nextEntry() {
            if (modCount != expectedModCount)//如果不相等就表示被其他线程修改过map
                throw new ConcurrentModificationException();
            Entry e = next;
            if (e == null)
                throw new NoSuchElementException();

            if ((next = e.next) == null) {
                Entry[] t = table;
                while (index < t.length && (next = t[index++]) == null)
                ;
            }
            current = e;
            return e;
        }

        public void remove() {
            if (current == null)
                throw new IllegalStateException();
            if (modCount != expectedModCount)
                throw new ConcurrentModificationException();
            Object k = current.key;
                current = null;
            HashMap.this.removeEntryForKey(k);
            expectedModCount = modCount;
        }

    }
```

- 在迭代过程中，判断modCount跟expectedModCount是否相等，如果不相等就表示已经有其他线程修改了map。 注意到modCount声明为volatile，保证线程之间修改的可见性。（volatile之所以线程安全是因为被volatile修饰的变量不保存缓存，直接在内存中修改，因此能够保证线程之间修改的可见性）。    
