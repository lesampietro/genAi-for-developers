my_dict = {
	'item1': 1,
	'item2': 2,
	'item3': 3,
	'item4': 4,
}

def	print_my_dict(dictionary: dict[str, int]) -> None:
	"""receives a dictionary and prints a list of key + value as strings, one str per line"""
	dict_list = [f'{key} {value}' for key, value in dictionary.items()]
	for item in dict_list:
		print(item)

if __name__ == "__main__":
   print_my_dict(my_dict)