"""
H-Language Parser
语法分析器 - 将Token序列转换为AST
"""

from typing import List, Optional
from .lexer import Token, TokenType, tokenize
from .ast.expressions import *
from .ast.statements import *


class ParseError(Exception):
    """语法分析错误"""
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"[Line {token.line}, Col {token.column}] {message} at '{token.lexeme}'")


class Parser:
    """
    递归下降语法分析器
    
    实现9级运算符优先级：
    1. . [] (属性访问、列表索引)
    2. not (逻辑非)
    3. * / % (乘除模)
    4. + - (加减)
    5. is, is not, is greater than, is less than, is at least, is at most, ==, !=, <, >, <=, >= (比较)
    6. has, is in (成员检查)
    7. and (逻辑与)
    8. or (逻辑或)
    9. () (函数调用)
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
    
    # ==================== 辅助方法 ====================
    
    def peek(self, offset: int = 0) -> Token:
        """查看当前token（不前进）"""
        pos = self.current + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[pos]
    
    def is_at_end(self) -> bool:
        """是否到达末尾"""
        return self.peek().type == TokenType.EOF
    
    def advance(self) -> Token:
        """前进并返回当前token"""
        if not self.is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]
    
    def check(self, token_type: TokenType) -> bool:
        """检查当前token类型"""
        if self.is_at_end():
            return False
        return self.peek().type == token_type
    
    def match(self, *types: TokenType) -> bool:
        """如果当前token匹配任一类型，则前进"""
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    def consume(self, token_type: TokenType, message: str) -> Token:
        """消耗预期类型的token，否则报错"""
        if self.check(token_type):
            return self.advance()
        raise ParseError(message, self.peek())
    
    def synchronize(self):
        """错误恢复：跳过到下一个语句边界"""
        self.advance()
        while not self.is_at_end():
            if self.peek().type == TokenType.NEWLINE:
                return
            if self.peek().type in [
                TokenType.SET, TokenType.IF, TokenType.WHILE,
                TokenType.FUNCTION, TokenType.RETURN, TokenType.FOR,
                TokenType.TEST, TokenType.ASSERT
            ]:
                return
            self.advance()
    
    # ==================== 入口方法 ====================
    
    def parse(self) -> Program:
        """
        解析入口：解析整个程序
        """
        program = Program()
        
        while not self.is_at_end():
            try:
                # 跳过空行
                if self.check(TokenType.NEWLINE):
                    self.advance()
                    continue
                
                # 跳过缩进/缩出标记（顶层不需要）
                if self.check(TokenType.INDENT) or self.check(TokenType.DEDENT):
                    self.advance()
                    continue
                
                stmt = self.declaration()
                if stmt:
                    if isinstance(stmt, FunctionDefinition):
                        program.functions[stmt.name] = stmt
                    program.statements.append(stmt)
                    
            except ParseError as e:
                print(f"Parse Error: {e}")
                self.synchronize()
        
        return program
    
    def declaration(self) -> Optional[Statement]:
        """
        解析声明（函数定义或语句）
        """
        try:
            if self.match(TokenType.FUNCTION):
                return self.function_definition()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None
    
    # ==================== 语句解析 ====================
    
    def statement(self) -> Statement:
        """
        解析语句
        """
        if self.match(TokenType.SET):
            return self.assignment_statement()
        
        if self.match(TokenType.IF):
            return self.if_statement()
        
        if self.match(TokenType.WHILE):
            return self.while_statement()
        
        if self.match(TokenType.RETURN):
            return self.return_statement()
        
        if self.match(TokenType.ASK):
            return self.ask_statement()
        
        if self.match(TokenType.ECHO):
            return self.echo_statement()
        
        if self.match(TokenType.INCREASE):
            return self.increase_statement()
        
        if self.match(TokenType.DECREASE):
            return self.decrease_statement()
        
        if self.match(TokenType.ADD):
            return self.add_statement()
        
        if self.match(TokenType.REMOVE):
            return self.remove_statement()
        
        if self.match(TokenType.MOVE):
            return self.move_statement()
        
        if self.match(TokenType.WAIT):
            return self.wait_statement()
        
        if self.match(TokenType.END):
            return self.end_game_statement()
        
        if self.match(TokenType.START):
            return self.start_timer_statement()
        
        if self.match(TokenType.STOP):
            return self.stop_timer_statement()
        
        if self.match(TokenType.PERFORM):
            return self.perform_statement()
        
        if self.match(TokenType.RUN):
            return self.parallel_statement()
        
        if self.match(TokenType.TEST):
            return self.test_statement()
        
        if self.match(TokenType.ASSERT):
            return self.assert_statement()
        
        if self.match(TokenType.FOR):
            # 简化处理：for循环
            pass
        
        # 表达式语句
        expr = self.expression()
        return ExpressionStatement(expr)

    
    def assignment_statement(self) -> Assignment:
        """
        解析赋值语句: set <target> to <value>
        """
        target = self.lvalue()
        self.consume(TokenType.TO, "Expected 'to' after assignment target")
        value = self.expression()
        return Assignment(target, value)
    
    def lvalue(self) -> Expression:
        """
        解析赋值目标（左值）
        可以是：标识符、全局变量、属性访问、列表索引
        """
        if self.match(TokenType.GLOBAL_VAR):
            name = self.tokens[self.current - 1].value
            expr = GlobalVariable(name)
        elif self.match(TokenType.IDENTIFIER):
            name = self.tokens[self.current - 1].value
            expr = Identifier(name)
        else:
            raise ParseError("Expected identifier or global variable", self.peek())
        
        # 处理属性访问链：player.health, room.exits.north
        while self.match(TokenType.DOT):
            property_name = self.consume(
                TokenType.IDENTIFIER, 
                "Expected property name after '.'"
            ).value
            expr = PropertyAccess(expr, property_name)
        
        # 处理列表索引：items[0], player.inventory[2]
        while self.match(TokenType.LBRACKET):
            index = self.expression()
            self.consume(TokenType.RBRACKET, "Expected ']' after index")
            expr = ListIndex(expr, index)
        
        return expr
    
    def if_statement(self) -> IfStatement:
        """
        解析条件语句: if <condition>: ... [else if ...] [else ...]
        """
        condition = self.expression()
        self.consume(TokenType.COLON, "Expected ':' after if condition")
        
        # 解析then分支
        then_branch = self.block()
        
        elif_branches = []
        else_branch = None
        
        # 处理 else if 和 else
        while self.check(TokenType.ELSE):
            self.advance()  # consume 'else'
            
            if self.match(TokenType.IF):
                # else if
                elif_condition = self.expression()
                self.consume(TokenType.COLON, "Expected ':' after else if condition")
                elif_body = self.block()
                elif_branches.append((elif_condition, elif_body))
            else:
                # else
                self.consume(TokenType.COLON, "Expected ':' after else")
                else_branch = self.block()
                break  # else 必须是最后一个
        
        return IfStatement(condition, then_branch, elif_branches, else_branch)
    
    def while_statement(self) -> WhileStatement:
        """
        解析while循环: while <condition>: ...
        """
        condition = self.expression()
        self.consume(TokenType.COLON, "Expected ':' after while condition")
        body = self.block()
        return WhileStatement(condition, body)
    
    def function_definition(self) -> FunctionDefinition:
        """
        解析函数定义: function <name>([params]): ... 或 function <name>: ...
        """
        name = self.consume(TokenType.IDENTIFIER, "Expected function name").value
        
        # 解析可选的参数列表
        parameters = []
        if self.match(TokenType.LPAREN):
            # 有括号的参数列表
            if not self.check(TokenType.RPAREN):
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
                while self.match(TokenType.COMMA):
                    parameters.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
            self.consume(TokenType.RPAREN, "Expected ')' after parameters")
        
        self.consume(TokenType.COLON, "Expected ':' after function signature")
        
        body = self.block()
        return FunctionDefinition(name, parameters, body)

    
    def return_statement(self) -> ReturnStatement:
        """
        解析返回语句: return [expression]
        """
        # 检查是否有返回值
        if self.check(TokenType.NEWLINE) or self.check(TokenType.EOF) or self.check(TokenType.DEDENT):
            return ReturnStatement(None)
        
        value = self.expression()
        return ReturnStatement(value)
    
    def ask_statement(self) -> AskStatement:
        """
        解析输入语句: ask ["prompt"] [as variable]
        """
        prompt = None
        variable = None
        
        # 可选的提示文本
        if self.check(TokenType.STRING):
            prompt = self.expression()
        
        # 可选的 as 子句
        if self.match(TokenType.AS):
            variable = self.consume(TokenType.IDENTIFIER, "Expected variable name after 'as'").value
        
        return AskStatement(prompt, variable)
    
    def echo_statement(self) -> EchoStatement:
        """
        解析输出语句: echo <expression>
        """
        expr = self.expression()
        return EchoStatement(expr)
    
    def increase_statement(self) -> IncreaseStatement:
        """
        解析增加语句: increase <target> by <amount>
        """
        target = self.lvalue()
        self.consume(TokenType.BY, "Expected 'by' after target")
        amount = self.expression()
        
        return IncreaseStatement(target, amount)
    
    def decrease_statement(self) -> DecreaseStatement:
        """
        解析减少语句: decrease <target> by <amount>
        """
        target = self.lvalue()
        self.consume(TokenType.BY, "Expected 'by' after target")
        amount = self.expression()
        
        return DecreaseStatement(target, amount)
    
    def add_statement(self) -> AddStatement:
        """
        解析添加语句: add <item> to <target>
        """
        item = self.expression()
        self.consume(TokenType.TO, "Expected 'to' after item")
        target = self.lvalue()
        return AddStatement(item, target)
    
    def remove_statement(self) -> RemoveStatement:
        """
        解析移除语句: remove <item> from <source>
        """
        item = self.expression()
        self.consume(TokenType.FROM, "Expected 'from' after item")
        source = self.lvalue()
        return RemoveStatement(item, source)
    
    def move_statement(self) -> MoveStatement:
        """
        解析移动语句: move to <location>
        """
        self.consume(TokenType.TO, "Expected 'to' after 'move'")
        location = self.expression()
        return MoveStatement(location)
    
    def wait_statement(self) -> WaitStatement:
        """
        解析等待语句: wait for <duration> <unit>
        """
        self.consume(TokenType.FOR, "Expected 'for' after 'wait'")
        duration = self.expression()
        
        # 解析时间单位
        unit = "seconds"
        if self.match(TokenType.SECONDS):
            unit = "seconds"
        elif self.match(TokenType.MINUTES):
            unit = "minutes"
        
        return WaitStatement(duration, unit)
    
    def end_game_statement(self) -> EndGameStatement:
        """
        解析结束游戏语句: end game
        """
        self.consume(TokenType.GAME, "Expected 'game' after 'end'")
        return EndGameStatement()
    
    def start_timer_statement(self) -> StartTimerStatement:
        """
        解析启动计时器语句: start timer <name> for <duration> <unit>
        """
        self.consume(TokenType.TIMER, "Expected 'timer' after 'start'")
        name = self.expression()
        self.consume(TokenType.FOR, "Expected 'for' after timer name")
        duration = self.expression()
        
        # 解析时间单位
        unit = "seconds"
        if self.match(TokenType.SECONDS):
            unit = "seconds"
        elif self.match(TokenType.MINUTES):
            unit = "minutes"
        
        return StartTimerStatement(name, duration, unit)
    
    def stop_timer_statement(self) -> StopTimerStatement:
        """
        解析停止计时器语句: stop timer <name>
        """
        self.consume(TokenType.TIMER, "Expected 'timer' after 'stop'")
        name = self.expression()
        return StopTimerStatement(name)
    
    def perform_statement(self) -> PerformStatement:
        """
        解析动作语句: perform <action> [with <arg1>, <arg2>, ...]
        """
        action = self.expression()
        
        arguments = []
        if self.match(TokenType.WITH):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.expression())
        
        return PerformStatement(action, arguments)
    
    def parallel_statement(self) -> ParallelStatement:
        """
        解析并行执行语句: run in parallel: ...
        """
        self.consume(TokenType.COLON, "Expected ':' after 'run in parallel'")
        self.consume(TokenType.NEWLINE, "Expected newline after 'run in parallel:'")
        
        body = self.block()
        return ParallelStatement(body)

    def class_definition(self, class_type: str) -> ClassDefinition:
        """
        解析类定义: room Name:, item Name extends Parent:, character Name:
        """
        name = self.consume(TokenType.IDENTIFIER, f"Expected {class_type} name").value
        
        extends = None
        if self.match(TokenType.EXTENDS):
            extends = self.consume(TokenType.IDENTIFIER, "Expected parent class name").value
        
        self.consume(TokenType.COLON, f"Expected ':' after {class_type} name")
        self.consume(TokenType.NEWLINE, f"Expected newline after {class_type} name:")
        
        properties = {}
        methods = {}
        event_handlers = []
        
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            if self.check(TokenType.IDENTIFIER):
                prop_name = self.advance().value
                
                if self.check(TokenType.COLON):
                    # Property definition: property_name: value
                    self.advance()  # consume :
                    properties[prop_name] = self.expression()
                    if self.check(TokenType.NEWLINE):
                        self.advance()
                elif self.check(TokenType.LPAREN):
                    # Method definition
                    methods[prop_name] = self.finish_function_definition(prop_name)
                else:
                    # Simple property without value
                    properties[prop_name] = Literal(None)
            elif self.check(TokenType.ON):
                # Event handler
                event_handlers.append(self.event_handler())
            else:
                break
        
        return ClassDefinition(class_type, name, extends, properties, methods, event_handlers)
    
    def event_handler(self) -> EventHandler:
        """
        解析事件处理器: on action: player uses item:, on state: health is 0:, etc.
        """
        self.advance()  # consume 'on'
        
        event_type = self.consume(TokenType.IDENTIFIER, "Expected event type").value
        
        condition = None
        action = None
        
        if event_type == "action":
            # on action: player uses item:
            self.consume(TokenType.COLON, "Expected ':' after 'action'")
            # Parse action description
            if self.check(TokenType.IDENTIFIER):
                action_parts = []
                while not self.check(TokenType.COLON) and not self.is_at_end():
                    action_parts.append(self.advance().value)
                action = " ".join(action_parts)
        
        elif event_type in ["state", "timer", "event"]:
            # on state: condition:, on timer: name expires:, on event: name:
            self.consume(TokenType.COLON, f"Expected ':' after '{event_type}'")
            if not self.check(TokenType.NEWLINE):
                condition = self.expression()
        
        elif event_type == "game":
            # on game start:
            if self.match(TokenType.IDENTIFIER):
                start_word = self.previous().value
                if start_word == "start":
                    event_type = "game_start"
        
        elif event_type == "every":
            # on every turn:
            if self.match(TokenType.IDENTIFIER):
                turn_word = self.previous().value
                if turn_word == "turn":
                    event_type = "every_turn"
        
        self.consume(TokenType.COLON, "Expected ':' after event specification")
        self.consume(TokenType.NEWLINE, "Expected newline after event specification")
        
        body = self.block()
        return EventHandler(event_type, condition, action, body)
    
    def dialog_statement(self) -> DialogStatement:
        """
        解析对话语句: dialog speaker "text": ...
        """
        speaker = self.expression()
        text = self.expression()
        
        self.consume(TokenType.COLON, "Expected ':' after dialog text")
        self.consume(TokenType.NEWLINE, "Expected newline after dialog text:")
        
        options = []
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            if self.match(TokenType.IDENTIFIER):
                if self.previous().value == "option":
                    option_text = self.consume(TokenType.STRING, "Expected option text").value
                    self.consume(TokenType.ARROW, "Expected '->' after option text")
                    target = self.consume(TokenType.IDENTIFIER, "Expected target label").value
                    options.append((option_text, target))
                    if self.check(TokenType.NEWLINE):
                        self.advance()
        
        return DialogStatement(speaker, text, options)
    
    def exit_definition(self) -> ExitDefinition:
        """
        解析出口定义: exit direction to Room [if condition]
        """
        direction = self.consume(TokenType.IDENTIFIER, "Expected direction").value
        
        self.consume(TokenType.TO, "Expected 'to' after direction")
        target_room = self.consume(TokenType.IDENTIFIER, "Expected room name").value
        
        condition = None
        if self.match(TokenType.IF):
            condition = self.expression()
        
        if self.check(TokenType.NEWLINE):
            self.advance()
        
        return ExitDefinition(direction, target_room, condition)

    
    def test_statement(self) -> TestStatement:
        """
        解析测试语句: test "name": ...
        """
        # 解析测试名称（字符串）
        name_token = self.consume(TokenType.STRING, "Expected test name (string)")
        name = name_token.value
        
        self.consume(TokenType.COLON, "Expected ':' after test name")
        body = self.block()
        
        return TestStatement(name, body)
    
    def assert_statement(self) -> AssertStatement:
        """
        解析断言语句:
        - assert <condition>
        - assert not <condition>
        - assert <value> is <expected>
        - assert <list> contains <item>
        """
        # 检查各种断言形式
        if self.match(TokenType.NOT):
            # assert not <condition>
            condition = self.expression()
            return AssertStatement(condition, operator="not", expected=None, message="Assertion failed: expected false")
        
        # 解析条件表达式
        condition = self.expression()
        
        # 检查是否是 assert ... is ...
        if self.match(TokenType.IS):
            expected = self.expression()
            return AssertStatement(condition, operator="is", expected=expected, message="Assertion failed: values not equal")
        
        # 检查是否是 assert ... contains ...
        if self.match(TokenType.CONTAINS):
            item = self.expression()
            return AssertStatement(condition, operator="contains", expected=item, message="Assertion failed: list does not contain item")
        
        # 简单断言: assert <condition>
        return AssertStatement(condition, operator="truthy", expected=None, message="Assertion failed: condition is falsy")


    
    def block(self) -> List[Statement]:

        """
        解析代码块（缩进块）
        """
        statements = []
        
        # 期望INDENT
        if self.check(TokenType.NEWLINE):
            self.advance()
        
        if not self.check(TokenType.INDENT):
            raise ParseError("Expected indented block", self.peek())
        
        self.advance()  # consume INDENT
        
        while not self.is_at_end() and not self.check(TokenType.DEDENT):
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        
        # 消耗DEDENT
        if self.check(TokenType.DEDENT):
            self.advance()
        
        return statements
    
    # ==================== 表达式解析（运算符优先级） ====================
    
    def expression(self) -> Expression:
        """
        表达式入口：从最低优先级开始
        """
        return self.or_expr()
    
    def or_expr(self) -> Expression:
        """
        逻辑或: and_expr (or and_expr)*
        """
        expr = self.and_expr()
        
        while self.match(TokenType.OR):
            operator = "or"
            right = self.and_expr()
            expr = LogicalOperation(expr, operator, right)
        
        return expr
    
    def and_expr(self) -> Expression:
        """
        逻辑与: not_expr (and not_expr)*
        """
        expr = self.not_expr()
        
        while self.match(TokenType.AND):
            operator = "and"
            right = self.not_expr()
            expr = LogicalOperation(expr, operator, right)
        
        return expr
    
    def not_expr(self) -> Expression:
        """
        逻辑非: not comparison | comparison
        """
        if self.match(TokenType.NOT):
            operand = self.comparison()
            return UnaryOperation("not", operand)
        
        return self.comparison()
    
    def comparison(self) -> Expression:
        """
        比较运算: additive (compare_op additive)*
        """
        expr = self.additive()
        
        # 比较运算符
        compare_ops = [
            TokenType.EQ, TokenType.NE, TokenType.GT, TokenType.LT,
            TokenType.GE, TokenType.LE
        ]
        
        while self.match(*compare_ops):
            operator = self.tokens[self.current - 1].value
            right = self.additive()
            expr = Comparison(expr, operator, right)
        
        return expr
    
    def additive(self) -> Expression:
        """
        加减运算: multiplicative ((+|-) multiplicative)*
        """
        expr = self.multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = "+" if self.tokens[self.current - 1].type == TokenType.PLUS else "-"
            right = self.multiplicative()
            expr = BinaryOperation(expr, operator, right)
        
        return expr
    
    def multiplicative(self) -> Expression:
        """
        乘除模运算: index_access ((*|/|%) index_access)*
        """
        expr = self.index_access()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            token = self.tokens[self.current - 1]
            if token.type == TokenType.MULTIPLY:
                operator = "*"
            elif token.type == TokenType.DIVIDE:
                operator = "/"
            else:
                operator = "%"
            
            right = self.index_access()
            expr = BinaryOperation(expr, operator, right)
        
        return expr
    
    def index_access(self) -> Expression:
        """
        索引访问: unary ([expression])*
        """
        expr = self.unary()
        
        # 处理列表索引和切片
        while self.match(TokenType.LBRACKET):
            # 检查是否是切片
            if self.match(TokenType.COLON):
                # [:end] 形式
                end = None
                if not self.check(TokenType.RBRACKET):
                    end = self.expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after slice")
                expr = ListSlice(expr, None, end)
            else:
                start = self.expression()
                
                if self.match(TokenType.COLON):
                    # [start:end] 形式
                    end = None
                    if not self.check(TokenType.RBRACKET):
                        end = self.expression()
                    self.consume(TokenType.RBRACKET, "Expected ']' after slice")
                    expr = ListSlice(expr, start, end)
                else:
                    # [index] 形式
                    self.consume(TokenType.RBRACKET, "Expected ']' after index")
                    expr = ListIndex(expr, start)
        
        return expr
    
    def unary(self) -> Expression:
        """
        一元运算: -unary | member_check
        """
        if self.match(TokenType.MINUS):
            operand = self.unary()
            return UnaryOperation("-", operand)
        
        return self.member_check()
    
    def member_check(self) -> Expression:
        """
        成员检查: primary (has identifier | is in expression)*
        """
        expr = self.primary()
        
        # 处理 has
        if self.match(TokenType.HAS):
            property_name = self.consume(TokenType.IDENTIFIER, "Expected property name after 'has'").value
            right = Identifier(property_name)
            expr = MemberCheck("has", expr, right)
        
        # 处理 is in
        elif self.match(TokenType.IS) and self.match(TokenType.IN):
            right = self.primary()
            expr = MemberCheck("is in", expr, right)
        
        return expr
    
    def primary(self) -> Expression:
        """
        基本表达式: 字面量、标识符、括号表达式、函数调用
        """
        # 布尔值
        if self.match(TokenType.BOOLEAN):
            return Literal(self.tokens[self.current - 1].value)
        
        # null
        if self.match(TokenType.NULL):
            return Literal(None)
        
        # 数字
        if self.match(TokenType.NUMBER):
            return Literal(self.tokens[self.current - 1].value)
        
        # 字符串
        if self.match(TokenType.STRING):
            return Literal(self.tokens[self.current - 1].value)
        
        # 全局变量
        if self.match(TokenType.GLOBAL_VAR):
            return GlobalVariable(self.tokens[self.current - 1].value)
        
        # 标识符（可能是变量、属性访问、函数调用）
        if self.match(TokenType.IDENTIFIER):
            name = self.tokens[self.current - 1].value
            
            # 检查是否是函数调用
            if self.match(TokenType.LPAREN):
                return self.finish_call(name)
            
            # 属性访问链
            expr = Identifier(name)
            while self.match(TokenType.DOT):
                property_name = self.consume(TokenType.IDENTIFIER, "Expected property name after '.'").value
                expr = PropertyAccess(expr, property_name)
                
                # 检查方法调用
                if self.match(TokenType.LPAREN):
                    return self.finish_method_call(expr, property_name)
            
            return expr
        
        # 括号表达式
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return Grouping(expr)
        
        # 列表字面量
        if self.match(TokenType.LBRACKET):
            return self.list_literal()
        
        raise ParseError("Expected expression", self.peek())
    
    def finish_call(self, name: str) -> FunctionCall:
        """
        完成函数调用解析
        """
        arguments = []
        
        if not self.check(TokenType.RPAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.expression())
        
        self.consume(TokenType.RPAREN, "Expected ')' after arguments")
        return FunctionCall(name, arguments)
    
    def finish_method_call(self, object: Expression, method_name: str) -> MethodCall:
        """
        完成方法调用解析
        """
        arguments = []
        
        if not self.check(TokenType.RPAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.expression())
        
        self.consume(TokenType.RPAREN, "Expected ')' after arguments")
        return MethodCall(object, method_name, arguments)
    
    def list_literal(self) -> ListLiteral:
        """
        解析列表字面量: [element1, element2, ...]
        """
        elements = []
        
        if not self.check(TokenType.RBRACKET):
            elements.append(self.expression())
            while self.match(TokenType.COMMA):
                elements.append(self.expression())
        
        self.consume(TokenType.RBRACKET, "Expected ']' after list elements")
        return ListLiteral(elements)


def parse(source: str) -> Program:
    """
    便捷函数：将源代码解析为AST
    """
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()


# 测试代码
if __name__ == "__main__":
    test_code = '''
// 测试代码
set $counter to 0
set $items to ["apple", "banana", "cherry"]

if $counter is less than 10:
    echo "Counter is low"
else if $counter is less than 100:
    echo "Counter is moderate"
else:
    echo "Counter is high"

function greet(name):
    echo "Hello, " + name

function sum(a, b):
    return a + b

set result to sum(10, 20)
ask "What is your name?" as userName

// 测试框架
test "basic arithmetic":
    set x to 10
    assert x is 10
    assert not (x is 5)
    assert [1, 2, 3] contains 2
'''
    
    try:
        program = parse(test_code)
        print("解析成功!")
        print(f"函数: {list(program.functions.keys())}")
        print(f"语句数: {len(program.statements)}")
        
        # 打印AST
        from .ast.statements import StatementPrinter
        printer = StatementPrinter()
        program.accept(printer)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
