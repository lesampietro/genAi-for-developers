from google import genai
from google.genai import types
from dotenv import load_dotenv # Manages environment variables
import sys
import os

load_dotenv()  # Load environment variables from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Access environment variables

def first_prompt(prompt: str, temperature: float) -> None:
	"""Generates content based on a prompt and temperature setting."""
	client = genai.Client(api_key=GEMINI_API_KEY)
	response = client.models.generate_content(
		model="gemini-2.5-flash", 
		contents=prompt,
		config=types.GenerateContentConfig(
			temperature=temperature, #Optional: controls the randomness of the output. Values can range from [0.0, 2.0].
			thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
		)
	)
	print(response.text)

if __name__ == "__main__":
	if len(sys.argv) == 3:
		first_prompt(sys.argv[1], float(sys.argv[2]))
	else:
		print("ERROR. Usage: python3 prompt.py '<prompt>' <temperature>")
		sys.exit(1)
	