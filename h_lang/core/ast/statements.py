"""
AST Statements
抽象语法树 - 语句节点定义
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
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
    source: Expression    # 来源列表
    
    def accept(self, visitor):
        return visitor.visit_remove_statement(self)
    
    def __repr__(self):
        return f"RemoveStatement(remove {self.item} from {self.source})"


# ==================== 标准库动作语句 ====================

@dataclass
class MoveStatement(Statement):
    """
    移动语句
    例如: move to Kitchen, move to $destination
    """
    location: Expression  # 目标位置
    
    def accept(self, visitor):
        return visitor.visit_move_statement(self)
    
    def __repr__(self):
        return f"MoveStatement(to {self.location})"


@dataclass
class WaitStatement(Statement):
    """
    等待语句
    例如: wait for 3 seconds, wait for 1 minutes
    """
    duration: Expression  # 持续时间
    unit: str = "seconds"  # 时间单位 (seconds/minutes)
    
    def accept(self, visitor):
        return visitor.visit_wait_statement(self)
    
    def __repr__(self):
        return f"WaitStatement({self.duration} {self.unit})"


@dataclass
class EndGameStatement(Statement):
    """
    结束游戏语句
    例如: end game
    """
    
    def accept(self, visitor):
        return visitor.visit_end_game_statement(self)
    
    def __repr__(self):
        return "EndGameStatement()"


@dataclass
class StartTimerStatement(Statement):
    """
    启动计时器语句
    例如: start timer bomb for 30 seconds
    """
    name: Expression      # 计时器名称
    duration: Expression  # 持续时间
    unit: str = "seconds" # 时间单位
    
    def accept(self, visitor):
        return visitor.visit_start_timer_statement(self)
    
    def __repr__(self):
        return f"StartTimerStatement({self.name} for {self.duration} {self.unit})"


@dataclass
class StopTimerStatement(Statement):
    """
    停止计时器语句
    例如: stop timer bomb
    """
    name: Expression  # 计时器名称
    
    def accept(self, visitor):
        return visitor.visit_stop_timer_statement(self)
    
    def __repr__(self):
        return f"StopTimerStatement({self.name})"


@dataclass
class PerformStatement(Statement):
    """
    执行动作语句
    例如: perform combat.attack with player, enemy
    """
    action: Expression    # 动作名称
    arguments: List[Expression] = field(default_factory=list)  # 动作参数
    
    def accept(self, visitor):
        return visitor.visit_perform_statement(self)
    
    def __repr__(self):
        args = ", ".join(str(arg) for arg in self.arguments)
        return f"PerformStatement({self.action} with {args})"


@dataclass
class ParallelStatement(Statement):
    """
    并行执行语句
    例如:
    run in parallel:
        echo "Task 1"
        wait for 1 seconds
    """
    body: List[Statement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_parallel_statement(self)
    
    def __repr__(self):
        return f"ParallelStatement(body={len(self.body)} stmts)"


# ==================== 测试框架语句 ====================

@dataclass
class TestStatement(Statement):
    """
    测试定义语句
    例如:
    test "combat system":
        // setup
        // action
        // assertions
    """
    name: str                    # 测试名称
    body: List[Statement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_test_statement(self)
    
    def __repr__(self):
        return f"TestStatement({self.name!r}, body={len(self.body)} stmts)"


@dataclass
class AssertStatement(Statement):
    """
    断言语句
    例如:
    assert condition
    assert not condition
    assert value is expected
    assert list contains item
    """
    condition: Expression
    operator: str  # "truthy", "not", "is", "contains"
    expected: Optional[Expression] = None  # 用于 is 和 contains
    message: Optional[str] = None  # 可选的错误消息
    
    def accept(self, visitor):
        return visitor.visit_assert_statement(self)
    
    def __repr__(self):
        if self.operator == "is":
            return f"AssertStatement({self.condition} is {self.expected})"
        elif self.operator == "contains":
            return f"AssertStatement({self.condition} contains {self.expected})"
        elif self.operator == "not":
            return f"AssertStatement(not {self.condition})"
        return f"AssertStatement({self.condition})"


# ==================== 游戏框架 - 类定义 ====================

@dataclass
class ClassDefinition(Statement):
    """
    类定义语句（Room, Item, Character等）
    例如:
    room Kitchen:
        description: "A cozy kitchen"
        
    item Sword extends Weapon:
        damage: 10
        
    character Goblin extends Enemy:
        health: 50
    """
    class_type: str  # "room", "item", "character"
    name: str
    extends: Optional[str] = None  # 父类名
    properties: Dict[str, Expression] = field(default_factory=dict)
    methods: Dict[str, 'FunctionDefinition'] = field(default_factory=dict)
    event_handlers: List['EventHandler'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_class_definition(self)
    
    def __repr__(self):
        extends_str = f" extends {self.extends}" if self.extends else ""
        return f"ClassDefinition({self.class_type} {self.name}{extends_str})"


@dataclass
class EventHandler(Statement):
    """
    事件处理器
    例如:
    on action: player uses item:
        // 处理代码
        
    on state: health is 0:
        // 处理代码
        
    on timer: bomb expires:
        // 处理代码
        
    on event: random_encounter:
        // 处理代码
    """
    event_type: str  # "action", "state", "timer", "event", "game_start", "every_turn"
    condition: Optional[Expression] = None  # 触发条件
    action: Optional[str] = None  # 动作名称（用于action类型）
    body: List[Statement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_event_handler(self)
    
    def __repr__(self):
        return f"EventHandler({self.event_type})"


@dataclass
class DialogStatement(Statement):
    """
    对话系统语句
    例如:
    dialog npc "Hello, adventurer!":
        option "Buy potion" -> buy_potion
        option "Leave" -> end_dialog
    """
    speaker: Expression
    text: Expression
    options: List[Tuple[str, str]] = field(default_factory=list)  # [(显示文本, 跳转目标), ...]
    
    def accept(self, visitor):
        return visitor.visit_dialog_statement(self)
    
    def __repr__(self):
        return f"DialogStatement({self.speaker}: {self.text})"


@dataclass
class ExitDefinition(Statement):
    """
    出口定义（带条件）
    例如:
    exit north to Garden
    exit east to Dungeon if has_key
    """
    direction: str
    target_room: str
    condition: Optional[Expression] = None  # 条件表达式
    
    def accept(self, visitor):
        return visitor.visit_exit_definition(self)
    
    def __repr__(self):
        if self.condition:
            return f"ExitDefinition({self.direction} to {self.target_room} if {self.condition})"
        return f"ExitDefinition({self.direction} to {self.target_room})"



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
    def visit_move_statement(self, stmt: MoveStatement):
        pass
    
    @abstractmethod
    def visit_wait_statement(self, stmt: WaitStatement):
        pass
    
    @abstractmethod
    def visit_end_game_statement(self, stmt: EndGameStatement):
        pass
    
    @abstractmethod
    def visit_start_timer_statement(self, stmt: StartTimerStatement):
        pass
    
    @abstractmethod
    def visit_stop_timer_statement(self, stmt: StopTimerStatement):
        pass
    
    @abstractmethod
    def visit_perform_statement(self, stmt: PerformStatement):
        pass
    
    @abstractmethod
    def visit_parallel_statement(self, stmt: ParallelStatement):
        pass
    
    @abstractmethod
    def visit_test_statement(self, stmt: TestStatement):
        pass
    
    @abstractmethod
    def visit_assert_statement(self, stmt: AssertStatement):
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
        self._print(f"RemoveStatement: remove {stmt.item} from {stmt.source}")
    
    def visit_move_statement(self, stmt: MoveStatement):
        self._print(f"MoveStatement: to {stmt.location}")
    
    def visit_wait_statement(self, stmt: WaitStatement):
        self._print(f"WaitStatement: {stmt.duration} {stmt.unit}")
    
    def visit_end_game_statement(self, stmt: EndGameStatement):
        self._print("EndGameStatement")
    
    def visit_start_timer_statement(self, stmt: StartTimerStatement):
        self._print(f"StartTimerStatement: {stmt.name} for {stmt.duration} {stmt.unit}")
    
    def visit_stop_timer_statement(self, stmt: StopTimerStatement):
        self._print(f"StopTimerStatement: {stmt.name}")
    
    def visit_perform_statement(self, stmt: PerformStatement):
        self._print(f"PerformStatement: {stmt.action}")
        if stmt.arguments:
            self.indent += 1
            for i, arg in enumerate(stmt.arguments):
                self._print(f"Arg {i}: {arg}")
            self.indent -= 1
    
    def visit_parallel_statement(self, stmt: ParallelStatement):
        self._print(f"ParallelStatement:")
        self._print_statements(stmt.body)
    
    def visit_test_statement(self, stmt: TestStatement):
        self._print(f"TestStatement: {stmt.name!r}")
        self._print_statements(stmt.body)
    
    def visit_assert_statement(self, stmt: AssertStatement):
        if stmt.operator == "is":
            self._print(f"AssertStatement: {stmt.condition} is {stmt.expected}")
        elif stmt.operator == "contains":
            self._print(f"AssertStatement: {stmt.condition} contains {stmt.expected}")
        elif stmt.operator == "not":
            self._print(f"AssertStatement: not {stmt.condition}")
        else:
            self._print(f"AssertStatement: {stmt.condition}")
    
    def visit_program(self, stmt: Program):
        self._print(f"Program:")
        self.indent += 1
        self._print(f"Functions: {list(stmt.functions.keys())}")
        self._print("Statements:")
        self._print_statements(stmt.statements)
        self.indent -= 1
