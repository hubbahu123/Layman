#NOTE: The file is parser_lm because parser already exists as a built-in python module
from tokens import TokenType
from ast_lm import *

class Parser:
	def __init__(self, tokens):
		self.tokens = iter(tokens)
		self.advance()

	def advance(self):
		try:
			self.currentToken = next(self.tokens)
		except StopIteration:
			self.currentToken = None

	def parse(self):
		if self.currentToken == None: return None

		result = self.expression()

		if self.currentToken != None:
			raise SyntaxError(f"{self.currentToken} did not get parsed")
		return result

	def expression(self):
		result = self.term()

		while self.currentToken != None and self.currentToken.type in (
				TokenType.ADD_POSITIVE, TokenType.SUBTRACT_NEGATIVE):
			if self.currentToken.type == TokenType.ADD_POSITIVE:
				self.advance()
				result = Add(result, self.term())
			elif self.currentToken.type == TokenType.SUBTRACT_NEGATIVE:
				self.advance()
				result = Subtract(result, self.term())

		return result

	def term(self):
		result = self.factor()

		while self.currentToken != None and self.currentToken.type in (
				TokenType.MULTIPLY, TokenType.DIVIDE):
			if self.currentToken.type == TokenType.MULTIPLY:
				self.advance()
				result = Multiply(result, self.factor())
			elif self.currentToken.type == TokenType.DIVIDE:
				self.advance()
				result = Divide(result, self.factor())

		return result

	def factor(self):
		token = self.currentToken
		if token.type == TokenType.LPAREN:
			self.advance()
			result = self.expression()
			if self.currentToken.type != TokenType.RPAREN: raise SyntaxError("Left parenthesis missing right parenthesis")
			self.advance()
			return result
		if token.type == TokenType.INT:
			self.advance()
			return Integer(token.value)
		if token.type == TokenType.FLOAT:
			self.advance()
			return Float(token.value)
		if token.type == TokenType.ADD_POSITIVE:
			self.advance()
			return Positive(self.factor())
		if token.type == TokenType.SUBTRACT_NEGATIVE:
			self.advance()
			return Negative(self.factor())

		raise SyntaxError(f"Invalid {token} token")