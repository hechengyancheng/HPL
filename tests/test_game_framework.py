import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 通过包导入
from h_lang.core import HLangInterpreter



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

echo "Game objects created successfully"
'''

interpreter = HLangInterpreter()
interpreter.execute(code)
for output in interpreter.get_output():
    print(output)
