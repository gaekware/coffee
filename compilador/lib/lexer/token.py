from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()

class Token:
    def __init__(self, type: TokenType, lexeme: str, position: int):
        self.type = type
        self.lexeme = lexeme
        self.position = position

    def __repr__(self):
        return f"Token({self.type.name}, '{self.lexeme}', pos:{self.position})"