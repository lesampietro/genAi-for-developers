import sys

if __name__ == "__main__":
	if len(sys.argv) > 1:
		for arg in sys.argv[1:]:
			print(arg)
	else:
		nl = "\n"
		print(f"Error: no arguments were passed.{nl}Usage example: python arguments.py <arg1> <arg2> ...") 