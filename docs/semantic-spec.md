# H 语言语义规范 v1.0

**本文档定义 H 语言的语义规则，包括作用域、类型系统、求值策略等运行时行为。**

---

## 目录

1. [概述](#一概述)
2. [作用域规则](#二作用域规则)
3. [变量生命周期](#三变量生命周期)
4. [类型系统](#四类型系统)
5. [求值策略](#五求值策略)
6. [类型转换规则](#六类型转换规则)
7. [闭包与词法环境](#七闭包与词法环境)
8. [错误处理语义](#八错误处理语义)

---

## 一、概述

H 语言采用**动态类型**和**词法作用域**的语义模型：

- **动态类型**：变量类型在运行时确定，可随时改变
- **词法作用域**：作用域由代码结构静态决定
- **传值调用**：函数参数默认按值传递
- **自动内存管理**：使用引用计数或垃圾回收

---

## 二、作用域规则

### 2.1 作用域类型

H 语言有四种作用域层级：

| 作用域 | 范围 | 声明方式 |
|--------|------|----------|
| 全局作用域 | 整个程序 | 全局变量 `$name` |
| 模块作用域 | 单个文件/模块 | 顶层定义的函数、类型 |
| 函数作用域 | 函数体内 | 函数参数、局部变量 |
| 块级作用域 | 代码块内 | `if`、`while` 等语句块 |

### 2.2 变量查找规则

**LGN 规则（Local → Global → Native）**：

1. **局部作用域**：首先查找当前块级/函数作用域
2. **全局作用域**：查找全局变量（`$` 前缀）
3. **内置作用域**：查找内置函数和常量

```h
set $global to "global value"

function example():
    set local to "local value"
    say local      // 查找局部作用域 → "local value"
    say $global    // 查找全局作用域 → "global value"
    say len([1,2]) // 查找内置作用域 → 3
```

### 2.3 变量遮蔽（Shadowing）

内层作用域可以遮蔽外层同名变量：

```h
set x to "outer"

function test():
    set x to "inner"  // 遮蔽外层的 x
    say x             // "inner"

test()
say x                 // "outer"（外层 x 不变）
```

### 2.4 全局变量声明

全局变量必须使用 `$` 前缀：

```h
set $score to 0      // 正确：全局变量
set score to 0       // 错误：顶层代码中这是局部变量
```

**注意**：函数内部可以读取全局变量，但修改需要显式 `$` 前缀：

```h
set $counter to 0

function increment():
    increase $counter by 1  // 必须加 $ 前缀
```

---

## 三、变量生命周期

### 3.1 生命周期阶段

| 阶段 | 说明 |
|------|------|
| 声明（Declaration） | 变量名被注册到作用域 |
| 初始化（Initialization） | 变量被赋予初始值 |
| 使用（Usage） | 变量被读取或修改 |
| 销毁（Destruction） | 变量超出作用域，内存释放 |

### 3.2 不同作用域的生命周期

```h
// 全局变量：程序启动时创建，程序结束时销毁
set $global to "I live long"

function example():
    // 局部变量：函数调用时创建，函数返回时销毁
    set local to "I live short"
    
    if true:
        // 块级变量：进入块时创建，离开块时销毁
        set blockVar to "I live shortest"
        say blockVar
    
    // blockVar 已销毁，不可访问
    // local 仍然有效
```

### 3.3 循环中的变量

`while` 循环中声明的变量在每次迭代中保持：

```h
set sum to 0
set i to 0

while i is less than 5:
    set sum to sum + i    // sum 保持状态
    increase i by 1

say sum  // 10
```

---

## 四、类型系统

### 4.1 类型层次结构

```
any
├── primitive
│   ├── number
│   ├── string
│   ├── boolean
│   └── null
└── collection
    ├── list
    └── object
        ├── Room
        ├── Item
        ├── Character
        └── ...
```

### 4.2 类型检查

H 语言是**动态类型**，运行时进行类型检查：

```h
set x to 42        // x 的类型为 number
set x to "hello"   // x 的类型变为 string（合法）

// 运行时类型检查
if type(x) is "string":
    say "x is a string"
```

### 4.3 类型标识

| 值 | type() 返回值 |
|----|---------------|
| `42`, `3.14` | `"number"` |
| `"hello"` | `"string"` |
| `true`, `false` | `"boolean"` |
| `null` | `"null"` |
| `[1, 2, 3]` | `"list"` |
| `Room` 实例 | `"Room"`（类型名称） |

---

## 五、求值策略

### 5.1 传值调用（Call by Value）

函数参数按**值传递**：

```h
function modify(x):
    set x to 100    // 只修改局部副本
    say x           // 100

set a to 1
modify(a)
say a               // 1（原值不变）
```

### 5.2 对象引用的值传递

对象（如列表、Room）按**引用值**传递：

```h
function addItem(inventory, item):
    add item to inventory    // 修改原对象

set inv to ["sword"]
addItem(inv, "shield")
say inv                      // ["sword", "shield"]
```

### 5.3 表达式求值顺序

**从左到右**求值：

```h
set result to foo() + bar()  // 先求值 foo()，再 bar()
```

### 5.4 短路求值

逻辑运算符支持短路：

```h
// and：左操作数为 false 时，不计算右操作数
if isValid() and expensiveCheck():
    // expensiveCheck() 仅在 isValid() 为 true 时执行

// or：左操作数为 true 时，不计算右操作数
if hasPermission() or isAdmin():
    // isAdmin() 仅在 hasPermission() 为 false 时执行
```

---

## 六、类型转换规则

### 6.1 隐式转换（自动）

| 场景 | 转换规则 | 示例 |
|------|----------|------|
| 字符串拼接 | 非字符串转为字符串 | `"Count: " + 5` → `"Count: 5"` |
| 数值运算 | 字符串尝试转为数字 | `"5" + 3` → `8`（若转换失败则报错） |
| 布尔上下文 | 真值判断 | `if 0:` 为 false，`if "":` 为 false |

### 6.2 真值判断（Truthy/Falsy）

**Falsy 值**（视为 false）：
- `false`
- `null`
- `0`
- `""`（空字符串）
- `[]`（空列表）

**Truthy 值**（其他所有值）：
- `true`
- 非零数字
- 非空字符串
- 非空列表

```h
if 0:
    say "不会执行"

if "hello":
    say "会执行"

if []:
    say "不会执行"
```

### 6.3 显式转换

使用类型转换函数：

```h
set num to toNumber("42")      // 42
set str to toString(42)        // "42"
set bool to toBoolean(1)       // true
set list to toList("abc")      // ["a", "b", "c"]
```

### 6.4 转换失败行为

| 转换 | 无效输入 | 结果 |
|------|----------|------|
| `toNumber("abc")` | 非数字字符串 | `null` |
| `toNumber("")` | 空字符串 | `0` |
| `toBoolean(null)` | null | `false` |
| `toList(42)` | 非可迭代值 | `null` |

---

## 七、闭包与词法环境

### 7.1 闭包定义

函数可以捕获其定义时的词法环境：

```h
function makeCounter():
    set count to 0
    
    function increment():
        increase count by 1    // 捕获外部变量
        return count
    
    return increment

set counter to makeCounter()
say counter()  // 1
say counter()  // 2
say counter()  // 3
```

### 7.2 词法环境结构

每个函数执行时创建**环境记录**：

```
环境记录 {
    局部变量: {...},
    参数: {...},
    上层环境指针: → 父级环境
}
```

### 7.3 闭包变量生命周期

被闭包捕获的变量生命周期延长：

```h
function createGreeting(name):
    // greeting 函数捕获 name
    function greeting():
        say "Hello, " + name
    
    return greeting

set greetAlice to createGreeting("Alice")
// createGreeting 已返回，但 name 仍被 greetAlice 引用

greetAlice()  // "Hello, Alice"
```

### 7.4 循环中的闭包陷阱

```h
set functions to []

set i to 0
while i is less than 3:
    function makeFunc():
        return i    // 捕获的是变量 i，不是值
    
    add makeFunc to functions
    increase i by 1

// 所有函数都返回 3（i 的最终值）
say functions[0]()  // 3
say functions[1]()  // 3
say functions[2]()  // 3
```

**解决方案**：使用立即执行函数或 let 绑定（如果支持）

---

## 八、错误处理语义

### 8.1 运行时错误类型

| 错误类型 | 触发场景 | 行为 |
|----------|----------|------|
| TypeError | 类型不匹配的操作 | 终止当前操作，返回 null |
| ReferenceError | 访问未定义变量 | 返回 null，记录警告 |
| RangeError | 索引越界 | 返回 null |
| DivisionError | 除以零 | 返回 Infinity 或 null |

### 8.2 错误传播

错误默认向上传播直到被处理或到达顶层：

```h
function risky():
    set x to 1 / 0    // DivisionError
    say "不会执行"     // 这行不会执行

function caller():
    risky()           // 错误传播到这里
    say "不会执行"

caller()              // 错误到达顶层，程序继续运行（容错模式）
```

### 8.3 防御式编程建议

```h
function safeDivide(a, b):
    if b is 0:
        say "Warning: Division by zero"
        return null
    return a / b

function safeAccess(list, index):
    if index is less than 0 or index is greater than or equal to len(list):
        say "Warning: Index out of bounds"
        return null
    return list[index]
```

---

## 附录：语义示例

### 示例 1：作用域链

```h
set $global to "G"

function outer():
    set outerVar to "O"
    
    function inner():
        set innerVar to "I"
        say innerVar    // I（局部）
        say outerVar    // O（外层）
        say $global     // G（全局）
    
    inner()

outer()
```

### 示例 2：引用与复制

```h
// 原始类型：按值复制
set a to 5
set b to a
set b to 10
say a  // 5（不变）

// 集合类型：引用共享
set list1 to [1, 2, 3]
set list2 to list1
add 4 to list2
say list1  // [1, 2, 3, 4]（被修改）

// 显式复制
function copyList(original):
    set copy to []
    for each item in original:
        add item to copy
    return copy
```

### 示例 3：延迟求值与立即求值

```h
// 立即求值：参数先计算
function eager(a, b):
    say "a = " + a
    say "b = " + b

eager(expensive1(), expensive2())  // 两个都立即计算

// 模拟延迟求值：使用函数包装
function lazy(getA, getB):
    if condition:
        say getA()  // 只在需要时调用
    else:
        say getB()
```

---

**文档版本：** v1.0  
**适用范围：** H-Core 语义规则  
**相关文档：** 
- [核心语言规范](./core-language-spec.md) - 语法定义
- [游戏框架规范](./game-framework-spec.md) - 游戏特定语义
