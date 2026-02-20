#!/usr/bin/env python3
"""
Test game framework parsing
"""
import sys
import os
import importlib.util

# Directly load lexer module without going through core.__init__
hlang_path = os.path.join(os.path.dirname(__file__), 'h-lang')
lexer_path = os.path.join(hlang_path, 'core', 'lexer.py')

spec = importlib.util.spec_from_file_location("core.lexer", lexer_path)
lexer_module = importlib.util.module_from_spec(spec)
sys.modules["core.lexer"] = lexer_module
spec.loader.exec_module(lexer_module)

tokenize = lexer_module.tokenize
Token = lexer_module.Token
TokenType = lexer_module.TokenType

# Directly load AST modules
ast_path = os.path.join(hlang_path, 'core', 'ast')
expressions_path = os.path.join(ast_path, 'expressions.py')
statements_path = os.path.join(ast_path, 'statements.py')

spec_expr = importlib.util.spec_from_file_location("core.ast.expressions", expressions_path)
expressions = importlib.util.module_from_spec(spec_expr)
sys.modules["core.ast.expressions"] = expressions
spec_expr.loader.exec_module(expressions)

spec_stmt = importlib.util.spec_from_file_location("core.ast.statements", statements_path)
statements = importlib.util.module_from_spec(spec_stmt)
sys.modules["core.ast.statements"] = statements
spec_stmt.loader.exec_module(statements)

# Directly load parser module
parser_path = os.path.join(hlang_path, 'core', 'parser.py')

spec_parser = importlib.util.spec_from_file_location("core.parser", parser_path)
parser_module = importlib.util.module_from_spec(spec_parser)
sys.modules["core.parser"] = parser_module
spec_parser.loader.exec_module(parser_module)

Parser = parser_module.Parser



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
        tokens = tokenize(code)
        parser = Parser(tokens)
        program = parser.parse()
        
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
