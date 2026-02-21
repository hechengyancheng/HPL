# H-Core 语言解释器

H-Core 是 H 语言的基础核心实现，提供通用的编程语言构造。

## 项目结构

```
h-lang/
├── core/                       # 核心模块
│   ├── lexer.py               # 词法分析器
│   ├── parser.py              # 语法分析器
│   ├── interpreter.py         # 主解释器入口
│   ├── ast/                   # AST节点定义
│   │   ├── expressions.py     # 表达式节点
│   │   └── statements.py      # 语句节点
│   ├── types/                 # 类型系统
│   │   ├── primitive.py       # 原始类型
│   │   └── operations.py      # 运算操作
│   ├── interpreter/           # 解释器实现
│   │   ├── environment.py     # 环境/作用域
│   │   ├── evaluator.py       # 求值器
│   │   └── control-flow.py    # 控制流
│   └── stdlib/                # 标准库
│       └── builtins.py        # 内置函数
├── tests/                     # 测试
│   └── test_core.py          # 核心测试
└── README.md                  # 本文件
```

## 功能特性

### 1. 词法分析 (lexer.py)
- UTF-8编码支持
- 4空格缩进识别（INDENT/DEDENT）
- 单行//和多行/* */注释
- 字符串转义序列（\", \\, \n, \t）
- 多词运算符识别（is greater than, is less than等）
- 全局变量标识（$xxx）

### 2. 语法分析 (parser.py)
- 递归下降解析器
- 9级运算符优先级
- 完整的表达式解析
- 语句块缩进处理
- 函数定义解析

### 3. 类型系统 (types/)
- **HNumber**: 64位浮点数
- **HString**: 字符串（支持转义）
- **HBoolean**: 布尔值
- **HList**: 列表（支持负索引、切片）
- **HNull**: 空值

### 4. 表达式支持 (ast/expressions.py)
- 字面量、标识符、全局变量
- 属性访问（obj.property）
- 算术运算（+, -, *, /, %）
- 比较运算（is, is not, is greater than, <, >等）
- 逻辑运算（and, or, not）
- 成员检查（has, is in）
- 列表索引和切片（items[0], items[1:3]）
- 函数调用

### 5. 语句支持 (ast/statements.py)
- 赋值（set x to y）
- 条件语句（if/else if/else）
- 循环（while）
- 函数定义（function name():）
- 返回（return）
- 输入（ask "prompt" as var）
- 输出（echo）
- 增减（increase/decrease by）

### 6. 内置函数 (stdlib/builtins.py)

**通用函数**: len, type, random, randomInt, range

**字符串函数**: substring, split, trim, upper, lower, contains, startsWith, endsWith, replace

**列表函数**: sort, reverse, join, indexOf, append, removeAt

**数学函数**: abs, floor, ceil, round, max, min, sqrt, pow

**类型转换**: toString, toNumber, toBoolean, toList

## 使用方法

### 基本使用

```python
from h_lang.core.interpreter import HLangInterpreter, run

# 执行代码
output = run('''
set x to 10
set y to 20
echo x + y
''')

# 使用解释器实例
interpreter = HLangInterpreter()
interpreter.execute('''
function greet(name):
    echo "Hello, " + name

greet("World")
''')
print(interpreter.get_output())
```

### 执行文件

```python
from h_lang.core.interpreter import run_file

output = run_file("example.hpl")

```

## 示例代码

```hpl
// 变量和运算

set $counter to 0
set $items to ["apple", "banana", "cherry"]

// 条件判断
if $counter is less than 10:
    echo "Counter is low"
else if $counter is less than 100:
    echo "Counter is moderate"
else:
    echo "Counter is high"

// 循环
while $counter is less than 5:
    increase $counter by 1
    echo "Counting..."

// 列表操作
if $items contains "banana":
    echo "We have bananas!"
    echo "First item is: " + $items[0]

// 函数定义
function greet(name):
    echo "Hello, " + name

function sum(a, b):
    return a + b

greet("World")
set result to sum(10, 20)

// 内置函数
set count to len($items)
set sorted to sort($items)
set upper_msg to upper("hello")
```

## 测试

运行测试：

```bash
cd h-lang
python -m tests.test_core
```

## 规范遵循

本实现遵循 `docs/core-language-spec.md` 中定义的 H-Core 语言规范 v1.0。

## 许可证

MIT License
