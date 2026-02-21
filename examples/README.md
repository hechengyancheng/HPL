# HPL 核心功能演示

本目录包含示例 HPL（H 编程语言）脚本，用于演示该语言的核心功能。

## 文件

- `core_features_demo.hpl` - 全面演示所有 HPL 核心功能

## 运行演示


```bash
cd h-lang
python run_demo.py
```

或运行特定部分：


```bash
python run_demo.py --section variables
python run_demo.py --section functions
python run_demo.py --section game
```

## 交互模式

```bash
python run_demo.py --interactive
```

## 演示的功能


### 1. 变量与赋值
- 基本变量：`set x to 10`
- 全局变量：`set $globalVar to 100`

### 2. 数据类型
- 数字（整数和浮点数）
- 带转义序列的字符串
- 布尔值（`true`、`false`）
- 空值（`null`）
- 列表：`[1, 2, 3]`

### 3. 算术运算
- 加、减、乘、除、取模
- 取反：`-42`
- 带括号的复杂表达式

### 4. 比较运算
- `is`（等于）
- `is not`（不等于）
- `is greater than` / `>`（大于）
- `is less than` / `<`（小于）
- `is at least` / `>=`（至少/大于等于）
- `is at most` / `<=`（至多/小于等于）

### 5. 逻辑运算
- `and`（逻辑与）
- `or`（逻辑或）
- `not`（逻辑非）

### 6. 控制流
- If/else if/else 语句
- While 循环
- Break/continue 支持

### 7. 函数
- 函数定义：`function name(params):`
- 带参数的函数调用
- Return 语句
- 递归函数

### 8. 列表操作
- 索引访问：`list[0]`、`list[-1]`
- 长度：`len(list)`
- 包含检查：`list contains element`
- 排序：`sort(list)`
- 反转：`reverse(list)`
- 追加：`append(list, element)`
- 查找索引：`indexOf(list, element)`

### 9. 字符串操作
- 长度：`len(string)`
- 大小写转换：`upper(string)`、`lower(string)`
- 包含检查：`contains(string, substring)`
- 开头/结尾检查：`startsWith(string, prefix)`、`endsWith(string, suffix)`
- 子字符串：`substring(string, start, length)`
- 分割：`split(string, separator)`
- 替换：`replace(string, old, new)`
- 去空格：`trim(string)`

### 10. 数学函数
- `floor(number)`（向下取整）
- `ceil(number)`（向上取整）
- `round(number, precision)`（四舍五入）
- `abs(number)`（绝对值）
- `max(a, b, c...)`（最大值）
- `min(a, b, c...)`（最小值）
- `sqrt(number)`（平方根）
- `pow(base, exponent)`（幂运算）
- `random()`、`randomInt(min, max)`（随机数）

### 11. 类型转换
- `toString(value)`（转字符串）
- `toNumber(value)`（转数字）
- `toBoolean(value)`（转布尔值）
- `toList(value)`（转列表）

### 12. 特殊语句
- `increase variable by amount`（增加变量值）
- `decrease variable by amount`（减少变量值）
- `ask "prompt" as variable`（询问输入）
- `echo expression`（输出表达式）


## 代码示例片段

### Hello World

```hpl
echo "Hello, World!"
```

### 变量与数学运算

```hpl
set x to 10
set y to 20
set sum to x + y
echo "Sum: " + sum
```

### 条件语句

```hpl
set temperature to 25
if temperature is greater than 30:
    echo "It's hot!"
else:
    echo "It's not too hot"
```

### 循环

```hpl
set counter to 0
while counter is less than 5:
    echo "Count: " + counter
    increase counter by 1
```

### 函数

```hpl
function greet(name):
    echo "Hello, " + name

greet("World")
```

### 列表

```hpl
set items to ["apple", "banana", "cherry"]
echo items[0]
echo "Length: " + len(items)
```

### 游戏逻辑示例

```hpl
set $playerHealth to 100

function takeDamage(damage):
    decrease $playerHealth by damage
    echo "Health: " + $playerHealth

takeDamage(20)
