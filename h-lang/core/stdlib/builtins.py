"""
H-Language Built-in Functions
H语言内置函数库
"""

import random
import math
from typing import Callable, Dict, List, Any
from ..types.primitive import *
from ..types.operations import Operations


class Builtins:
    """
    内置函数注册表
    所有内置函数都注册在这里
    """
    
    def __init__(self):
        self.functions: Dict[str, Callable] = {}
        self._register_all()
    
    def _register_all(self):
        """注册所有内置函数"""
        # 通用函数
        self._register_general()
        
        # 字符串函数
        self._register_string()
        
        # 列表函数
        self._register_list()
        
        # 数学函数
        self._register_math()
        
        # 类型转换函数
        self._register_type_conversion()
    
    def _register_general(self):
        """注册通用函数"""
        
        def h_len(value: HValue) -> HNumber:
            """
            len(value) - 返回长度
            支持: 字符串、列表
            """
            if isinstance(value, HString):
                return HNumber(len(value.value))
            elif isinstance(value, HList):
                return HNumber(len(value.value))
            else:
                raise HRuntimeError(f"len() requires string or list, got {value.type_name()}")
        
        def h_type(value: HValue) -> HString:
            """
            type(value) - 返回类型名称
            """
            return HString(value.type_name())
        
        def h_random() -> HNumber:
            """
            random() - 返回0-1之间的随机数
            """
            return HNumber(random.random())
        
        def h_randomInt(min_val: HNumber, max_val: HNumber) -> HNumber:
            """
            randomInt(min, max) - 返回指定范围的随机整数
            """
            if not isinstance(min_val, HNumber) or not isinstance(max_val, HNumber):
                raise HRuntimeError("randomInt() requires number arguments")
            
            min_int = int(min_val.value)
            max_int = int(max_val.value)
            
            return HNumber(random.randint(min_int, max_int))
        
        def h_range(start: HNumber, end: HNumber, step: HNumber = None) -> HList:
            """
            range(start, end, [step]) - 生成数字序列
            """
            if not isinstance(start, HNumber) or not isinstance(end, HNumber):
                raise HRuntimeError("range() requires number arguments")
            
            start_int = int(start.value)
            end_int = int(end.value)
            
            if step is None:
                step_int = 1 if start_int < end_int else -1
            else:
                if not isinstance(step, HNumber):
                    raise HRuntimeError("range() step must be a number")
                step_int = int(step.value)
            
            # 生成序列
            result = []
            current = start_int
            
            if step_int > 0:
                while current < end_int:
                    result.append(HNumber(current))
                    current += step_int
            elif step_int < 0:
                while current > end_int:
                    result.append(HNumber(current))
                    current += step_int
            
            return HList(result)
        
        self.functions['len'] = h_len
        self.functions['type'] = h_type
        self.functions['random'] = h_random
        self.functions['randomInt'] = h_randomInt
        self.functions['range'] = h_range
    
    def _register_string(self):
        """注册字符串函数"""
        
        def h_substring(s: HString, start: HNumber, length: HNumber = None) -> HString:
            """
            substring(string, start, [length]) - 提取子字符串
            """
            if not isinstance(s, HString):
                raise HRuntimeError("substring() requires string as first argument")
            if not isinstance(start, HNumber):
                raise HRuntimeError("substring() start must be a number")
            
            start_idx = int(start.value)
            len_val = None
            if length is not None:
                if not isinstance(length, HNumber):
                    raise HRuntimeError("substring() length must be a number")
                len_val = int(length.value)
            
            return s.substring(start_idx, len_val)
        
        def h_split(s: HString, separator: HString) -> HList:
            """
            split(string, separator) - 分割字符串
            """
            if not isinstance(s, HString):
                raise HRuntimeError("split() requires string as first argument")
            if not isinstance(separator, HString):
                raise HRuntimeError("split() separator must be a string")
            
            return s.split(separator)
        
        def h_trim(s: HString) -> HString:
            """
            trim(string) - 去除首尾空白
            """
            if not isinstance(s, HString):
                raise HRuntimeError("trim() requires string argument")
            
            return s.trim()
        
        def h_upper(s: HString) -> HString:
            """
            upper(string) - 转为大写
            """
            if not isinstance(s, HString):
                raise HRuntimeError("upper() requires string argument")
            
            return s.upper()
        
        def h_lower(s: HString) -> HString:
            """
            lower(string) - 转为小写
            """
            if not isinstance(s, HString):
                raise HRuntimeError("lower() requires string argument")
            
            return s.lower()
        
        def h_contains(s: HString, substring: HString) -> HBoolean:
            """
            contains(string, substring) - 检查包含关系
            """
            if not isinstance(s, HString) or not isinstance(substring, HString):
                raise HRuntimeError("contains() requires string arguments")
            
            return HBoolean(s.contains(substring))
        
        def h_startsWith(s: HString, prefix: HString) -> HBoolean:
            """
            startsWith(string, prefix) - 检查前缀
            """
            if not isinstance(s, HString) or not isinstance(prefix, HString):
                raise HRuntimeError("startsWith() requires string arguments")
            
            return HBoolean(s.starts_with(prefix))
        
        def h_endsWith(s: HString, suffix: HString) -> HBoolean:
            """
            endsWith(string, suffix) - 检查后缀
            """
            if not isinstance(s, HString) or not isinstance(suffix, HString):
                raise HRuntimeError("endsWith() requires string arguments")
            
            return HBoolean(s.ends_with(suffix))
        
        def h_replace(s: HString, old: HString, new: HString) -> HString:
            """
            replace(string, old, new) - 替换子串
            """
            if not isinstance(s, HString) or not isinstance(old, HString) or not isinstance(new, HString):
                raise HRuntimeError("replace() requires string arguments")
            
            return s.replace(old, new)
        
        self.functions['substring'] = h_substring
        self.functions['split'] = h_split
        self.functions['trim'] = h_trim
        self.functions['upper'] = h_upper
        self.functions['lower'] = h_lower
        self.functions['contains'] = h_contains
        self.functions['startsWith'] = h_startsWith
        self.functions['endsWith'] = h_endsWith
        self.functions['replace'] = h_replace
    
    def _register_list(self):
        """注册列表函数"""
        
        def h_sort(lst: HList, descending: HBoolean = None) -> HList:
            """
            sort(list, [descending]) - 排序列表
            """
            if not isinstance(lst, HList):
                raise HRuntimeError("sort() requires list argument")
            
            desc = False
            if descending is not None:
                if not isinstance(descending, HBoolean):
                    raise HRuntimeError("sort() descending must be a boolean")
                desc = descending.value
            
            return lst.sort(desc)
        
        def h_reverse(lst: HList) -> HList:
            """
            reverse(list) - 反转列表
            """
            if not isinstance(lst, HList):
                raise HRuntimeError("reverse() requires list argument")
            
            return lst.reverse()
        
        def h_join(lst: HList, separator: HString) -> HString:
            """
            join(list, separator) - 合并为字符串
            """
            if not isinstance(lst, HList):
                raise HRuntimeError("join() requires list as first argument")
            if not isinstance(separator, HString):
                raise HRuntimeError("join() separator must be a string")
            
            return lst.join(separator)
        
        def h_indexOf(lst: HList, element: HValue) -> HNumber:
            """
            indexOf(list, element) - 查找元素索引
            """
            if not isinstance(lst, HList):
                raise HRuntimeError("indexOf() requires list as first argument")
            
            index = lst.index_of(element)
            return HNumber(index)
        
        def h_append(lst: HList, element: HValue) -> HList:
            """
            append(list, element) - 添加元素（返回新列表）
            """
            if not isinstance(lst, HList):
                raise HRuntimeError("append() requires list as first argument")
            
            return lst.append(element)
        
        def h_removeAt(lst: HList, index: HNumber) -> HList:
            """
            removeAt(list, index) - 移除指定索引元素
            """
            if not isinstance(lst, HList):
                raise HRuntimeError("removeAt() requires list as first argument")
            if not isinstance(index, HNumber):
                raise HRuntimeError("removeAt() index must be a number")
            
            return lst.remove_at(int(index.value))
        
        self.functions['sort'] = h_sort
        self.functions['reverse'] = h_reverse
        self.functions['join'] = h_join
        self.functions['indexOf'] = h_indexOf
        self.functions['append'] = h_append
        self.functions['removeAt'] = h_removeAt
    
    def _register_math(self):
        """注册数学函数"""
        
        def h_abs(n: HNumber) -> HNumber:
            """
            abs(number) - 绝对值
            """
            if not isinstance(n, HNumber):
                raise HRuntimeError("abs() requires number argument")
            
            return HNumber(abs(n.value))
        
        def h_floor(n: HNumber) -> HNumber:
            """
            floor(number) - 向下取整
            """
            if not isinstance(n, HNumber):
                raise HRuntimeError("floor() requires number argument")
            
            return HNumber(math.floor(n.value))
        
        def h_ceil(n: HNumber) -> HNumber:
            """
            ceil(number) - 向上取整
            """
            if not isinstance(n, HNumber):
                raise HRuntimeError("ceil() requires number argument")
            
            return HNumber(math.ceil(n.value))
        
        def h_round(n: HNumber, precision: HNumber = None) -> HNumber:
            """
            round(number, [precision]) - 四舍五入
            """
            if not isinstance(n, HNumber):
                raise HRuntimeError("round() requires number as first argument")
            
            if precision is None:
                return HNumber(round(n.value))
            
            if not isinstance(precision, HNumber):
                raise HRuntimeError("round() precision must be a number")
            
            prec = int(precision.value)
            factor = 10 ** prec
            return HNumber(round(n.value * factor) / factor)
        
        def h_max(*args: HNumber) -> HNumber:
            """
            max(value1, value2, ...) - 最大值
            """
            if not args:
                raise HRuntimeError("max() requires at least one argument")
            
            values = []
            for arg in args:
                if not isinstance(arg, HNumber):
                    raise HRuntimeError("max() requires number arguments")
                values.append(arg.value)
            
            return HNumber(max(values))
        
        def h_min(*args: HNumber) -> HNumber:
            """
            min(value1, value2, ...) - 最小值
            """
            if not args:
                raise HRuntimeError("min() requires at least one argument")
            
            values = []
            for arg in args:
                if not isinstance(arg, HNumber):
                    raise HRuntimeError("min() requires number arguments")
                values.append(arg.value)
            
            return HNumber(min(values))
        
        def h_sqrt(n: HNumber) -> HNumber:
            """
            sqrt(number) - 平方根
            """
            if not isinstance(n, HNumber):
                raise HRuntimeError("sqrt() requires number argument")
            
            if n.value < 0:
                raise HRuntimeError("sqrt() cannot calculate square root of negative number")
            
            return HNumber(math.sqrt(n.value))
        
        def h_pow(base: HNumber, exponent: HNumber) -> HNumber:
            """
            pow(base, exponent) - 幂运算
            """
            if not isinstance(base, HNumber) or not isinstance(exponent, HNumber):
                raise HRuntimeError("pow() requires number arguments")
            
            return HNumber(base.value ** exponent.value)
        
        self.functions['abs'] = h_abs
        self.functions['floor'] = h_floor
        self.functions['ceil'] = h_ceil
        self.functions['round'] = h_round
        self.functions['max'] = h_max
        self.functions['min'] = h_min
        self.functions['sqrt'] = h_sqrt
        self.functions['pow'] = h_pow
    
    def _register_type_conversion(self):
        """注册类型转换函数"""
        
        def h_toString(value: HValue) -> HString:
            """
            toString(value) - 转为字符串
            """
            return HString(value.to_string())
        
        def h_toNumber(value: HValue) -> HNumber:
            """
            toNumber(value) - 转为数字
            """
            return to_number(value)
        
        def h_toBoolean(value: HValue) -> HBoolean:
            """
            toBoolean(value) - 转为布尔值
            """
            return to_boolean(value)
        
        def h_toList(value: HValue) -> HList:
            """
            toList(value) - 转为列表
            """
            return to_list(value)
        
        self.functions['toString'] = h_toString
        self.functions['toNumber'] = h_toNumber
        self.functions['toBoolean'] = h_toBoolean
        self.functions['toList'] = h_toList
    
    def get(self, name: str) -> Callable:
        """
        获取内置函数
        """
        if name not in self.functions:
            raise HRuntimeError(f"Unknown built-in function: {name}")
        
        return self.functions[name]
    
    def has(self, name: str) -> bool:
        """
        检查是否存在内置函数
        """
        return name in self.functions
    
    def get_all_names(self) -> List[str]:
        """
        获取所有内置函数名称
        """
        return list(self.functions.keys())
    
    def register_to_evaluator(self, evaluator):
        """
        将所有内置函数注册到求值器
        """
        for name, func in self.functions.items():
            evaluator.set_builtin(name, func)


# 便捷函数：获取所有内置函数
def get_builtins() -> Builtins:
    """
    获取内置函数注册表实例
    """
    return Builtins()


# 测试代码
if __name__ == "__main__":
    builtins = Builtins()
    
    print("内置函数列表:")
    for name in sorted(builtins.get_all_names()):
        print(f"  - {name}")
    
    print("\n测试一些函数:")
    
    # 测试通用函数
    test_list = HList([HNumber(3), HNumber(1), HNumber(2)])
    print(f"len([3, 1, 2]) = {builtins.get('len')(test_list)}")
    print(f"sort([3, 1, 2]) = {builtins.get('sort')(test_list)}")
    
    # 测试字符串函数
    test_str = HString("hello world")
    print(f"upper('hello world') = {builtins.get('upper')(test_str)}")
    print(f"contains('hello world', 'world') = {builtins.get('contains')(test_str, HString('world'))}")
    
    # 测试数学函数
    test_num = HNumber(3.7)
    print(f"floor(3.7) = {builtins.get('floor')(test_num)}")
    print(f"round(3.7) = {builtins.get('round')(test_num)}")
    
    # 测试类型转换
    print(f"toString(42) = {builtins.get('toString')(HNumber(42))}")
    print(f"toNumber('3.14') = {builtins.get('toNumber')(HString('3.14'))}")
