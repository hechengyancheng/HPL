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

---

## 六、形式化语法

### 6.1 EBNF 定义（核心部分）

```ebnf
(* ============================================
   H-Core 形式化语法定义 v1.0
   ============================================ *)

program         = { definition | statement | event_handler };

(* --------------------------------------------
   核心定义
   -------------------------------------------- *)
definition      = test_def;

test_def        = "test", string, ":", indent, { statement }, { assert_stmt }, dedent;

(* --------------------------------------------
   语句
   -------------------------------------------- *)
statement       = assignment | if_stmt | while_stmt | say_stmt
                 | add_stmt | remove_stmt | move_stmt | endgame_stmt
                 | timer_stmt | stop_timer_stmt | increase_stmt | decrease_stmt
                 | perform_stmt | parallel_stmt;

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
multiplicative  = unary, { ( "*" | "/" | "%" ), unary };

unary           = member_check | primary;
member_check    = identifier, "has", identifier
                 | identifier, "is", "in", expression;

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

### 6.2 运算符优先级表

| 优先级 | 运算符 | 说明 |
|--------|--------|------|
| 1 | `.` | 属性访问 |
| 2 | `not` | 逻辑非 |
| 3 | `*`, `/`, `%` | 乘、除、取模 |
| 4 | `+`, `-` | 加、减 |
| 5 | `is`, `is not`, `is greater than`, `is less than`, `is at least`, `is at most`, `==`, `!=`, `<`, `>`, `<=`, `>=` | 比较运算 |
| 6 | `has`, `is in` | 成员检查 |
| 7 | `and` | 逻辑与 |
| 8 | `or` | 逻辑或 |

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

// 列表操作
if $items contains "banana":
    say "We have bananas!"

// 属性访问示例（假设有对象）
set player.name to "Alice"
set player.level to 1

if player.level is greater than 0:
    say "Welcome, " + player.name
```

---

**文档版本：** v1.0  
**适用范围：** H-Core 语言核心  
**相关文档：** 
- [游戏框架规范](./game-framework-spec.md) - 游戏特定扩展
- [标准库参考](./stdlib-reference.md) - 内置动作和API
