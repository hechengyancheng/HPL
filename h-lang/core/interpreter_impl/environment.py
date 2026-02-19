"""
H-Language Environment
H语言环境（作用域）管理
"""

from typing import Dict, Optional, Any
from ..types.primitive import HValue, HNull


class Environment:
    """
    H语言环境类
    管理变量作用域，支持嵌套
    """
    
    def __init__(self, enclosing: Optional['Environment'] = None):
        """
        创建新环境
        
        Args:
            enclosing: 外层环境（用于实现嵌套作用域）
        """
        self.variables: Dict[str, HValue] = {}
        self.globals: Dict[str, HValue] = {}  # 全局变量 $xxx
        self.enclosing = enclosing  # 外层环境
    
    def define(self, name: str, value: HValue):
        """
        在当前环境定义局部变量
        
        Args:
            name: 变量名
            value: 变量值
        """
        self.variables[name] = value
    
    def define_global(self, name: str, value: HValue):
        """
        定义全局变量 $xxx
        
        Args:
            name: 变量名（不包含$前缀）
            value: 变量值
        """
        # 如果有外层环境，向上传递到最外层
        if self.enclosing is not None:
            self.enclosing.define_global(name, value)
        else:
            self.globals[name] = value
    
    def get(self, name: str) -> HValue:
        """
        获取局部变量值
        
        Args:
            name: 变量名
            
        Returns:
            变量值
            
        Raises:
            KeyError: 如果变量未定义
        """
        # 先在当前环境查找
        if name in self.variables:
            return self.variables[name]
        
        # 递归在外层环境查找
        if self.enclosing is not None:
            return self.enclosing.get(name)
        
        raise KeyError(f"Undefined variable: {name}")
    
    def get_global(self, name: str) -> HValue:
        """
        获取全局变量值
        
        Args:
            name: 变量名（不包含$前缀）
            
        Returns:
            变量值
            
        Raises:
            KeyError: 如果全局变量未定义
        """
        # 向上查找到最外层环境
        if self.enclosing is not None:
            return self.enclosing.get_global(name)
        
        if name in self.globals:
            return self.globals[name]
        
        raise KeyError(f"Undefined global variable: ${name}")
    
    def assign(self, name: str, value: HValue):
        """
        赋值给已存在的局部变量
        
        Args:
            name: 变量名
            value: 新值
            
        Raises:
            KeyError: 如果变量未定义
        """
        # 先在当前环境查找
        if name in self.variables:
            self.variables[name] = value
            return
        
        # 递归在外层环境查找并赋值
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        
        raise KeyError(f"Undefined variable: {name}")
    
    def assign_global(self, name: str, value: HValue):
        """
        赋值给全局变量
        
        Args:
            name: 变量名（不包含$前缀）
            value: 新值
        """
        # 向上查找到最外层环境
        if self.enclosing is not None:
            self.enclosing.assign_global(name, value)
            return
        
        self.globals[name] = value
    
    def exists(self, name: str) -> bool:
        """
        检查局部变量是否存在
        
        Args:
            name: 变量名
            
        Returns:
            是否存在
        """
        if name in self.variables:
            return True
        if self.enclosing is not None:
            return self.enclosing.exists(name)
        return False
    
    def exists_global(self, name: str) -> bool:
        """
        检查全局变量是否存在
        
        Args:
            name: 变量名（不包含$前缀）
            
        Returns:
            是否存在
        """
        if self.enclosing is not None:
            return self.enclosing.exists_global(name)
        return name in self.globals
    
    def get_at(self, distance: int, name: str) -> HValue:
        """
        在指定距离的环境获取变量（用于优化）
        
        Args:
            distance: 向外层环境的距离
            name: 变量名
            
        Returns:
            变量值
        """
        env = self
        for _ in range(distance):
            env = env.enclosing
        
        return env.variables[name]
    
    def assign_at(self, distance: int, name: str, value: HValue):
        """
        在指定距离的环境赋值（用于优化）
        
        Args:
            distance: 向外层环境的距离
            name: 变量名
            value: 新值
        """
        env = self
        for _ in range(distance):
            env = env.enclosing
        
        env.variables[name] = value
    
    def get_all_locals(self) -> Dict[str, HValue]:
        """
        获取所有局部变量（用于调试）
        """
        return self.variables.copy()
    
    def get_all_globals(self) -> Dict[str, HValue]:
        """
        获取所有全局变量（用于调试）
        """
        if self.enclosing is not None:
            return self.enclosing.get_all_globals()
        return self.globals.copy()
    
    def __repr__(self):
        return f"Environment(locals={list(self.variables.keys())}, globals={list(self.globals.keys())})"


class EnvironmentChain:
    """
    环境链工具类
    用于快速创建和管理环境链
    """
    
    @staticmethod
    def create_global() -> Environment:
        """创建全局环境"""
        return Environment()
    
    @staticmethod
    def create_local(enclosing: Environment) -> Environment:
        """创建局部环境"""
        return Environment(enclosing)
    
    @staticmethod
    def create_function_scope(enclosing: Environment) -> Environment:
        """创建函数作用域"""
        return Environment(enclosing)


# 测试代码
if __name__ == "__main__":
    # 创建全局环境
    global_env = Environment()
    
    # 定义全局变量
    global_env.define_global("score", HValue.from_python(0))
    global_env.define_global("name", HValue.from_python("Player"))
    
    # 定义局部变量
    global_env.define("x", HValue.from_python(10))
    global_env.define("y", HValue.from_python(20))
    
    print("全局环境:")
    print(f"  局部变量: {global_env.get_all_locals()}")
    print(f"  全局变量: {global_env.get_all_globals()}")
    
    # 创建嵌套环境
    local_env = Environment(global_env)
    local_env.define("z", HValue.from_python(30))
    
    print("\\n嵌套环境:")
    print(f"  局部变量: {local_env.get_all_locals()}")
    print(f"  访问外层x: {local_env.get('x')}")
    print(f"  访问全局$score: {local_env.get_global('score')}")
    
    # 测试赋值
    local_env.assign("x", HValue.from_python(100))
    print(f"\\n赋值后全局环境的x: {global_env.get('x')}")
    
    # 测试全局变量赋值
    local_env.assign_global("score", HValue.from_python(50))
    print(f"赋值后全局$score: {global_env.get_global('score')}")
