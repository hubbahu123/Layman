#!/usr/bin/env python3
import shell, argparse, layman_logger, sys, interpreter

def laymanFile(filename):
	if filename == "-": return None
	if not filename.endswith(".lm"): filename += ".lm"
	try:
		with open(filename, "r", encoding="utf-8") as lm:
			return lm.read()
	except OSError as e:
		raise argparse.ArgumentTypeError(f"can't open file '{filename}': {e}")

def main():
	parser = argparse.ArgumentParser(prog="Layman", description="a shell and interpreter for the Layman programming language")

	parser.add_argument("file", nargs="?", type=laymanFile, help="input a file to be interpreted ('-' or nothing whill be intepreted as stdin)")
	parser.add_argument('--version', action="version", version="%(prog)s 1.0.0")
	parser.add_argument("-c", "--cmd", help="directly input a string command to be interpreted")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-v", dest="verbose", action="store_true", help="logs will be verbose")
	group.add_argument("-q", dest="quiet", action="store_true", help="logs will be quiet")

	args = parser.parse_args()

	if args.verbose:
		layman_logger.LOG_LEVEL = layman_logger.LogLevel.VERBOSE
	elif args.quiet:
		layman_logger.LOG_LEVEL = layman_logger.LogLevel.QUIET

	toParse = args.cmd or args.file
	if toParse:
		try:
			interpreter.interpret(toParse)
			sys.exit(0)
		except Exception as e:
			layman_logger.error(e)
			sys.exit(65)
	else:
		shell.runShell()

if __name__ == "__main__": main()