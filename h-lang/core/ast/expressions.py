"""
AST Expressions
抽象语法树 - 表达式节点定义
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Any


class Expression(ABC):
    """
    表达式基类
    所有表达式节点都继承此类
    """
    
    @abstractmethod
    def accept(self, visitor):
        """接受访问者"""
        pass


# ==================== 字面量 ====================

@dataclass
class Literal(Expression):
    """
    字面量表达式
    例如: 42, "hello", true, null, [1, 2, 3]
    """
    value: Any  # 可以是 number, string, boolean, null, list
    
    def accept(self, visitor):
        return visitor.visit_literal(self)
    
    def __repr__(self):
        return f"Literal({self.value!r})"


# ==================== 标识符和变量 ====================

@dataclass
class Identifier(Expression):
    """
    标识符表达式（变量引用）
    例如: player, itemCount
    """
    name: str
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)
    
    def __repr__(self):
        return f"Identifier({self.name})"


@dataclass
class GlobalVariable(Expression):
    """
    全局变量表达式
    例如: $score, $gameTime
    """
    name: str  # 不包含 $ 前缀
    
    def accept(self, visitor):
        return visitor.visit_global_variable(self)
    
    def __repr__(self):
        return f"GlobalVariable(${self.name})"


# ==================== 属性访问 ====================

@dataclass
class PropertyAccess(Expression):
    """
    属性访问表达式
    例如: player.health, room.exits.north
    """
    object: Expression  # 被访问的对象
    property_name: str  # 属性名
    
    def accept(self, visitor):
        return visitor.visit_property_access(self)
    
    def __repr__(self):
        return f"PropertyAccess({self.object}, {self.property_name})"


# ==================== 二元运算 ====================

@dataclass
class BinaryOperation(Expression):
    """
    二元运算表达式
    例如: a + b, x * y, health - damage
    """
    left: Expression
    operator: str  # '+', '-', '*', '/', '%'
    right: Expression
    
    def accept(self, visitor):
        return visitor.visit_binary_operation(self)
    
    def __repr__(self):
        return f"BinaryOperation({self.left} {self.operator} {self.right})"


# ==================== 比较运算 ====================

@dataclass
class Comparison(Expression):
    """
    比较运算表达式
    例如: a is b, x > y, health is less than 50
    """
    left: Expression
    operator: str  # 'is', 'is not', 'is greater than', 'is less than', 
                   # 'is at least', 'is at most', '==', '!=', '<', '>', '<=', '>='
    right: Expression
    
    def accept(self, visitor):
        return visitor.visit_comparison(self)
    
    def __repr__(self):
        return f"Comparison({self.left} {self.operator} {self.right})"


# ==================== 逻辑运算 ====================

@dataclass
class LogicalOperation(Expression):
    """
    逻辑运算表达式
    例如: a and b, x or y, not z
    """
    left: Expression
    operator: str  # 'and', 'or'
    right: Expression
    
    def accept(self, visitor):
        return visitor.visit_logical_operation(self)
    
    def __repr__(self):
        return f"LogicalOperation({self.left} {self.operator} {self.right})"


@dataclass
class UnaryOperation(Expression):
    """
    一元运算表达式
    例如: -x, not condition
    """
    operator: str  # '-', 'not'
    operand: Expression
    
    def accept(self, visitor):
        return visitor.visit_unary_operation(self)
    
    def __repr__(self):
        return f"UnaryOperation({self.operator} {self.operand})"


# ==================== 成员检查 ====================

@dataclass
class MemberCheck(Expression):
    """
    成员检查表达式
    例如: player has sword, sword is in inventory
    """
    operator: str  # 'has', 'is in'
    left: Expression
    right: Expression
    
    def accept(self, visitor):
        return visitor.visit_member_check(self)
    
    def __repr__(self):
        return f"MemberCheck({self.left} {self.operator} {self.right})"


# ==================== 列表索引和切片 ====================

@dataclass
class ListIndex(Expression):
    """
    列表索引访问表达式
    例如: items[0], items[-1], matrix[1][2]
    """
    list_expr: Expression  # 列表表达式
    index: Expression      # 索引表达式
    
    def accept(self, visitor):
        return visitor.visit_list_index(self)
    
    def __repr__(self):
        return f"ListIndex({self.list_expr}[{self.index}])"


@dataclass
class ListSlice(Expression):
    """
    列表切片表达式
    例如: items[1:3], items[:2], items[2:], items[:]
    """
    list_expr: Expression
    start: Optional[Expression] = None  # 起始索引（可选）
    end: Optional[Expression] = None    # 结束索引（可选）
    
    def accept(self, visitor):
        return visitor.visit_list_slice(self)
    
    def __repr__(self):
        start_str = str(self.start) if self.start else ""
        end_str = str(self.end) if self.end else ""
        return f"ListSlice({self.list_expr}[{start_str}:{end_str}])"


# ==================== 函数调用 ====================

@dataclass
class FunctionCall(Expression):
    """
    函数调用表达式
    例如: greet("Alice"), sum(10, 20), len(items)
    """
    function_name: str      # 函数名
    arguments: List[Expression] = field(default_factory=list)  # 参数列表
    
    def accept(self, visitor):
        return visitor.visit_function_call(self)
    
    def __repr__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"FunctionCall({self.function_name}({args_str}))"


@dataclass
class MethodCall(Expression):
    """
    方法调用表达式（对象方法）
    例如: player.getName(), list.append(item)
    """
    object: Expression      # 对象表达式
    method_name: str        # 方法名
    arguments: List[Expression] = field(default_factory=list)  # 参数列表
    
    def accept(self, visitor):
        return visitor.visit_method_call(self)
    
    def __repr__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"MethodCall({self.object}.{self.method_name}({args_str}))"


# ==================== 列表字面量 ====================

@dataclass
class ListLiteral(Expression):
    """
    列表字面量表达式
    例如: [1, 2, 3], ["a", "b", "c"]
    """
    elements: List[Expression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_list_literal(self)
    
    def __repr__(self):
        elements_str = ", ".join(str(elem) for elem in self.elements)
        return f"ListLiteral([{elements_str}])"


# ==================== 括号表达式 ====================

@dataclass
class Grouping(Expression):
    """
    括号分组表达式
    例如: (a + b) * c
    """
    expression: Expression
    
    def accept(self, visitor):
        return visitor.visit_grouping(self)
    
    def __repr__(self):
        return f"Grouping({self.expression})"


# ==================== 表达式访问者基类 ====================

class ExpressionVisitor(ABC):
    """
    表达式访问者基类
    用于实现表达式求值、打印等操作
    """
    
    @abstractmethod
    def visit_literal(self, expr: Literal):
        pass
    
    @abstractmethod
    def visit_identifier(self, expr: Identifier):
        pass
    
    @abstractmethod
    def visit_global_variable(self, expr: GlobalVariable):
        pass
    
    @abstractmethod
    def visit_property_access(self, expr: PropertyAccess):
        pass
    
    @abstractmethod
    def visit_binary_operation(self, expr: BinaryOperation):
        pass
    
    @abstractmethod
    def visit_comparison(self, expr: Comparison):
        pass
    
    @abstractmethod
    def visit_logical_operation(self, expr: LogicalOperation):
        pass
    
    @abstractmethod
    def visit_unary_operation(self, expr: UnaryOperation):
        pass
    
    @abstractmethod
    def visit_member_check(self, expr: MemberCheck):
        pass
    
    @abstractmethod
    def visit_list_index(self, expr: ListIndex):
        pass
    
    @abstractmethod
    def visit_list_slice(self, expr: ListSlice):
        pass
    
    @abstractmethod
    def visit_function_call(self, expr: FunctionCall):
        pass
    
    @abstractmethod
    def visit_method_call(self, expr: MethodCall):
        pass
    
    @abstractmethod
    def visit_list_literal(self, expr: ListLiteral):
        pass
    
    @abstractmethod
    def visit_grouping(self, expr: Grouping):
        pass


# ==================== AST 打印器（用于调试） ====================

class ASTPrinter(ExpressionVisitor):
    """
    AST 打印器
    用于打印表达式的树形结构
    """
    
    def __init__(self):
        self.indent = 0
    
    def _print(self, text: str):
        print("  " * self.indent + text)
    
    def _visit_children(self, *children):
        self.indent += 1
        for child in children:
            if child:
                child.accept(self)
        self.indent -= 1
    
    def visit_literal(self, expr: Literal):
        self._print(f"Literal: {expr.value!r}")
    
    def visit_identifier(self, expr: Identifier):
        self._print(f"Identifier: {expr.name}")
    
    def visit_global_variable(self, expr: GlobalVariable):
        self._print(f"GlobalVariable: ${expr.name}")
    
    def visit_property_access(self, expr: PropertyAccess):
        self._print(f"PropertyAccess: .{expr.property_name}")
        self._visit_children(expr.object)
    
    def visit_binary_operation(self, expr: BinaryOperation):
        self._print(f"BinaryOperation: {expr.operator}")
        self._visit_children(expr.left, expr.right)
    
    def visit_comparison(self, expr: Comparison):
        self._print(f"Comparison: {expr.operator}")
        self._visit_children(expr.left, expr.right)
    
    def visit_logical_operation(self, expr: LogicalOperation):
        self._print(f"LogicalOperation: {expr.operator}")
        self._visit_children(expr.left, expr.right)
    
    def visit_unary_operation(self, expr: UnaryOperation):
        self._print(f"UnaryOperation: {expr.operator}")
        self._visit_children(expr.operand)
    
    def visit_member_check(self, expr: MemberCheck):
        self._print(f"MemberCheck: {expr.operator}")
        self._visit_children(expr.left, expr.right)
    
    def visit_list_index(self, expr: ListIndex):
        self._print(f"ListIndex")
        self._visit_children(expr.list_expr, expr.index)
    
    def visit_list_slice(self, expr: ListSlice):
        self._print(f"ListSlice")
        self._visit_children(expr.list_expr, expr.start, expr.end)
    
    def visit_function_call(self, expr: FunctionCall):
        self._print(f"FunctionCall: {expr.function_name}")
        self._visit_children(*expr.arguments)
    
    def visit_method_call(self, expr: MethodCall):
        self._print(f"MethodCall: .{expr.method_name}")
        self._visit_children(expr.object, *expr.arguments)
    
    def visit_list_literal(self, expr: ListLiteral):
        self._print(f"ListLiteral")
        self._visit_children(*expr.elements)
    
    def visit_grouping(self, expr: Grouping):
        self._print(f"Grouping")
        self._visit_children(expr.expression)


# 测试代码
if __name__ == "__main__":
    # 构建一个示例 AST: (player.health + 10) > 50 and player has sword
    ast = LogicalOperation(
        left=Comparison(
            left=BinaryOperation(
                left=PropertyAccess(
                    object=Identifier("player"),
                    property_name="health"
                ),
                operator="+",
                right=Literal(10)
            ),
            operator="is greater than",
            right=Literal(50)
        ),
        operator="and",
        right=MemberCheck(
            operator="has",
            left=Identifier("player"),
            right=Identifier("sword")
        )
    )
    
    print("AST 结构:")
    printer = ASTPrinter()
    ast.accept(printer)
