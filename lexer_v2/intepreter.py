from ast_lm import *

class Interpreter:
    def visit(self, node):
        methodName = f"visit{node.__class__.__name__}"
        method = getattr(self, methodName)
        return method(node)