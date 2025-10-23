from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
import os

load_dotenv()  # Load environment variables from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Access environment variables

def generate_prompt(term: str) -> str: 
	"""Build a few-shot prompt that asks the model to return only the expansion in parentheses."""
	examples = """
		INPUT: SQL
		OUTPUT: (Structured Query Language)

		INPUT: HTTP
		OUTPUT: (Hypertext Transfer Protocol)

		INPUT: JSON
		OUTPUT: (JavaScript Object Notation

		INPUT: CPU
		OUTPUT: (Central Processing Unit)

		INPUT: API
		OUTPUT: (Application Programming Interface)
		""".strip()
	instructions = """
		Now translate the final input. Rules:
		- Return ONLY the full canonical expansion enclosed in parentheses, e.g. (Structured Query Language).
		- Correct spelling and capitalization.
		- If the input is empty or nonsensical, return (NO CONTENT).
		- If the input is not a computer technical term, return (NOT SUPPORTED).
		- If unknown, return (UNKNOWN TERM).
		""".strip()
	return f"""{examples}{instructions}
		INPUT: {term}
		OUTPUT:"""


def fewshot_prompt(prompt: str) -> None:
	"""Translates a computer technical term based on a prompt using the few-shot prompting technique."""
	
	prompt = generate_prompt(prompt)
	client = genai.Client(api_key=GEMINI_API_KEY)

	try:
		response = client.models.generate_content(
			model="gemini-2.5-flash",
			contents=prompt,
			config=types.GenerateContentConfig(
			temperature=0.0, # 0.0 Ensures deterministic output = no creativity
		)
	)
	except Exception as e:
		print(f"An error occurred: {e}")
		return
	print(response.text.strip())

if __name__ == "__main__":
	if len(sys.argv) == 2:
		fewshot_prompt(sys.argv[1])
	else:
		print("ERROR. Usage: python3 fewshot.py '<term>'")
		sys.exit(1)
	