---
layout: post
title: Java Collections HashMap JDK1.8 源码分析
excerpt: Java Collections HashMap JDK1.8 源码分析
category: Java
---

JDK1.8的实现上与之前JDK有所不同,它采用了底层数组+数据链(链的node结点小于8)/红黑树(链表数据大于等于8)。 提高查询效率，避免了哈希碰撞后一条链表情况的发生。

```java
  public class HashMap<K,V> extends AbstractMap<K,V> implements Map<K,V>, Cloneable, Serializable {
    static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16  初始化容量大小16,为2的n次方
    static final int MAXIMUM_CAPACITY = 1 << 30;//最大容量
    static final float DEFAULT_LOAD_FACTOR = 0.75f;//负载因子,一个时间-空间的平衡点
   //根据此值判断是否将链表转为树,如果链表数据集合大于等于8则转为红黑树数据结构
    static final int TREEIFY_THRESHOLD = 8;
    /**
     * The bin count threshold for untreeifying a (split) bin during a
     * resize operation. Should be less than TREEIFY_THRESHOLD, and at
     * most 6 to mesh with shrinkage detection under removal.
     * ???
     */
    static final int UNTREEIFY_THRESHOLD = 6;

    /**
     * The smallest table capacity for which bins may be treeified.
     * (Otherwise the table is resized if too many nodes in a bin.)
     * Should be at least 4 * TREEIFY_THRESHOLD to avoid conflicts
     * between resizing and treeification thresholds.
     * ???
     */
    static final int MIN_TREEIFY_CAPACITY = 64;
    /**
     * Basic hash bin node, used for most entries.  (See below for
     * TreeNode subclass, and in LinkedHashMap for its Entry subclass.)
     * 链对象
     */
    static class Node<K,V> implements Map.Entry<K,V> {
        final int hash;
        final K key;
        V value;
        Node<K,V> next;//同下标的下一个元素

        Node(int hash, K key, V value, Node<K,V> next) {
            this.hash = hash;
            this.key = key;
            this.value = value;
            this.next = next;
        }

        public final K getKey()        { return key; }
        public final V getValue()      { return value; }
        public final String toString() { return key + "=" + value; }

        public final int hashCode() {
            return Objects.hashCode(key) ^ Objects.hashCode(value);
        }

        public final V setValue(V newValue) {
            V oldValue = value;
            value = newValue;
            return oldValue;
        }
        //注意:此处的比较方法,要重写对象的equals(),hashcode()
        public final boolean equals(Object o) {
            if (o == this)
                return true;
            if (o instanceof Map.Entry) {
                Map.Entry<?,?> e = (Map.Entry<?,?>)o;
                if (Objects.equals(key, e.getKey()) &&
                    Objects.equals(value, e.getValue()))
                    return true;
            }
            return false;
        }
    }
    /**异化算hashCode值,在put元素时,很可能发生桶内碰撞,为了均匀数据,采用此算法,无符号右移16位,然后异或
      *保证了散列的均匀性。反过来讲，当length为奇数时，length-1最后一位为0，这样与h按位与
      *的最后一位肯定为0，即索引位置肯定是偶数，这样数组的奇数位置全部没有放置元素，浪费了大量空间 .
      */
    static final int hash(Object key) {
        int h;
        //key.hashCode(),默认采用Object的native方法,native方法是调用底层实现为c语言的一种方式
        return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
    }
    /**
     * Returns x's Class if it is of the form "class C implements
     * Comparable<C>", else null.
     */
    static Class<?> comparableClassFor(Object x) {}
    /**
     * Returns a power of two size for the given target capacity.
     *格式化数组容量为2的n次方,为了达到合理的数据分布以及数据碰撞,从而很好解决hash冲突问题,返回值永远为2的n次方
    */
    static final int tableSizeFor(int cap) {
        int n = cap - 1;
        n |= n >>> 1;
        n |= n >>> 2;
        n |= n >>> 4;
        n |= n >>> 8;
        n |= n >>> 16;
        return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1;
    }
    transient Node<K,V>[] table;//其大小总为二的n次方,transient表示,不对此属性进行序列化
    transient Set<Map.Entry<K,V>> entrySet;//Set集合,对Map进行遍历
    /**
     * The number of key-value mappings contained in this map.
     */
    transient int size;//表示存储数据的大小
    /**
      * The number of times this HashMap has been structurally modified
      * Structural modifications are those that change the number of mappings in
      * the HashMap or otherwise modify its internal structure (e.g.,
      * rehash).  This field is used to make iterators on Collection-views of
      * the HashMap fail-fast.  (See ConcurrentModificationException).
      ×修改次数,以及快速失效机制的验证
      */
    transient int modCount;
    int threshold;//阀值 = (capacity * load factor)
    final float loadFactor;//负载因子
    /*
     *HashMap(初始化数组容量大小,负载因子);可以根据自己实际情况做这个的初始化,以提高运算效率。
     *因为如果多次进行数组的扩容,要重新计算hash值,重新对数据进行分布
     */
    public HashMap(int initialCapacity, float loadFactor) {
        if (initialCapacity < 0)
            throw new IllegalArgumentException("Illegal initial capacity: " + initialCapacity);
        if (initialCapacity > MAXIMUM_CAPACITY)
            initialCapacity = MAXIMUM_CAPACITY;
        if (loadFactor <= 0 || Float.isNaN(loadFactor))
            throw new IllegalArgumentException("Illegal load factor: " + loadFactor);
        this.loadFactor = loadFactor;
        this.threshold = tableSizeFor(initialCapacity);//初始化数组大小
    }
    public HashMap(int initialCapacity) {
        this(initialCapacity, DEFAULT_LOAD_FACTOR);//初始化指定容量,默认负载因子0.75
    }
    public HashMap() {//空载构造方法,默认数组大小为16,负载因子0.75
        this.loadFactor = DEFAULT_LOAD_FACTOR; // all other fields defaulted
    }
    /*
     * Constructs a new HashMap  with the same mappings as the
     * specified Map .  The  HashMap  is created with
     * default load factor (0.75) and an initial capacity sufficient to
     * hold the mappings in the specified Map.
     */
    public HashMap(Map<? extends K, ? extends V> m) {
        this.loadFactor = DEFAULT_LOAD_FACTOR;
        putMapEntries(m, false);
    }
    /**
      * Implements Map.putAll and Map constructor
      * @param evict false when initially constructing this map, else true (relayed to method afterNodeInsertion).
      */
    final void putMapEntries(Map<? extends K, ? extends V> m, boolean evict) {
        int s = m.size();
        if (s > 0) {
            if (table == null) { // pre-size
                float ft = ((float)s / loadFactor) + 1.0F;
                int t = ((ft < (float)MAXIMUM_CAPACITY) ? (int)ft : MAXIMUM_CAPACITY);
                if (t > threshold)
                threshold = tableSizeFor(t);
            }
            else if (s > threshold)
                resize();
            for (Map.Entry<? extends K, ? extends V> e : m.entrySet()) {
                K key = e.getKey();
                V value = e.getValue();
                putVal(hash(key), key, value, false, evict);
            }
        }
    }
    public boolean isEmpty() {
        return size == 0;
    }
    public V get(Object key) {
        Node<K,V> e;
        return (e = getNode(hash(key), key)) == null ? null : e.value;
    }
    final Node<K,V> getNode(int hash, Object key) {//hash:key的hash值
        Node<K,V>[] tab; Node<K,V> first, e; int n; K k;
        if ((tab = table) != null && (n = tab.length) > 0 &&
            (first = tab[(n - 1) & hash]) != null) {//？？？？first = tab[(n - 1) & hash]这样就能得到第一个Node??
            if (first.hash == hash && // always check first node
                ((k = first.key) == key || (key != null && key.equals(k))))
            return first;
            if ((e = first.next) != null) {
                if (first instanceof TreeNode)//是否为treeNode,如果是,表面是tree结构,采用getTreeNode(hash,key)方式取得Node
                    return ((TreeNode<K,V>)first).getTreeNode(hash, key);
                do {//采用链表结构获取Node
                    if (e.hash == hash &&
                        ((k = e.key) == key || (key != null && key.equals(k))))
                        return e;
                } while ((e = e.next) != null);
            }
        }
        return null;
    }
    public boolean containsKey(Object key) {
        return getNode(hash(key), key) != null;//采用上面的方法获取Node
    }
    /*
     * Associates the specified value with the specified key in this map.
     * If the map previously contained a mapping for the key, the old value is replaced.
     */
    public V put(K key, V value) {
        return putVal(hash(key), key, value, false, true);
    }
    /**
     * Implements Map.put and related methods
     * @param hash hash for key   key的hash值
     * @param key the key
     * @param value the value to put
     * @param onlyIfAbsent if true, don't change existing value
            true:不覆盖已存在的value,否则覆盖,可以看到put(key,value),默认为false(覆盖已存在的value)
     * @param evict if false, the table is in creation mode.   ????什么作用？？
     * @return previous value, or null if none
     */
    final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
                   boolean evict) {
        Node<K,V>[] tab; Node<K,V> p; int n, i;
        if ((tab = table) == null || (n = tab.length) == 0)
            n = (tab = resize()).length;//扩容
        //(n - 1) & hash 找到table数组下标位置,这个位置为链表/树的第一个元素,如果为null,则直接newNode存值
        if ((p = tab[i = (n - 1) & hash]) == null)
            tab[i] = newNode(hash, key, value, null);
        else {
            Node<K,V> e; K k;
            if (p.hash == hash &&
                ((k = p.key) == key || (key != null && key.equals(k))))//如果hash与key或equals(key)都相同则赋给e,Node变量
                e = p;
            else if (p instanceof TreeNode)//如果第一个Node为TreeNode则添加当前value值到树中,红黑树解决冲突
                e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
            else {
                //链表解决冲突
                for (int binCount = 0; ; ++binCount) {//map每次只能添加一个key,value,此处为何是for循环结构？？？
                    if ((e = p.next) == null) {//第一次指向链头,依次后移
                        p.next = newNode(hash, key, value, null);//添加value值
                        // -1 for 1st/新增节点后如果节点个数到达阈值，则将链表转换为红黑树,注意此处-1,因为binCount从0开始
                        if (binCount >= TREEIFY_THRESHOLD - 1)
                            treeifyBin(tab, hash);
                        break;
                    }
                    if (e.hash == hash &&
                        ((k = e.key) == key || (key != null && key.equals(k))))//map集合中允许一个(null,null)
                        break;
                    p = e;//更新p指向下一个节点
                }
            }
            if (e != null) { // existing mapping for key
                V oldValue = e.value;
                if (!onlyIfAbsent || oldValue == null) //如果onlyIfAbsent为false,并且key的hash值相同,则覆盖
                    e.value = value;
                afterNodeAccess(e);
                return oldValue;
            }
        }
        ++modCount;
        if (++size > threshold)//size+1,若大于当前阀值,则扩容
            resize();
        afterNodeInsertion(evict);
        return null;
    }
  }
```    
