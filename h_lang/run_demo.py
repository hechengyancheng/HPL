#!/usr/bin/env python3
"""
HPL Core Features Demo Runner
H语言核心功能演示运行器
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.interpreter import HLangInterpreter, run_file, run

from core.lexer import LexerError
from core.parser import ParseError
from core.runtime.control_flow import HRuntimeError


def run_demo():
    """运行核心功能演示"""
    print("=" * 70)
    print("H语言核心功能演示 (HPL Core Features Demo)")
    print("=" * 70)
    
    demo_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples", "core_features_demo.hpl")

    
    if not os.path.exists(demo_file):
        print(f"错误: 找不到演示文件 {demo_file}")
        return False
    
    print(f"\n正在执行: {demo_file}")
    print("-" * 70)
    
    try:
        # 创建解释器并执行
        interpreter = HLangInterpreter()
        interpreter.execute_file(demo_file)
        
        # 获取并显示输出
        output = interpreter.get_output()
        
        print("-" * 70)
        print(f"\n执行成功！共产生 {len(output)} 行输出")
        print("\n输出内容:")
        print("-" * 70)
        
        for i, line in enumerate(output, 1):
            print(f"{i:3d}. {line}")
        
        print("-" * 70)
        print("演示完成！")
        return True
        
    except LexerError as e:
        print(f"\n词法错误 (Lexer Error): {e}")
        return False
    except ParseError as e:
        print(f"\n语法错误 (Parse Error): {e}")
        return False
    except HRuntimeError as e:
        print(f"\n运行时错误 (Runtime Error): {e}")
        return False
    except Exception as e:
        print(f"\n未知错误 (Unknown Error): {e}")
        import traceback
        traceback.print_exc()
        return False


def run_specific_section(section_name):
    """运行特定部分的演示"""
    sections = {
        "variables": (1, 50),      # 变量和赋值
        "types": (51, 100),        # 数据类型
        "arithmetic": (101, 130),   # 算术运算
        "comparison": (131, 180),  # 比较运算
        "logic": (181, 220),       # 逻辑运算
        "conditionals": (221, 260), # 条件语句
        "loops": (261, 300),       # 循环
        "functions": (301, 380),   # 函数
        "lists": (381, 450),       # 列表操作
        "strings": (451, 520),     # 字符串操作
        "math": (521, 580),        # 数学函数
        "conversion": (581, 620),  # 类型转换
        "nested": (621, 650),      # 嵌套结构
        "complex": (651, 690),     # 复杂表达式
        "game": (691, 780),        # 游戏示例
    }
    
    if section_name not in sections:
        print(f"可用的部分: {', '.join(sections.keys())}")
        return False
    
    start_line, end_line = sections[section_name]
    
    demo_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples", "core_features_demo.hpl")
    
    with open(demo_file, 'r', encoding='utf-8') as f:

        lines = f.readlines()
    
    # 提取特定行
    section_code = ''.join(lines[start_line-1:end_line])
    
    print(f"=" * 70)
    print(f"运行部分: {section_name} (行 {start_line}-{end_line})")
    print("=" * 70)
    print(f"\n代码:\n{section_code}")
    print("-" * 70)
    print("输出:")
    
    try:
        output = run(section_code)
        for line in output:
            print(f"  {line}")
        return True
    except Exception as e:
        print(f"错误: {e}")
        return False


def interactive_mode():
    """交互式模式"""
    print("=" * 70)
    print("HPL 交互式解释器")
    print("输入 'exit' 或 'quit' 退出")
    print("输入 'clear' 清空环境")
    print("=" * 70)
    
    interpreter = HLangInterpreter()
    
    while True:
        try:
            # 读取输入
            lines = []
            print("\nHPL> ", end="")
            
            while True:
                try:
                    line = input()
                except EOFError:
                    print("\n再见!")
                    return
                
                if line.strip() in ['exit', 'quit']:
                    print("再见!")
                    return
                
                if line.strip() == 'clear':
                    interpreter.reset()
                    print("环境已清空")
                    break
                
                if line.strip() == '':
                    # 空行表示输入结束
                    break
                
                lines.append(line)
                print("...  ", end="")
            
            if not lines:
                continue
            
            code = '\n'.join(lines)
            
            # 执行代码
            interpreter.execute(code)
            output = interpreter.get_output()
            
            # 显示输出
            for line in output:
                print(f"  => {line}")
            
            # 清空本次输出，保留历史
            interpreter.clear_output()
            
        except LexerError as e:
            print(f"词法错误: {e}")
        except ParseError as e:
            print(f"语法错误: {e}")
        except HRuntimeError as e:
            print(f"运行时错误: {e}")
        except Exception as e:
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='HPL Core Features Demo Runner')
    parser.add_argument('--section', '-s', help='运行特定部分 (variables/types/arithmetic/comparison/logic/conditionals/loops/functions/lists/strings/math/conversion/nested/complex/game)')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互式模式')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.section:
        run_specific_section(args.section)
    else:
        success = run_demo()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
