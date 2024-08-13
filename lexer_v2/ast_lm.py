#NOTE: The file is parser_lm because parser already exists as a built-in python module
from dataclasses import dataclass

@dataclass
class UnaryOperator:
	opName = "UnaryOp"
	node: any
	
	def __str__(self):
		return f"{self.opName}({self.node})"
	__repr__ = __str__
class Positive(UnaryOperator):
	opName = "Positive"
class Negative(UnaryOperator):
	opName = "Negative"

@dataclass
class BinaryOperator:
	opName = "BinaryOp"
	leftNode: any
	rightNode: any

	def __str__(self):
		return f"{self.opName}({self.leftNode}, {self.rightNode})"
	__repr__ = __str__
class Add(BinaryOperator):
	opName = "Add"
class Subtract(BinaryOperator):
	opName = "Subtract"
class Multiply(BinaryOperator):
	opName = "Multiply"
class Divide(BinaryOperator):
	opName = "Divide"

class Constant:
	typeName = "All"

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return f"({self.typeName}: {self.value})"

	__repr__ = __str__
class Float(Constant):
	typeName = "Float"

	def __init__(self, value):
		self.value = float(value)
class Integer(Constant):
	typeName = "Integer"

	def __init__(self, value):
		self.value = int(value)