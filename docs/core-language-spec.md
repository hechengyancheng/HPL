# H 语言核心规范 v1.0

**H-Core** 是 H 语言的基础核心，提供通用的编程语言构造，独立于任何特定应用领域。

---

## 目录

1. [概述](#一概述)
2. [词法结构](#二词法结构)
3. [数据类型](#三数据类型)
4. [表达式](#四表达式)
5. [语句](#五语句)
6. [形式化语法](#六形式化语法)

---

## 一、概述

H-Core 定义了语言的基石：

- **词法规则**：如何识别代码中的基本单元
- **类型系统**：可用的数据类型及其操作
- **表达式**：如何计算值
- **语句**：如何组织执行流程

> **注意**：本文档仅描述语言核心。特定领域（如游戏开发）的扩展在单独的框架规范中定义。

---

## 二、词法结构

### 2.1 字符集

H 语言使用 **UTF-8** 编码，标识符支持 Unicode 字符。

### 2.2 注释

| 类型 | 语法 | 说明 |
|------|------|------|
| 单行注释 | `// 内容` | 从 `//` 到行尾 |
| 多行注释 | `/* 内容 */` | 可跨越多行，不支持嵌套 |

### 2.3 缩进

缩进具有语法意义，用于表示代码块的层级结构：

- 使用 **4 个空格** 表示一级缩进
- 禁止使用 Tab 字符
- 同一层级的语句必须严格对齐

```h
if health is less than 50:
    say "You are wounded."
    set player.status to "injured"
```

### 2.4 标识符

**命名规则：**
- 以字母或下划线开头
- 可包含字母、数字、下划线
- 区分大小写

**命名约定：**

| 类型 | 约定 | 示例 |
|------|------|------|
| 变量 | 小写开头，驼峰式 | `playerHealth`, `itemCount` |
| 常量 | 全大写，下划线分隔 | `MAX_INVENTORY` |
| 全局变量 | `$` 前缀 | `$score`, `$gameTime` |
| 类型标识符 | 大写开头 | `Room`, `Item`, `Character` |

**核心保留关键字：**

```
and, by, contains, else, end, every, false, for, from, has, if, in
increase, is, not, null, on, or, remove, run, set, start, stop, this
timer, to, true, wait, when, while
```

> 完整关键字列表可能因框架扩展而增加。

---

## 三、数据类型

### 3.1 基本类型

| 类型 | 描述 | 示例 |
|------|------|------|
| `number` | 64位浮点数 | `42`, `3.14`, `-7` |
| `string` | 双引号包裹的文本 | `"hello"`, `"line1\nline2"` |
| `boolean` | 布尔值 | `true`, `false` |
| `list` | 有序集合 | `[item1, item2]` |
| `null` | 空值 | `null` |

### 3.2 字符串

字符串使用双引号 `"` 包裹，支持以下转义序列：

| 序列 | 含义 |
|------|------|
| `\"` | 双引号 |
| `\\` | 反斜杠 |
| `\n` | 换行符 |
| `\t` | 制表符 |

### 3.3 列表

列表使用方括号 `[]` 包裹，元素用逗号分隔：

```h
set inventory to [sword, shield, potion]
set directions to [north, south, east, west]
```

列表支持的操作：
- `contains`：检查包含关系
- `is in`：检查元素是否在列表中

---

## 四、表达式

### 4.1 运算符优先级

从高到低排列：

| 优先级 | 运算符 | 结合性 |
|--------|--------|--------|
| 1 | `.`（属性访问） | 左结合 |
| 2 | `not` | 右结合 |
| 3 | `*`, `/`, `%` | 左结合 |
| 4 | `+`, `-` | 左结合 |
| 5 | `is`, `is not`, `is greater than`, `is less than`, `is at least`, `is at most`, `==`, `!=`, `<`, `>`, `<=`, `>=` | 左结合 |
| 6 | `has`, `is in` | 左结合 |
| 7 | `and` | 左结合 |
| 8 | `or` | 左结合 |

### 4.2 算术运算

```h
set total to price * quantity + tax
set damage to baseDamage * critMultiplier - armor
```

### 4.3 比较运算

支持自然语言风格和符号别名两种形式，完全等价：

| 自然语言 | 符号 | 含义 |
|----------|------|------|
| `is` | `==` | 等于 |
| `is not` | `!=` | 不等于 |
| `is greater than` | `>` | 大于 |
| `is less than` | `<` | 小于 |
| `is at least` | `>=` | 大于等于 |
| `is at most` | `<=` | 小于等于 |

```h
if player.level is greater than 10:
if player.level > 10:
```

### 4.4 逻辑运算

```h
if player.hasKey and door.isLocked:
if not enemy.isAlive or player.isInvisible:
```

### 4.5 成员检查

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `has` | 检查拥有关系 | `player has sword` |
| `is in` | 检查位置关系 | `sword is in player.inventory` |

### 4.6 属性访问

使用 `.` 访问对象属性：

```h
player.health
chest.isLocked
room.exits.north
```

---

## 五、语句

### 5.1 赋值语句

```h
set <变量> to <表达式>
```

变量类型：
- 局部变量：直接命名
- 全局变量：`$` 前缀
- 对象属性：使用 `.` 访问

```h
set health to 100
set $score to 0
set player.health to 100
set chest.items to [gold, gem]
```

### 5.2 条件语句

```h
if <条件>:
    <语句块>
else if <条件>:
    <语句块>
else:
    <语句块>
```

示例：

```h
if player.health is less than 25:
    say "Critical health!"
    set player.status to "critical"
else if player.health is less than 50:
    say "You are wounded."
else:
    say "You are healthy."
```

### 5.3 循环语句

```h
while <条件>:
    <语句块>
```

示例：

```h
while enemy.health is greater than 0:
    perform combat.attack with player, enemy
    say "You attack the enemy!"
```

### 5.4 函数定义

H-Core 支持定义可复用的函数块。

**函数声明：**

```h
function <标识符>([<参数>, ...]):
    <语句块>
    [return <表达式>]
```

**示例：**

```h
function calculateDamage(base, multiplier):
    set result to base * multiplier
    return result

function greet(name):
    say "Hello, " + name

function checkHealth(entity):
    if entity.health is less than 25:
        return "critical"
    else if entity.health is less than 50:
        return "wounded"
    else:
        return "healthy"
```

**函数调用：**

```h
set damage to calculateDamage(10, 2.5)
greet("Alice")
set status to checkHealth(player)
```

**说明：**
- 函数使用 `function` 关键字定义
- 参数列表可选，多个参数用逗号分隔
- 使用 `return` 语句返回值，可选
- 无 `return` 语句时函数返回 `null`
- 函数支持递归调用

### 5.5 输入语句

使用 `ask` 语句获取用户输入。

**语法：**

```h
ask [<提示文本>]
ask [<提示文本>] as <变量>
```

**示例：**

```h
ask "What is your name?"
ask "How many items?" as itemCount
ask "Choose a direction (north/south/east/west):" as direction
```

**说明：**
- 无 `as` 子句时，输入直接返回（需配合赋值使用）
- 有 `as` 子句时，自动将输入值存入指定变量
- 输入值默认为字符串类型，可用类型转换函数转换

---

## 六、内置函数

H-Core 提供以下内置函数：

### 6.1 通用函数

| 函数 | 语法 | 说明 | 示例 |
|------|------|------|------|
| `len` | `len(<集合>)` | 返回列表长度或字符串长度 | `len([1, 2, 3])` → `3` |
| `type` | `type(<值>)` | 返回值的类型名称 | `type(42)` → `"number"` |
| `random` | `random()` | 返回 0-1 之间的随机数 | `random()` → `0.73` |
| `randomInt` | `randomInt(<最小>, <最大>)` | 返回指定范围的随机整数 | `randomInt(1, 6)` → `4` |
| `range` | `range(<开始>, <结束>, [<步长>])` | 生成数字序列 | `range(0, 5)` → `[0, 1, 2, 3, 4]` |

### 6.2 字符串函数

| 函数 | 语法 | 说明 | 示例 |
|------|------|------|------|
| `substring` | `substring(<字符串>, <开始>, [<长度>])` | 提取子字符串 | `substring("hello", 1, 3)` → `"ell"` |
| `split` | `split(<字符串>, <分隔符>)` | 分割字符串为列表 | `split("a,b,c", ",")` → `["a", "b", "c"]` |
| `trim` | `trim(<字符串>)` | 去除首尾空白 | `trim("  hi  ")` → `"hi"` |
| `upper` | `upper(<字符串>)` | 转为大写 | `upper("hello")` → `"HELLO"` |
| `lower` | `lower(<字符串>)` | 转为小写 | `lower("HELLO")` → `"hello"` |
| `contains` | `contains(<字符串>, <子串>)` | 检查包含关系 | `contains("hello", "ell")` → `true` |
| `startsWith` | `startsWith(<字符串>, <前缀>)` | 检查前缀 | `startsWith("hello", "he")` → `true` |
| `endsWith` | `endsWith(<字符串>, <后缀>)` | 检查后缀 | `endsWith("hello", "lo")` → `true` |
| `replace` | `replace(<字符串>, <旧>, <新>)` | 替换子串 | `replace("hello", "l", "x")` → `"hexxo"` |

### 6.3 列表函数

| 函数 | 语法 | 说明 | 示例 |
|------|------|------|------|
| `sort` | `sort(<列表>, [<降序>])` | 排序列表 | `sort([3, 1, 2])` → `[1, 2, 3]` |
| `reverse` | `reverse(<列表>)` | 反转列表 | `reverse([1, 2, 3])` → `[3, 2, 1]` |
| `join` | `join(<列表>, <分隔符>)` | 合并为字符串 | `join(["a", "b"], "-")` → `"a-b"` |
| `indexOf` | `indexOf(<列表>, <元素>)` | 查找元素索引 | `indexOf([a, b, c], b)` → `1` |
| `append` | `append(<列表>, <元素>)` | 添加元素（返回新列表） | `append([1, 2], 3)` → `[1, 2, 3]` |
| `removeAt` | `removeAt(<列表>, <索引>)` | 移除指定索引元素 | `removeAt([1, 2, 3], 1)` → `[1, 3]` |

### 6.4 数学函数

| 函数 | 语法 | 说明 | 示例 |
|------|------|------|------|
| `abs` | `abs(<数值>)` | 绝对值 | `abs(-5)` → `5` |
| `floor` | `floor(<数值>)` | 向下取整 | `floor(3.7)` → `3` |
| `ceil` | `ceil(<数值>)` | 向上取整 | `ceil(3.2)` → `4` |
| `round` | `round(<数值>, [<精度>])` | 四舍五入 | `round(3.14159, 2)` → `3.14` |
| `max` | `max(<值1>, <值2>, ...)` | 最大值 | `max(1, 5, 3)` → `5` |
| `min` | `min(<值1>, <值2>, ...)` | 最小值 | `min(1, 5, 3)` → `1` |
| `sqrt` | `sqrt(<数值>)` | 平方根 | `sqrt(16)` → `4` |
| `pow` | `pow(<底数>, <指数>)` | 幂运算 | `pow(2, 3)` → `8` |

### 6.5 类型转换函数

| 函数 | 语法 | 说明 | 示例 |
|------|------|------|------|
| `toString` | `toString(<值>)` | 转为字符串 | `toString(42)` → `"42"` |
| `toNumber` | `toNumber(<字符串>)` | 转为数字 | `toNumber("3.14")` → `3.14` |
| `toBoolean` | `toBoolean(<值>)` | 转为布尔值 | `toBoolean(1)` → `true` |
| `toList` | `toList(<可迭代>)` | 转为列表 | `toList("abc")` → `["a", "b", "c"]` |

---

## 七、列表索引访问

### 7.1 基本索引

使用方括号 `[]` 访问列表元素：

```h
set items to ["sword", "shield", "potion"]
set first to items[0]      // "sword"
set last to items[2]       // "potion"
```

### 7.2 负索引

支持负索引从末尾访问：

```h
set items to ["a", "b", "c", "d"]
set last to items[-1]      // "d"
set secondLast to items[-2] // "c"
```

### 7.3 索引赋值

可直接通过索引修改元素：

```h
set items[0] to "dagger"
set player.inventory[2] to null
```

### 7.4 多维索引

支持嵌套列表的多维访问：

```h
set matrix to [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
set center to matrix[1][1]  // 5
```

### 7.5 切片（范围访问）

使用 `start:end` 语法获取子列表：

```h
set items to ["a", "b", "c", "d", "e"]
set slice1 to items[1:3]    // ["b", "c"] (索引1到2)
set slice2 to items[:2]      // ["a", "b"] (开始到索引1)
set slice3 to items[2:]      // ["c", "d", "e"] (索引2到末尾)
set slice4 to items[:]       // 完整副本
```

**说明：**
- 切片范围 `[start:end]` 包含 `start`，不包含 `end`
- 省略 `start` 默认为 0
- 省略 `end` 默认为列表长度
- 切片返回新列表，不修改原列表

---

## 八、形式化语法
## 八、形式化语法

### 8.1 EBNF 定义（核心部分）

```ebnf
(* ============================================
   H-Core 形式化语法定义 v1.1
   新增：函数定义、列表索引、内置函数调用
   ============================================ *)

program         = { import_stmt | definition | statement | event_handler };

(* --------------------------------------------
   导入语句
   -------------------------------------------- *)
import_stmt     = "import", identifier, [ "as", identifier ];

(* --------------------------------------------
   核心定义
   -------------------------------------------- *)
definition      = test_def | function_def;

test_def        = "test", string, ":", indent, { statement }, { assert_stmt }, dedent;

function_def    = "function", identifier, "(", [ param_list ], ")", ":", 
                  indent, { statement }, [ return_stmt ], dedent;
param_list      = identifier, { ",", identifier };
return_stmt     = "return", [ expression ];


(* --------------------------------------------
   语句
   -------------------------------------------- *)
statement       = assignment | if_stmt | while_stmt | say_stmt | ask_stmt
                 | add_stmt | remove_stmt | move_stmt | endgame_stmt
                 | timer_stmt | stop_timer_stmt | increase_stmt | decrease_stmt
                 | perform_stmt | parallel_stmt | function_call_stmt;

ask_stmt        = "ask", [ string ], [ "as", identifier ];

function_call_stmt = function_call;


assignment      = "set", lvalue, "to", expression;
lvalue          = identifier | global_var | property_access;
global_var      = "$", identifier;
property_access = identifier, ".", identifier;

if_stmt         = "if", expression, ":", indent, { statement }, [ elif_block ], [ else_block ], dedent;
elif_block      = "else", "if", expression, ":", indent, { statement }, dedent;
else_block      = "else", ":", indent, { statement }, dedent;

while_stmt      = "while", expression, ":", indent, { statement }, dedent;

say_stmt        = "say", string;

add_stmt        = "add", identifier, "to", expression;
remove_stmt     = "remove", identifier, "from", expression;
move_stmt       = "move", "to", identifier;
endgame_stmt    = "end", "game";

increase_stmt   = "increase", lvalue, "by", expression;
decrease_stmt   = "decrease", lvalue, "by", expression;

perform_stmt    = "perform", identifier, [ "with", expression, { ",", expression } ];

timer_stmt      = "start", "timer", identifier, "for", number, time_unit;
time_unit       = "seconds" | "minutes";
stop_timer_stmt = "stop", "timer", identifier;

parallel_stmt   = "run", "in", "parallel", ":", indent, { statement }, dedent;

(* --------------------------------------------
   事件处理（核心语法结构）
   -------------------------------------------- *)
event_handler   = "on", event_type, ":", event_target, ":", indent, { statement }, dedent;
event_type      = "action" | "state" | "timer" | "event" | "game start" | "every turn";
event_target    = player_action | expression | identifier, "expires";

player_action   = "player", identifier, [ "this" ]
                 | "player", identifier, identifier, "on", identifier;

(* --------------------------------------------
   断言
   -------------------------------------------- *)
assert_stmt     = "assert", [ "not" ], assert_expr;
assert_expr     = expression | expression, "is", value | expression, "contains", expression;

(* --------------------------------------------
   表达式
   -------------------------------------------- *)
expression      = or_expr;

or_expr         = and_expr, { "or", and_expr };
and_expr        = not_expr, { "and", not_expr };
not_expr        = [ "not" ], comparison;

comparison      = additive, [ compare_op, additive ];
compare_op      = "is" | "is not" | "is greater than" | "is less than" 
                 | "is at least" | "is at most"
                 | "==" | "!=" | "<" | ">" | "<=" | ">=";

additive        = multiplicative, { ( "+" | "-" ), multiplicative };
multiplicative  = index_access, { ( "*" | "/" | "%" ), index_access };

index_access    = unary, { "[", expression, [ ":", expression ], "]" };

unary           = member_check | function_call | primary;
member_check    = identifier, "has", identifier
                 | identifier, "is", "in", expression;

function_call   = identifier, "(", [ arg_list ], ")";
arg_list        = expression, { ",", expression };

primary         = literal | lvalue | "(", expression, ")";

literal         = number | string | boolean | null | list;

(* --------------------------------------------
   词法单元
   -------------------------------------------- *)
identifier      = letter, { letter | digit | "_" };
string          = "\"", { char | escape }, "\"";
number          = [ "-" ], digit, { digit }, [ ".", digit, { digit } ];
boolean         = "true" | "false";
null            = "null";
list            = "[", [ value, { ",", value } ], "]";
value           = expression;

letter          = "a" .. "z" | "A" .. "Z" | unicode_letter;
digit           = "0" .. "9";
escape          = "\\", ( "\"" | "\\" | "n" | "t" );

indent          = "    ";  (* 4 spaces *)
dedent          = "";      (* 缩进结束，由词法分析器处理 *)

(* --------------------------------------------
   注释
   -------------------------------------------- *)
comment         = line_comment | block_comment;
line_comment    = "//", { any_char }, "\n";
block_comment   = "/*", { any_char | "*" }, "*/";
```

### 8.2 运算符优先级表

| 优先级 | 运算符 | 说明 |
|--------|--------|------|
| 1 | `.` `[]` | 属性访问、列表索引 |
| 2 | `not` | 逻辑非 |
| 3 | `*`, `/`, `%` | 乘、除、取模 |
| 4 | `+`, `-` | 加、减 |
| 5 | `is`, `is not`, `is greater than`, `is less than`, `is at least`, `is at most`, `==`, `!=`, `<`, `>`, `<=`, `>=` | 比较运算 |
| 6 | `has`, `is in` | 成员检查 |
| 7 | `and` | 逻辑与 |
| 8 | `or` | 逻辑或 |
| 9 | `()` | 函数调用 |


---

## 附录：核心语言示例

```h
// 纯核心语言示例 - 不依赖游戏框架

set $counter to 0
set $items to ["apple", "banana", "cherry"]

// 条件判断
if $counter is less than 10:
    say "Counter is low"
else if $counter is less than 100:
    say "Counter is moderate"
else:
    say "Counter is high"

// 循环
while $counter is less than 5:
    increase $counter by 1
    say "Counting..."

// 列表操作与索引访问
if $items contains "banana":
    say "We have bananas!"
    say "First item is: " + $items[0]

// 函数定义与调用
function greet(name):
    say "Hello, " + name

function sum(a, b):
    return a + b

greet("World")
set result to sum(10, 20)

// 内置函数使用
set count to len($items)
set sorted to sort($items)
set reversed to reverse($items)

// 输入处理
ask "What is your name?" as userName
greet(userName)

// 属性访问示例（假设有对象）
set player.name to "Alice"
set player.level to 1

if player.level is greater than 0:
    say "Welcome, " + player.name

// 列表切片示例
set numbers to [1, 2, 3, 4, 5]
set middle to numbers[1:4]  // [2, 3, 4]
set firstTwo to numbers[:2]  // [1, 2]
```


---

**文档版本：** v1.1  
**更新内容：** 新增函数定义、列表索引访问、内置函数、输入语句  
**适用范围：** H-Core 语言核心  
**相关文档：** 
- [游戏框架规范](./game-framework-spec.md) - 游戏特定扩展
- [标准库参考](./stdlib-reference.md) - 内置动作和API
- [语义规范](./semantic-spec.md) - 语义规则与类型系统（待创建）
