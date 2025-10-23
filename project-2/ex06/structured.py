from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_json_prompt(person_details: str) -> str:
	"""Builds and returns structured output based on a system role, examples, formatting instruction and a person's details as input, using XML tags."""
	SYSTEM_PROMPT = """You are a secretary that registers people's main information in a database. After receiving a person's details given by the user, return a JSON object with the following fields: name, age, ocupation and address. The output MUST be in Portuguese, single-line and itens should be separated bu comma. If any information is missing, use null as the value. If the input is empty or nonsensical, return exactly: (NO CONTENT)."""
	EXAMPLES = """
	INPUT: "Charlotte Emma Aitchison, 33 anos, é cantora e mora em Londres"
	OUTPUT: {
		"nome": "Charlotte Emma Aitchison",
		"idade": 33,
		"profissão": "cantora",
		"cidade": "Londres"
	}
	INPUT: "Maria Menezes, 28, designer, vive no Rio de Janeiro"
	OUTPUT: {
		"nome": "Maria Menezes",
		"idade": 28,
		"profissão": "designer",
		"cidade": "Rio de Janeiro"
	}
	INPUT: "Lucas Silva e Silva, 45 anos, é apresentador e mora em São Paulo"
    OUTPUT: {
        "nome": "Lucas Silva e Silva",
        "idade": 45,
        "profissão": "apresentador",
        "cidade": "São Paulo"
    }
	"""
	FORMAT = """Return ONLY valid JSON"""
	return f"""<system_prompt>{SYSTEM_PROMPT}</system_prompt><examples>{EXAMPLES}</examples><formatting>{FORMAT}</formatting><input>{person_details}</input>"""

def json_output(prompt: str) -> None:
	"""Generates JSON output based on user input."""
	client = genai.Client(api_key=GEMINI_API_KEY)
	full_prompt = generate_json_prompt(prompt)
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
		json_output(sys.argv[1])
	else:
		print("ERROR. Usage: python3 structured.py '<person-details>'")
		sys.exit(1)