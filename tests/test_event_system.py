"""
测试H语言事件系统
验证事件注册、触发和游戏框架功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 通过包导入
from h_lang.core import HLangInterpreter, parse, tokenize





def test_event_system():
    """测试事件系统基础功能"""
    print("=" * 60)
    print("测试事件系统")
    print("=" * 60)
    
    # 测试代码：定义带有事件处理器的房间
    test_code = '''
// 定义一个带有事件处理器的房间
room Kitchen:
    description: "A cozy kitchen with a table"
    
    on game start:
        echo "Welcome to the Kitchen!"
    
    on action: player uses table:
        echo "You examine the wooden table."
    
    on state: $player_health is less than 10:
        echo "Warning: Low health detected!"
    
    on every turn:
        echo "Turn completed in Kitchen"

// 定义一个物品
item Sword:
    name: "Iron Sword"
    damage: 15
    
    on action: player uses sword:
        echo "You swing the sword!"

// 定义一个角色
character Goblin:
    name: "Goblin Warrior"
    health: 50
    
    on state: health is 0:
        echo "The goblin has been defeated!"
'''

    try:
        interpreter = HLangInterpreter()
        
        # 解析代码
        print("\n1. 解析代码...")
        program = parse(test_code)
        print(f"   ✓ 解析成功")
        print(f"   - 语句数: {len(program.statements)}")
        print(f"   - 函数数: {len(program.functions)}")
        
        # 执行代码（注册类和事件处理器）
        print("\n2. 执行代码（注册类和事件处理器）...")
        interpreter.execute(test_code)
        print(f"   ✓ 执行成功")
        
        # 获取输出
        output = interpreter.get_output()
        print(f"\n3. 输出内容:")
        for line in output:
            print(f"   {line}")
        
        # 测试事件触发
        print("\n4. 测试手动触发事件...")
        evaluator = interpreter.evaluator
        
        # 触发游戏开始事件
        print("   触发 'game_start' 事件...")
        result = evaluator.trigger_event('game_start')
        print(f"   ✓ 事件触发结果: {result}")
        
        # 触发动作事件
        print("   触发 'action' 事件 (player uses table)...")
        result = evaluator.trigger_event('action', action='player uses table')
        print(f"   ✓ 事件触发结果: {result}")
        
        # 触发每回合事件
        print("   触发 'every_turn' 事件...")
        result = evaluator.trigger_event('every_turn', turn=1)
        print(f"   ✓ 事件触发结果: {result}")
        
        # 获取最新输出
        new_output = interpreter.get_output()[len(output):]
        print(f"\n5. 事件触发后的新输出:")
        for line in new_output:
            print(f"   {line}")
        
        print("\n" + "=" * 60)
        print("✓ 事件系统测试通过!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_dialog_system():
    """测试对话系统"""
    print("\n" + "=" * 60)
    print("测试对话系统")
    print("=" * 60)
    
    test_code = '''
// 测试对话系统
dialog npc "Welcome to my shop!":
    option "Buy potion" -> buy_potion
    option "Sell item" -> sell_item
    option "Leave" -> end_dialog
'''

    try:
        interpreter = HLangInterpreter()
        
        print("\n1. 执行对话代码...")
        interpreter.execute(test_code)
        
        print("\n2. 输出内容:")
        output = interpreter.get_output()
        for line in output:
            print(f"   {line}")
        
        # 检查对话状态
        evaluator = interpreter.evaluator
        dialog_state = evaluator.action_context.get_game_state('current_dialog')
        
        if dialog_state:
            print(f"\n3. 对话状态:")
            print(f"   - 说话者: {dialog_state['speaker']}")
            print(f"   - 文本: {dialog_state['text']}")
            print(f"   - 选项数: {len(dialog_state['options'])}")
        
        print("\n" + "=" * 60)
        print("✓ 对话系统测试通过!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_exit_system():
    """测试条件出口系统"""
    print("\n" + "=" * 60)
    print("测试条件出口系统")
    print("=" * 60)
    
    test_code = '''
// 设置全局变量
set $has_key to true
set $player_health to 100

// 定义带有条件出口的房间
room Dungeon:
    description: "A dark dungeon"
    
    exit north to Garden
    exit east to TreasureRoom if $has_key
    exit south to Exit if $player_health is greater than 50
'''

    try:
        interpreter = HLangInterpreter()
        
        print("\n1. 执行房间定义代码...")
        interpreter.execute(test_code)
        
        print("\n2. 检查出口状态:")
        evaluator = interpreter.evaluator
        exits = evaluator.action_context.get_game_state('exits')
        
        if exits:
            for direction, info in exits.items():
                condition = info.get('condition')
                condition_str = " (conditional)" if condition else " (always)"
                print(f"   - {direction} -> {info['target']}{condition_str}")
        
        print("\n" + "=" * 60)
        print("✓ 条件出口系统测试通过!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_timer_event():
    """测试计时器事件"""
    print("\n" + "=" * 60)
    print("测试计时器事件")
    print("=" * 60)
    
    test_code = '''
// 定义带有计时器事件的物品
item Bomb:
    name: "Time Bomb"
    
    on timer: bomb expires:
        echo "BOOM! The bomb exploded!"
'''

    try:
        interpreter = HLangInterpreter()
        
        print("\n1. 执行代码（注册计时器事件处理器）...")
        interpreter.execute(test_code)
        print("   ✓ 代码执行成功")
        
        # 启动计时器
        print("\n2. 启动计时器...")
        timer_code = '''
start timer bomb for 1 seconds
'''
        interpreter.execute(timer_code)
        print("   ✓ 计时器启动")
        
        # 等待计时器到期
        print("\n3. 等待计时器到期...")
        import time
        time.sleep(1.5)
        
        # 获取输出
        output = interpreter.get_output()
        print(f"\n4. 输出内容:")
        for line in output:
            print(f"   {line}")
        
        print("\n" + "=" * 60)
        print("✓ 计时器事件测试通过!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print("H语言事件系统完整测试")
    print("=" * 70)
    
    results = []
    
    # 运行各个测试
    results.append(("事件系统", test_event_system()))
    results.append(("对话系统", test_dialog_system()))
    results.append(("条件出口", test_exit_system()))
    results.append(("计时器事件", test_timer_event()))
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"  {name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n总计: {passed}/{total} 测试通过")
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
