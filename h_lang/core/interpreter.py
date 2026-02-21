"""
H-Language Interpreter
H语言主解释器入口
集成词法分析、语法分析和执行
"""

from typing import List, Optional, Any
import sys
import os

# Try multiple import strategies
_imported = False

# Strategy 1: Relative imports (when running as part of package)
try:
    from .lexer import tokenize, LexerError
    from .parser import parse, ParseError
    from .ast.statements import Program
    from .runtime.environment import Environment
    from .runtime.evaluator import Evaluator
    from .runtime.control_flow import HRuntimeError
    from ..stdlib.builtins import Builtins
    from .types.primitive import from_python, to_python
    _imported = True
except ImportError:
    pass

# Strategy 2: Direct imports (when h-lang is in path)
if not _imported:
    try:
        from core.lexer import tokenize, LexerError
        from core.parser import parse, ParseError
        from core.ast.statements import Program
        from core.runtime.environment import Environment
        from core.runtime.evaluator import Evaluator
        from core.runtime.control_flow import HRuntimeError
        from stdlib.builtins import Builtins
        from core.types.primitive import from_python, to_python
        _imported = True
    except ImportError:
        pass

# Strategy 3: Add paths and try again
if not _imported:
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        h_lang_dir = os.path.dirname(current_dir)
        
        if h_lang_dir not in sys.path:
            sys.path.insert(0, h_lang_dir)
        
        from core.lexer import tokenize, LexerError
        from core.parser import parse, ParseError
        from core.ast.statements import Program
        from core.runtime.environment import Environment
        from core.runtime.evaluator import Evaluator
        from core.runtime.control_flow import HRuntimeError
        from stdlib.builtins import Builtins
        from core.types.primitive import from_python, to_python
        _imported = True
    except ImportError as e:
        raise ImportError(f"Could not import required modules: {e}")




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
        h_value = from_python(value)
        self.environment.define(name, h_value)
    
    def get_variable(self, name: str) -> Any:
        """
        获取变量值（用于与Python交互）
        """
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
