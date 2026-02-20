"""
H-Language Evaluator
H语言求值器 - 执行AST
"""

from typing import Any, Dict, List, Optional
from ..ast.expressions import *
from ..ast.statements import *
from ..hl_types.primitive import *
from ..hl_types.operations import Operations, COMPARISON_OPERATORS

from .environment import Environment
from .control_flow import ReturnException, HRuntimeError, EndGameException
from ...stdlib.actions import StdlibActions, ActionContext



class Evaluator(ExpressionVisitor, StatementVisitor):
    """
    H语言求值器
    
    实现表达式和语句的执行
    使用访问者模式遍历AST
    """
    
    def __init__(self, environment: Optional[Environment] = None):
        self.env = environment if environment else Environment()
        self.output_buffer: List[str] = []  # 输出缓冲区
        self.input_provider = input  # 输入函数（可替换为mock）
        
        # 内置函数注册表
        self.builtins: Dict[str, Any] = {}
        
        # 标准库动作上下文
        self.action_context = ActionContext()
        self.stdlib_actions = StdlibActions(self.action_context)
        
        # 测试结果跟踪
        self.test_results: List[Dict[str, Any]] = []
        self.current_test: Optional[str] = None
        
        self._register_builtins()
    
    def _register_builtins(self):
        """注册内置函数"""
        # 标准库动作指令作为内置函数注册
        pass

    
    def set_builtin(self, name: str, func):
        """设置内置函数"""
        self.builtins[name] = func
    
    def evaluate(self, program: Program) -> Any:
        """
        执行程序
        
        Args:
            program: 程序AST
            
        Returns:
            程序执行结果
        """
        try:
            return program.accept(self)
        except ReturnException as e:
            # 顶层return返回其值
            return e.value
        except Exception as e:
            raise HRuntimeError(f"Runtime error: {str(e)}")
    
    # ==================== 表达式求值 ====================
    
    def visit_literal(self, expr: Literal) -> HValue:
        """求值字面量"""
        value = expr.value
        
        if value is None:
            return HNull()
        elif isinstance(value, bool):
            return HBoolean(value)
        elif isinstance(value, (int, float)):
            return HNumber(float(value))
        elif isinstance(value, str):
            return HString(value)
        elif isinstance(value, list):
            return HList([self._to_hvalue(elem) for elem in value])
        
        # 如果已经是HValue，直接返回
        if isinstance(value, HValue):
            return value
        
        raise HRuntimeError(f"Unknown literal type: {type(value)}")
    
    def _to_hvalue(self, value: Any) -> HValue:
        """将Python值转换为HValue"""
        if isinstance(value, HValue):
            return value
        return from_python(value)
    
    def visit_identifier(self, expr: Identifier) -> HValue:
        """求值标识符（变量引用）"""
        try:
            value = self.env.get(expr.name)
            return value
        except KeyError:
            raise HRuntimeError(f"Undefined variable: {expr.name}")


    
    def visit_global_variable(self, expr: GlobalVariable) -> HValue:
        """求值全局变量"""
        try:
            return self.env.get_global(expr.name)
        except KeyError:
            raise HRuntimeError(f"Undefined global variable: ${expr.name}")
    
    def visit_property_access(self, expr: PropertyAccess) -> HValue:
        """求值属性访问"""
        obj = expr.object.accept(self)
        return Operations.get_property(obj, expr.property_name)
    
    def visit_binary_operation(self, expr: BinaryOperation) -> HValue:
        """求值二元运算"""
        left = expr.left.accept(self)
        right = expr.right.accept(self)
        
        if expr.operator == '+':
            return Operations.add(left, right)
        elif expr.operator == '-':
            return Operations.subtract(left, right)
        elif expr.operator == '*':
            return Operations.multiply(left, right)
        elif expr.operator == '/':
            return Operations.divide(left, right)
        elif expr.operator == '%':
            return Operations.modulo(left, right)
        
        raise HRuntimeError(f"Unknown binary operator: {expr.operator}")
    
    def visit_comparison(self, expr: Comparison) -> HBoolean:
        """求值比较运算"""
        left = expr.left.accept(self)
        right = expr.right.accept(self)
        
        op = expr.operator
        if op in COMPARISON_OPERATORS:
            return COMPARISON_OPERATORS[op](left, right)
        
        raise HRuntimeError(f"Unknown comparison operator: {op}")
    
    def visit_logical_operation(self, expr: LogicalOperation) -> HBoolean:
        """求值逻辑运算"""
        left = expr.left.accept(self)
        
        if expr.operator == 'and':
            # 短路求值
            if not left.is_truthy():
                return HBoolean(False)
            right = expr.right.accept(self)
            return HBoolean(right.is_truthy())
        
        elif expr.operator == 'or':
            # 短路求值
            if left.is_truthy():
                return HBoolean(True)
            right = expr.right.accept(self)
            return HBoolean(right.is_truthy())
        
        raise HRuntimeError(f"Unknown logical operator: {expr.operator}")
    
    def visit_unary_operation(self, expr: UnaryOperation) -> HValue:
        """求值一元运算"""
        operand = expr.operand.accept(self)
        
        if expr.operator == '-':
            return Operations.negate(operand)
        elif expr.operator == 'not':
            return Operations.logical_not(operand)
        
        raise HRuntimeError(f"Unknown unary operator: {expr.operator}")
    
    def visit_member_check(self, expr: MemberCheck) -> HBoolean:
        """求值成员检查"""
        left = expr.left.accept(self)
        right = expr.right.accept(self)
        
        if expr.operator == 'has':
            if isinstance(right, HString):
                return Operations.has(left, right)
            raise HRuntimeError(f"'has' operator requires string property name")
        
        elif expr.operator == 'is in':
            return Operations.is_in(left, right)
        
        raise HRuntimeError(f"Unknown member check operator: {expr.operator}")
    
    def visit_list_index(self, expr: ListIndex) -> HValue:
        """求值列表索引访问"""
        lst = expr.list_expr.accept(self)
        index = expr.index.accept(self)
        return Operations.list_index(lst, index)
    
    def visit_list_slice(self, expr: ListSlice) -> HList:
        """求值列表切片"""
        lst = expr.list_expr.accept(self)
        
        start = None
        end = None
        
        if expr.start:
            start = expr.start.accept(self)
        if expr.end:
            end = expr.end.accept(self)
        
        return Operations.list_slice(lst, start, end)
    
    def visit_function_call(self, expr: FunctionCall) -> HValue:
        """求值函数调用"""
        # 检查是否是内置函数
        if expr.function_name in self.builtins:
            # 求值参数
            args = [arg.accept(self) for arg in expr.arguments]
            return self.builtins[expr.function_name](*args)
        
        # 用户定义函数
        try:
            func = self.env.get(expr.function_name)
        except KeyError:
            raise HRuntimeError(f"Undefined function: {expr.function_name}")
        
        # 这里需要函数对象的支持
        # 简化处理：假设函数是FunctionDefinition
        if isinstance(func, FunctionDefinition):
            return self._call_function(func, expr.arguments)
        
        raise HRuntimeError(f"'{expr.function_name}' is not a function")
    
    def _call_function(self, func: FunctionDefinition, arguments: List[Expression]) -> HValue:
        """调用用户定义函数"""
        # 创建新环境
        func_env = Environment(self.env)
        
        # 绑定参数
        if len(arguments) != len(func.parameters):
            raise HRuntimeError(f"Function {func.name} expects {len(func.parameters)} arguments, got {len(arguments)}")
        
        for param_name, arg_expr in zip(func.parameters, arguments):
            arg_value = arg_expr.accept(self)
            func_env.define(param_name, arg_value)
        
        # 保存当前环境并切换
        previous_env = self.env
        self.env = func_env
        
        try:
            # 执行函数体
            result = HNull()
            for stmt in func.body:
                stmt.accept(self)
            return result
        except ReturnException as ret:
            return ret.value
        finally:
            # 恢复环境
            self.env = previous_env
    
    def visit_method_call(self, expr: MethodCall) -> HValue:
        """求值方法调用"""
        obj = expr.object.accept(self)
        
        # 这里需要方法调用支持
        # 简化处理：查找内置方法
        method_name = expr.method_name
        
        # 列表方法
        if isinstance(obj, HList):
            if method_name == "append":
                if len(expr.arguments) != 1:
                    raise HRuntimeError("append() takes exactly 1 argument")
                elem = expr.arguments[0].accept(self)
                return obj.append(elem)
            elif method_name == "removeAt":
                if len(expr.arguments) != 1:
                    raise HRuntimeError("removeAt() takes exactly 1 argument")
                index = expr.arguments[0].accept(self)
                if not isinstance(index, HNumber):
                    raise HRuntimeError("removeAt() index must be a number")
                return obj.remove_at(index.to_int())
        
        # 字符串方法
        if isinstance(obj, HString):
            if method_name == "upper":
                return obj.upper()
            elif method_name == "lower":
                return obj.lower()
            elif method_name == "trim":
                return obj.trim()
        
        raise HRuntimeError(f"'{method_name}' is not a method of {obj.type_name()}")
    
    def visit_list_literal(self, expr: ListLiteral) -> HList:
        """求值列表字面量"""
        elements = [elem.accept(self) for elem in expr.elements]
        return HList(elements)
    
    def visit_grouping(self, expr: Grouping) -> HValue:
        """求值括号表达式"""
        return expr.expression.accept(self)
    
    # ==================== 语句执行 ====================
    
    def visit_expression_statement(self, stmt: ExpressionStatement):
        """执行表达式语句"""
        stmt.expression.accept(self)
    
    def visit_assignment(self, stmt: Assignment):
        """执行赋值语句"""
        value = stmt.value.accept(self)
        
        target = stmt.target
        
        if isinstance(target, Identifier):
            # 局部变量
            if self.env.exists(target.name):
                self.env.assign(target.name, value)
            else:
                # 新变量定义
                self.env.define(target.name, value)
        
        elif isinstance(target, GlobalVariable):
            # 全局变量
            self.env.assign_global(target.name, value)
        
        elif isinstance(target, PropertyAccess):
            # 属性赋值
            obj = target.object.accept(self)
            Operations.set_property(obj, target.property_name, value)
        
        elif isinstance(target, ListIndex):
            # 列表索引赋值
            lst = target.list_expr.accept(self)
            index = target.index.accept(self)
            Operations.list_set(lst, index, value)
        
        else:
            raise HRuntimeError(f"Invalid assignment target: {type(target)}")
    
    def visit_if_statement(self, stmt: IfStatement):
        """执行条件语句"""
        condition = stmt.condition.accept(self)
        
        if condition.is_truthy():
            for s in stmt.then_branch:
                s.accept(self)
            return
        
        # 检查elif分支
        for elif_condition, elif_body in stmt.elif_branches:
            if elif_condition.accept(self).is_truthy():
                for s in elif_body:
                    s.accept(self)
                return
        
        # 执行else分支
        if stmt.else_branch:
            for s in stmt.else_branch:
                s.accept(self)
    
    def visit_while_statement(self, stmt: WhileStatement):
        """执行while循环"""
        while stmt.condition.accept(self).is_truthy():
            try:
                for s in stmt.body:
                    s.accept(self)
            except ReturnException:
                raise  # 向上传播return
            # 注意：break/continue需要额外支持
    
    def visit_function_definition(self, stmt: FunctionDefinition):
        """执行函数定义"""
        # 将函数定义存储在环境中
        self.env.define(stmt.name, stmt)
    
    def visit_return_statement(self, stmt: ReturnStatement):
        """执行返回语句"""
        value = HNull()
        if stmt.value:
            value = stmt.value.accept(self)
        raise ReturnException(value)
    
    def visit_ask_statement(self, stmt: AskStatement):
        """执行输入语句"""
        # 显示提示
        if stmt.prompt:
            prompt_value = stmt.prompt.accept(self)
            prompt_str = prompt_value.to_string()
        else:
            prompt_str = ""
        
        # 获取输入
        try:
            user_input = self.input_provider(prompt_str)
        except EOFError:
            user_input = ""
        
        # 存储到变量
        if stmt.variable:
            # 输入默认为字符串
            input_value = HString(user_input)
            if self.env.exists(stmt.variable):
                self.env.assign(stmt.variable, input_value)
            else:
                self.env.define(stmt.variable, input_value)
        
        return HString(user_input)
    
    def visit_echo_statement(self, stmt: EchoStatement):
        """执行输出语句"""
        value = stmt.expression.accept(self)
        self.stdlib_actions.echo(value)
        output = value.to_string()
        self.output_buffer.append(output)

    
    def visit_increase_statement(self, stmt: IncreaseStatement):
        """执行增加语句"""
        target = stmt.target
        amount = stmt.amount.accept(self)
        
        if isinstance(target, Identifier):
            current = self.env.get(target.name)
            new_value = self.stdlib_actions.increase_by(current, amount)
            self.env.assign(target.name, new_value)
        
        elif isinstance(target, GlobalVariable):
            current = self.env.get_global(target.name)
            new_value = self.stdlib_actions.increase_by(current, amount)
            self.env.assign_global(target.name, new_value)
        
        elif isinstance(target, PropertyAccess):
            obj = target.object.accept(self)
            current = Operations.get_property(obj, target.property_name)
            new_value = self.stdlib_actions.increase_by(current, amount)
            Operations.set_property(obj, target.property_name, new_value)
        
        else:
            raise HRuntimeError(f"Invalid increase target: {type(target)}")
    
    def visit_decrease_statement(self, stmt: DecreaseStatement):
        """执行减少语句"""
        target = stmt.target
        amount = stmt.amount.accept(self)
        
        if isinstance(target, Identifier):
            current = self.env.get(target.name)
            new_value = self.stdlib_actions.decrease_by(current, amount)
            self.env.assign(target.name, new_value)
        
        elif isinstance(target, GlobalVariable):
            current = self.env.get_global(target.name)
            new_value = self.stdlib_actions.decrease_by(current, amount)
            self.env.assign_global(target.name, new_value)
        
        elif isinstance(target, PropertyAccess):
            obj = target.object.accept(self)
            current = Operations.get_property(obj, target.property_name)
            new_value = self.stdlib_actions.decrease_by(current, amount)
            Operations.set_property(obj, target.property_name, new_value)
        
        else:
            raise HRuntimeError(f"Invalid decrease target: {type(target)}")

    
    def visit_add_statement(self, stmt: AddStatement):
        """执行添加元素语句"""
        item = stmt.item.accept(self)
        target = stmt.target.accept(self)
        
        # 使用标准库动作
        new_list = self.stdlib_actions.add_to(item, target)
        
        # 重新赋值
        if isinstance(stmt.target, Identifier):
            self.env.assign(stmt.target.name, new_list)
        elif isinstance(stmt.target, GlobalVariable):
            self.env.assign_global(stmt.target.name, new_list)
        elif isinstance(stmt.target, PropertyAccess):
            obj = stmt.target.object.accept(self)
            Operations.set_property(obj, stmt.target.property_name, new_list)
    
    def visit_remove_statement(self, stmt: RemoveStatement):
        """执行移除元素语句"""
        item = stmt.item.accept(self)
        source = stmt.source.accept(self)
        
        # 使用标准库动作
        new_list = self.stdlib_actions.remove_from(item, source)
        
        # 重新赋值
        if isinstance(stmt.source, Identifier):
            self.env.assign(stmt.source.name, new_list)
        elif isinstance(stmt.source, GlobalVariable):
            self.env.assign_global(stmt.source.name, new_list)
        elif isinstance(stmt.source, PropertyAccess):
            obj = stmt.source.object.accept(self)
            Operations.set_property(obj, stmt.source.property_name, new_list)

    
    def visit_program(self, stmt: Program):
        """执行程序"""
        # 先注册所有函数定义
        for func in stmt.functions.values():
            self.env.define(func.name, func)
        
        # 执行所有语句
        try:
            for s in stmt.statements:
                s.accept(self)
        except EndGameException:
            # 游戏正常结束
            pass
        
        return HNull()
    
    def visit_move_statement(self, stmt: MoveStatement):
        """执行移动语句"""
        location = stmt.location.accept(self)
        self.stdlib_actions.move_to(location)
    
    def visit_wait_statement(self, stmt: WaitStatement):
        """执行等待语句"""
        duration = stmt.duration.accept(self)
        unit = HString(stmt.unit) if stmt.unit else HString("seconds")
        self.stdlib_actions.wait_for(duration, unit)
    
    def visit_end_game_statement(self, stmt: EndGameStatement):
        """执行结束游戏语句"""
        self.stdlib_actions.end_game()
    
    def visit_start_timer_statement(self, stmt: StartTimerStatement):
        """执行启动计时器语句"""
        name = stmt.name.accept(self)
        duration = stmt.duration.accept(self)
        unit = HString(stmt.unit) if stmt.unit else HString("seconds")
        self.stdlib_actions.start_timer(name, duration, unit)
    
    def visit_stop_timer_statement(self, stmt: StopTimerStatement):
        """执行停止计时器语句"""
        name = stmt.name.accept(self)
        self.stdlib_actions.stop_timer(name)
    
    def visit_perform_statement(self, stmt: PerformStatement):
        """执行动作语句"""
        action_name = stmt.action.accept(self)
        args = HList([arg.accept(self) for arg in stmt.arguments])
        self.stdlib_actions.perform(action_name, args)
    
    def visit_parallel_statement(self, stmt: ParallelStatement):
        """执行并行语句"""
        # 创建函数包装语句块
        def parallel_func():
            for s in stmt.body:
                s.accept(self)
        
        self.stdlib_actions.run_parallel(parallel_func)
    
    def visit_test_statement(self, stmt: TestStatement):
        """执行测试语句"""
        # 设置当前测试名称
        previous_test = self.current_test
        self.current_test = stmt.name
        
        # 记录测试结果
        test_result = {
            'name': stmt.name,
            'passed': True,
            'errors': []
        }
        
        # 输出测试开始信息
        output_msg = f"\nRunning test: {stmt.name}"
        self.output_buffer.append(output_msg)
        self.stdlib_actions.echo(HString(output_msg))
        
        try:
            # 执行测试体
            for s in stmt.body:
                s.accept(self)
            
            # 测试通过
            success_msg = f"  ✓ Test '{stmt.name}' passed"
            self.output_buffer.append(success_msg)
            self.stdlib_actions.echo(HString(success_msg))
            
        except AssertionError as e:
            # 测试失败（断言失败）
            test_result['passed'] = False
            test_result['errors'].append(str(e))
            fail_msg = f"  ✗ Test '{stmt.name}' failed: {e}"
            self.output_buffer.append(fail_msg)
            self.stdlib_actions.echo(HString(fail_msg))
            
        except Exception as e:
            # 测试错误（运行时错误）
            test_result['passed'] = False
            test_result['errors'].append(f"Runtime error: {str(e)}")
            error_msg = f"  ✗ Test '{stmt.name}' error: {e}"
            self.output_buffer.append(error_msg)
            self.stdlib_actions.echo(HString(error_msg))
        
        finally:
            # 恢复之前的测试上下文
            self.current_test = previous_test
            self.test_results.append(test_result)
    
    def visit_assert_statement(self, stmt: AssertStatement):
        """执行断言语句"""
        if stmt.operator == "truthy":
            condition = stmt.condition.accept(self)
            if not condition.is_truthy():
                raise AssertionError(stmt.message or "Assertion failed")
        
        elif stmt.operator == "not":
            condition = stmt.condition.accept(self)
            if condition.is_truthy():
                raise AssertionError(stmt.message or "Assertion failed: expected false")
        
        elif stmt.operator == "is":
            actual = stmt.condition.accept(self)
            expected = stmt.expected.accept(self)
            if not actual.equals(expected).value:
                raise AssertionError(
                    stmt.message or f"Expected {expected.to_string()}, got {actual.to_string()}"
                )
        
        elif stmt.operator == "contains":
            container = stmt.condition.accept(self)
            item = stmt.expected.accept(self)
            if not isinstance(container, HList):
                raise HRuntimeError("assert contains requires a list")
            
            found = False
            for elem in container.value:
                if elem.equals(item).value:
                    found = True
                    break
            
            if not found:
                raise AssertionError(
                    stmt.message or f"List does not contain {item.to_string()}"
                )

    def visit_class_definition(self, stmt: ClassDefinition):
        """执行类定义语句"""
        # 创建类实例并存储在环境中
        class_instance = {
            'type': stmt.class_type,
            'name': stmt.name,
            'extends': stmt.extends,
            'properties': {},
            'methods': stmt.methods,
            'event_handlers': stmt.event_handlers
        }
        
        # 评估所有属性
        for prop_name, prop_expr in stmt.properties.items():
            class_instance['properties'][prop_name] = prop_expr.accept(self)
        
        # 存储类定义
        self.env.define(stmt.name, from_python(class_instance))
        return HNull()

    def visit_event_handler(self, stmt: EventHandler):
        """执行事件处理器"""
        # 事件处理器在类定义时注册，这里不需要执行
        # 实际的事件触发由游戏框架处理
        return HNull()

    def visit_dialog_statement(self, stmt: DialogStatement):
        """执行对话语句"""
        speaker = stmt.speaker.accept(self)
        text = stmt.text.accept(self)
        
        # 输出对话
        self.output_buffer.append(f"{speaker.to_string()}: {text.to_string()}")
        
        # 显示选项
        for i, (option_text, target) in enumerate(stmt.options, 1):
            self.output_buffer.append(f"  {i}. {option_text}")
        
        return HNull()

    def visit_exit_definition(self, stmt: ExitDefinition):
        """执行出口定义"""
        # 出口定义在类定义时处理，这里不需要执行
        return HNull()

    
    def get_output(self) -> List[str]:

        """获取输出缓冲区内容"""
        return self.output_buffer.copy()
    
    def clear_output(self):
        """清空输出缓冲区"""
        self.output_buffer.clear()
    
    def get_test_results(self) -> List[Dict[str, Any]]:
        """获取所有测试结果"""
        return self.test_results.copy()


# 便捷函数
def evaluate(program: Program, environment: Optional[Environment] = None) -> Any:
    """
    便捷函数：执行程序
    """
    evaluator = Evaluator(environment)
    return evaluator.evaluate(program)


# 测试代码
if __name__ == "__main__":
    from ..parser import parse
    
    test_code = '''
set x to 10
set y to 20
set sum to x + y
echo "Sum is: " + sum

if sum is greater than 25:
    echo "Sum is large!"
else:
    echo "Sum is small."

function greet(name):
    echo "Hello, " + name

greet("World")

// 测试框架示例
test "basic arithmetic":
    set a to 5
    set b to 3
    set result to a + b
    assert result is 8
    assert not (result is 10)
    assert [1, 2, 3, 4, 5] contains 3

test "string operations":
    set msg to "hello"
    assert msg is "hello"
    assert not (msg is "world")
'''
    
    try:
        program = parse(test_code)
        evaluator = Evaluator()
        evaluator.evaluate(program)
        print(f"\n输出缓冲区: {evaluator.get_output()}")
        print(f"\n测试结果: {evaluator.get_test_results()}")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
