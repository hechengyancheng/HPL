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
            say "The chest is magically sealed."
        else:
            say "The chest opens with a soft glow."
            set this.isOpen to true
    
    on uses magic_key:
        if player has magic_key:
            set this.isLocked to false
            say "The key fits perfectly. The seal breaks!"
        else:
            say "You need a magic key to open this."
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

## 三、事件系统

### 3.1 事件监听

所有事件使用统一的 `on` 关键字声明：

```h
on <事件类型>: <触发条件>:
    <语句块>
```

### 3.2 事件类型

| 类型 | 语法 | 触发时机 |
|------|------|----------|
| 玩家动作 | `on action: player <动词> [this]` | 玩家对物品执行动作 |
| 玩家交互 | `on action: player <动词> <物品> on <目标>` | 玩家使用物品作用于目标 |
| 状态变化 | `on state: <条件>` | 条件变为真时 |
| 计时器 | `on timer: <标识符> expires` | 计时器到期时 |
| 随机事件 | `on event: <标识符>` | 按概率触发 |

### 3.3 事件处理示例

**玩家动作事件：**

```h
on action: player uses rusty_key on chest:
    if chest.isLocked:
        set chest.isLocked to false
        set chest.isOpen to true
        set rusty_key.isBroken to true
        increase $score by 10
        say "The key turns with a snap... and breaks!"
        say "But the chest swings open."
    else:
        say "The chest is already unlocked."
```

**状态变化事件：**

```h
on state: hour is 18:
    set weather to "night"
    say "The sun sets. Darkness falls."

on state: player.location is "Courtyard" and not player has lantern:
    say "It's getting dark. You should find a light source."
```

**计时器事件：**

```h
on timer: bomb expires:
    say "BOOM!"
    end game
```

**随机事件：**

```h
on event: random_encounter:
    30% chance:
        say "A wild wolf appears!"
        start combat with wolf
    70% chance:
        say "The path remains clear."
```

---

## 四、对话系统

### 4.1 对话树定义

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

### 4.2 选项控制

- `requires`：前置条件，不满足时选项不显示
- `action`：选择后执行的动作
- `goto`：跳转到的状态

### 4.3 完整对话示例

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

## 五、游戏生命周期

### 5.1 游戏启动

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

### 5.2 每回合更新

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
        say "You are engulfed by darkness..."
        end game
```

---

## 六、形式化语法扩展

### 6.1 EBNF 定义（游戏框架扩展）

```ebnf
(* ============================================
   H-Game 形式化语法扩展 v1.0
   基于 H-Core 语法
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
exit_def        = identifier, "to", identifier, [ "if", expression ];

item_def        = "Item", identifier, ":", indent, item_body, dedent;
item_body       = desc_attr, [ tags_attr ], { property }, { verb_handler };
tags_attr       = "tags", "is", list;
property        = identifier, "is", value;
verb_handler    = "on", identifier, ":", indent, { statement }, dedent;

character_def   = "Character", identifier, ":", indent, char_body, dedent;
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

player_action   = "player", identifier, [ "this" ]
                 | "player", identifier, identifier, "on", identifier;

(* --------------------------------------------
   概率事件
   -------------------------------------------- *)
chance_stmt     = number, "%", "chance", ":", indent, { statement }, dedent;
```

### 6.2 新增关键字

游戏框架添加了以下关键字（相对于 H-Core）：

```
action, assert, by, contains, description, dialog, event, every, exits
game, goto, has, increase, item, items, on, option, perform, player
remove, room, run, say, set, speaker, start, state, stop, tags, test
text, this, timer, to, turn, uses, wait, when
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
            say "The key turns with a grinding sound... and snaps!"
            say "But the door swings open."
        else:
            say "The door is already unlocked."

Item lantern:
    description is "A brass lantern. It needs oil."
    hasOil is false
    
    on uses oil_flask:
        set this.hasOil to true
        set this.isLit to true
        say "You fill and light the lantern. Warm glow fills the area."

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
    say "The guard raises his spear. 'You dare?'"
    set guard.isHostile to true

on state: player.location is "Courtyard" and not player has lantern:
    say "It's getting dark. You should find a light source."

on every turn:
    increase $moves by 1
    if $moves is greater than 100:
        say "You collapse from exhaustion..."
        end game
```

---

**文档版本：** v1.0  
**依赖：** [H-Core 语言规范](./core-language-spec.md)  
**相关文档：** 
- [标准库参考](./stdlib-reference.md) - 内置动作和API
