"""
H-Language Core Tests
H语言核心模块单元测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.lexer import tokenize, TokenType, LexerError
from core.parser import parse, ParseError
from core.interpreter import HLangInterpreter, run
from core.types.primitive import *
from core.types.operations import Operations
from core.runtime.control_flow import HRuntimeError



def test_lexer():
    """测试词法分析器"""
    print("测试词法分析器...")
    
    # 测试基本token
    tokens = tokenize('set x to 42')
    assert len(tokens) > 0
    assert tokens[0].type == TokenType.SET
    
    # 测试数字
    tokens = tokenize('3.14')
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == 3.14
    
    # 测试字符串
    tokens = tokenize('"hello world"')
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "hello world"
    
    # 测试多词运算符
    tokens = tokenize('x is greater than y')
    assert any(t.type == TokenType.GT for t in tokens)
    
    print("  ✓ 词法分析器测试通过")


def test_parser():
    """测试语法分析器"""
    print("测试语法分析器...")
    
    # 测试赋值
    program = parse('set x to 42')
    assert len(program.statements) == 1
    
    # 测试条件
    program = parse('if x is greater than 10:\n    echo "big"')
    assert len(program.statements) == 1
    
    # 测试函数定义
    code = '''function add(a, b):
    return a + b'''
    program = parse(code)
    assert "add" in program.functions
    
    print("  ✓ 语法分析器测试通过")


def test_types():
    """测试类型系统"""
    print("测试类型系统...")
    
    # 测试数字
    num = HNumber(42)
    assert num.type_name() == "number"
    assert num.to_string() == "42"
    
    # 测试字符串
    s = HString("hello")
    assert s.type_name() == "string"
    assert s.to_string() == "hello"
    
    # 测试列表
    lst = HList([HNumber(1), HNumber(2), HNumber(3)])
    assert lst.type_name() == "list"
    assert len(lst) == 3
    assert lst.get_element(0).value == 1
    assert lst.get_element(-1).value == 3
    
    # 测试布尔值
    b = HBoolean(True)
    assert b.type_name() == "boolean"
    assert b.is_truthy() == True
    
    # 测试null
    n = HNull()
    assert n.type_name() == "null"
    assert n.is_truthy() == False
    
    print("  ✓ 类型系统测试通过")


def test_operations():
    """测试运算操作"""
    print("测试运算操作...")
    
    # 测试算术运算
    n1 = HNumber(10)
    n2 = HNumber(3)
    
    result = Operations.add(n1, n2)
    assert result.value == 13
    
    result = Operations.subtract(n1, n2)
    assert result.value == 7
    
    result = Operations.multiply(n1, n2)
    assert result.value == 30
    
    result = Operations.divide(n1, n2)
    assert abs(result.value - 3.333) < 0.01
    
    # 测试比较运算
    b = Operations.greater_than(n1, n2)
    assert b.value == True
    
    b = Operations.less_than(n1, n2)
    assert b.value == False
    
    # 测试逻辑运算
    b1 = HBoolean(True)
    b2 = HBoolean(False)
    
    result = Operations.logical_and(b1, b2)
    assert result.value == False
    
    result = Operations.logical_or(b1, b2)
    assert result.value == True
    
    result = Operations.logical_not(b1)
    assert result.value == False
    
    print("  ✓ 运算操作测试通过")


def test_interpreter():
    """测试解释器"""
    print("测试解释器...")
    
    # 测试基本执行
    output = run('echo "Hello"')
    assert "Hello" in output
    
    # 测试变量
    code = '''
set x to 10
set y to 20
set sum to x + y
echo sum'''
    output = run(code)
    assert "30" in output[0]
    
    # 测试条件
    code = '''
set x to 15
if x is greater than 10:
    echo "big"
else:
    echo "small"'''
    output = run(code)
    assert "big" in output[0]
    
    # 测试循环
    code = '''
set i to 0
while i is less than 3:
    echo i
    increase i by 1'''
    output = run(code)
    assert len(output) == 3
    
    # 测试函数
    code = '''
function greet(name):
    echo "Hello, " + name

greet("World")'''
    output = run(code)
    assert "Hello, World" in output[0]
    
    # 测试列表
    code = '''
set items to [1, 2, 3]
echo items[0]
echo len(items)'''
    output = run(code)
    assert "1" in output[0]
    assert "3" in output[1]
    
    print("  ✓ 解释器测试通过")


def test_builtin_functions():
    """测试内置函数"""
    print("测试内置函数...")
    
    # 测试数学函数
    code = '''
set x to 3.7
echo floor(x)
echo ceil(x)
echo round(x)'''
    output = run(code)
    assert "3" in output[0]  # floor
    assert "4" in output[1]  # ceil
    
    # 测试字符串函数
    code = '''
set s to "hello"
echo upper(s)
echo contains(s, "ell")'''
    output = run(code)
    assert "HELLO" in output[0]
    assert "true" in output[1].lower()
    
    # 测试列表函数
    code = '''
set lst to [3, 1, 2]
echo sort(lst)
echo reverse(lst)'''
    output = run(code)
    # 排序结果应该是 [1, 2, 3]
    # 反转结果应该是 [2, 1, 3]
    
    print("  ✓ 内置函数测试通过")


def test_examples_from_spec():
    """测试规范中的示例"""
    print("测试规范示例...")
    
    # 附录中的示例
    example_code = '''
set $counter to 0
set $items to ["apple", "banana", "cherry"]

// 条件判断
if $counter is less than 10:
    echo "Counter is low"
else if $counter is less than 100:
    echo "Counter is moderate"
else:
    echo "Counter is high"

// 循环
while $counter is less than 5:
    increase $counter by 1
    echo "Counting..."

// 列表操作与索引访问
if $items contains "banana":
    echo "We have bananas!"
    echo "First item is: " + $items[0]

// 函数定义与调用
function greet(name):
    echo "Hello, " + name

function sum(a, b):
    return a + b

greet("World")
set result to sum(10, 20)

// 内置函数使用
set count to len($items)
set sorted to sort($items)
set reversed to reverse($items)
'''
    
    try:
        interpreter = HLangInterpreter()
        interpreter.execute(example_code)
        output = interpreter.get_output()
        
        # 验证输出
        assert any("Counter is low" in s for s in output)
        assert any("Counting..." in s for s in output)
        assert any("We have bananas!" in s for s in output)
        assert any("Hello, World" in s for s in output)
        
        print("  ✓ 规范示例测试通过")
        
    except Exception as e:
        print(f"  ✗ 规范示例测试失败: {e}")
        raise


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("H语言核心模块测试")
    print("=" * 60)
    
    tests = [
        test_lexer,
        test_parser,
        test_types,
        test_operations,
        test_interpreter,
        test_builtin_functions,
        test_examples_from_spec,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} 失败: {e}")
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
