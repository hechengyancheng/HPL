"""
H-Language Parser Tests
H语言语法分析器测试
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 通过包导入
from h_lang.core import parse, tokenize, ParseError


def test_basic_parsing():
    """测试基本解析功能"""
    print("测试基本解析...")
    
    # 测试赋值语句
    program = parse('set x to 42')
    assert len(program.statements) == 1
    print("  ✓ 赋值语句解析通过")
    
    # 测试条件语句
    program = parse('if x is greater than 10:\n    echo "big"')
    assert len(program.statements) == 1
    print("  ✓ 条件语句解析通过")
    
    # 测试函数定义
    code = '''function add(a, b):
    return a + b'''
    program = parse(code)
    assert "add" in program.functions
    print("  ✓ 函数定义解析通过")


def test_expressions():
    """测试表达式解析"""
    print("测试表达式解析...")
    
    # 测试二元运算
    program = parse('set result to 1 + 2')
    assert len(program.statements) == 1
    print("  ✓ 二元运算解析通过")
    
    # 测试函数调用
    program = parse('echo "Hello"')
    assert len(program.statements) == 1
    print("  ✓ 函数调用解析通过")


def run_all_tests():
    """运行所有解析器测试"""
    print("=" * 60)
    print("H语言语法分析器测试")
    print("=" * 60)
    
    try:
        test_basic_parsing()
        test_expressions()
        print("\n" + "=" * 60)
        print("✓ 所有测试通过!")
        print("=" * 60)
        return True
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
