# H 标准库参考 v1.0

**H-Stdlib** 提供 H 语言的内置动作指令、计时器、测试框架等标准功能。这些功能由运行时环境提供，可通过标准语句调用。

---

## 目录

1. [概述](#一概述)
2. [动作指令](#二动作指令)
3. [计时器](#三计时器)
4. [并行执行](#四并行执行)
5. [测试框架](#五测试框架)
6. [按类别索引](#六按类别索引)

---

## 一、概述

标准库提供以下功能类别：

| 类别 | 功能 | 适用场景 |
|------|------|----------|
| 输出 | `echo` | 向用户显示信息 |
| 库存管理 | `add`, `remove` | 管理物品集合 |
| 移动 | `move to` | 改变位置 |
| 数值操作 | `increase`, `decrease` | 修改变量值 |
| 流程控制 | `wait`, `end game` | 控制执行流程 |
| 动作执行 | `perform` | 调用复杂动作 |
| 计时器 | `start timer`, `stop timer` | 时间管理 |
| 并发 | `run in parallel` | 并行执行 |
| 测试 | `test`, `assert` | 单元测试 |

> **注意**：标准库函数的具体行为可能依赖于所使用的框架（如 H-Game）。

---

## 二、动作指令

### 2.1 输出指令

#### `echo <字符串>`

向玩家或用户显示文本信息。

**语法：**
```h
echo <字符串表达式>
```

**示例：**
```h
echo "Welcome to the adventure!"
echo "Your score is: " + $score
```

**说明：**
- 支持字符串拼接
- 在 H-Game 框架中，这是主要的叙事输出方式

---

### 2.2 库存管理

#### `add <物品> to <目标>`

将物品添加到目标集合中。

**语法：**
```h
add <标识符> to <表达式>
```

**示例：**
```h
add sword to player.inventory
add gold to chest.contents
```

**说明：**
- 目标通常是列表类型
- 如果目标不是列表，行为由具体实现定义

---

#### `remove <物品> from <来源>`

从来源集合中移除物品。

**语法：**
```h
remove <标识符> from <表达式>
```

**示例：**
```h
remove rusty_key from player.inventory
remove curse from player.status_effects
```

**说明：**
- 如果物品不存在于来源中，通常不产生错误
- 具体行为由实现定义

---

### 2.3 移动

#### `move to <房间/位置>`

将玩家移动到指定位置。

**语法：**
```h
move to <标识符>
```

**示例：**
```h
move to Kitchen
move to $destination
```

**说明：**
- 在 H-Game 框架中，这会更新 `player.location`
- 可以配合条件实现有条件的移动

---

### 2.4 数值操作

#### `increase <变量> by <数值>`

增加变量的值。

**语法：**
```h
increase <lvalue> by <表达式>
```

**示例：**
```h
increase player.health by 10
increase $score by bonus_points
```

**说明：**
- 变量必须是数值类型或可转换为数值
- 等效于 `set x to x + y`，但更简洁

---

#### `decrease <变量> by <数值>`

减少变量的值。

**语法：**
```h
decrease <lvalue> by <表达式>
```

**示例：**
```h
decrease enemy.health by damage
decrease player.gold by item_price
```

**说明：**
- 变量值不会自动下限为 0，除非有额外逻辑

---

### 2.5 流程控制

#### `wait for <时间>`

暂停执行指定时间。

**语法：**
```h
wait for <数值> <时间单位>
```

**时间单位：** `seconds`, `minutes`

**示例：**
```h
wait for 3 seconds
wait for 1 minutes
```

**说明：**
- 在实时游戏中用于创建延迟效果
- 在纯文本环境中可能只是模拟等待

---

#### `end game`

结束游戏。

**语法：**
```h
end game
```

**示例：**
```h
if player.health is less than 1:
    echo "You have fallen..."
    end game
```

**说明：**
- 立即终止游戏执行
- 可以配合条件实现游戏结束判定

---

### 2.6 动作执行

#### `perform <动作> with <参数>, ...`

执行预定义的复杂动作。

**语法：**
```h
perform <标识符> [with <表达式>, ...]
```

**示例：**
```h
perform combat.attack with player, enemy
perform trade.buy with merchant, sword, 50
perform magic.cast with player, "fireball", target
```

**说明：**
- 动作名称使用点号表示命名空间
- 参数数量和类型由具体动作定义
- 常用于封装复杂逻辑

---

## 三、计时器

### 3.1 启动计时器

#### `start timer <标识符> for <数值> <单位>`

创建并启动一个命名计时器。

**语法：**
```h
start timer <标识符> for <数值> <时间单位>
```

**时间单位：** `seconds`, `minutes`

**示例：**
```h
start timer bomb for 30 seconds
start timer regeneration for 5 minutes
```

**说明：**
- 计时器到期时会触发 `on timer: <标识符> expires` 事件
- 计时器名称在作用域内唯一

---

### 3.2 停止计时器

#### `stop timer <标识符>`

停止并移除指定计时器。

**语法：**
```h
stop timer <标识符>
```

**示例：**
```h
if bomb.defused:
    stop timer bomb
    echo "Bomb defused safely!"
```

**说明：**
- 停止不会触发计时器到期事件
- 对不存在的计时器执行停止通常是安全的

---

### 3.3 计时器使用示例

```h
// 设置定时炸弹
on action: player activates bomb:
    echo "The timer starts ticking!"
    start timer explosion for 10 seconds

// 计时器到期处理
on timer: explosion expires:
    echo "BOOM! The explosion rocks the room."
    decrease player.health by 50
    set room.hasExploded to true

// 解除炸弹
on action: player uses wire_cutters on bomb:
    if player.has wire_cutters:
        stop timer explosion
        echo "You carefully cut the right wire. The bomb is defused!"
    else:
        echo "You need wire cutters to defuse this."
```

---

## 四、并行执行

### 4.1 `run in parallel`

并行执行代码块。

**语法：**
```h
run in parallel:
    <语句块>
```

**示例：**
```h
run in parallel:
    echo "The fire spreads..."
    increase fire.intensity by 1
    wait for 2 seconds

run in parallel:
    echo "Water drips from the ceiling..."
    wait for 3 seconds
```

**说明：**
- 具体并行语义由运行时实现定义
- 可能用于：
  - 同时显示多个动画/效果
  - 后台处理（如自动保存）
  - 多线程场景模拟

---

## 五、测试框架

### 5.1 测试定义

#### `test <名称>`

定义一个测试用例。

**语法：**
```h
test <字符串>:
    <设置语句>
    <执行语句>
    <断言语句>
```

**示例：**
```h
test "chest unlocking":
    // Setup
    set player.inventory to [rusty_key]
    set chest.isLocked to true
    
    // Action
    perform player.uses with rusty_key, chest
    
    // Assertions
    assert chest.isLocked is false
    assert rusty_key.isBroken is true
    assert player.inventory contains rusty_key
```

---

### 5.2 断言

#### `assert <条件>`

验证条件为真。

**语法：**
```h
assert <表达式>
assert not <表达式>
```

**示例：**
```h
assert player.health is greater than 0
assert not enemy.isAlive
```

---

#### `assert <表达式> is <值>`

验证表达式等于指定值。

**语法：**
```h
assert <表达式> is <值>
```

**示例：**
```h
assert player.location is "Kitchen"
assert $score is 100
```

---

#### `assert <列表> contains <元素>`

验证列表包含指定元素。

**语法：**
```h
assert <表达式> contains <表达式>
```

**示例：**
```h
assert player.inventory contains sword
assert room.characters contains guard
```

---

### 5.3 完整测试示例

```h
test "combat system":
    // Setup combat scenario
    set player.health to 100
    set player.attack to 15
    set goblin.health to 30
    set goblin.defense to 5
    
    // Execute attack
    perform combat.attack with player, goblin
    
    // Verify results
    assert goblin.health is 20  // 30 - (15 - 5) = 20
    assert player.health is 100  // Player took no damage

test "inventory management":
    set player.inventory to []
    
    add sword to player.inventory
    assert player.inventory contains sword
    
    remove sword from player.inventory
    assert not player.inventory contains sword
```

---

## 六、按类别索引

### 快速参考表

| 功能 | 语法 | 所在章节 |
|------|------|----------|
| 输出文本 | `echo <string>` | 2.1 |
| 添加物品 | `add <item> to <target>` | 2.2 |
| 移除物品 | `remove <item> from <source>` | 2.2 |
| 移动位置 | `move to <location>` | 2.3 |
| 增加数值 | `increase <var> by <amount>` | 2.4 |
| 减少数值 | `decrease <var> by <amount>` | 2.4 |
| 等待 | `wait for <n> <unit>` | 2.5 |
| 结束游戏 | `end game` | 2.5 |
| 执行动作 | `perform <action> [with <args>]` | 2.6 |
| 启动计时器 | `start timer <id> for <n> <unit>` | 3.1 |
| 停止计时器 | `stop timer <id>` | 3.2 |
| 并行执行 | `run in parallel:` | 4.1 |
| 定义测试 | `test <name>:` | 5.1 |
| 断言条件 | `assert <condition>` | 5.2 |
| 断言相等 | `assert <expr> is <value>` | 5.2 |
| 断言包含 | `assert <list> contains <item>` | 5.2 |

---

## 附录：实现说明

标准库的实现可能因平台而异：

- **H-Game 运行时**：提供完整的游戏相关功能
- **H-Core 独立运行时**：可能只提供基础功能（echo, wait, test等）
- **Web 平台**：可能将 `echo` 映射为 DOM 操作
- **命令行**：可能将 `echo` 映射为控制台输出

---

**文档版本：** v1.0  
**依赖：** [H-Core 语言规范](./core-language-spec.md)  
**相关文档：** 
- [游戏框架规范](./game-framework-spec.md) - 游戏特定功能
