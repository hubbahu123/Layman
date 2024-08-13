import layman_logger
from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

def interpret(text: str):
	tokens = Lexer(text).lex()
	syntaxTree = Parser(tokens).parse()
	eval = Evaluator(syntaxTree).evaluate()
	#only used by shell - to use in script just add a print statement
	return eval