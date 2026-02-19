"""
AST Statements
抽象语法树 - 语句节点定义
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
from .expressions import Expression


class Statement(ABC):
    """
    语句基类
    所有语句节点都继承此类
    """
    
    @abstractmethod
    def accept(self, visitor):
        """接受访问者"""
        pass


# ==================== 表达式语句 ====================

@dataclass
class ExpressionStatement(Statement):
    """
    表达式语句
    例如: greet("Alice"), player.health + 10
    """
    expression: Expression
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)
    
    def __repr__(self):
        return f"ExpressionStatement({self.expression})"


# ==================== 赋值语句 ====================

@dataclass
class Assignment(Statement):
    """
    赋值语句
    例如: set health to 100, set $score to 0, set player.health to 50
    """
    target: Expression  # 赋值目标（Identifier, GlobalVariable, PropertyAccess, ListIndex）
    value: Expression   # 赋值值
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)
    
    def __repr__(self):
        return f"Assignment({self.target} = {self.value})"


# ==================== 条件语句 ====================

@dataclass
class IfStatement(Statement):
    """
    条件语句
    例如:
    if condition:
        statements
    else if other_condition:
        statements
    else:
        statements
    """
    condition: Expression
    then_branch: List[Statement] = field(default_factory=list)
    elif_branches: List[tuple] = field(default_factory=list)  # [(condition, statements), ...]
    else_branch: Optional[List[Statement]] = None
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)
    
    def __repr__(self):
        result = f"IfStatement({self.condition})"
        if self.elif_branches:
            result += f" elif={len(self.elif_branches)}"
        if self.else_branch:
            result += " else"
        return result


# ==================== 循环语句 ====================

@dataclass
class WhileStatement(Statement):
    """
    while循环语句
    例如:
    while enemy.health is greater than 0:
        perform attack
        echo "Attacking..."
    """
    condition: Expression
    body: List[Statement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)
    
    def __repr__(self):
        return f"WhileStatement({self.condition}, body={len(self.body)} stmts)"


# ==================== 函数定义 ====================

@dataclass
class FunctionDefinition(Statement):
    """
    函数定义语句
    例如:
    function greet(name):
        echo "Hello, " + name
    
    function sum(a, b):
        return a + b
    """
    name: str
    parameters: List[str] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_function_definition(self)
    
    def __repr__(self):
        params = ", ".join(self.parameters)
        return f"FunctionDefinition({self.name}({params}), body={len(self.body)} stmts)"


# ==================== 返回语句 ====================

@dataclass
class ReturnStatement(Statement):
    """
    返回语句
    例如: return result, return (无返回值)
    """
    value: Optional[Expression] = None
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)
    
    def __repr__(self):
        if self.value:
            return f"ReturnStatement({self.value})"
        return "ReturnStatement()"


# ==================== 输入语句 ====================

@dataclass
class AskStatement(Statement):
    """
    输入语句
    例如:
    ask "What is your name?"
    ask "How many items?" as itemCount
    """
    prompt: Optional[Expression] = None  # 提示文本（可选）
    variable: Optional[str] = None       # 存储输入的变量名（可选）
    
    def accept(self, visitor):
        return visitor.visit_ask_statement(self)
    
    def __repr__(self):
        if self.variable:
            return f"AskStatement({self.prompt!r} as {self.variable})"
        return f"AskStatement({self.prompt!r})"


# ==================== 输出语句 ====================

@dataclass
class EchoStatement(Statement):
    """
    输出语句
    例如: echo "Hello, World!"
    """
    expression: Expression
    
    def accept(self, visitor):
        return visitor.visit_echo_statement(self)
    
    def __repr__(self):
        return f"EchoStatement({self.expression})"


# ==================== 增减语句 ====================

@dataclass
class IncreaseStatement(Statement):
    """
    增加语句
    例如: increase $counter by 1, increase player.health by 10
    """
    target: Expression  # 增加目标
    amount: Expression  # 增加量
    
    def accept(self, visitor):
        return visitor.visit_increase_statement(self)
    
    def __repr__(self):
        return f"IncreaseStatement({self.target} += {self.amount})"


@dataclass
class DecreaseStatement(Statement):
    """
    减少语句
    例如: decrease $counter by 1, decrease enemy.health by damage
    """
    target: Expression  # 减少目标
    amount: Expression  # 减少量
    
    def accept(self, visitor):
        return visitor.visit_decrease_statement(self)
    
    def __repr__(self):
        return f"DecreaseStatement({self.target} -= {self.amount})"


# ==================== 列表操作语句 ====================

@dataclass
class AddStatement(Statement):
    """
    添加元素语句
    例如: add item to inventory
    """
    item: Expression      # 要添加的元素
    target: Expression    # 目标列表
    
    def accept(self, visitor):
        return visitor.visit_add_statement(self)
    
    def __repr__(self):
        return f"AddStatement(add {self.item} to {self.target})"


@dataclass
class RemoveStatement(Statement):
    """
    移除元素语句
    例如: remove item from inventory
    """
    item: Expression      # 要移除的元素
    target: Expression    # 目标列表
    
    def accept(self, visitor):
        return visitor.visit_remove_statement(self)
    
    def __repr__(self):
        return f"RemoveStatement(remove {self.item} from {self.target})"


# ==================== 程序根节点 ====================

@dataclass
class Program(Statement):
    """
    程序根节点
    包含所有顶层语句和函数定义
    """
    statements: List[Statement] = field(default_factory=list)
    functions: dict = field(default_factory=dict)  # 函数名 -> FunctionDefinition
    
    def accept(self, visitor):
        return visitor.visit_program(self)
    
    def __repr__(self):
        return f"Program(statements={len(self.statements)}, functions={len(self.functions)})"


# ==================== 语句访问者基类 ====================

class StatementVisitor(ABC):
    """
    语句访问者基类
    用于实现语句执行、打印等操作
    """
    
    @abstractmethod
    def visit_expression_statement(self, stmt: ExpressionStatement):
        pass
    
    @abstractmethod
    def visit_assignment(self, stmt: Assignment):
        pass
    
    @abstractmethod
    def visit_if_statement(self, stmt: IfStatement):
        pass
    
    @abstractmethod
    def visit_while_statement(self, stmt: WhileStatement):
        pass
    
    @abstractmethod
    def visit_function_definition(self, stmt: FunctionDefinition):
        pass
    
    @abstractmethod
    def visit_return_statement(self, stmt: ReturnStatement):
        pass
    
    @abstractmethod
    def visit_ask_statement(self, stmt: AskStatement):
        pass
    
    @abstractmethod
    def visit_echo_statement(self, stmt: EchoStatement):
        pass
    
    @abstractmethod
    def visit_increase_statement(self, stmt: IncreaseStatement):
        pass
    
    @abstractmethod
    def visit_decrease_statement(self, stmt: DecreaseStatement):
        pass
    
    @abstractmethod
    def visit_add_statement(self, stmt: AddStatement):
        pass
    
    @abstractmethod
    def visit_remove_statement(self, stmt: RemoveStatement):
        pass
    
    @abstractmethod
    def visit_program(self, stmt: Program):
        pass


# ==================== AST 打印器（用于调试） ====================

class StatementPrinter(StatementVisitor):
    """
    语句 AST 打印器
    用于打印语句的树形结构
    """
    
    def __init__(self):
        self.indent = 0
    
    def _print(self, text: str):
        print("  " * self.indent + text)
    
    def _print_statements(self, statements: List[Statement]):
        self.indent += 1
        for stmt in statements:
            stmt.accept(self)
        self.indent -= 1
    
    def visit_expression_statement(self, stmt: ExpressionStatement):
        self._print(f"ExpressionStatement:")
        self.indent += 1
        self._print(f"{stmt.expression}")
        self.indent -= 1
    
    def visit_assignment(self, stmt: Assignment):
        self._print(f"Assignment:")
        self.indent += 1
        self._print(f"Target: {stmt.target}")
        self._print(f"Value: {stmt.value}")
        self.indent -= 1
    
    def visit_if_statement(self, stmt: IfStatement):
        self._print(f"IfStatement:")
        self.indent += 1
        self._print(f"Condition: {stmt.condition}")
        self._print("Then:")
        self._print_statements(stmt.then_branch)
        
        for condition, branch in stmt.elif_branches:
            self._print(f"Elif ({condition}):")
            self._print_statements(branch)
        
        if stmt.else_branch:
            self._print("Else:")
            self._print_statements(stmt.else_branch)
        self.indent -= 1
    
    def visit_while_statement(self, stmt: WhileStatement):
        self._print(f"WhileStatement:")
        self.indent += 1
        self._print(f"Condition: {stmt.condition}")
        self._print("Body:")
        self._print_statements(stmt.body)
        self.indent -= 1
    
    def visit_function_definition(self, stmt: FunctionDefinition):
        self._print(f"FunctionDefinition: {stmt.name}({', '.join(stmt.parameters)})")
        self.indent += 1
        self._print("Body:")
        self._print_statements(stmt.body)
        self.indent -= 1
    
    def visit_return_statement(self, stmt: ReturnStatement):
        if stmt.value:
            self._print(f"ReturnStatement: {stmt.value}")
        else:
            self._print("ReturnStatement")
    
    def visit_ask_statement(self, stmt: AskStatement):
        if stmt.variable:
            self._print(f"AskStatement: {stmt.prompt!r} as {stmt.variable}")
        else:
            self._print(f"AskStatement: {stmt.prompt!r}")
    
    def visit_echo_statement(self, stmt: EchoStatement):
        self._print(f"EchoStatement: {stmt.expression}")
    
    def visit_increase_statement(self, stmt: IncreaseStatement):
        self._print(f"IncreaseStatement: {stmt.target} += {stmt.amount}")
    
    def visit_decrease_statement(self, stmt: DecreaseStatement):
        self._print(f"DecreaseStatement: {stmt.target} -= {stmt.amount}")
    
    def visit_add_statement(self, stmt: AddStatement):
        self._print(f"AddStatement: add {stmt.item} to {stmt.target}")
    
    def visit_remove_statement(self, stmt: RemoveStatement):
        self._print(f"RemoveStatement: remove {stmt.item} from {stmt.target}")
    
    def visit_program(self, stmt: Program):
        self._print(f"Program:")
        self.indent += 1
        self._print(f"Functions: {list(stmt.functions.keys())}")
        self._print("Statements:")
        self._print_statements(stmt.statements)
        self.indent -= 1


# 测试代码
if __name__ == "__main__":
    from .expressions import Literal, Identifier, Comparison, BinaryOperation
    
    # 构建一个示例程序 AST
    program = Program()
    
    # set $counter to 0
    program.statements.append(Assignment(
        target=GlobalVariable("counter"),
        value=Literal(0)
    ))
    
    # if $counter is less than 10:
    #     echo "Counter is low"
    program.statements.append(IfStatement(
        condition=Comparison(
            left=GlobalVariable("counter"),
            operator="is less than",
            right=Literal(10)
        ),
        then_branch=[
            EchoStatement(Literal("Counter is low"))
        ]
    ))
    
    # function greet(name):
    #     echo "Hello, " + name
    greet_func = FunctionDefinition(
        name="greet",
        parameters=["name"],
        body=[
            EchoStatement(BinaryOperation(
                left=Literal("Hello, "),
                operator="+",
                right=Identifier("name")
            ))
        ]
    )
    program.functions["greet"] = greet_func
    program.statements.append(greet_func)
    
    print("程序 AST 结构:")
    printer = StatementPrinter()
    program.accept(printer)
