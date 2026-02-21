#!/usr/bin/env python3
"""
Test game framework parsing
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 通过包导入
from h_lang.core import tokenize, parse, TokenType




def test_game_framework():
    """Test parsing of game framework constructs"""
    
    code = '''
// Game Framework Test

room Kitchen:
    description: "A cozy kitchen with a table"
    has_table: true

item Sword extends Weapon:
    damage: 10
    weight: 5

character Goblin extends Enemy:
    health: 50
    attack: 8

// Test event handlers
on action: player uses item:
    echo "Item used!"

on state: health is 0:
    echo "Game Over!"

on game start:
    echo "Welcome to the game!"

on every turn:
    echo "Turn ended"

// Test dialog
dialog merchant "Welcome to my shop":
    option "Buy potion" -> buy_potion
    option "Sell item" -> sell_item
    option "Leave" -> leave_shop

// Test conditional exit
exit north to Garden if has_key is true

echo "Game objects created successfully"
'''
    
    print("=" * 60)
    print("Testing Game Framework Parser")
    print("=" * 60)
    
    try:
        program = parse(code)

        
        print(f"\n✓ Parsing successful!")
        print(f"  Total statements: {len(program.statements)}")
        print(f"  Functions defined: {list(program.functions.keys())}")
        
        print("\n  Statement types:")
        for i, stmt in enumerate(program.statements, 1):
            stmt_type = type(stmt).__name__
            print(f"    {i}. {stmt_type}")
            
            # Print details for specific statement types
            if hasattr(stmt, 'name'):
                print(f"       Name: {stmt.name}")
            if hasattr(stmt, 'class_type'):
                print(f"       Class Type: {stmt.class_type}")
            if hasattr(stmt, 'extends'):
                print(f"       Extends: {stmt.extends}")
        
        print("\n" + "=" * 60)
        print("All game framework features parsed successfully!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_game_framework()
    sys.exit(0 if success else 1)
