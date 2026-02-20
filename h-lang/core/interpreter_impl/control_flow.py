"""
H-Language Control Flow
H语言控制流异常定义
用于实现return、break、continue等控制流
"""

from ..types.primitive import HValue, HNull


class ReturnException(Exception):
    """
    函数返回控制流
    当执行return语句时抛出，携带返回值
    """
    
    def __init__(self, value: HValue = None):
        self.value = value if value is not None else HNull()
        super().__init__(f"Return: {self.value}")


class BreakException(Exception):
    """
    循环中断控制流
    当执行break语句时抛出（如果语言支持）
    """
    
    def __init__(self):
        super().__init__("Break")


class ContinueException(Exception):
    """
    循环继续控制流
    当执行continue语句时抛出（如果语言支持）
    """
    
    def __init__(self):
        super().__init__("Continue")


class HRuntimeError(Exception):
    """
    H语言运行时错误
    用于报告执行期间的错误
    """
    
    def __init__(self, message: str, line: int = None, column: int = None):
        self.message = message
        self.line = line
        self.column = column
        
        location = ""
        if line is not None:
            location = f"[Line {line}"
            if column is not None:
                location += f", Col {column}"
            location += "] "
        
        super().__init__(f"{location}{message}")


class HTypeError(HRuntimeError):
    """
    H语言类型错误
    """
    pass


class HNameError(HRuntimeError):
    """
    H语言名称错误（未定义变量等）
    """
    pass


class HIndexError(HRuntimeError):
    """
    H语言索引错误
    """
    pass


class HAttributeError(HRuntimeError):
    """
    H语言属性错误
    """
    pass
