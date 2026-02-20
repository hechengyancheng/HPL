"""
H-Language Standard Library Actions
H语言标准库动作指令实现
"""

import time
import threading
import sys
import os
from typing import Any, Dict, List, Optional, Callable

# Try multiple import strategies
_types_imported = False

# Strategy 1: Relative import
try:
    from ..core.types.primitive import *
    from ..core.runtime.control_flow import HRuntimeError, EndGameException
    _types_imported = True
except ImportError:
    pass

# Strategy 2: Add h-lang to path and import directly
if not _types_imported:
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        h_lang_dir = os.path.dirname(current_dir)
        
        if h_lang_dir not in sys.path:
            sys.path.insert(0, h_lang_dir)
        
        from core.types.primitive import *
        from core.runtime.control_flow import HRuntimeError, EndGameException
        _types_imported = True
    except ImportError:
        pass

# Strategy 3: Try with project root
if not _types_imported:
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        h_lang_path = os.path.join(project_root, 'h-lang')
        if h_lang_path not in sys.path:
            sys.path.insert(0, h_lang_path)
        
        from core.types.primitive import *
        from core.runtime.control_flow import HRuntimeError, EndGameException
        _types_imported = True
    except ImportError as e:
        raise ImportError(f"Could not import types from any location: {e}")





class OutputHandler:
    """
    输出处理器抽象类
    支持不同平台的输出实现
    """
    
    def output(self, message: str):
        """输出消息"""
        raise NotImplementedError
    
    def clear(self):
        """清空输出"""
        raise NotImplementedError


class ConsoleOutputHandler(OutputHandler):
    """控制台输出处理器"""
    
    def __init__(self):
        self.buffer: List[str] = []
    
    def output(self, message: str):
        print(message)
        self.buffer.append(message)
    
    def clear(self):
        self.buffer.clear()
    
    def get_buffer(self) -> List[str]:
        return self.buffer.copy()


class ActionContext:
    """
    动作执行上下文
    维护标准库动作的执行状态
    """
    
    def __init__(self):
        self.output_handler: OutputHandler = ConsoleOutputHandler()
        self.timers: Dict[str, 'Timer'] = {}
        self.game_running: bool = True
        self.parallel_tasks: List[threading.Thread] = []
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.player_location: Optional[str] = None
        self.inventory: HList = HList([])
        
        # 游戏状态
        self.game_state: Dict[str, Any] = {}
        self.current_turn: int = 0
        self.registered_classes: Dict[str, Any] = {}  # 存储类定义

    
    def set_output_handler(self, handler: OutputHandler):
        """设置输出处理器"""
        self.output_handler = handler
    
    def echo(self, message: str):
        """输出消息"""
        self.output_handler.output(message)
    
    def start_timer(self, name: str, seconds: float, callback: Callable):
        """启动计时器"""
        timer = Timer(name, seconds, callback)
        self.timers[name] = timer
        timer.start()
    
    def stop_timer(self, name: str) -> bool:
        """停止计时器"""
        if name in self.timers:
            self.timers[name].stop()
            del self.timers[name]
            return True
        return False
    
    def end_game(self):
        """结束游戏"""
        self.game_running = False
        # 停止所有计时器
        for timer in self.timers.values():
            timer.stop()
        self.timers.clear()
        raise EndGameException("Game ended")
    
    def wait(self, seconds: float):
        """等待指定时间"""
        time.sleep(seconds)
    
    def run_parallel(self, func: Callable):
        """并行执行任务"""
        thread = threading.Thread(target=func, daemon=True)
        self.parallel_tasks.append(thread)
        thread.start()
    
    def cleanup(self):
        """清理资源"""
        # 停止所有计时器
        for timer in list(self.timers.values()):
            timer.stop()
        self.timers.clear()
        
        # 等待并行任务完成
        for thread in self.parallel_tasks:
            if thread.is_alive():
                thread.join(timeout=1.0)
        self.parallel_tasks.clear()
    
    # ==================== 事件系统 ====================
    
    def register_event_handler(self, event_type: str, handler: Callable, 
                                  condition: Optional[Any] = None,
                                  action: Optional[str] = None):
        """
        注册事件处理器
        
        Args:
            event_type: 事件类型 (action, state, timer, event, game_start, every_turn)
            handler: 处理函数
            condition: 触发条件（可选）
            action: 动作名称（用于action类型）
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        
        handler_info = {
            'handler': handler,
            'condition': condition,
            'action': action
        }
        self.event_handlers[event_type].append(handler_info)
    
    def trigger_event(self, event_type: str, **kwargs) -> bool:
        """
        触发事件
        
        Args:
            event_type: 事件类型
            **kwargs: 事件参数
            
        Returns:
            是否有处理器处理了事件
        """
        if event_type not in self.event_handlers:
            return False
        
        handlers = self.event_handlers[event_type]
        triggered = False
        
        for handler_info in handlers:
            handler = handler_info['handler']
            condition = handler_info.get('condition')
            action = handler_info.get('action')
            
            # 检查动作匹配（用于action类型）
            if action is not None:
                event_action = kwargs.get('action')
                if event_action != action:
                    continue
            
            # 检查条件（用于state类型）
            if condition is not None:
                if not self._check_condition(condition):
                    continue
            
            # 执行处理器
            try:
                handler(**kwargs)
                triggered = True
            except Exception as e:
                self.echo(f"Event handler error: {e}")
        
        return triggered
    
    def _check_condition(self, condition: Any) -> bool:
        """检查条件是否满足"""
        # 简化实现：条件可以是函数或值
        if callable(condition):
            return condition()
        return bool(condition)
    
    def register_class(self, class_type: str, name: str, class_def: Any):
        """注册类定义"""
        if class_type not in self.registered_classes:
            self.registered_classes[class_type] = {}
        self.registered_classes[class_type][name] = class_def
    
    def get_class(self, class_type: str, name: str) -> Optional[Any]:
        """获取类定义"""
        if class_type in self.registered_classes:
            return self.registered_classes[class_type].get(name)
        return None
    
    def set_game_state(self, key: str, value: Any):
        """设置游戏状态"""
        self.game_state[key] = value
    
    def get_game_state(self, key: str) -> Any:
        """获取游戏状态"""
        return self.game_state.get(key)
    
    def next_turn(self):
        """进入下一回合"""
        self.current_turn += 1
        # 触发每回合事件
        self.trigger_event('every_turn', turn=self.current_turn)



class Timer:
    """
    计时器类
    """
    
    def __init__(self, name: str, seconds: float, callback: Callable):
        self.name = name
        self.seconds = seconds
        self.callback = callback
        self._timer: Optional[threading.Timer] = None
        self._cancelled = False
    
    def start(self):
        """启动计时器"""
        self._cancelled = False
        self._timer = threading.Timer(self.seconds, self._on_expire)
        self._timer.start()
    
    def stop(self):
        """停止计时器"""
        self._cancelled = True
        if self._timer:
            self._timer.cancel()
    
    def _on_expire(self):
        """计时器到期回调"""
        if not self._cancelled:
            try:
                self.callback()
            except Exception as e:
                print(f"Timer {self.name} callback error: {e}")


class StdlibActions:
    """
    标准库动作指令实现
    """
    
    def __init__(self, context: Optional[ActionContext] = None):
        self.context = context if context else ActionContext()
    
    # ==================== 输出指令 ====================
    
    def echo(self, message: HValue) -> HNull:
        """
        echo <消息>
        向用户显示信息
        """
        msg_str = message.to_string()
        self.context.echo(msg_str)
        return HNull()
    
    # ==================== 库存管理 ====================
    
    def add_to(self, item: HValue, target: HValue) -> HValue:
        """
        add <物品> to <目标>
        将物品添加到目标集合中
        """
        if not isinstance(target, HList):
            raise HRuntimeError(f"Cannot add to non-list: {target.type_name()}")
        
        # 返回新列表
        return target.append(item)
    
    def remove_from(self, item: HValue, source: HValue) -> HValue:
        """
        remove <物品> from <来源>
        从来源集合中移除物品
        """
        if not isinstance(source, HList):
            raise HRuntimeError(f"Cannot remove from non-list: {source.type_name()}")
        
        # 查找并移除元素
        new_elements = []
        removed = False
        for elem in source.value:
            if not removed and elem.equals(item).value:
                removed = True
                continue
            new_elements.append(elem)
        
        return HList(new_elements)
    
    # ==================== 移动 ====================
    
    def move_to(self, location: HString) -> HNull:
        """
        move to <位置>
        改变当前位置
        """
        if not isinstance(location, HString):
            raise HRuntimeError("Location must be a string")
        
        self.context.player_location = location.value
        return HNull()
    
    # ==================== 数值操作 ====================
    
    def increase_by(self, current: HNumber, amount: HNumber) -> HNumber:
        """
        increase <变量> by <数值>
        增加变量的值
        """
        if not isinstance(current, HNumber):
            raise HRuntimeError(f"Cannot increase non-number: {current.type_name()}")
        if not isinstance(amount, HNumber):
            raise HRuntimeError("Increase amount must be a number")
        
        return current + amount
    
    def decrease_by(self, current: HNumber, amount: HNumber) -> HNumber:
        """
        decrease <变量> by <数值>
        减少变量的值
        """
        if not isinstance(current, HNumber):
            raise HRuntimeError(f"Cannot decrease non-number: {current.type_name()}")
        if not isinstance(amount, HNumber):
            raise HRuntimeError("Decrease amount must be a number")
        
        return current - amount
    
    # ==================== 流程控制 ====================
    
    def wait_for(self, seconds: HNumber, unit: HString) -> HNull:
        """
        wait for <数值> <单位>
        暂停执行指定时间
        """
        if not isinstance(seconds, HNumber):
            raise HRuntimeError("Wait time must be a number")
        
        unit_str = unit.value.lower() if isinstance(unit, HString) else "seconds"
        
        if unit_str in ["second", "seconds"]:
            wait_time = seconds.value
        elif unit_str in ["minute", "minutes"]:
            wait_time = seconds.value * 60
        else:
            raise HRuntimeError(f"Unknown time unit: {unit_str}")
        
        self.context.wait(wait_time)
        return HNull()
    
    def end_game(self) -> HNull:
        """
        end game
        结束游戏
        """
        self.context.end_game()
        return HNull()
    
    # ==================== 计时器 ====================
    
    def start_timer(self, name: HString, seconds: HNumber, unit: HString, 
                   callback: Optional[Callable] = None) -> HNull:
        """
        start timer <标识符> for <数值> <单位>
        创建并启动一个命名计时器
        """
        if not isinstance(name, HString):
            raise HRuntimeError("Timer name must be a string")
        if not isinstance(seconds, HNumber):
            raise HRuntimeError("Timer duration must be a number")
        
        unit_str = unit.value.lower() if isinstance(unit, HString) else "seconds"
        
        if unit_str in ["second", "seconds"]:
            duration = seconds.value
        elif unit_str in ["minute", "minutes"]:
            duration = seconds.value * 60
        else:
            raise HRuntimeError(f"Unknown time unit: {unit_str}")
        
        def default_callback():
            self.context.echo(f"Timer {name.value} expired")
        
        self.context.start_timer(name.value, duration, callback or default_callback)
        return HNull()
    
    def stop_timer(self, name: HString) -> HBoolean:
        """
        stop timer <标识符>
        停止并移除指定计时器
        """
        if not isinstance(name, HString):
            raise HRuntimeError("Timer name must be a string")
        
        result = self.context.stop_timer(name.value)
        return HBoolean(result)
    
    # ==================== 并行执行 ====================
    
    def run_parallel(self, func: Callable) -> HNull:
        """
        run in parallel:
            <语句块>
        并行执行代码块
        """
        self.context.run_parallel(func)
        return HNull()
    
    # ==================== 动作执行 ====================
    
    def perform(self, action_name: HString, args: HList) -> HValue:
        """
        perform <动作> with <参数>, ...
        执行预定义的复杂动作
        """
        # 动作执行将由游戏框架实现
        # 这里提供基础接口
        action_str = action_name.value
        
        # 解析动作名称（支持命名空间，如 combat.attack）
        parts = action_str.split('.')
        
        if len(parts) == 1:
            # 简单动作
            self.context.echo(f"Performing action: {action_str}")
        else:
            # 命名空间动作
            namespace = parts[0]
            action = parts[1]
            self.context.echo(f"Performing {action} in {namespace}")
        
        return HNull()
    
    # ==================== 测试框架 ====================
    
    def run_test(self, test_name: str, setup_func: Callable, 
                 action_func: Callable, assert_func: Callable) -> Dict[str, Any]:
        """
        test <名称>:
            <设置>
            <执行>
            <断言>
        执行测试用例
        """
        result = {
            'name': test_name,
            'passed': True,
            'errors': []
        }
        
        try:
            # 执行设置
            setup_func()
            
            # 执行动作
            action_func()
            
            # 执行断言
            assert_func()
            
        except AssertionError as e:
            result['passed'] = False
            result['errors'].append(str(e))
        except Exception as e:
            result['passed'] = False
            result['errors'].append(f"Runtime error: {str(e)}")
        
        return result
    
    def assert_condition(self, condition: HBoolean, message: str = "") -> HNull:
        """
        assert <条件>
        验证条件为真
        """
        if not isinstance(condition, HBoolean):
            raise HRuntimeError("Assert condition must be a boolean")
        
        if not condition.value:
            raise AssertionError(message or "Assertion failed")
        
        return HNull()
    
    def assert_equals(self, actual: HValue, expected: HValue, message: str = "") -> HNull:
        """
        assert <表达式> is <值>
        验证表达式等于指定值
        """
        if not actual.equals(expected).value:
            actual_str = actual.to_string()
            expected_str = expected.to_string()
            raise AssertionError(message or f"Expected {expected_str}, got {actual_str}")
        
        return HNull()
    
    def assert_contains(self, container: HValue, item: HValue, message: str = "") -> HNull:
        """
        assert <列表> contains <元素>
        验证列表包含指定元素
        """
        if not isinstance(container, HList):
            raise HRuntimeError("assert contains requires a list")
        
        found = False
        for elem in container.value:
            if elem.equals(item).value:
                found = True
                break
        
        if not found:
            item_str = item.to_string()
            raise AssertionError(message or f"List does not contain {item_str}")
        
        return HNull()


# 便捷函数：创建标准库实例
def create_stdlib(context: Optional[ActionContext] = None) -> StdlibActions:
    """创建标准库实例"""
    return StdlibActions(context)


# 测试代码
if __name__ == "__main__":
    print("测试标准库动作指令")
    
    stdlib = create_stdlib()
    
    # 测试 echo
    print("\n1. 测试 echo:")
    stdlib.echo(HString("Hello, World!"))
    
    # 测试 add/remove
    print("\n2. 测试 add/remove:")
    items = HList([HString("sword"), HString("shield")])
    print(f"原始列表: {items}")
    
    new_items = stdlib.add_to(HString("potion"), items)
    print(f"添加后: {new_items}")
    
    final_items = stdlib.remove_from(HString("shield"), new_items)
    print(f"移除后: {final_items}")
    
    # 测试 increase/decrease
    print("\n3. 测试 increase/decrease:")
    health = HNumber(100)
    new_health = stdlib.increase_by(health, HNumber(20))
    print(f"100 + 20 = {new_health}")
    
    final_health = stdlib.decrease_by(new_health, HNumber(30))
    print(f"120 - 30 = {final_health}")
    
    # 测试 assert
    print("\n4. 测试 assert:")
    try:
        stdlib.assert_condition(HBoolean(True), "Should pass")
        print("✓ assert true passed")
        
        stdlib.assert_condition(HBoolean(False), "Should fail")
        print("✗ assert false should have raised")
    except AssertionError as e:
        print(f"✓ assert false correctly raised: {e}")
    
    print("\n标准库测试完成!")
