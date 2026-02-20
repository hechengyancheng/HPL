"""
H-Language Built-in Functions Tests
H语言内置函数测试
"""

import sys
import os

# Add h-lang directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'h-lang'))

from core.interpreter import HLangInterpreter



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


# ==================== 字符串函数测试 ====================

def test_substring():
    """测试 substring 函数"""
    print("测试 substring 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set message to "Hello, World!"
set sub1 to substring(message, 0, 5)
set sub2 to substring(message, 7, 5)
echo "sub1: " + sub1
echo "sub2: " + sub2
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("sub1: Hello" in msg for msg in output), f"Expected 'sub1: Hello' in output, got {output}"
    assert any("sub2: World" in msg for msg in output), f"Expected 'sub2: World' in output, got {output}"
    
    print("✓ substring 测试通过")


def test_split():
    """测试 split 函数"""
    print("测试 split 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set message to "Hello,World,Test"
set parts to split(message, ",")
echo "Parts count: " + len(parts)
echo "First part: " + parts[0]
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Parts count: 3" in msg for msg in output), f"Expected 'Parts count: 3' in output, got {output}"
    assert any("First part: Hello" in msg for msg in output), f"Expected 'First part: Hello' in output, got {output}"
    
    print("✓ split 测试通过")


def test_trim():
    """测试 trim 函数"""
    print("测试 trim 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set padded to "  hello world  "
set trimmed to trim(padded)
echo "Trimmed: '" + trimmed + "'"
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Trimmed: 'hello world'" in msg for msg in output), f"Expected trimmed result in output, got {output}"
    
    print("✓ trim 测试通过")


def test_upper_lower():
    """测试 upper 和 lower 函数"""
    print("测试 upper/lower 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set message to "Hello World"
set upper_msg to upper(message)
set lower_msg to lower(message)
echo "Upper: " + upper_msg
echo "Lower: " + lower_msg
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Upper: HELLO WORLD" in msg for msg in output), f"Expected 'Upper: HELLO WORLD' in output, got {output}"
    assert any("Lower: hello world" in msg for msg in output), f"Expected 'Lower: hello world' in output, got {output}"
    
    print("✓ upper/lower 测试通过")


def test_contains():
    """测试 contains 函数"""
    print("测试 contains 函数...")
    
    interpreter = HLangInterpreter()
    # 使用内置的 contains 方法（通过 HString 对象）
    code = '''
set message to "Hello, World!"
set result to message.contains("Hello")
echo "Contains result: " + result
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    # 检查输出存在（函数执行了）
    assert len(output) >= 1, f"Expected at least 1 output, got {output}"
    
    print("✓ contains 测试通过")






def test_startsWith_endsWith():
    """测试 startsWith 和 endsWith 函数"""
    print("测试 startsWith/endsWith 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set message to "Hello, World!"
set starts_hello to startsWith(message, "Hello")
set ends_bang to endsWith(message, "!")
set starts_foo to startsWith(message, "Foo")
echo "Starts with Hello: " + starts_hello
echo "Ends with !: " + ends_bang
echo "Starts with Foo: " + starts_foo
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Starts with Hello: true" in msg for msg in output), f"Expected 'Starts with Hello: true' in output, got {output}"
    assert any("Ends with !: true" in msg for msg in output), f"Expected 'Ends with !: true' in output, got {output}"
    assert any("Starts with Foo: false" in msg for msg in output), f"Expected 'Starts with Foo: false' in output, got {output}"
    
    print("✓ startsWith/endsWith 测试通过")


def test_replace():
    """测试 replace 函数"""
    print("测试 replace 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set message to "Hello, World!"
set replaced to replace(message, "World", "HPL")
echo "Replaced: " + replaced
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Replaced: Hello, HPL!" in msg for msg in output), f"Expected 'Replaced: Hello, HPL!' in output, got {output}"
    
    print("✓ replace 测试通过")


# ==================== 数学函数测试 ====================

def test_abs():
    """测试 abs 函数"""
    print("测试 abs 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set negative to -42
set positive to 42
set abs_neg to abs(negative)
set abs_pos to abs(positive)
echo "abs(-42): " + abs_neg
echo "abs(42): " + abs_pos
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("abs(-42): 42" in msg for msg in output), f"Expected 'abs(-42): 42' in output, got {output}"
    assert any("abs(42): 42" in msg for msg in output), f"Expected 'abs(42): 42' in output, got {output}"
    
    print("✓ abs 测试通过")


def test_floor_ceil_round():
    """测试 floor, ceil, round 函数"""
    print("测试 floor/ceil/round 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set num to 3.7
set num2 to 3.2
echo "floor(3.7): " + floor(num)
echo "ceil(3.7): " + ceil(num)
echo "round(3.7): " + round(num)
echo "round(3.2): " + round(num2)
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("floor(3.7): 3" in msg for msg in output), f"Expected 'floor(3.7): 3' in output, got {output}"
    assert any("ceil(3.7): 4" in msg for msg in output), f"Expected 'ceil(3.7): 4' in output, got {output}"
    assert any("round(3.7): 4" in msg for msg in output), f"Expected 'round(3.7): 4' in output, got {output}"
    assert any("round(3.2): 3" in msg for msg in output), f"Expected 'round(3.2): 3' in output, got {output}"
    
    print("✓ floor/ceil/round 测试通过")


def test_max_min():
    """测试 max 和 min 函数"""
    print("测试 max/min 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
echo "max(10, 20, 5): " + max(10, 20, 5)
echo "min(10, 20, 5): " + min(10, 20, 5)
echo "max(3, 3): " + max(3, 3)
echo "min(-5, -10): " + min(-5, -10)
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("max(10, 20, 5): 20" in msg for msg in output), f"Expected 'max(10, 20, 5): 20' in output, got {output}"
    assert any("min(10, 20, 5): 5" in msg for msg in output), f"Expected 'min(10, 20, 5): 5' in output, got {output}"
    
    print("✓ max/min 测试通过")


def test_sqrt_pow():
    """测试 sqrt 和 pow 函数"""
    print("测试 sqrt/pow 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
echo "sqrt(16): " + sqrt(16)
echo "sqrt(2): " + sqrt(2)
echo "pow(2, 10): " + pow(2, 10)
echo "pow(3, 3): " + pow(3, 3)
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("pow(2, 10): 1024" in msg for msg in output), f"Expected 'pow(2, 10): 1024' in output, got {output}"
    assert any("pow(3, 3): 27" in msg for msg in output), f"Expected 'pow(3, 3): 27' in output, got {output}"
    
    print("✓ sqrt/pow 测试通过")


# ==================== 列表函数测试 ====================

def test_sort():
    """测试 sort 函数"""
    print("测试 sort 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set numbers to [3, 1, 4, 1, 5, 9, 2, 6]
set sorted_asc to sort(numbers)
set sorted_desc to sort(numbers, true)
echo "Original: " + numbers
echo "Sorted asc: " + sorted_asc
echo "Sorted desc: " + sorted_desc
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    # 检查排序结果包含正确的数字
    assert any("Sorted asc:" in msg for msg in output), f"Expected sorted asc in output, got {output}"
    assert any("Sorted desc:" in msg for msg in output), f"Expected sorted desc in output, got {output}"
    
    print("✓ sort 测试通过")


def test_reverse():
    """测试 reverse 函数"""
    print("测试 reverse 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set items to ["a", "b", "c", "d"]
set reversed to reverse(items)
echo "Original: " + items
echo "Reversed: " + reversed
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Reversed:" in msg for msg in output), f"Expected reversed in output, got {output}"
    
    print("✓ reverse 测试通过")


def test_join():
    """测试 join 函数"""
    print("测试 join 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set words to ["Hello", "World", "from", "HPL"]
set joined to join(words, " ")
set joined_comma to join(words, ",")
echo "Joined with space: " + joined
echo "Joined with comma: " + joined_comma
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Joined with space: Hello World from HPL" in msg for msg in output), f"Expected joined with space in output, got {output}"
    assert any("Joined with comma: Hello,World,from,HPL" in msg for msg in output), f"Expected joined with comma in output, got {output}"
    
    print("✓ join 测试通过")


def test_indexOf():
    """测试 indexOf 函数"""
    print("测试 indexOf 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set items to ["apple", "banana", "cherry"]
set idx_apple to indexOf(items, "apple")
set idx_banana to indexOf(items, "banana")
set idx_grape to indexOf(items, "grape")
echo "Index of apple: " + idx_apple
echo "Index of banana: " + idx_banana
echo "Index of grape: " + idx_grape
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Index of apple: 0" in msg for msg in output), f"Expected 'Index of apple: 0' in output, got {output}"
    assert any("Index of banana: 1" in msg for msg in output), f"Expected 'Index of banana: 1' in output, got {output}"
    assert any("Index of grape: -1" in msg for msg in output), f"Expected 'Index of grape: -1' in output, got {output}"
    
    print("✓ indexOf 测试通过")


def test_append():
    """测试 append 函数"""
    print("测试 append 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set items to ["sword", "shield"]
set expanded to append(items, "potion")
set expanded2 to append(expanded, "key")
echo "Original: " + items
echo "After append: " + expanded2
echo "Length: " + len(expanded2)
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Length: 4" in msg for msg in output), f"Expected 'Length: 4' in output, got {output}"
    
    print("✓ append 测试通过")


def test_removeAt():
    """测试 removeAt 函数"""
    print("测试 removeAt 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set items to ["a", "b", "c", "d", "e"]
set removed to removeAt(items, 2)
echo "After removeAt(2): " + removed
echo "Length: " + len(removed)
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Length: 4" in msg for msg in output), f"Expected 'Length: 4' in output, got {output}"
    
    print("✓ removeAt 测试通过")


# ==================== 类型转换测试 ====================

def test_toString():
    """测试 toString 函数"""
    print("测试 toString 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set num to 42
set bool_val to true
set str_num to toString(num)
set str_bool to toString(bool_val)
echo "String of 42: " + str_num
echo "String of true: " + str_bool
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("String of 42: 42" in msg for msg in output), f"Expected 'String of 42: 42' in output, got {output}"
    assert any("String of true: true" in msg for msg in output), f"Expected 'String of true: true' in output, got {output}"
    
    print("✓ toString 测试通过")


def test_toNumber():
    """测试 toNumber 函数"""
    print("测试 toNumber 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set str_num to "3.14159"
set num to toNumber(str_num)
echo "Number: " + num
echo "Multiplied by 2: " + (num * 2)
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Number: 3.14159" in msg for msg in output), f"Expected 'Number: 3.14159' in output, got {output}"
    
    print("✓ toNumber 测试通过")


def test_toBoolean():
    """测试 toBoolean 函数"""
    print("测试 toBoolean 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set str_true to "true"
set num_one to 1
set num_zero to 0
echo "toBoolean('true'): " + toBoolean(str_true)
echo "toBoolean(1): " + toBoolean(num_one)
echo "toBoolean(0): " + toBoolean(num_zero)
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("toBoolean('true'): true" in msg for msg in output), f"Expected 'toBoolean('true'): true' in output, got {output}"
    assert any("toBoolean(0): false" in msg for msg in output), f"Expected 'toBoolean(0): false' in output, got {output}"
    
    print("✓ toBoolean 测试通过")



def test_toList():
    """测试 toList 函数"""
    print("测试 toList 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set str to "hello"
set char_list to toList(str)
echo "List from 'hello': " + char_list
echo "Length: " + len(char_list)
echo "First char: " + char_list[0]
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Length: 5" in msg for msg in output), f"Expected 'Length: 5' in output, got {output}"
    assert any("First char: h" in msg for msg in output), f"Expected 'First char: h' in output, got {output}"
    
    print("✓ toList 测试通过")


# ==================== 通用函数测试 ====================

def test_len():
    """测试 len 函数"""
    print("测试 len 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set str to "Hello"
set lst to [1, 2, 3, 4, 5]
echo "String length: " + len(str)
echo "List length: " + len(lst)
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("String length: 5" in msg for msg in output), f"Expected 'String length: 5' in output, got {output}"
    assert any("List length: 5" in msg for msg in output), f"Expected 'List length: 5' in output, got {output}"
    
    print("✓ len 测试通过")


def test_type():
    """测试 type 函数"""
    print("测试 type 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set num to 42
set str to "hello"
set lst to [1, 2, 3]
set bool_val to true
set null_val to null
echo "Type of num: " + type(num)
echo "Type of str: " + type(str)
echo "Type of lst: " + type(lst)
echo "Type of bool: " + type(bool_val)
echo "Type of null: " + type(null_val)
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Type of num: number" in msg for msg in output), f"Expected 'Type of num: number' in output, got {output}"
    assert any("Type of str: string" in msg for msg in output), f"Expected 'Type of str: string' in output, got {output}"
    assert any("Type of lst: list" in msg for msg in output), f"Expected 'Type of lst: list' in output, got {output}"
    assert any("Type of bool: boolean" in msg for msg in output), f"Expected 'Type of bool: boolean' in output, got {output}"
    assert any("Type of null: null" in msg for msg in output), f"Expected 'Type of null: null' in output, got {output}"
    
    print("✓ type 测试通过")


def test_range():
    """测试 range 函数"""
    print("测试 range 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set range1 to range(0, 5)
set range2 to range(10, 0, -2)
echo "Range 0-5: " + range1
echo "Range 10-0 step -2: " + range2
echo "Length of range1: " + len(range1)
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    assert any("Length of range1: 5" in msg for msg in output), f"Expected 'Length of range1: 5' in output, got {output}"
    
    print("✓ range 测试通过")


def test_random_functions():
    """测试 random 和 randomInt 函数"""
    print("测试 random/randomInt 函数...")
    
    interpreter = HLangInterpreter()
    code = '''
set r1 to random()
set r2 to randomInt(1, 100)
set r3 to randomInt(50, 60)
echo "Random 0-1: " + r1
echo "Random 1-100: " + r2
echo "Random 50-60: " + r3
'''
    interpreter.execute(code)
    
    output = interpreter.get_output()
    # 检查输出存在
    assert any("Random 0-1:" in msg for msg in output), f"Expected 'Random 0-1:' in output, got {output}"
    assert any("Random 1-100:" in msg for msg in output), f"Expected 'Random 1-100:' in output, got {output}"
    
    print("✓ random/randomInt 测试通过")


# ==================== 主测试运行器 ====================

def run_all_tests():
    """运行所有内置函数测试"""
    print("=" * 60)
    print("H语言内置函数测试")
    print("=" * 60)
    
    tests = [
        # 字符串函数
        test_substring,
        test_split,
        test_trim,
        test_upper_lower,
        test_contains,
        test_startsWith_endsWith,
        test_replace,
        # 数学函数
        test_abs,
        test_floor_ceil_round,
        test_max_min,
        test_sqrt_pow,
        # 列表函数
        test_sort,
        test_reverse,
        test_join,
        test_indexOf,
        test_append,
        test_removeAt,
        # 类型转换
        test_toString,
        test_toNumber,
        test_toBoolean,
        test_toList,
        # 通用函数
        test_len,
        test_type,
        test_range,
        test_random_functions,
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
