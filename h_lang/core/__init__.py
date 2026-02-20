"""
H-Language Core Package
H语言核心包

包含H语言的核心组件：
- lexer: 词法分析器
- parser: 语法分析器
- interpreter: 解释器
- ast: 抽象语法树
- types: 类型系统
- runtime: 运行时组件
"""

import sys
import os

# Try multiple import strategies
_imported = False

# Strategy 1: Relative imports
try:
    from .interpreter import HLangInterpreter, run, run_file
    from .lexer import tokenize, TokenType, LexerError
    from .parser import parse, ParseError
    from .runtime.control_flow import HRuntimeError, EndGameException
    from .types import HNumber, HString, HBoolean, HList, HNull, Operations
    _imported = True
except ImportError:
    pass

# Strategy 2: Direct imports (when h-lang is in path)
if not _imported:
    try:
        from core.interpreter import HLangInterpreter, run, run_file
        from core.lexer import tokenize, TokenType, LexerError
        from core.parser import parse, ParseError
        from core.runtime.control_flow import HRuntimeError, EndGameException
        from core.types import HNumber, HString, HBoolean, HList, HNull, Operations
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
        
        from core.interpreter import HLangInterpreter, run, run_file
        from core.lexer import tokenize, TokenType, LexerError
        from core.parser import parse, ParseError
        from core.runtime.control_flow import HRuntimeError, EndGameException
        from core.types import HNumber, HString, HBoolean, HList, HNull, Operations
        _imported = True
    except ImportError as e:
        raise ImportError(f"Could not import core modules: {e}")

__all__ = [
    'HLangInterpreter',
    'run',
    'run_file',
    'tokenize',
    'TokenType',
    'LexerError',
    'parse',
    'ParseError',
    'HRuntimeError',
    'EndGameException',
    'HNumber',
    'HString',
    'HBoolean',
    'HList',
    'HNull',
    'Operations',
]
