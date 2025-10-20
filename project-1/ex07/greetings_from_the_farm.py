import  sys
import  cowsay # type: ignore

def greetings_from_the_farm(name: str = "42") -> None:
	"""receives a name as an argument form the command line and prints a greeting using a cowsay character. if no names are passed, uses '42' as default"""
	cowsay.cow(f"Hello, {name}!")


if __name__ == "__main__":
	if len(sys.argv) > 1:
		for arg in sys.argv[1:]:
			greetings_from_the_farm(arg)
	else:
		greetings_from_the_farm()
