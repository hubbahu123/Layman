from enum import IntEnum, auto
from layman_logger import TextIter, errorMessage
from dataclasses import dataclass

class TokenType(IntEnum):
	#Single-char tokens
	PLUS = auto()
	MINUS = auto()
	STAR = auto()
	SLASH = auto()
	LPAREN = auto()
	RPAREN = auto()
	DOT = auto()

	#Literals
	INT = auto()
	FLOAT = auto()
	TEXT = auto() #String? STRING?!? Not happening in layman
	BOOL = auto()
	NOTHING = auto() #Null is not allowed in layman speak

	#Other
	EOF = auto()

@dataclass
class Token:
	type: TokenType
	loc: TextIter
	lexeme: str = ""
	literal: any = None

	def __str__(self):
		#Ex: INT(1.0 at line 2, column 3)
		return f"{self.type}({self.lexeme} {self.loc})"
	__repr__ = __str__

class Lexer:
	def __init__(self, text):
		self.textIter = TextIter(text)

	def advance(self):
		try:
			self.current = next(self.textIter)
		except StopIteration:
			self.current = None
		return self.current

	def lex(self):
		while self.current != None:
			token = self.lexToken()
			if token: yield token
		yield Token(TokenType.EOF, self.textIter)
	
	def lexToken(self, char):
		char = self.advance()

		if char == "(": return Token(TokenType.LPAREN, self.textIter, char)
		elif char == ")": return Token(TokenType.RPAREN, self.textIter, char)
		elif char == "-": return Token(TokenType.MINUS, self.textIter, char)
		elif char == "+": return Token(TokenType.PLUS, self.textIter, char)
		elif char == "*": return Token(TokenType.STAR, self.textIter, char)
		elif char == "/": return Token(TokenType.SLASH, self.textIter, char)
		elif char == ".": return Token(TokenType.DOT, self.textIter, char)
		else: raise errorMessage(self.textIter, ValueError, "Unexpected character")