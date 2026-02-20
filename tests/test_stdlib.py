"""
H-Language Standard Library Tests
H语言标准库测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.interpreter import HLangInterpreter
from core.interpreter_impl.control_flow import EndGameException


class MockOutputHandler:
    """模拟输出处理器，用于测试"""
    
    def __init__(self):
        self.buffer = []
    
    def output(self, message):
        self.buffer.append(message)
    
    def clear(self):
        self.buffer.clear()
    
    def get_output(self):
        return self.buffer.copy()


def test_echo():
    """测试 echo 指令"""
    print("测试 echo 指令...")
    
    interpreter = HLangInterpreter()
    code = '''
echo "Hello, World!"
echo "Test message"
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert "Hello, World!" in output, f"Expected 'Hello, World!' in output, got {output}"
    assert "Test message" in output, f"Expected 'Test message' in output, got {output}"
    
    print("✓ echo 测试通过")


def test_add_remove():
    """测试 add/remove 指令"""
    print("测试 add/remove 指令...")
    
    interpreter = HLangInterpreter()
    code = '''
set inventory to ["sword", "shield"]
add "potion" to inventory
echo "After add: " + inventory
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    # 检查输出中包含 potion
    assert any("potion" in msg for msg in output), f"Expected 'potion' in output, got {output}"
    
    print("✓ add/remove 测试通过")



def test_increase_decrease():
    """测试 increase/decrease 指令"""
    print("测试 increase/decrease 指令...")
    
    interpreter = HLangInterpreter()
    code = '''
set health to 100
increase health by 20
echo "Health after increase: " + health
decrease health by 30
echo "Health after decrease: " + health
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    # 检查输出中包含 120 和 90
    assert any("120" in msg for msg in output), f"Expected '120' in output, got {output}"
    assert any("90" in msg for msg in output), f"Expected '90' in output, got {output}"
    
    print("✓ increase/decrease 测试通过")


def test_move_to():
    """测试 move to 指令"""
    print("测试 move to 指令...")
    
    interpreter = HLangInterpreter()
    code = '''
move to "Kitchen"
echo "Moved to location"
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Moved" in msg for msg in output), f"Expected 'Moved' in output, got {output}"
    
    print("✓ move to 测试通过")


def test_wait():
    """测试 wait for 指令"""
    print("测试 wait for 指令...")
    
    import time
    
    interpreter = HLangInterpreter()
    start_time = time.time()
    
    code = '''
wait for 0.1 seconds
echo "Wait completed"
'''
    interpreter.execute(code)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    # 检查是否至少等待了0.1秒
    assert elapsed >= 0.1, f"Expected wait of at least 0.1s, got {elapsed}s"
    
    output = interpreter.get_output()
    assert any("Wait completed" in msg for msg in output), f"Expected 'Wait completed' in output, got {output}"
    
    print("✓ wait for 测试通过")


def test_end_game():
    """测试 end game 指令"""
    print("测试 end game 指令...")
    
    interpreter = HLangInterpreter()
    code = '''
echo "Before end"
end game
echo "After end"
'''
    
    try:
        interpreter.execute(code)
        # 如果没有抛出异常，检查输出
        output = interpreter.get_output()
        assert "Before end" in output, f"Expected 'Before end' in output, got {output}"
        assert "After end" not in output, f"Expected 'After end' NOT in output, got {output}"
    except EndGameException:
        # 正常情况：end game 抛出异常
        output = interpreter.get_output()
        assert "Before end" in output, f"Expected 'Before end' in output, got {output}"
    
    print("✓ end game 测试通过")


def test_perform():
    """测试 perform 指令"""
    print("测试 perform 指令...")
    
    interpreter = HLangInterpreter()
    code = '''
perform "combat.attack" with "player", "enemy"
echo "Action performed"
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    # perform 应该输出动作信息
    assert len(output) > 0, f"Expected some output, got {output}"
    
    print("✓ perform 测试通过")



def test_timer():
    """测试计时器指令"""
    print("测试计时器指令...")
    
    import time
    
    interpreter = HLangInterpreter()
    code = '''
start timer "bomb" for 0.1 seconds
echo "Timer started"
wait for 0.15 seconds
echo "After timer"
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Timer started" in msg for msg in output), f"Expected 'Timer started' in output, got {output}"
    
    print("✓ timer 测试通过")



def test_stop_timer():
    """测试停止计时器指令"""
    print("测试 stop timer 指令...")
    
    interpreter = HLangInterpreter()
    code = '''
start timer "test_timer" for 10 seconds
echo "Timer started"
stop timer "test_timer"
echo "Timer stopped"
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Timer started" in msg for msg in output), f"Expected 'Timer started' in output, got {output}"
    assert any("Timer stopped" in msg for msg in output), f"Expected 'Timer stopped' in output, got {output}"
    
    print("✓ stop timer 测试通过")



def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("H语言标准库测试")
    print("=" * 60)
    
    tests = [
        test_echo,
        test_add_remove,
        test_increase_decrease,
        test_move_to,
        test_wait,
        test_end_game,
        test_perform,
        test_timer,
        test_stop_timer,
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
