# H语言标准库与游戏框架实施计划

## 实施阶段

### 第1阶段：核心语义完善
- [ ] 1.1 完善作用域规则（LGN规则：Local → Global → Native）
- [ ] 1.2 实现全局变量 `$` 前缀强制检查
- [ ] 1.3 完善错误处理机制（TypeError, ReferenceError, RangeError）
- [ ] 1.4 验证闭包支持

### 第2阶段：标准库基础
- [ ] 2.1 实现 `echo` 指令（抽象输出接口）
- [ ] 2.2 实现 `add ... to ...` 指令
- [ ] 2.3 实现 `remove ... from ...` 指令
- [ ] 2.4 实现 `move to ...` 指令
- [ ] 2.5 实现 `increase ... by ...` 指令
- [ ] 2.6 实现 `decrease ... by ...` 指令
- [ ] 2.7 实现 `wait for ...` 指令
- [ ] 2.8 实现 `end game` 指令

### 第3阶段：测试框架
- [ ] 3.1 实现 `test "name": ...` 定义
- [ ] 3.2 实现 `assert ...` 断言
- [ ] 3.3 实现 `assert ... is ...` 断言
- [ ] 3.4 实现 `assert ... contains ...` 断言

### 第4阶段：高级标准库
- [ ] 4.1 实现 `start timer ... for ...` 计时器
- [ ] 4.2 实现 `stop timer ...` 计时器停止
- [ ] 4.3 实现 `perform ... with ...` 动作调用
- [ ] 4.4 实现 `run in parallel: ...` 并行执行

### 第5阶段：游戏框架基础
- [ ] 5.1 实现继承机制（`extends` 关键字）
- [ ] 5.2 实现 `Room` 类型定义
- [ ] 5.3 实现 `Item` 类型定义
- [ ] 5.4 实现 `Character` 类型定义
- [ ] 5.5 实现事件系统基础（`on` 关键字）

### 第6阶段：游戏框架事件系统
- [ ] 6.1 实现 `on action: player ...` 事件
- [ ] 6.2 实现 `on state: ...` 状态事件
- [ ] 6.3 实现 `on timer: ... expires` 计时器事件
- [ ] 6.4 实现 `on event: ...` 随机事件
- [ ] 6.5 实现复合动作语法（`uses X on Y`）

### 第7阶段：游戏框架高级功能
- [ ] 7.1 实现 `dialog` 对话系统
- [ ] 7.2 实现 `on game start` 生命周期
- [ ] 7.3 实现 `on every turn` 生命周期
- [ ] 7.4 实现条件出口（`to Room if condition`）

### 第8阶段：测试与验证
- [ ] 8.1 编写标准库单元测试
- [ ] 8.2 编写游戏框架测试
- [ ] 8.3 编写完整游戏示例

## 当前进度

### 已完成 ✅
- [x] 1.1 完善作用域规则（LGN规则：Local → Global → Native）
- [x] 1.2 实现全局变量 `$` 前缀强制检查
- [x] 1.3 完善错误处理机制（TypeError, ReferenceError, RangeError）
- [x] 1.4 验证闭包支持
- [x] 2.1 实现 `echo` 指令（抽象输出接口）
- [x] 2.2 实现 `add ... to ...` 指令
- [x] 2.3 实现 `remove ... from ...` 指令
- [x] 2.4 实现 `move to ...` 指令
- [x] 2.5 实现 `increase ... by ...` 指令
- [x] 2.6 实现 `decrease ... by ...` 指令
- [x] 2.7 实现 `wait for ...` 指令
- [x] 2.8 实现 `end game` 指令
- [x] 4.1 实现 `start timer ... for ...` 计时器
- [x] 4.2 实现 `stop timer ...` 计时器停止
- [x] 4.3 实现 `perform ... with ...` 动作调用

### 进行中 🔄
- [x] 3.1 实现 `test "name": ...` 定义
- [x] 3.2 实现 `assert ...` 断言
- [x] 3.3 实现 `assert ... is ...` 断言
- [x] 3.4 实现 `assert ... contains ...` 断言
- [x] 4.4 实现 `run in parallel: ...` 并行执行


### 待开始 ⏳
- [ ] 5.1 实现继承机制（`extends` 关键字）
- [ ] 5.2 实现 `Room` 类型定义
- [ ] 5.3 实现 `Item` 类型定义
- [ ] 5.4 实现 `Character` 类型定义
- [ ] 5.5 实现事件系统基础（`on` 关键字）
- [ ] 6.1 实现 `on action: player ...` 事件
- [ ] 6.2 实现 `on state: ...` 状态事件
- [ ] 6.3 实现 `on timer: ... expires` 计时器事件
- [ ] 6.4 实现 `on event: ...` 随机事件
- [ ] 6.5 实现复合动作语法（`uses X on Y`）
- [ ] 7.1 实现 `dialog` 对话系统
- [ ] 7.2 实现 `on game start` 生命周期
- [ ] 7.3 实现 `on every turn` 生命周期
- [ ] 7.4 实现条件出口（`to Room if condition`）
- [ ] 8.1 编写标准库单元测试
- [ ] 8.2 编写游戏框架测试
- [ ] 8.3 编写完整游戏示例
