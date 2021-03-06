一个简单的Python制Scheme实现，施工中
====================================

TODO
------
* 更多的测试代码
* 补完词法
* 实现语句宏
* 代码生成

说明
-----
一个简单的Python制Scheme实现

#### 名称
Casuistry Scheme

#### 用途
娱乐

#### 作者
ee.zsy

#### 特性
坑

Changelog
----------
### 阶段一
实现了主要的功能

* Nov.25  
  第一个版本，可以定义阶乘（递归）函数然后计算，一般的表达式计算也。
  用正则模拟lex，手写的递归下降解析器，read函数，以及基本的eval。
  可define可lambda，可用Python或Scheme来预定义环境。
* Nov.27  
  实现内部宏，方便扩充语法了，跑了一个计算24的代码，很慢很花内存。
  现在的预定义的函数是用到一个就加进去一个，已经工作很良好了。
* Nov.28  
  单独实现了初步支持call/cc的eval版本，之后建立导出的API的时候再来合并代码吧。
  如果call/cc支持多返回值的话，又得重实现一个eval了，虽然代码可照搬。
* Nov.29  
  用Trampoline让eval可以尾递归，函数尾部自己调用自己不再StackOverflow了。
  另外让py可以调用scm里面返回的lambda表达式了，最然暂且只是序列形式的参数。

### 阶段二
对代码进行整理和修补

* Nov.30  
  调整API来独立出测试代码，Repl也以单独的文件提供，顺带合并代码和功能。
  独立当前版本的eval函数及相关代码，移除对先前版本的依赖，引用移到新的实现上。
* Dec.1  
  可通过内部定义的全局Macro来扩展eval的行为，并可用Scm文件提供预定义过程。
  稍稍整理了一下预定义的过程，不过其实这个不是很必要，可以到需要时再定义。
* Dec.2  
  补完了一些词法，不过目前都是些不大要紧调整，

TODO2
------
只做TODO1里面的事情

### 优先级不高的TODO
* 和Py的混合使用
* 定义导出的API
* 词法中的#
* 合并相同功能的不同实现
* 规范一下抛出异常的类型
* 模块化代码
* quote词法以及宏
* pypy
* 持久化和dump
* 让env成为first-class

### 优先级更不高的TOGO
* 性能啊
* 整理代码
* define-syntax词法作用域或者预处理
* 内部marco
* 词法和句法中的'#'
* 代码生成
* 调用PyGame
* 调用HttpServer/Bottle
* 除‘null?’外以'?'结尾的过程

### 不想添加的功能
* 所有'!'结尾的过程
* io相关的过程
* 交互中提供eval过程
* 交互中提供macro相关

代码风格
----------
* 保持简单
* 不必要遵守以下代码风格
* 能暂时不实现的功能就不去实现它，能推迟的改动尽量推迟
* 推迟可能的rename，很麻烦且没必要，重在另一个模块里定义倒是可以的
* 当功能有眼前看得见的好处的时候才去实现它，比如实现另一个功能用到
* 优先考虑实现新的功能，即使重也是整理新版本出来，切勿做出多余的事情来
* 对函数的参数和返回值的类型进行限定，要求特定的类型的子类或者特定的类型的并集
* 写测试分解测试然后实现，特别是实现新功能的时候，测试过只做修补和添加分派
* 有大的改动时，重写新的版本的函数，不改变已写代码的命名和行为习惯
* 不论需求怎么多样化，保持一个最平坦最原始最简陋的core模块
* 不看注释也要很容易看明白代码，通过细分函数的功能约束副作用以及测试代码
* 一个过程限制在最小的功能和行数，额外的扩展可以写一个依赖它的新过程
* 导出的API可以以后修改，旧的实现在有更新时可以重构到新的实现上
* 别用OO堆结构，按照测试实现接口的顺序，实现少量的method并用异常减少条件判断
* 优先考虑写在代码开头的说明文件

链接
-----
* [SICP](http://mitpress.mit.edu/sicp/full-text/book/book.html)
* [IEEE](http://www.ieee.org/index.html)
* [R5RS](http://schemers.org/Documents/Standards/R5RS/)
* [tinyscheme](http://tinyscheme.sourceforge.net/)
* [scm/slb]
* [biwascheme](http://www.biwascheme.org/)
* [pyscheme](https://hkn.eecs.berkeley.edu/~dyoo/python/pyscheme/)
* [psyche]
