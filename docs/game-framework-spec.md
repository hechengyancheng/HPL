# H 游戏框架规范 v1.0

**H-Game** 是构建在 H-Core 之上的游戏开发框架，专为文字冒险游戏设计，提供世界建模、事件处理、对话系统等游戏特定功能。

---

## 目录

1. [概述](#一概述)
2. [世界定义](#二世界定义)
3. [事件系统](#三事件系统)
4. [对话系统](#四对话系统)
5. [游戏生命周期](#五游戏生命周期)
6. [形式化语法扩展](#六形式化语法扩展)

---

## 一、概述

H-Game 框架扩展了 H-Core，添加了以下游戏特定概念：

- **世界模型**：房间、物品、角色及其关系
- **事件驱动**：响应玩家动作、状态变化、计时器等
- **对话树**：分支对话系统，支持条件选项
- **游戏循环**：启动、回合更新、结束管理

> **依赖关系**：本文档描述的所有功能都建立在 [H-Core 语言规范](./core-language-spec.md) 之上。

---

## 二、世界定义

### 2.1 房间（Room）

房间是游戏世界的基本空间单元。

```h
Room <标识符>:
    description is <字符串>
    items is [<物品列表>]
    characters is [<角色列表>]
    exits is [<出口列表>]
```

**出口定义：**

```h
<方向> to <目标房间>
<方向> to <目标房间> if <条件>
```

**完整示例：**

```h
Room Kitchen:
    description is "A cozy kitchen with a fireplace."
    items is [knife, apple, pot]
    characters is [cook]
    exits is [
        north to Garden,
        down to Cellar if trapdoor.isOpen,
        east to DiningRoom
    ]
```

### 2.2 物品（Item）

物品是可以被玩家交互的游戏对象。

```h
Item <标识符>:
    description is <字符串>
    tags is [<标签列表>]
    <属性> is <值>
    
    on <动词>:
        <语句块>
```

**特殊关键字 `this`：**

在 Item 定义内部，`this` 指代当前物品实例。

**示例：**

```h
Item magic_chest:
    description is "An ornate chest with mystical runes."
    tags is [container, magic]
    isLocked is true
    contents is [magic_ring]
    
    on opens:
        if this.isLocked:
            echo "The chest is magically sealed."
        else:
            echo "The chest opens with a soft glow."
            set this.isOpen to true
    
    on uses magic_key:
        if player has magic_key:
            set this.isLocked to false
            echo "The key fits perfectly. The seal breaks!"
        else:
            echo "You need a magic key to open this."
```

### 2.3 角色（Character）

角色是游戏中的非玩家角色（NPC）。

```h
Character <标识符>:
    description is <字符串>
    <属性> is <值>
    uses dialog <对话树标识符>
```

**示例：**

```h
Character old_merchant:
    description is "A weary merchant with a loaded cart."
    mood is "friendly"
    uses dialog merchant_dialog
```

---

## 三、继承与扩展机制

### 3.1 类型继承

H-Game 支持通过 `extends` 关键字实现类型继承，允许创建基于现有类型的特化版本。

**语法：**

```h
Item <标识符> extends <父类型>:
    <新增或覆盖的属性>
    
    on <动词>:
        <语句块>
```

### 3.2 继承规则

- **属性继承**：子类型自动继承父类型的所有属性
- **属性覆盖**：子类型可以重新定义父类型的属性
- **处理器继承**：父类型的 `on` 处理器对子类型有效
- **处理器覆盖**：子类型可以定义同名处理器来覆盖父类行为
- **多态性**：子类型实例可以出现在任何需要父类型的地方

### 3.3 继承示例

**定义可锁定物品基类：**

```h
Item lockable_container:
    description is "A container that can be locked."
    isLocked is false
    isOpen is false
    
    on opens:
        if this.isLocked:
            echo "It's locked."
        else:
            set this.isOpen to true
            echo "You open it."
    
    on closes:
        set this.isOpen to false
        echo "You close it."
    
    on uses key:
        if this.isLocked:
            set this.isLocked to false
            echo "You unlock it."
        else:
            set this.isLocked to true
            echo "You lock it."
```

**创建继承的子类型：**

```h
Item treasure_chest extends lockable_container:
    description is "A heavy chest reinforced with iron bands."
    contents is [gold_coins, magic_scroll]
    isLocked is true
    
    on opens:
        // 先调用父类逻辑（隐式）
        if this.isOpen:
            echo "The chest creaks open, revealing glittering treasure!"
            increase $score by 50
```

### 3.4 多重继承（Mixin 模式）

支持从多个父类型继承特性：

```h
Item magic_lockbox extends lockable_container, magic_item:
    description is "A box that is both locked and magical."
    // 继承 lockable_container 的锁定机制
    // 继承 magic_item 的魔法属性
```

---

## 四、复合动作系统


---

## 五、事件系统

### 5.1 事件监听

所有事件使用统一的 `on` 关键字声明：

```h
on <事件类型>: <触发条件>:
    <语句块>
```


### 5.2 事件类型

| 类型 | 语法 | 触发时机 |
|------|------|----------|
| 玩家动作 | `on action: player <动词> [this]` | 玩家对物品执行动作 |
| 玩家交互 | `on action: player <动词> <物品> on <目标>` | 玩家使用物品作用于目标 |
| 状态变化 | `on state: <条件>` | 条件变为真时 |
| 计时器 | `on timer: <标识符> expires` | 计时器到期时 |
| 随机事件 | `on event: <标识符>` | 按概率触发 |

### 5.3 复合动作语法详解

复合动作允许玩家使用一个物品作用于另一个目标，形成 `verb + instrument + target` 的完整交互模式。

**基本语法：**

```h
on action: player <动词> <工具> [on|with|at|to] <目标>:
    <语句块>
```

**介词别名：**

| 介词 | 适用场景 |
|------|----------|
| `on` | 作用于表面（uses key on door） |
| `with` | 配合使用（attacks with sword） |
| `at` | 指向目标（throws rock at window） |
| `to` | 给予/连接（gives potion to ally） |

**完整示例：**

```h
Item sword:
    description is "A sharp steel blade."
    
    on attacks with this at enemy:
        set damage to calculateDamage(player.strength, this.sharpness)
        decrease enemy.health by damage
        echo "You slash the enemy for " + damage + " damage!"
        
        if enemy.health is less than or equal to 0:
            echo "The enemy falls!"
            set enemy.isAlive to false

Item healing_potion:
    description is "A red liquid that restores health."
    
    on uses this on player:
        increase player.health by 30
        remove this from player.inventory
        echo "You feel rejuvenated!"
    
    on gives this to ally:
        increase ally.health by 30
        remove this from player.inventory
        add this to ally.inventory
        echo "You give the potion to " + ally.name
```

**动作别名机制：**

允许为同一动作定义多个触发词：

```h
Item torch:
    on lights|ignites|kindles this:
        set this.isLit to true
        echo "The torch bursts into flame."
    
    on extinguishes|puts_out|douses this:
        set this.isLit to false
        echo "The torch goes dark."
```


### 5.4 事件处理示例

**玩家动作事件：**

```h
on action: player uses rusty_key on chest:
    if chest.isLocked:
        set chest.isLocked to false
        set chest.isOpen to true
        set rusty_key.isBroken to true
        increase $score by 10
        echo "The key turns with a snap... and breaks!"
        echo "But the chest swings open."
    else:
        echo "The chest is already unlocked."
```


**状态变化事件：**

```h
on state: hour is 18:
    set weather to "night"
    echo "The sun sets. Darkness falls."

on state: player.location is "Courtyard" and not player has lantern:
    echo "It's getting dark. You should find a light source."
```

**复合动作事件：**

```h
on action: player uses crowbar on sealed_crate:
    if player.strength is greater than 10:
        set sealed_crate.isOpen to true
        echo "You pry open the crate with brute force!"
    else:
        echo "You're not strong enough to pry it open."
        echo "Maybe find another way."

on action: player throws bomb at wall:
    start timer explosion for 3 seconds
    echo "The bomb sticks to the wall, ticking ominously..."

on action: player combines glue with broken_statue:
    remove glue from player.inventory
    remove broken_statue from player.inventory
    add repaired_statue to player.inventory
    echo "You carefully glue the pieces back together."
```


**计时器事件：**

```h
on timer: bomb expires:
    echo "BOOM!"
    end game
```


**随机事件：**

```h
on event: random_encounter:
    30% chance:
        echo "A wild wolf appears!"
        start combat with wolf
    70% chance:
        echo "The path remains clear."
```

---

## 六、对话系统


### 6.1 对话树定义

对话树定义角色与玩家之间的分支对话。

```h
dialog <标识符>:
    state <标识符>:
        speaker is <角色标识符>
        text is <字符串>
        
        option <文本>:
            [requires: <条件>]
            [action:
                <语句块>]
            goto <下一状态>
```


### 6.2 选项控制

- `requires`：前置条件，不满足时选项不显示
- `action`：选择后执行的动作
- `goto`：跳转到的状态

### 6.3 完整对话示例


```h
dialog merchant_dialog:
    state greeting:
        speaker is old_merchant
        text is "Greetings, traveler! Care to see my wares?"
        
        option "Show me what you have":
            requires: player.gold is greater than 0
            goto show_goods
        
        option "I'm just looking":
            goto browsing
        
        option "Goodbye":
            goto farewell
    
    state show_goods:
        speaker is old_merchant
        text is "Finest quality! Sword for 50 gold, shield for 40."
        
        option "Buy sword":
            requires: player.gold is greater than 50
            action:
                decrease player.gold by 50
                add sword to player.inventory
            goto greeting
        
        option "Buy shield":
            requires: player.gold is greater than 40
            action:
                decrease player.gold by 40
                add shield to player.inventory
            goto greeting
        
        option "Maybe later":
            goto greeting
    
    state browsing:
        speaker is old_merchant
        text is "Take your time. Let me know if you need anything."
        
        option "Actually, show me your wares":
            goto show_goods
        
        option "Goodbye":
            goto farewell
    
    state farewell:
        speaker is old_merchant
        text is "Safe travels, friend!"
```

---

## 七、游戏生命周期


### 7.1 游戏启动

在游戏开始时执行一次性初始化。

```h
on game start:
    <初始化语句>
```


**示例：**

```h
on game start:
    set $score to 0
    set $turns to 0
    set player.health to 100
    set player.inventory to []
    set player.location to "StartRoom"
    set world.time to "morning"
```

### 7.2 每回合更新

在每个游戏回合执行更新逻辑。

```h
on every turn:
    <更新语句>
```


**示例：**

```h
on every turn:
    increase $turns by 1
    increase world.hour by 1
    
    if world.hour is greater than 22 and not player.has lantern:
        echo "You are engulfed by darkness..."
        end game
```

---


---

## 八、形式化语法扩展

### 8.1 EBNF 定义（游戏框架扩展）

```ebnf
(* ============================================
   H-Game 形式化语法扩展 v1.1
   基于 H-Core 语法
   新增：继承机制、复合动作、条件出口
   ============================================ *)

(* --------------------------------------------
   游戏世界定义
   -------------------------------------------- *)
definition      = room_def | item_def | character_def | dialog_def | test_def;

room_def        = "Room", identifier, ":", indent, room_body, dedent;
room_body       = desc_attr, [ items_attr ], [ chars_attr ], [ exits_attr ];
desc_attr       = "description", "is", string;
items_attr      = "items", "is", list;
chars_attr      = "characters", "is", list;
exits_attr      = "exits", "is", "[", [ exit_def, { ",", exit_def } ], "]";
exit_def        = direction, "to", identifier, [ exit_condition ];
direction       = "north" | "south" | "east" | "west" | "up" | "down" 
                 | "northeast" | "northwest" | "southeast" | "southwest"
                 | identifier;
exit_condition  = "if", expression;

item_def        = "Item", identifier, [ extends_clause ], ":", indent, item_body, dedent;
extends_clause  = "extends", identifier, { ",", identifier };
item_body       = desc_attr, [ tags_attr ], { property }, { verb_handler };
tags_attr       = "tags", "is", list;
property        = identifier, "is", value;
verb_handler    = "on", verb_pattern, ":", indent, { statement }, dedent;
verb_pattern    = verb_alias, { "|", verb_alias }, [ action_target ];
verb_alias      = identifier;
action_target   = "this" | identifier, [ preposition, identifier ];
preposition     = "on" | "with" | "at" | "to" | "from" | "in";

character_def   = "Character", identifier, [ extends_clause ], ":", indent, char_body, dedent;
char_body       = desc_attr, { property }, [ "uses", "dialog", identifier ];

dialog_def      = "dialog", identifier, ":", indent, { state_def }, dedent;
state_def       = "state", identifier, ":", indent, speaker_attr, text_attr, { option_def }, dedent;
speaker_attr    = "speaker", "is", identifier;
text_attr       = "text", "is", string;
option_def      = "option", string, ":", indent, option_body, dedent;
option_body     = [ "requires", ":", expression ], [ "action", ":", indent, { statement }, dedent ], "goto", identifier;

(* --------------------------------------------
   事件处理（游戏框架扩展）
   -------------------------------------------- *)
event_handler   = "on", event_type, ":", event_target, ":", indent, { statement }, dedent;
event_type      = "action" | "state" | "timer" | "event" | "game start" | "every turn";
event_target    = player_action | expression | identifier, "expires";

player_action   = "player", verb_pattern
                 | "player", verb_pattern, preposition, identifier;

(* --------------------------------------------
   概率事件
   -------------------------------------------- *)
chance_stmt     = number, "%", "chance", ":", indent, { statement }, dedent;
```

### 8.2 条件出口详细规范

条件出口允许房间出口根据游戏状态动态可用：

```h
Room SecretChamber:
    description is "A hidden room behind the bookcase."
    exits is [
        south to Library,                                    // 无条件出口
        up to TreasureVault if secret_stair.isRevealed,    // 条件出口
        east to EscapeTunnel if player.has map and player.has lantern
    ]
```

**条件出口求值规则：**

1. 每次玩家尝试移动时重新求值
2. 条件为 `true` 时出口显示并可用
3. 条件为 `false` 时出口隐藏（玩家看不到）
4. 条件求值失败（错误）时视为 `false`

**动态出口示例：**

```h
Room CollapsingBridge:
    description is "A rickety bridge over a chasm."
    exits is [
        east to SafeGround,
        west to TreasureRoom if bridge.supports is greater than 0
    ]

on every turn:
    if player.location is "CollapsingBridge":
        decrease bridge.supports by 1
        if bridge.supports is 3:
            echo "The bridge creaks ominously..."
        else if bridge.supports is 1:
            echo "The bridge is about to collapse!"
        else if bridge.supports is less than or equal to 0:
            echo "The bridge collapses behind you!"
            // 出口自动不可用
```



### 8.3 新增关键字

游戏框架添加了以下关键字（相对于 H-Core）：

```
action, assert, at, by, contains, description, dialog, east, event, every, exits
extends, from, game, goto, has, increase, in, item, items, northeast, northwest, 
north, on, option, perform, player, remove, room, run, echo, set, south, southeast, 
southwest, speaker, start, state, stop, tags, test, text, this, timer, to, turn, 
uses, wait, when, with
```



---

## 附录：完整游戏示例

```h
// 古堡探险 - 完整游戏示例

on game start:
    set $score to 0
    set $moves to 0
    set player.health to 100
    set player.inventory to []
    set player.location to "Entrance"

Room Entrance:
    description is "You stand before a towering iron gate. The castle looms above."
    items is [rusty_key]
    exits is [north to Courtyard]

Room Courtyard:
    description is "A cobblestone courtyard. Vines climb the weathered walls."
    items is [lantern]
    characters is [guard]
    exits is [
        south to Entrance,
        east to GreatHall if great_door.isOpen
    ]

Item rusty_key:
    description is "An old iron key, covered in rust."
    
    on uses this on great_door:
        if great_door.isLocked:
            set great_door.isLocked to false
            set great_door.isOpen to true
            set this.isBroken to true
            echo "The key turns with a grinding sound... and snaps!"
            echo "But the door swings open."
        else:
            echo "The door is already unlocked."

Item lantern:
    description is "A brass lantern. It needs oil."
    hasOil is false
    
    on uses oil_flask:
        set this.hasOil to true
        set this.isLit to true
        echo "You fill and light the lantern. Warm glow fills the area."

Character guard:
    description is "A tired guard leaning on his spear."
    uses dialog guard_dialog

dialog guard_dialog:
    state initial:
        speaker is guard
        text is "Halt! The east wing is locked. No one enters."
        
        option "I have business inside":
            goto business
        
        option "Where is the key?":
            goto key_inquiry
        
        option "Goodbye":
            goto farewell
    
    state business:
        speaker is guard
        text is "What business could you have in there?"
        
        option "I'm the new librarian":
            requires: player has appointment_letter
            action:
                increase $score by 5
            goto impressed
        
        option "None of your concern":
            goto annoyed
    
    state key_inquiry:
        speaker is guard
        text is "The master has the only key. He never leaves the tower."
        
        option "Thanks for the information":
            goto initial
    
    state impressed:
        speaker is guard
        text is "Ah, forgive me sir! Please enter."
        action:
            set guard.letsPass to true
        goto farewell
    
    state annoyed:
        speaker is guard
        text is "Watch your tongue, stranger!"
        goto initial
    
    state farewell:
        speaker is guard
        text is "Move along now."

on action: player attacks guard:
    echo "The guard raises his spear. 'You dare?'"
    set guard.isHostile to true

on state: player.location is "Courtyard" and not player has lantern:
    echo "It's getting dark. You should find a light source."

on every turn:
    increase $moves by 1
    if $moves is greater than 100:
        echo "You collapse from exhaustion..."
        end game
```

---

**文档版本：** v1.0  
**依赖：** [H-Core 语言规范](./core-language-spec.md)  
**相关文档：** 
- [标准库参考](./stdlib-reference.md) - 内置动作和API
