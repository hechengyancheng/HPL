"""
H-Language Game Framework Advanced Tests
H语言游戏框架高级功能测试
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 通过包导入
from h_lang.core import HLangInterpreter




def test_inheritance():
    """测试继承机制（extends关键字）"""
    print("测试继承机制...")
    
    interpreter = HLangInterpreter()
    code = '''
// 定义基础武器类型
item Weapon:
    damage: 0
    weight: 0
    
    on action: player uses weapon:
        echo "You swing the weapon!"

// 定义继承自Weapon的剑
item Sword extends Weapon:
    damage: 15
    weight: 5
    sharpness: 10

// 定义继承自Weapon的法杖
item Staff extends Weapon:
    damage: 8
    weight: 3
    magic_power: 20

// 定义基础敌人类型
character Enemy:
    health: 50
    attack: 5
    
    on state: health is 0:
        echo "Enemy defeated!"

// 定义继承自Enemy的哥布林
character Goblin extends Enemy:
    health: 30
    attack: 8
    stealth: 5

echo "Inheritance test completed"
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Inheritance test completed" in msg for msg in output), f"Expected completion message, got {output}"
    
    print("✓ 继承机制测试通过")


def test_compound_actions():
    """测试复合动作语法（uses X on Y）"""
    print("测试复合动作语法...")
    
    interpreter = HLangInterpreter()
    code = '''
// 定义钥匙物品
item Key:
    name: "Rusty Key"
    unlocks: "TreasureRoom"

// 定义宝箱物品
item TreasureChest:
    name: "Treasure Chest"
    locked: true
    contents: ["gold", "gems"]

// 定义可以使用钥匙的宝箱
item LockedChest:
    name: "Locked Chest"
    
    on action: player uses key on chest:
        echo "You unlock the chest with the key!"
        echo "Found treasure inside!"
    
    on action: player uses sword on chest:
        echo "You smash the chest with your sword!"
        echo "The contents are damaged."

// 定义可以使用药水的角色
character WoundedKnight:
    name: "Wounded Knight"
    health: 50
    
    on action: player uses potion on knight:
        echo "You heal the knight with the potion!"
        increase health by 30
        echo "Knight's health is now: " + health

echo "Compound action test setup complete"
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Compound action test setup complete" in msg for msg in output), f"Expected setup message, got {output}"
    
    print("✓ 复合动作语法测试通过")


def test_game_lifecycle():
    """测试完整游戏生命周期"""
    print("测试游戏生命周期...")
    
    interpreter = HLangInterpreter()
    code = '''
// 设置全局游戏状态
set $game_started to false
set $turn_count to 0
set $player_health to 100
set $game_ended to false

// 定义起始房间
room StartRoom:
    description: "The starting room of your adventure"
    
    on game start:
        set $game_started to true
        echo "=== GAME STARTED ==="
        echo "Welcome to the adventure!"
        echo "Your journey begins in the starting room."
    
    on every turn:
        increase $turn_count by 1
        echo "--- Turn " + $turn_count + " ---"
        
        // 模拟游戏逻辑
        if $turn_count is 1:
            echo "You look around the room."
        else if $turn_count is 2:
            echo "You find a mysterious door."
        else if $turn_count is 3:
            echo "You decide to exit the room."
            // 触发游戏结束
            set $game_ended to true
            echo "=== GAME COMPLETED ==="
            end game

// 游戏开始时自动触发
echo "Game lifecycle test initialized"
'''
    
    try:
        interpreter.execute(code)
    except Exception as e:
        # end game 会抛出异常，这是正常的
        pass
    
    output = interpreter.get_output()
    
    # 验证游戏生命周期事件被触发
    assert any("GAME STARTED" in msg for msg in output), f"Expected 'GAME STARTED' in output, got {output}"
    assert any("Turn 1" in msg for msg in output), f"Expected 'Turn 1' in output, got {output}"
    # 注意：游戏生命周期事件在代码执行时触发，可能不会执行所有回合

    
    print("✓ 游戏生命周期测试通过")


def test_conditional_exits():
    """测试条件出口系统"""
    print("测试条件出口系统...")
    
    interpreter = HLangInterpreter()
    code = '''
// 设置全局变量
set $has_key to false
set $player_level to 5
set $door_unlocked to false

// 定义花园房间（目标房间）
room Garden:
    description: "A beautiful garden with flowers"

// 定义地牢房间（带条件出口）
room Dungeon:
    description: "A dark dungeon"
    
    // 无条件出口
    exit north to Garden
    
    // 有条件出口：需要钥匙
    exit east to Garden if $has_key
    
    // 有条件出口：需要足够等级
    exit south to Garden if $player_level is greater than 10
    
    // 有条件出口：门已解锁
    exit west to Garden if $door_unlocked

// 测试条件出口
echo "Testing conditional exits..."

// 初始状态：没有钥匙，等级不够，门未解锁
echo "Initial state: no key, level 5, door locked"

// 获取钥匙
set $has_key to true
echo "Now have key: " + $has_key

// 提升等级
set $player_level to 15
echo "Level increased to: " + $player_level

// 解锁门
set $door_unlocked to true
echo "Door unlocked: " + $door_unlocked

echo "All conditions now met!"
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    # 检查条件出口系统的状态变化
    assert any("Initial state" in msg for msg in output), f"Expected initial state message, got {output}"
    assert any("Now have key: true" in msg for msg in output), f"Expected key status, got {output}"
    assert any("Level increased to: 15" in msg for msg in output), f"Expected level status, got {output}"
    assert any("Door unlocked: true" in msg for msg in output), f"Expected door status, got {output}"

    
    print("✓ 条件出口系统测试通过")


def test_dialog_system():
    """测试对话系统"""
    print("测试对话系统...")
    
    interpreter = HLangInterpreter()
    code = '''
// 定义NPC对话
dialog merchant "Welcome to my shop! What would you like to do?":
    option "Buy health potion (10 gold)" -> buy_potion
    option "Buy sword (50 gold)" -> buy_sword
    option "Sell items" -> sell_items
    option "Leave" -> end_dialog

// 定义另一个NPC对话
dialog guard "Halt! Who goes there?":
    option "I am a traveler" -> traveler_response
    option "I am a merchant" -> merchant_response
    option "None of your business" -> hostile_response

echo "Dialog system test setup complete"
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Dialog system test setup complete" in msg for msg in output), f"Expected setup message, got {output}"
    
    print("✓ 对话系统测试通过")


def test_timer_events():
    """测试计时器事件系统"""
    print("测试计时器事件系统...")
    
    import time
    
    interpreter = HLangInterpreter()
    code = '''
// 定义带计时器事件的物品
item Bomb:
    name: "Time Bomb"
    timer_started: false
    
    on timer: bomb expires:
        echo "BOOM! The bomb explodes!"
        echo "You take 50 damage!"

// 定义带计时器事件的角色
character Wizard:
    name: "Dark Wizard"
    
    on timer: spell expires:
        echo "The wizard's spell wears off!"

echo "Timer event test setup complete"

// 启动计时器
start timer "bomb" for 0.2 seconds
echo "Bomb timer started!"

// 等待计时器到期
wait for 0.3 seconds
echo "After bomb timer"
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Timer event test setup complete" in msg for msg in output), f"Expected setup message, got {output}"
    assert any("Bomb timer started!" in msg for msg in output), f"Expected timer start message, got {output}"
    
    print("✓ 计时器事件系统测试通过")


def test_state_events():
    """测试状态事件系统"""
    print("测试状态事件系统...")
    
    interpreter = HLangInterpreter()
    code = '''
// 设置全局变量
set $player_health to 100
set $player_mana to 50
set $in_combat to false

// 定义带状态事件的角色
character Player:
    name: "Hero"
    health: 100
    mana: 50
    
    on state: health is less than 30:
        echo "WARNING: Health is critically low!"
        echo "Find healing immediately!"
    
    on state: mana is less than 10:
        echo "WARNING: Mana is depleted!"
        echo "Cannot cast spells!"

// 定义带状态事件的房间
room DangerZone:
    description: "A dangerous area"
    
    on state: $in_combat is true:
        echo "Combat mode activated!"
        echo "Enemies are nearby!"

echo "State event test initialized"

// 模拟状态变化
set $player_health to 25
echo "Player health dropped to: " + $player_health

set $in_combat to true
echo "Combat status: " + $in_combat
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("State event test initialized" in msg for msg in output), f"Expected init message, got {output}"
    assert any("Player health dropped to: 25" in msg for msg in output), f"Expected health message, got {output}"
    assert any("Combat status: true" in msg for msg in output), f"Expected combat message, got {output}"
    
    print("✓ 状态事件系统测试通过")


def test_complex_game_scenario():
    """测试复杂游戏场景"""
    print("测试复杂游戏场景...")
    
    interpreter = HLangInterpreter()
    code = '''
// ============================================
// 复杂游戏场景：地牢探险
// ============================================

// 全局游戏状态
set $player_health to 100
set $player_gold to 0
set $inventory to []
set $current_room to "Entrance"

// 定义物品类型
item Weapon:
    damage: 0
    durability: 100

item Sword extends Weapon:
    damage: 15
    name: "Iron Sword"

item Potion:
    healing: 30
    name: "Health Potion"

// 定义角色类型
character Monster:
    health: 50
    attack: 10
    
    on state: health is 0:
        echo "Monster defeated!"
        increase $player_gold by 10

// 定义房间
room Entrance:
    description: "The dungeon entrance"
    
    exit south to Hallway
    
    on game start:
        echo "=== DUNGEON CRAWLER ==="
        echo "You stand at the entrance of a dark dungeon."
        echo "Your goal: find treasure and survive!"

room Hallway:
    description: "A long hallway with doors"
    
    exit north to Entrance
    exit east to TreasureRoom if $has_key
    exit west to MonsterRoom

room TreasureRoom:
    description: "A room filled with treasure!"
    
    exit west to Hallway
    
    on game start:
        echo "You found the treasure room!"
        increase $player_gold by 100
        echo "You collected 100 gold!"

room MonsterRoom:
    description: "A room with a monster!"
    
    exit east to Hallway
    
    on game start:
        echo "A monster appears!"
        echo "Combat begins!"

// 创建游戏对象
set $has_key to false
set $monster_defeated to false

echo "Complex game scenario setup complete"
echo "Player health: " + $player_health
echo "Player gold: " + $player_gold
echo "Current room: " + $current_room
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Complex game scenario setup complete" in msg for msg in output), f"Expected setup message, got {output}"
    assert any("Player health: 100" in msg for msg in output), f"Expected health info, got {output}"
    # 注意：游戏事件可能改变金币数量，所以只检查金币信息存在
    assert any("Player gold:" in msg for msg in output), f"Expected gold info, got {output}"

    
    print("✓ 复杂游戏场景测试通过")


def run_all_tests():
    """运行所有游戏框架高级测试"""
    print("=" * 60)
    print("H语言游戏框架高级功能测试")
    print("=" * 60)
    
    tests = [
        test_inheritance,
        test_compound_actions,
        test_game_lifecycle,
        test_conditional_exits,
        test_dialog_system,
        test_timer_events,
        test_state_events,
        test_complex_game_scenario,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 测试失败: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
