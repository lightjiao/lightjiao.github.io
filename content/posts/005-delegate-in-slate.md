---
title: Slate 中的委托
date: 2020-04-18 14:04:31
categories: 
 - UE4
tags: 
 - UE4
isCJKLanguage: true
---

以class 名为 `TestWidget` 为例

#### 1、声明委托名与委托参数 
定义一个委托（委托名可以认为是新的类型）

`DECLARE_DELEGATE_OneParam(TestDelegate, const string)`

####  2、Slate 框架宏定义支持一种声明`我的一个变量是一个委托`

```C++
// 在 .h 文件中可以这样写
SLATE_BEGIN_ARGS(TestWidget){}     

// 凭空的绑定一个变量叫 PrintString ，它是一个委托，委托名叫 TestDelegate，也可以认为它的委托类型是 TestDelegate
SLATE_EVENT(TestDelegate, PrintString) 

SLATE_END_ARGS()
```

#### 3、这样声明之后有两个作用：  
- 1、这个Slate类在实例化后可以将凭空声明的 `PrintString` 变量绑定到函数指针，函数指针的入参类型必须要与`Delegat` 声明的一样：
```SNew(TestWidget).PrintString(this, &FunctionPrintString)  ```

- 2、在 TestWidget 类自动生成的函数 `void TestWidget ::Construct(const FArguments& InArgs)` 中可以获取到上面绑定到的变量
```
void TestWidget ::Construct(const FArguments& InArgs)
{  
	TestDelegate m_PrintString = InArgs._PrintString; // 委托的变量都以下划线开头传递进这个函数
	
	// 执行绑定的委托函数  
	m_PrintString.Execute("Hello world");
}
```

#### 4、那么这种委托有什么应用呢？
 - 1、降低代码之间的耦合（高内聚、低耦合）
 - 2、可以动态的指定一个Widget的行为，这里距离的是绑定的函数，也可以用`SLATE_ATTRIBUTE(Type, Param)` 绑定属性   比如自定义点击Button后执行的函数
 - 3、一般的实践，会在 construct 函数中传递进来的函数指针最终绑定到类的属性，这样可以做比较灵活的调用
