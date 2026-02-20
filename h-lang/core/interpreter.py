"""
H-Language Interpreter
H语言主解释器入口
集成词法分析、语法分析和执行
"""

from typing import List, Optional, Any
from .lexer import tokenize, LexerError
from .parser import parse, ParseError
from .ast.statements import Program
from .interpreter_impl.environment import Environment
from .interpreter_impl.evaluator import Evaluator
from .interpreter_impl.control_flow import HRuntimeError
from .stdlib.builtins import Builtins


class HLangInterpreter:
    """
    H语言主解释器
    
    提供完整的代码执行流程：
    源代码 → 词法分析 → 语法分析 → 执行
    """
    
    def __init__(self):
        self.environment = Environment()
        self.evaluator = Evaluator(self.environment)
        self.output_history: List[str] = []
        
        # 注册内置函数
        builtins = Builtins()
        builtins.register_to_evaluator(self.evaluator)
    
    def execute(self, source: str) -> Any:
        """
        执行H语言源代码
        
        Args:
            source: H语言源代码字符串
            
        Returns:
            执行结果
            
        Raises:
            LexerError: 词法错误
            ParseError: 语法错误
            HRuntimeError: 运行时错误
        """
        # 1. 词法分析
        tokens = tokenize(source)
        
        # 2. 语法分析
        program = parse(source)  # parse内部会重新tokenize
        
        # 3. 执行
        result = self.evaluator.evaluate(program)
        
        # 收集输出
        self.output_history.extend(self.evaluator.get_output())
        self.evaluator.clear_output()
        
        return result
    
    def execute_file(self, filepath: str) -> Any:
        """
        执行H语言源文件
        
        Args:
            filepath: 文件路径
            
        Returns:
            执行结果
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        
        return self.execute(source)
    
    def reset(self):
        """
        重置解释器状态
        """
        self.environment = Environment()
        self.evaluator = Evaluator(self.environment)
        self.output_history.clear()
        
        # 重新注册内置函数
        builtins = Builtins()
        builtins.register_to_evaluator(self.evaluator)
    
    def get_output(self) -> List[str]:
        """
        获取输出历史
        """
        return self.output_history.copy()
    
    def clear_output(self):
        """
        清空输出历史
        """
        self.output_history.clear()
    
    def set_variable(self, name: str, value: Any):
        """
        设置变量值（用于与Python交互）
        """
        from .types.primitive import from_python
        h_value = from_python(value)
        self.environment.define(name, h_value)
    
    def get_variable(self, name: str) -> Any:
        """
        获取变量值（用于与Python交互）
        """
        from .types.primitive import to_python
        h_value = self.environment.get(name)
        return to_python(h_value)


# 便捷函数
def run(source: str) -> List[str]:
    """
    便捷函数：执行代码并返回输出
    
    Args:
        source: H语言源代码
        
    Returns:
        输出列表
    """
    interpreter = HLangInterpreter()
    interpreter.execute(source)
    return interpreter.get_output()


def run_file(filepath: str) -> List[str]:
    """
    便捷函数：执行文件并返回输出
    
    Args:
        filepath: 文件路径
        
    Returns:
        输出列表
    """
    interpreter = HLangInterpreter()
    interpreter.execute_file(filepath)
    return interpreter.get_output()


# 测试代码
if __name__ == "__main__":
    # 测试示例代码
    test_code = '''
// 测试H语言核心功能

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
echo "Sum result: " + result

// 内置函数使用
set count to len($items)
set sorted to sort($items)
set reversed to reverse($items)

echo "Item count: " + count
echo "Sorted: " + sorted
echo "Reversed: " + reversed

// 字符串函数
set message to "hello world"
set upper_msg to upper(message)
set contains_hello to contains(message, "hello")

echo "Upper: " + upper_msg
echo "Contains 'hello': " + contains_hello

// 数学函数
set num to 3.7
set rounded to round(num)
set floored to floor(num)

echo "Rounded: " + rounded
echo "Floored: " + floored
'''
    
    print("=" * 60)
    print("H语言解释器测试")
    print("=" * 60)
    
    try:
        interpreter = HLangInterpreter()
        interpreter.execute(test_code)
        
        print("\n" + "=" * 60)
        print("执行完成!")
        print("=" * 60)
        print("\n输出历史:")
        for i, output in enumerate(interpreter.get_output(), 1):
            print(f"  {i}. {output}")
            
    except LexerError as e:
        print(f"词法错误: {e}")
    except ParseError as e:
        print(f"语法错误: {e}")
    except HRuntimeError as e:
        print(f"运行时错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")
        import traceback
        traceback.print_exc()
