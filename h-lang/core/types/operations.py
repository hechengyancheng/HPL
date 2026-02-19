"""
H-Language Operations
H语言运算操作实现
"""

from typing import Any, Dict
from .primitive import *


class Operations:
    """
    H语言运算操作类
    实现所有类型的运算操作
    """
    
    # ==================== 算术运算 ====================
    
    @staticmethod
    def add(left: HValue, right: HValue) -> HValue:
        """
        加法运算: left + right
        支持: number + number, string + string, list + element
        """
        if isinstance(left, HNumber) and isinstance(right, HNumber):
            return left + right
        
        if isinstance(left, HString) and isinstance(right, HString):
            return left + right
        
        # 列表追加元素
        if isinstance(left, HList):
            return left.append(right)
        
        raise HRuntimeError(f"Cannot add {left.type_name()} and {right.type_name()}")
    
    @staticmethod
    def subtract(left: HValue, right: HValue) -> HValue:
        """
        减法运算: left - right
        支持: number - number
        """
        if isinstance(left, HNumber) and isinstance(right, HNumber):
            return left - right
        
        raise HRuntimeError(f"Cannot subtract {right.type_name()} from {left.type_name()}")
    
    @staticmethod
    def multiply(left: HValue, right: HValue) -> HValue:
        """
        乘法运算: left * right
        支持: number * number
        """
        if isinstance(left, HNumber) and isinstance(right, HNumber):
            return left * right
        
        raise HRuntimeError(f"Cannot multiply {left.type_name()} and {right.type_name()}")
    
    @staticmethod
    def divide(left: HValue, right: HValue) -> HValue:
        """
        除法运算: left / right
        支持: number / number
        """
        if isinstance(left, HNumber) and isinstance(right, HNumber):
            return left / right
        
        raise HRuntimeError(f"Cannot divide {left.type_name()} by {right.type_name()}")
    
    @staticmethod
    def modulo(left: HValue, right: HValue) -> HValue:
        """
        取模运算: left % right
        支持: number % number
        """
        if isinstance(left, HNumber) and isinstance(right, HNumber):
            return left % right
        
        raise HRuntimeError(f"Cannot modulo {left.type_name()} by {right.type_name()}")
    
    # ==================== 比较运算 ====================
    
    @staticmethod
    def equals(left: HValue, right: HValue) -> HBoolean:
        """
        等于比较: left is right, left == right
        """
        return HBoolean(left == right)
    
    @staticmethod
    def not_equals(left: HValue, right: HValue) -> HBoolean:
        """
        不等于比较: left is not right, left != right
        """
        return HBoolean(not (left == right))
    
    @staticmethod
    def greater_than(left: HValue, right: HValue) -> HBoolean:
        """
        大于比较: left is greater than right, left > right
        """
        if isinstance(left, HNumber) and isinstance(right, HNumber):
            return HBoolean(left > right)
        
        # 字符串比较
        if isinstance(left, HString) and isinstance(right, HString):
            return HBoolean(left.value > right.value)
        
        raise HRuntimeError(f"Cannot compare {left.type_name()} and {right.type_name()}")
    
    @staticmethod
    def less_than(left: HValue, right: HValue) -> HBoolean:
        """
        小于比较: left is less than right, left < right
        """
        if isinstance(left, HNumber) and isinstance(right, HNumber):
            return HBoolean(left < right)
        
        # 字符串比较
        if isinstance(left, HString) and isinstance(right, HString):
            return HBoolean(left.value < right.value)
        
        raise HRuntimeError(f"Cannot compare {left.type_name()} and {right.type_name()}")
    
    @staticmethod
    def greater_equal(left: HValue, right: HValue) -> HBoolean:
        """
        大于等于比较: left is at least right, left >= right
        """
        if isinstance(left, HNumber) and isinstance(right, HNumber):
            return HBoolean(left >= right)
        
        # 字符串比较
        if isinstance(left, HString) and isinstance(right, HString):
            return HBoolean(left.value >= right.value)
        
        raise HRuntimeError(f"Cannot compare {left.type_name()} and {right.type_name()}")
    
    @staticmethod
    def less_equal(left: HValue, right: HValue) -> HBoolean:
        """
        小于等于比较: left is at most right, left <= right
        """
        if isinstance(left, HNumber) and isinstance(right, HNumber):
            return HBoolean(left <= right)
        
        # 字符串比较
        if isinstance(left, HString) and isinstance(right, HString):
            return HBoolean(left.value <= right.value)
        
        raise HRuntimeError(f"Cannot compare {left.type_name()} and {right.type_name()}")
    
    # ==================== 逻辑运算 ====================
    
    @staticmethod
    def logical_and(left: HValue, right: HValue) -> HBoolean:
        """
        逻辑与: left and right
        """
        return HBoolean(left.is_truthy() and right.is_truthy())
    
    @staticmethod
    def logical_or(left: HValue, right: HValue) -> HBoolean:
        """
        逻辑或: left or right
        """
        return HBoolean(left.is_truthy() or right.is_truthy())
    
    @staticmethod
    def logical_not(operand: HValue) -> HBoolean:
        """
        逻辑非: not operand
        """
        return HBoolean(not operand.is_truthy())
    
    # ==================== 成员检查 ====================
    
    @staticmethod
    def has(obj: HValue, property_name: HString) -> HBoolean:
        """
        属性检查: obj has property_name
        对于列表，检查是否包含元素
        对于字符串，检查是否包含子串
        """
        # 列表包含检查
        if isinstance(obj, HList):
            # 查找元素
            for elem in obj.value:
                if isinstance(elem, HString) and elem.value == property_name.value:
                    return HBoolean(True)
                if str(elem.value) == property_name.value:
                    return HBoolean(True)
            return HBoolean(False)
        
        # 字符串包含检查
        if isinstance(obj, HString):
            return HBoolean(property_name.value in obj.value)
        
        # 对象属性检查（需要对象系统支持）
        # 暂时返回false
        return HBoolean(False)
    
    @staticmethod
    def is_in(element: HValue, container: HValue) -> HBoolean:
        """
        成员检查: element is in container
        """
        # 列表包含
        if isinstance(container, HList):
            return HBoolean(container.contains(element))
        
        # 字符串包含
        if isinstance(container, HString) and isinstance(element, HString):
            return HBoolean(element.value in container.value)
        
        raise HRuntimeError(f"Cannot check membership in {container.type_name()}")
    
    @staticmethod
    def contains(container: HValue, element: HValue) -> HBoolean:
        """
        包含检查: container contains element
        """
        return Operations.is_in(element, container)
    
    # ==================== 列表索引访问 ====================
    
    @staticmethod
    def list_index(lst: HList, index: HValue) -> HValue:
        """
        列表索引访问: lst[index]
        """
        if not isinstance(lst, HList):
            raise HRuntimeError(f"Cannot index {lst.type_name()}")
        
        if not isinstance(index, HNumber):
            raise HRuntimeError(f"List index must be a number, got {index.type_name()}")
        
        if not index.is_integer():
            raise HRuntimeError("List index must be an integer")
        
        return lst.get_element(index.to_int())
    
    @staticmethod
    def list_slice(lst: HList, start: Optional[HValue], end: Optional[HValue]) -> HList:
        """
        列表切片访问: lst[start:end]
        """
        if not isinstance(lst, HList):
            raise HRuntimeError(f"Cannot slice {lst.type_name()}")
        
        start_idx = None
        end_idx = None
        
        if start is not None:
            if not isinstance(start, HNumber):
                raise HRuntimeError(f"Slice start must be a number")
            if not start.is_integer():
                raise HRuntimeError("Slice start must be an integer")
            start_idx = start.to_int()
        
        if end is not None:
            if not isinstance(end, HNumber):
                raise HRuntimeError(f"Slice end must be a number")
            if not end.is_integer():
                raise HRuntimeError("Slice end must be an integer")
            end_idx = end.to_int()
        
        return lst.get_slice(start_idx, end_idx)
    
    @staticmethod
    def list_set(lst: HList, index: HValue, value: HValue):
        """
        列表索引赋值: lst[index] = value
        """
        if not isinstance(lst, HList):
            raise HRuntimeError(f"Cannot index assign to {lst.type_name()}")
        
        if not isinstance(index, HNumber):
            raise HRuntimeError(f"List index must be a number")
        
        if not index.is_integer():
            raise HRuntimeError("List index must be an integer")
        
        lst.set_element(index.to_int(), value)
    
    # ==================== 属性访问 ====================
    
    @staticmethod
    def get_property(obj: HValue, property_name: str) -> HValue:
        """
        获取对象属性: obj.property_name
        对于列表，支持 length 属性
        """
        # 列表特殊属性
        if isinstance(obj, HList):
            if property_name == "length":
                return HNumber(len(obj))
        
        # 字符串特殊属性
        if isinstance(obj, HString):
            if property_name == "length":
                return HNumber(len(obj))
        
        # 通用属性访问（需要对象系统支持）
        # 暂时抛出错误
        raise HRuntimeError(f"{obj.type_name()} has no property '{property_name}'")
    
    @staticmethod
    def set_property(obj: HValue, property_name: str, value: HValue):
        """
        设置对象属性: obj.property_name = value
        """
        # 通用属性设置（需要对象系统支持）
        raise HRuntimeError(f"Cannot set property on {obj.type_name()}")
    
    # ==================== 一元运算 ====================
    
    @staticmethod
    def negate(operand: HValue) -> HNumber:
        """
        取反运算: -operand
        """
        if not isinstance(operand, HNumber):
            raise HRuntimeError(f"Cannot negate {operand.type_name()}")
        
        return -operand


# 便捷函数映射
COMPARISON_OPERATORS = {
    "is": Operations.equals,
    "==": Operations.equals,
    "is not": Operations.not_equals,
    "!=": Operations.not_equals,
    "is greater than": Operations.greater_than,
    ">": Operations.greater_than,
    "is less than": Operations.less_than,
    "<": Operations.less_than,
    "is at least": Operations.greater_equal,
    ">=": Operations.greater_equal,
    "is at most": Operations.less_equal,
    "<=": Operations.less_equal,
}


# 测试代码
if __name__ == "__main__":
    ops = Operations()
    
    # 测试算术运算
    num1 = HNumber(10)
    num2 = HNumber(3)
    print(f"Add: {ops.add(num1, num2)}")
    print(f"Subtract: {ops.subtract(num1, num2)}")
    print(f"Multiply: {ops.multiply(num1, num2)}")
    print(f"Divide: {ops.divide(num1, num2)}")
    print(f"Modulo: {ops.modulo(num1, num2)}")
    
    # 测试比较运算
    print(f"\\nEquals: {ops.equals(num1, num2)}")
    print(f"Greater than: {ops.greater_than(num1, num2)}")
    print(f"Less than: {ops.less_than(num1, num2)}")
    
    # 测试逻辑运算
    bool1 = HBoolean(True)
    bool2 = HBoolean(False)
    print(f"\\nLogical AND: {ops.logical_and(bool1, bool2)}")
    print(f"Logical OR: {ops.logical_or(bool1, bool2)}")
    print(f"Logical NOT: {ops.logical_not(bool1)}")
    
    # 测试列表操作
    lst = HList([HNumber(1), HNumber(2), HNumber(3)])
    print(f"\\nList: {lst}")
    print(f"Index [0]: {ops.list_index(lst, HNumber(0))}")
    print(f"Index [-1]: {ops.list_index(lst, HNumber(-1))}")
    print(f"Slice [1:3]: {ops.list_slice(lst, HNumber(1), HNumber(3))}")
    print(f"Contains 2: {ops.contains(lst, HNumber(2))}")
    
    # 测试成员检查
    str_val = HString("hello")
    print(f"\\nString contains 'ell': {ops.contains(str_val, HString('ell'))}")
