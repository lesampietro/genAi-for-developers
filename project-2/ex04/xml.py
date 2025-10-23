from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_xml_tagged_prompt(text: str) -> str: 
	"""Builds a prompt with examples, instructions and a text as input, using XML tags."""
	EXAMPLES = """
		INPUT: Durante a Idade Média, as universidades europeias surgiram como centros de conhecimento, reunindo estudiosos de diversas áreas. Elas desempenharam papel essencial na preservação e transmissão de saberes clássicos, além de estimular debates filosóficos e científicos que moldaram o pensamento ocidental e prepararam terreno para o Renascimento.
		OUTPUT: Universidades medievais preservaram saber clássico, promoveram debates e criaram base intelectual que impulsionou o Renascimento europeu.
		""".strip()
	INSTRUCTIONS = """
		Now sum the final input. Rules:
		- Return ONLY the concise summary of the input text.
		- Correct spelling and grammar.
		- If the input is empty or nonsensical, return (NO CONTENT).
		- Output maximum length is 20 words.
		""".strip()
	return f"""<examples>{EXAMPLES}</examples><instructions>{INSTRUCTIONS}</instructions><input>{text}</input>"""


def sum_text(prompt: str) -> None:
	"""Generates a summary of the input text."""
	prompt = generate_xml_tagged_prompt(prompt)
	client = genai.Client(api_key=GEMINI_API_KEY)
	try:
		response = client.models.generate_content(
			model="gemini-2.5-flash",
			contents=prompt,
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
		sum_text(sys.argv[1])
	else:
		print("ERROR. Usage: python3 xml.py '<text>'")
		sys.exit(1)


