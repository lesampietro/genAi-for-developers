from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_prompt_roleplay(destination: str) -> str:
	"""Returns a prompt based on a system role and a description as input, using XML tags."""
	SYSTEM_PROMPT = """You are a travel advisor wich speciality is to list the five main sightseeing spots of any city. After receiving a destination given by the user return a numbered list of the 5 best attractions in the city with NO additional text. You should not describe the city or the attractions. The answers must be translated in Portuguese. If the input is empty or nonsensical, return exactly: (NO CONTENT)."""
	return f"""<system_prompt>{SYSTEM_PROMPT}</system_prompt><input>{destination}</input>"""

def roleplay_prompt(input: str) -> None:
	"""Generates travel recommendations based on the user's destination input."""
	client = genai.Client(api_key=GEMINI_API_KEY)
	full_prompt = generate_prompt_roleplay(input)
	try:
		response = client.models.generate_content(
			model="gemini-2.5-flash",
			contents=full_prompt,
			config=types.GenerateContentConfig(
				temperature=0.0,
				thinking_config=types.ThinkingConfig(thinking_budget=0)
			)
		)
	except Exception as e:
		print(f"An error occurred: {e}")
		return
	print(response.text.strip())

if __name__ == "__main__":
	if len(sys.argv) == 2:
		roleplay_prompt(sys.argv[1])
	else:
		print("ERROR: Usage: python3 roleplay.py '<destination>'")
		sys.exit(1)