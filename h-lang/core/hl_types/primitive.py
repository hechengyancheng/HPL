"""
H-Language Primitive Types
H语言原始类型定义
"""

from abc import ABC, abstractmethod
from typing import List, Any, Optional
import math


class HValue(ABC):
    """
    H语言值基类
    所有H语言值都继承此类
    """
    
    def __init__(self, value: Any):
        self.value = value
    
    @abstractmethod
    def type_name(self) -> str:
        """返回类型名称"""
        pass
    
    @abstractmethod
    def to_string(self) -> str:
        """转换为字符串表示"""
        pass
    
    @abstractmethod
    def copy(self) -> 'HValue':
        """创建副本"""
        pass
    
    def is_truthy(self) -> bool:
        """判断是否为真值"""
        return True
    
    def __repr__(self):
        return f"{self.type_name()}({self.value!r})"
    
    def __eq__(self, other):
        if not isinstance(other, HValue):
            return False
        return self.value == other.value
    
    def equals(self, other: 'HValue') -> 'HBoolean':
        """比较两个值是否相等，返回HBoolean"""
        if not isinstance(other, HValue):
            return HBoolean(False)
        return HBoolean(self.value == other.value)



class HNumber(HValue):
    """
    H语言数字类型（64位浮点数）
    例如: 42, 3.14, -7
    """
    
    def __init__(self, value: float):
        super().__init__(float(value))
    
    def type_name(self) -> str:
        return "number"
    
    def to_string(self) -> str:
        # 如果是整数，不显示小数点
        if self.value == int(self.value):
            return str(int(self.value))
        return str(self.value)
    
    def copy(self) -> 'HNumber':
        return HNumber(self.value)
    
    def is_truthy(self) -> bool:
        return self.value != 0
    
    def is_integer(self) -> bool:
        """检查是否为整数"""
        return self.value == int(self.value)
    
    def to_int(self) -> int:
        """转换为Python整数"""
        return int(self.value)
    
    def __add__(self, other: 'HNumber') -> 'HNumber':
        return HNumber(self.value + other.value)
    
    def __sub__(self, other: 'HNumber') -> 'HNumber':
        return HNumber(self.value - other.value)
    
    def __mul__(self, other: 'HNumber') -> 'HNumber':
        return HNumber(self.value * other.value)
    
    def __truediv__(self, other: 'HNumber') -> 'HNumber':
        if other.value == 0:
            raise HRuntimeError("Division by zero")
        return HNumber(self.value / other.value)
    
    def __mod__(self, other: 'HNumber') -> 'HNumber':
        if other.value == 0:
            raise HRuntimeError("Modulo by zero")
        return HNumber(self.value % other.value)
    
    def __neg__(self) -> 'HNumber':
        return HNumber(-self.value)
    
    def __lt__(self, other: 'HNumber') -> bool:
        return self.value < other.value
    
    def __le__(self, other: 'HNumber') -> bool:
        return self.value <= other.value
    
    def __gt__(self, other: 'HNumber') -> bool:
        return self.value > other.value
    
    def __ge__(self, other: 'HNumber') -> bool:
        return self.value >= other.value


class HString(HValue):
    """
    H语言字符串类型
    例如: "hello", "line1\\nline2"
    """
    
    def __init__(self, value: str):
        super().__init__(str(value))
    
    def type_name(self) -> str:
        return "string"
    
    def to_string(self) -> str:
        return self.value
    
    def copy(self) -> 'HString':
        return HString(self.value)
    
    def is_truthy(self) -> bool:
        return len(self.value) > 0
    
    def __add__(self, other: 'HString') -> 'HString':
        return HString(self.value + other.value)
    
    def __len__(self) -> int:
        return len(self.value)
    
    def get_char(self, index: int) -> 'HString':
        """获取指定位置的字符"""
        if index < 0:
            index = len(self.value) + index
        if index < 0 or index >= len(self.value):
            raise HRuntimeError(f"String index out of range: {index}")
        return HString(self.value[index])
    
    def substring(self, start: int, length: Optional[int] = None) -> 'HString':
        """提取子字符串"""
        if start < 0:
            start = len(self.value) + start
        
        if length is None:
            return HString(self.value[start:])
        
        end = start + length
        return HString(self.value[start:end])
    
    def contains(self, substring: 'HString') -> bool:
        """检查是否包含子串"""
        return substring.value in self.value
    
    def starts_with(self, prefix: 'HString') -> bool:
        """检查前缀"""
        return self.value.startswith(prefix.value)
    
    def ends_with(self, suffix: 'HString') -> bool:
        """检查后缀"""
        return self.value.endswith(suffix.value)
    
    def upper(self) -> 'HString':
        """转为大写"""
        return HString(self.value.upper())
    
    def lower(self) -> 'HString':
        """转为小写"""
        return HString(self.value.lower())
    
    def trim(self) -> 'HString':
        """去除首尾空白"""
        return HString(self.value.strip())
    
    def split(self, separator: 'HString') -> 'HList':
        """分割字符串"""
        parts = self.value.split(separator.value)
        return HList([HString(part) for part in parts])
    
    def replace(self, old: 'HString', new: 'HString') -> 'HString':
        """替换子串"""
        return HString(self.value.replace(old.value, new.value))


class HBoolean(HValue):
    """
    H语言布尔类型
    例如: true, false
    """
    
    def __init__(self, value: bool):
        super().__init__(bool(value))
    
    def type_name(self) -> str:
        return "boolean"
    
    def to_string(self) -> str:
        return "true" if self.value else "false"
    
    def copy(self) -> 'HBoolean':
        return HBoolean(self.value)
    
    def is_truthy(self) -> bool:
        return self.value
    
    def __and__(self, other: 'HBoolean') -> 'HBoolean':
        return HBoolean(self.value and other.value)
    
    def __or__(self, other: 'HBoolean') -> 'HBoolean':
        return HBoolean(self.value or other.value)
    
    def __not__(self) -> 'HBoolean':
        return HBoolean(not self.value)


class HList(HValue):
    """
    H语言列表类型
    例如: [1, 2, 3], ["a", "b", "c"]
    """
    
    def __init__(self, elements: Optional[List[HValue]] = None):
        if elements is None:
            elements = []
        # 确保所有元素都是HValue
        self.value = [elem if isinstance(elem, HValue) else from_python(elem) 
                      for elem in elements]
    
    def type_name(self) -> str:
        return "list"
    
    def to_string(self) -> str:
        elements_str = ", ".join(elem.to_string() for elem in self.value)
        return f"[{elements_str}]"
    
    def copy(self) -> 'HList':
        return HList([elem.copy() for elem in self.value])
    
    def is_truthy(self) -> bool:
        return len(self.value) > 0
    
    def __len__(self) -> int:
        return len(self.value)
    
    def get_element(self, index: int) -> HValue:
        """获取指定索引的元素（支持负索引）"""
        if index < 0:
            index = len(self.value) + index
        
        if index < 0 or index >= len(self.value):
            raise HRuntimeError(f"List index out of range: {index} (list length: {len(self.value)})")
        
        return self.value[index]
    
    def set_element(self, index: int, value: HValue):
        """设置指定索引的元素"""
        if index < 0:
            index = len(self.value) + index
        
        if index < 0 or index >= len(self.value):
            raise HRuntimeError(f"List index out of range: {index} (list length: {len(self.value)})")
        
        self.value[index] = value
    
    def get_slice(self, start: Optional[int] = None, end: Optional[int] = None) -> 'HList':
        """获取切片"""
        # 处理负索引
        length = len(self.value)
        
        if start is None:
            start = 0
        elif start < 0:
            start = max(0, length + start)
        
        if end is None:
            end = length
        elif end < 0:
            end = max(0, length + end)
        
        # 确保范围有效
        start = max(0, min(start, length))
        end = max(0, min(end, length))
        
        return HList(self.value[start:end])
    
    def append(self, element: HValue) -> 'HList':
        """添加元素（返回新列表）"""
        new_list = self.copy()
        new_list.value.append(element)
        return new_list
    
    def remove_at(self, index: int) -> 'HList':
        """移除指定索引元素（返回新列表）"""
        if index < 0:
            index = len(self.value) + index
        
        if index < 0 or index >= len(self.value):
            raise HRuntimeError(f"List index out of range: {index}")
        
        new_list = self.copy()
        del new_list.value[index]
        return new_list
    
    def contains(self, element: HValue) -> bool:
        """检查是否包含元素"""
        for elem in self.value:
            if elem == element:
                return True
        return False
    
    def index_of(self, element: HValue) -> int:
        """查找元素索引"""
        for i, elem in enumerate(self.value):
            if elem == element:
                return i
        return -1
    
    def sort(self, descending: bool = False) -> 'HList':
        """排序列表"""
        # 需要所有元素可比较
        try:
            sorted_list = sorted(self.value, key=lambda x: x.value, reverse=descending)
            return HList(sorted_list)
        except TypeError:
            raise HRuntimeError("Cannot sort list with mixed types")
    
    def reverse(self) -> 'HList':
        """反转列表"""
        return HList(list(reversed(self.value)))
    
    def join(self, separator: HString) -> HString:
        """合并为字符串"""
        str_list = [elem.to_string() for elem in self.value]
        return HString(separator.value.join(str_list))


class HNull(HValue):
    """
    H语言空值类型
    例如: null
    """
    
    def __init__(self):
        super().__init__(None)
    
    def type_name(self) -> str:
        return "null"
    
    def to_string(self) -> str:
        return "null"
    
    def copy(self) -> 'HNull':
        return HNull()
    
    def is_truthy(self) -> bool:
        return False


class HRuntimeError(Exception):
    """H语言运行时错误"""
    pass


# ==================== 类型转换函数 ====================

def from_python(value: Any) -> HValue:
    """
    将Python值转换为HValue
    """
    if value is None:
        return HNull()
    elif isinstance(value, bool):
        return HBoolean(value)
    elif isinstance(value, (int, float)):
        return HNumber(float(value))
    elif isinstance(value, str):
        return HString(value)
    elif isinstance(value, (list, tuple)):
        return HList([from_python(elem) for elem in value])
    elif isinstance(value, HValue):
        return value
    else:
        raise HRuntimeError(f"Cannot convert Python type {type(value)} to HValue")


def to_python(value: HValue) -> Any:
    """
    将HValue转换为Python值
    """
    if isinstance(value, HNull):
        return None
    elif isinstance(value, HBoolean):
        return value.value
    elif isinstance(value, HNumber):
        return value.value
    elif isinstance(value, HString):
        return value.value
    elif isinstance(value, HList):
        return [to_python(elem) for elem in value.value]
    else:
        return value.value


def to_string(value: HValue) -> HString:
    """转换为字符串"""
    return HString(value.to_string())


def to_number(value: HValue) -> HNumber:
    """转换为数字"""
    if isinstance(value, HNumber):
        return value
    
    if isinstance(value, HString):
        try:
            return HNumber(float(value.value))
        except ValueError:
            raise HRuntimeError(f"Cannot convert '{value.value}' to number")
    
    if isinstance(value, HBoolean):
        return HNumber(1.0 if value.value else 0.0)
    
    if isinstance(value, HNull):
        return HNumber(0.0)
    
    raise HRuntimeError(f"Cannot convert {value.type_name()} to number")


def to_boolean(value: HValue) -> HBoolean:
    """转换为布尔值"""
    return HBoolean(value.is_truthy())


def to_list(value: HValue) -> HList:
    """转换为列表"""
    if isinstance(value, HList):
        return value
    
    if isinstance(value, HString):
        # 字符串转为字符列表
        return HList([HString(c) for c in value.value])
    
    # 其他类型转为单元素列表
    return HList([value])


# 测试代码
if __name__ == "__main__":
    # 测试数字
    num1 = HNumber(42)
    num2 = HNumber(3.14)
    print(f"Number: {num1}, {num2}")
    print(f"Add: {num1 + num2}")
    print(f"Is integer: {num1.is_integer()}")
    
    # 测试字符串
    str1 = HString("hello")
    str2 = HString("world")
    print(f"\\nString: {str1 + HString(' ') + str2}")
    print(f"Substring: {str1.substring(1, 3)}")
    print(f"Contains 'ell': {str1.contains(HString('ell'))}")
    
    # 测试列表
    lst = HList([HNumber(1), HNumber(2), HNumber(3)])
    print(f"\\nList: {lst}")
    print(f"Element [0]: {lst.get_element(0)}")
    print(f"Element [-1]: {lst.get_element(-1)}")
    print(f"Slice [1:3]: {lst.get_slice(1, 3)}")
    print(f"Appended: {lst.append(HNumber(4))}")
    
    # 测试布尔值
    bool1 = HBoolean(True)
    bool2 = HBoolean(False)
    print(f"\\nBoolean: {bool1}, {bool2}")
    print(f"AND: {bool1.__and__(bool2)}")
    print(f"Is truthy: {bool1.is_truthy()}")
    
    # 测试null
    null_val = HNull()
    print(f"\\nNull: {null_val}")
    print(f"Is truthy: {null_val.is_truthy()}")
    
    # 测试类型转换
    print(f"\\nType conversions:")
    print(f"to_number('42'): {to_number(HString('42'))}")
    print(f"to_boolean(0): {to_boolean(HNumber(0))}")
    print(f"to_list('abc'): {to_list(HString('abc'))}")
