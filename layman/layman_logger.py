from enum import IntFlag, auto
from dataclasses import dataclass
import traceback

class LogLevel(IntFlag):
	QUIET   = auto()
	NORMAL  = auto()
	VERBOSE = auto()

LOG_LEVEL = LogLevel.NORMAL

@dataclass
class TextIter:
	text: str
	index: int = 0
	col: int = 1
	line: int = 1

	def __iter__(self):
		return self

	def __next__(self):
		if self.index >= len(self.text):
			raise StopIteration
		current = self.text[self.index]
		self.index += 1
		self.col += 1

		#newline
		if current in "\r\n":
			self.line += 1
			self.col = 0
		
		return current

	def __str__(self):
		return f"at line {self.line}, column {self.col}"
	__repr__ = __str__

def error(e):
	#Prints an error in three different ways depending on level
	if LOG_LEVEL == LogLevel.QUIET:
		LOG_LEVEL("Error")
	elif LOG_LEVEL == LogLevel.NORMAL:
		print(f"{e.__class__.__name__}: {e}")
	elif LOG_LEVEL == LogLevel.VERBOSE:
		traceback.print_exc()

def errorMessage(loc: TextIter, type: Exception = Exception, context: str="Error"):
	#TODO: Arrow pointing to error location
	return type(f"{context} {loc}")

def flaggedPrint(text: str, flagMask: LogLevel):
	#Will only log a message if the flag is include in the flagMask
	if LOG_LEVEL in flagMask:
		print(text)
		return True
	return False