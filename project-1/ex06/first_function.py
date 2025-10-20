import sys

def greeting(name: str = '42') -> None:
	"""receives a name as an argument form the command line and prints a greeting. if no names are passed, uses '42' as default"""
	print(f"Hello, {name}!")

if __name__ == "__main__":
	if len(sys.argv) > 1:
		for arg in sys.argv[1:]:
			greeting(arg)
	else:
		greeting()