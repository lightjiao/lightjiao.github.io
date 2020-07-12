---
title: C++智能指针：shared_ptr
date: 2020-03-31 22:08:41
categories:
 - Cpp
tags:
 - Cpp
---

##  一、`shared_ptr`是什么
`shared_ptr`是模板类。

因此我们创建一个智能指针时，必须提供额外的信息——指针可以指向的类型。
默认初始化的智能指针中保存着一个空指针。



## 二、`shared_ptr`简单用法

```C++
int main()
{
    // 初始化共享指针
    shared_ptr<string> sp1 = make_shared<string>("hello world");
    // 打印共享指针的地址
    cout << "&sp1: " << &sp1 << endl;
    // 打印共享指针所指的地址
    cout << "sp1: " << sp1 << endl;
    // 打印智共享针所指的内容
    cout << "*sp1: " << *sp1 << endl;
    // 共享指针是否唯一
    cout << "unique: " << sp1.unique() << endl;
    // 共享指针引用的数量
    cout << "use count: " << sp1.use_count() << endl;
	
    // 空的共享指针
    shared_ptr<string> sp2;
    cout << "sp2: " << sp2 << endl;
}
```
输出
```bash
&sp1: 0x7fffd19f3120
sp1: 0x2053e80
*sp1: hello world
unique: 1
use count: 1
sp2: 0
```



## 三、`shared_ptr`最安全的初始化方式
使用`make_shared`函数初始化智能指针
```C++
shared_ptr<int> p3 = make_shared<int>(42);
auto p4 = make_shared<vector<string>>();
```



## 四、`shared_ptr`的赋值与拷贝

当进行拷贝或者赋值操作时候，每个`shared_ptr`都会记录有多少个其他`shared_ptr`指向相同的对象  
我们可以认为每个`shared_ptr`都有一个关联的计数器，通常称其为**引用计数器**(reference count)  
无论何时我们拷贝一个`shared_ptr`，计数器都会递增。

计数器递增  ：

 - 用一个`shared_ptr`初始化另一个`shared_ptr`
 - 将它作为参数传递给一个函数
 - 将它作为函数的返回值  

计数器递减：
 - 当我们给`shared_ptr`赋予新值
 - `shared_ptr`被销毁（例如局部的`shared_ptr`离开其作用域时）
```C++
auto r = make_shared<int>(42); // r 指向的int只有一个引用者
r = q; // 给 r 赋值，令它指向另一个新地址
        // 递增 q 指向的对象引用计数器
        // 递减 r 原来指向的对象的引用计数
        // r 原来指向的对象已经没有引用， 会自动释放
```
一旦一个`shared_ptr`的计数器变为0， 它就会自动释放自己锁管理的对象



## 五、`shared_ptr`自动销毁所管理的对象

当指向一个对象的最后一个`shared_ptr`被销毁时，`shared_ptr`类会自动销毁此对象。利用**析构函数**（`destructor`）

`shared_ptr`自身的析构函数会递减它所指向的对象的引用计数。如果引用计数为0， `shared_ptr`的析构函数就会销毁对象，并释放它占用的内存。

> 我的理解：
>
> `shared_ptr`的引用计数应该是一个静态变量，数据结构可能是`static map<ptr, int>`， static保证属性是全局的，map数据结构用于记录不同的内存地址的指针数量，而`shared_ptr`本身是模板类保证了指针的类型，当`map<ptr, int>` 中的某一个`ptr`值为`0`时，则释放该`ptr` 的资源



## 六、`shared_ptr`在无用之后仍然保留的一种可能情况

你将`shared_ptr`存放在一个容器中，随后重排了容器，从而不再需要某些元素。在这种情况下，你应该确保使用`erase`删除哪些不再需要的`shared_ptr`元素

> 什么叫**“重排了容器”**
>
> 《C++ Premier 第五版》第342页有一节叫**`重排容器元素的算法`**，其中把`sort` `unique`等方法称作重排容器的算法。
>
> `unique`方法会将相邻的重复项“消除”，并返回一个指向不重复值范围末尾的迭代器（即`vector<T>::end()`）。调用`unique`后，`vector`将有如下变化
>
> | fox  | jumps | over | quick | red  | <font color=red>red</font> | slow | the  | <font color=red>the</font> | turtle |
> 去除重复项目后，变化为
> | fox  | jumps | over | quick | red  | slow | the  | turtle | ???  | ???  |
> ​                                                                                                      ↑ `vector<T>::end()`
>
> 容器的大小并未改变，它仍有10个元素。`unique`并不真正的删除任何元素，它只是覆盖相邻的重复元素，使得不重复元素出现在序列的开始部分。`unique`返回的迭代器指向最后一个不重复元素之后的位置。此位置之后的元素仍然存在，但我们并不知道它们的值是什么。
>
> 为了真正的删除无用元素，我们必须使用容器操作，比如`erase`
