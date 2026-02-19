"""
H-Language Lexer
词法分析器 - 将源代码转换为Token序列
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Iterator


class TokenType(Enum):
    # 字面量
    NUMBER = auto()           # 数字: 42, 3.14
    STRING = auto()           # 字符串: "hello"
    BOOLEAN = auto()          # true, false
    NULL = auto()             # null
    
    # 标识符
    IDENTIFIER = auto()       # 变量名、函数名
    GLOBAL_VAR = auto()       # $xxx 全局变量
    
    # 关键字
    AND = auto()
    BY = auto()
    CONTAINS = auto()
    ELSE = auto()
    END = auto()
    EVERY = auto()
    FALSE = auto()
    FOR = auto()
    FROM = auto()
    HAS = auto()
    IF = auto()
    IN = auto()
    INCREASE = auto()
    IS = auto()
    NOT = auto()
    NULL_KEYWORD = auto()
    ON = auto()
    OR = auto()
    REMOVE = auto()
    RUN = auto()
    SET = auto()
    START = auto()
    STOP = auto()
    THIS = auto()
    TIMER = auto()
    TO = auto()
    TRUE = auto()
    WAIT = auto()
    WHEN = auto()
    WHILE = auto()
    
    # 函数相关关键字
    FUNCTION = auto()         # function
    RETURN = auto()           # return
    ASK = auto()              # ask
    AS = auto()               # as
    ECHO = auto()             # echo
    
    # 运算符
    PLUS = auto()             # +
    MINUS = auto()            # -
    MULTIPLY = auto()         # *
    DIVIDE = auto()           # /
    MODULO = auto()           # %
    
    # 比较运算符
    EQ = auto()               # ==, is
    NE = auto()               # !=, is not
    GT = auto()               # >, is greater than
    LT = auto()               # <, is less than
    GE = auto()               # >=, is at least
    LE = auto()               # <=, is at most
    
    # 其他符号
    ASSIGN = auto()           # = (备用)
    DOT = auto()              # .
    COMMA = auto()            # ,
    COLON = auto()            # :
    LPAREN = auto()           # (
    RPAREN = auto()           # )
    LBRACKET = auto()         # [
    RBRACKET = auto()         # ]
    LBRACE = auto()           # {
    RBRACE = auto()           # }
    
    # 缩进
    INDENT = auto()           # 缩进开始
    DEDENT = auto()           # 缩进结束
    NEWLINE = auto()          # 换行
    
    # 特殊
    EOF = auto()              # 文件结束
    COMMENT = auto()          # 注释


@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int
    lexeme: str = ""  # 原始文本
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"


# 关键字映射表
KEYWORDS = {
    'and': TokenType.AND,
    'by': TokenType.BY,
    'contains': TokenType.CONTAINS,
    'else': TokenType.ELSE,
    'end': TokenType.END,
    'every': TokenType.EVERY,
    'false': TokenType.FALSE,
    'for': TokenType.FOR,
    'from': TokenType.FROM,
    'has': TokenType.HAS,
    'if': TokenType.IF,
    'in': TokenType.IN,
    'increase': TokenType.INCREASE,
    'is': TokenType.IS,
    'not': TokenType.NOT,
    'null': TokenType.NULL_KEYWORD,
    'on': TokenType.ON,
    'or': TokenType.OR,
    'remove': TokenType.REMOVE,
    'run': TokenType.RUN,
    'set': TokenType.SET,
    'start': TokenType.START,
    'stop': TokenType.STOP,
    'this': TokenType.THIS,
    'timer': TokenType.TIMER,
    'to': TokenType.TO,
    'true': TokenType.TRUE,
    'wait': TokenType.WAIT,
    'when': TokenType.WHEN,
    'while': TokenType.WHILE,
    'function': TokenType.FUNCTION,
    'return': TokenType.RETURN,
    'ask': TokenType.ASK,
    'as': TokenType.AS,
    'echo': TokenType.ECHO,
}


class LexerError(Exception):
    """词法分析错误"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"[Line {line}, Col {column}] {message}")


class Lexer:
    """
    H语言词法分析器
    
    特性：
    - UTF-8编码支持
    - 4空格缩进识别（生成INDENT/DEDENT）
    - 单行//和多行/* */注释
    - 多词运算符识别（如 "is greater than"）
    - 字符串转义序列支持
    """
    
    INDENT_SIZE = 4  # 4空格缩进
    
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0           # 当前token开始位置
        self.current = 0         # 当前扫描位置
        self.line = 1            # 当前行号
        self.column = 1          # 当前列号
        self.indent_stack = [0]  # 缩进栈，记录每级缩进的空格数
        
    def error(self, message: str):
        raise LexerError(message, self.line, self.column)
    
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def peek(self, offset: int = 0) -> str:
        """查看当前字符（不前进）"""
        pos = self.current + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def advance(self) -> str:
        """前进并返回当前字符"""
        if self.is_at_end():
            return '\0'
        char = self.source[self.current]
        self.current += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def match(self, expected: str) -> bool:
        """如果当前字符匹配预期，则前进"""
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.advance()
        return True
    
    def skip_whitespace(self):
        """跳过空白字符（不包括换行和缩进）"""
        while not self.is_at_end():
            char = self.peek()
            if char in ' \t\r':
                self.advance()
            else:
                break
    
    def skip_line_whitespace(self):
        """跳过行内空白（不包括换行）"""
        while not self.is_at_end():
            char = self.peek()
            if char == ' ' or char == '\t':
                self.advance()
            else:
                break
    
    def read_string(self) -> str:
        """读取字符串，支持转义序列"""
        # 假设开头双引号已消耗
        result = []
        
        while not self.is_at_end() and self.peek() != '"':
            char = self.advance()
            
            if char == '\\':
                # 处理转义序列
                if self.is_at_end():
                    self.error("未终止的字符串转义")
                escape_char = self.advance()
                if escape_char == 'n':
                    result.append('\n')
                elif escape_char == 't':
                    result.append('\t')
                elif escape_char == '"':
                    result.append('"')
                elif escape_char == '\\':
                    result.append('\\')
                else:
                    self.error(f"未知的转义序列: \\{escape_char}")
            else:
                result.append(char)
        
        if self.is_at_end():
            self.error("未终止的字符串")
        
        # 消耗结束双引号
        self.advance()
        
        return ''.join(result)
    
    def read_number(self) -> float:
        """读取数字（整数或浮点数）"""
        # 假设开头数字已消耗
        start_pos = self.current - 1
        
        # 整数部分
        while self.peek().isdigit():
            self.advance()
        
        # 小数部分
        if self.peek() == '.' and self.peek(1).isdigit():
            self.advance()  # 消耗 .
            while self.peek().isdigit():
                self.advance()
        
        num_str = self.source[start_pos:self.current]
        return float(num_str)
    
    def read_identifier(self) -> str:
        """读取标识符"""
        # 假设开头字符已消耗
        start_pos = self.current - 1
        
        while (not self.is_at_end() and 
               (self.peek().isalnum() or self.peek() == '_')):
            self.advance()
        
        return self.source[start_pos:self.current]
    
    def read_line_comment(self):
        """跳过单行注释 // ... """
        while not self.is_at_end() and self.peek() != '\n':
            self.advance()
    
    def read_block_comment(self):
        """跳过多行注释 /* ... */"""
        self.advance()  # 消耗 *
        
        while not self.is_at_end():
            if self.peek() == '*' and self.peek(1) == '/':
                self.advance()  # 消耗 *
                self.advance()  # 消耗 /
                return
            self.advance()
        
        self.error("未终止的多行注释")
    
    def handle_indentation(self):
        """处理缩进，生成INDENT/DEDENT token"""
        # 计算当前行的前导空格数
        space_count = 0
        
        while self.peek() == ' ':
            space_count += 1
            self.advance()
        
        # 检查是否是Tab（不允许）
        if self.peek() == '\t':
            self.error("禁止使用Tab字符，请使用4个空格缩进")
        
        current_indent = self.indent_stack[-1]
        
        if space_count > current_indent:
            # 增加缩进
            if (space_count - current_indent) != self.INDENT_SIZE:
                self.error(f"缩进必须是{self.INDENT_SIZE}个空格的倍数")
            self.indent_stack.append(space_count)
            self.add_token(TokenType.INDENT, space_count)
        elif space_count < current_indent:
            # 减少缩进
            while space_count < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.add_token(TokenType.DEDENT, self.indent_stack[-1])
            
            if space_count != self.indent_stack[-1]:
                self.error("缩进级别不匹配")
    
    def add_token(self, token_type: TokenType, value=None):
        """添加token到列表"""
        lexeme = self.source[self.start:self.current]
        token = Token(
            type=token_type,
            value=value if value is not None else lexeme,
            line=self.line,
            column=self.column - len(lexeme),
            lexeme=lexeme
        )
        self.tokens.append(token)
    
    def scan_token(self):
        """扫描单个token"""
        self.start = self.current
        
        if self.is_at_end():
            return False
        
        char = self.advance()
        
        # 处理各种字符
        if char == '\n':
            self.add_token(TokenType.NEWLINE)
            return True
        
        # 跳过行内空白
        if char in ' \t\r':
            return True  # 继续扫描
        
        # 字符串
        if char == '"':
            value = self.read_string()
            self.add_token(TokenType.STRING, value)
            return True
        
        # 数字
        if char.isdigit() or (char == '-' and self.peek().isdigit()):
            # 回退，让read_number处理完整数字
            self.current -= 1
            self.column -= 1
            value = self.read_number()
            self.add_token(TokenType.NUMBER, value)
            return True
        
        # 标识符或关键字
        if char.isalpha() or char == '_':
            # 回退，让read_identifier处理完整标识符
            self.current -= 1
            self.column -= 1
            identifier = self.read_identifier()
            
            # 检查是否是关键字
            if identifier in KEYWORDS:
                token_type = KEYWORDS[identifier]
                # 特殊处理布尔值和null
                if token_type == TokenType.TRUE:
                    self.add_token(TokenType.BOOLEAN, True)
                elif token_type == TokenType.FALSE:
                    self.add_token(TokenType.BOOLEAN, False)
                elif token_type == TokenType.NULL_KEYWORD:
                    self.add_token(TokenType.NULL, None)
                else:
                    self.add_token(token_type)
            else:
                self.add_token(TokenType.IDENTIFIER, identifier)
            return True
        
        # 全局变量 $xxx
        if char == '$':
            if self.peek().isalpha() or self.peek() == '_':
                identifier = self.read_identifier()
                self.add_token(TokenType.GLOBAL_VAR, identifier)
            else:
                self.error("全局变量名必须以字母或下划线开头")
            return True
        
        # 注释
        if char == '/':
            if self.peek() == '/':
                self.read_line_comment()
                return True  # 注释不产生token
            elif self.peek() == '*':
                self.read_block_comment()
                return True
        
        # 单字符运算符和符号
        single_char_tokens = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,
            '.': TokenType.DOT,
            ',': TokenType.COMMA,
            ':': TokenType.COLON,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
        }
        
        if char in single_char_tokens:
            self.add_token(single_char_tokens[char])
            return True
        
        # 双字符运算符
        if char == '=':
            if self.match('='):
                self.add_token(TokenType.EQ)
            else:
                self.add_token(TokenType.ASSIGN)
            return True
        
        if char == '!':
            if self.match('='):
                self.add_token(TokenType.NE)
            else:
                self.error("单独的 '!' 不被支持，请使用 'not'")
            return True
        
        if char == '<':
            if self.match('='):
                self.add_token(TokenType.LE)
            else:
                self.add_token(TokenType.LT)
            return True
        
        if char == '>':
            if self.match('='):
                self.add_token(TokenType.GE)
            else:
                self.add_token(TokenType.GT)
            return True
        
        # 未知字符
        self.error(f"未知字符: '{char}'")
        return False
    
    def scan_tokens(self) -> List[Token]:
        """
        扫描所有token，处理缩进和多词运算符
        """
        lines = self.source.split('\n')
        
        for line_idx, line in enumerate(lines):
            self.line = line_idx + 1
            self.column = 1
            self.current = sum(len(l) + 1 for l in lines[:line_idx])
            
            # 跳过空行和纯注释行
            stripped = line.lstrip()
            if not stripped or stripped.startswith('//'):
                continue
            
            # 处理缩进
            indent_spaces = len(line) - len(stripped)
            self.current += indent_spaces
            self.column += indent_spaces
            
            current_indent = self.indent_stack[-1]
            
            if indent_spaces > current_indent:
                # 增加缩进
                if (indent_spaces - current_indent) % self.INDENT_SIZE != 0:
                    self.error(f"缩进必须是{self.INDENT_SIZE}个空格的倍数")
                while self.indent_stack[-1] < indent_spaces:
                    self.indent_stack.append(self.indent_stack[-1] + self.INDENT_SIZE)
                    self.tokens.append(Token(TokenType.INDENT, self.indent_stack[-1], self.line, self.column))
            elif indent_spaces < current_indent:
                # 减少缩进
                while self.indent_stack[-1] > indent_spaces:
                    self.indent_stack.pop()
                    self.tokens.append(Token(TokenType.DEDENT, self.indent_stack[-1], self.line, self.column))
            
            # 处理行内容
            line_lexer = Lexer(stripped)
            line_lexer.line = self.line
            line_lexer.column = self.column
            line_lexer.indent_stack = self.indent_stack.copy()
            
            while not line_lexer.is_at_end():
                if not line_lexer.scan_token():
                    break
            
            # 添加行尾换行
            if line_lexer.tokens and line_lexer.tokens[-1].type != TokenType.NEWLINE:
                line_lexer.tokens.append(Token(TokenType.NEWLINE, None, self.line, len(line) + 1))
            
            self.tokens.extend(line_lexer.tokens)
        
        # 文件结束，关闭所有缩进
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, 0, self.line, self.column))
        
        # 添加EOF
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        
        # 后处理：合并多词运算符
        self.merge_compound_operators()
        
        return self.tokens
    
    def merge_compound_operators(self):
        """
        合并多词运算符，如：
        - "is not" -> NE
        - "is greater than" -> GT
        - "is less than" -> LT
        - "is at least" -> GE
        - "is at most" -> LE
        """
        i = 0
        new_tokens = []
        
        while i < len(self.tokens):
            token = self.tokens[i]
            
            # 检查 "is ..."
            if token.type == TokenType.IS and i + 1 < len(self.tokens):
                next_token = self.tokens[i + 1]
                
                if next_token.type == TokenType.NOT:
                    new_tokens.append(Token(TokenType.NE, "is not", token.line, token.column))
                    i += 2
                    continue
                
                if next_token.type == TokenType.IDENTIFIER:
                    if next_token.value == "greater" and i + 2 < len(self.tokens):
                        if self.tokens[i + 2].type == TokenType.IDENTIFIER and self.tokens[i + 2].value == "than":
                            new_tokens.append(Token(TokenType.GT, "is greater than", token.line, token.column))
                            i += 3
                            continue
                    
                    if next_token.value == "less" and i + 2 < len(self.tokens):
                        if self.tokens[i + 2].type == TokenType.IDENTIFIER and self.tokens[i + 2].value == "than":
                            new_tokens.append(Token(TokenType.LT, "is less than", token.line, token.column))
                            i += 3
                            continue
                    
                    if next_token.value == "at" and i + 2 < len(self.tokens):
                        if self.tokens[i + 2].type == TokenType.IDENTIFIER:
                            if self.tokens[i + 2].value == "least":
                                new_tokens.append(Token(TokenType.GE, "is at least", token.line, token.column))
                                i += 3
                                continue
                            elif self.tokens[i + 2].value == "most":
                                new_tokens.append(Token(TokenType.LE, "is at most", token.line, token.column))
                                i += 3
                                continue
                
                # 单独的 "is" 就是 EQ
                new_tokens.append(Token(TokenType.EQ, "is", token.line, token.column))
                i += 1
                continue
            
            new_tokens.append(token)
            i += 1
        
        self.tokens = new_tokens


def tokenize(source: str) -> List[Token]:
    """
    便捷函数：将源代码转换为token列表
    """
    lexer = Lexer(source)
    return lexer.scan_tokens()


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

ask "What is your name?" as userName
'''
    
    try:
        tokens = tokenize(test_code)
        for token in tokens:
            print(token)
    except LexerError as e:
        print(f"词法错误: {e}")
