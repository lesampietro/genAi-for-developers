my_list = ['item1', 'item2', 'item3', 'item4']

def print_my_list(my_list: list[str]) -> None:
	"""receives a list and prints item by item, one per line"""
	for item in my_list:
		print(item)

if __name__ == "__main__":
   print_my_list(my_list)