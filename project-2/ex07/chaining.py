from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_detailed_description_prompt(product: str) -> str:
	"""Builds and returns a detailed description based on a system role, examples, instructions and a product as input, using XML tags."""
	SYSTEM_PROMPT_SALESPERSON = os.getenv("SYSTEM_PROMPT_SALESPERSON")
	EXAMPLES_LONG_DESCRIPTION = os.getenv("EXAMPLES_LONG_DESCRIPTION")
	INSTRUCTIONS = os.getenv("INSTRUCTIONS")
	return f"""<system_prompt>{SYSTEM_PROMPT_SALESPERSON}</system_prompt><examples>{EXAMPLES_LONG_DESCRIPTION}</examples><instructions>{INSTRUCTIONS}</instructions><input>{product}</input>"""

def generate_short_ad_prompt(description: str) -> str:
	"""Builds and returns a short ad text based on a system role, examples and a detailed description as input, using XML tags."""
	SYSTEM_PROMPT_ADVERTISER = os.getenv("SYSTEM_PROMPT_ADVERTISER")
	EXAMPLES_SHORT_AD = os.getenv("EXAMPLES_SHORT_AD")
	INSTRUCTIONS = os.getenv("INSTRUCTIONS")
	return f"""<system_prompt>{SYSTEM_PROMPT_ADVERTISER}</system_prompt><examples>{EXAMPLES_SHORT_AD}</examples><instructions>{INSTRUCTIONS}</instructions><input>{description}</input>"""

def generate_translated_output(description: str) -> str:
	"""Builds and returns a translated text based on examples, instructions and a short advertising text as input, using XML tags."""
	EXAMPLES_EN_TRANSLATION = os.getenv("EXAMPLES_EN_TRANSLATION")
	INSTRUCTIONS_TRANSLATION = os.getenv("INSTRUCTIONS_TRANSLATION")
	return f"""<examples>{EXAMPLES_EN_TRANSLATION}</examples><instructions>{INSTRUCTIONS_TRANSLATION}</instructions><input>{description}</input>"""

def chained_prompts(prompt: str) -> None:
	"""Generates advertisement content based on chained prompting technique."""
	client = genai.Client(api_key=GEMINI_API_KEY)
	first_prompt = generate_detailed_description_prompt(prompt)/nfs/homes/letsampi/project-2/ex07/chaining.py
	try:
		response1 = client.models.generate_content(
			model="gemini-2.5-flash",
			contents=first_prompt,
			config=types.GenerateContentConfig(
				temperature=1.0,
				thinking_config=types.ThinkingConfig(thinking_budget=1)
			)
		)
	except Exception as e:
		print(f"An error occurred: {e}")
		return
	print(response1.text.strip())
	print("_ _ _\n")
	second_prompt = generate_short_ad_prompt(response1.text.strip())
	try:
		response2 = client.models.generate_content(
			model="gemini-2.5-flash",
			contents=second_prompt,
			config=types.GenerateContentConfig(
				temperature=1.5,
				thinking_config=types.ThinkingConfig(thinking_budget=0)
			)
		)
	except Exception as e:
		print(f"An error occurred: {e}")
		return
	print(response2.text.strip())
	print("_ _ _\n")
	third_prompt = generate_translated_output(response2.text.strip())
	try:
		response3 = client.models.generate_content(
			model="gemini-2.5-flash",
			contents=third_prompt,
			config=types.GenerateContentConfig(
				temperature=0.0,
				thinking_config=types.ThinkingConfig(thinking_budget=0)
			)
		)
	except Exception as e:
		print(f"An error occurred: {e}")
		return
	print(response3.text.strip())


if __name__ == "__main__":
	if len(sys.argv) == 2:
		chained_prompts(sys.argv[1])
	else:
		print("ERROR. Usage: python3 chaining.py '<product_name>'")
		sys.exit(1)