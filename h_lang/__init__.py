"""
H-Language Package
H语言包

H语言是一种面向游戏开发的领域特定语言(DSL)。
"""

__version__ = "0.1.0"

# 便捷导入 - 核心组件
from .core import (
    HLangInterpreter,
    run,
    run_file,
    tokenize,
    TokenType,
    LexerError,
    parse,
    ParseError,
    HRuntimeError,
    EndGameException,
    HNumber,
    HString,
    HBoolean,
    HList,
    HNull,
    Operations,
)

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
