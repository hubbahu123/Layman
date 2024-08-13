import layman_logger, interpreter
from dataclasses import dataclass

@dataclass
class Command:
	desc: str = ""
	takesInput: bool = False
	action: any = None

class CommandParser:
	def __init__(self):
		self.commandsMap = {}
		self.addCommand("help", "shows this help message", False, self.commandsHelp)

	def commandsHelp(self):
		formattedCommands = "\n".join(f"  {name} - {command.desc}" for name, command in sorted(self.commandsMap.items()))
		print(f"Welcome to Layman Help. For more documentation and help visit [link should be added here].\n\navailable commands:\n{formattedCommands}")

	def addCommand(self, name: str, desc: str, takesInput: bool, action):
		self.commandsMap[name] = Command(desc, takesInput, action)

	def evalCommand(self, inputStr: str):
		#Return true means a command was found, return false means the opposite happened
		splitInput = inputStr.strip().split()
		inputCount = len(splitInput)

		if inputCount > 2: return False
		hasCommandVariable = inputCount == 2
		for name, command in self.commandsMap.items():
			if command.takesInput:
				if not hasCommandVariable: continue
				if name == splitInput[0]:
					invalidInput = command.action(splitInput[1])
					return not invalidInput
			else:
				if hasCommandVariable: continue
				if name == splitInput[0]:
					command.action()
					return True
		return False


run = False

def endShell():
	global run
	run = False

def setLogLevel(level):
	if level == "quiet":
		layman_logger.LOG_LEVEL = layman_logger.LogLevel.QUIET
	elif level == "normal":
		layman_logger.LOG_LEVEL = layman_logger.LogLevel.NORMAL
	elif level == "verbose":
		layman_logger.LOG_LEVEL = layman_logger.LogLevel.VERBOSE
	else:
		return True
	print(f"Log level set to {layman_logger.LOG_LEVEL.name.lower()}")
	return False

parser = CommandParser()
parser.addCommand("exit", "ends the shell", False, endShell)
parser.addCommand("level", "the logging level of the shell (must be 'quiet', 'normal', or 'verbose')", True, setLogLevel)

def runShell():
	layman_logger.flaggedPrint("Layman 1.0.0 by Reda Elmountassir\nType 'help' in the console to get a list of available commands",
		layman_logger.LogLevel.NORMAL | layman_logger.LogLevel.VERBOSE)
	global run
	run = True
	while run:
		try:
			inputStr = input(">>> ")
			try:
				if not parser.evalCommand(inputStr):
					eval  = interpreter.interpret(inputStr)
					if eval is not None: print(eval)
			except Exception as e:
				layman_logger.error(e)
		except KeyboardInterrupt as e:
			layman_logger.flaggedPrint("\nUse 'exit' to quit", layman_logger.LogLevel.QUIET)
			layman_logger.flaggedPrint("\nKeyboardInterrupt: If you would like to quit, use 'exit' instead", layman_logger.LogLevel.NORMAL)
			layman_logger.flaggedPrint(f"\nIf you would like to quit, use 'exit' instead\nKeyboardInterrupt: {e}", layman_logger.LogLevel.VERBOSE)

if __name__ == '__main__': runShell()