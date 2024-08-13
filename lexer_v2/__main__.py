from lexer import Lexer
from parser_lm import Parser
import json, traceback
from pathlib import Path


run = __name__ == '__main__'
debug = False

def handleError(e):
	if debug:
		traceback.print_exc()
		return
	print(f"{e.__class__.__name__}: {e}")

def parseCommand(command):
	command = command.lower()
	
	if command == "debug":
		global debug
		debug = not debug
		print(f"Debug mode is now {debug}")
	elif command == "exit":
		global run
		run = False
	elif command == "help":
		try:
			with (Path(__file__).parent / "commands_ref.json").open("r") as jsonFile:
				formattedCommands = "\n".join(f"{name.upper()} - {desc}" for name, desc in sorted(json.load(jsonFile).items()))
				print(f"\n--- Available Commands ---\n{formattedCommands}\n")
		except FileNotFoundError:
			print("The file 'commands_ref.json' cannot be found")
	else:
		raise SyntaxError("Unknown command")

def tokenize(text):
	try:
		lexer = Lexer(text)
		return lexer.generateTokens()
	except Exception as e:
		handleError(e)
		return None
def parse(tokens):
	try:
		parser = Parser(tokens)
		return parser.parse()
	except Exception as e:
		handleError(e)

def beginShell():
	print("Layman 1.0.0 by Reda Elmountassir\nType 'help' in the console to get a list of available commands")
	while run:
		try:
			userInput = input(">>> ")
			parseCommand(userInput)
		except KeyboardInterrupt:
			print("\nKeyboardInterrupt: If you would like to quit, use 'exit' instead")
		except SyntaxError:
			tokens = tokenize(userInput)

			if tokens == None: continue
			syntaxTree = parse(tokens)
			if debug: print(tokens)

			if syntaxTree == None: continue
			print(syntaxTree)
if run: beginShell()