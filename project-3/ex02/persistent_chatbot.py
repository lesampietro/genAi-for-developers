from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv
from datetime import datetime
from collections import deque
import string
import json
import os

class History(BaseModel):
	user: str | None = None
	assistant: str | None = None
	summary: str | None = None

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_PATH = os.path.join(os.path.dirname(__file__), "chat_history.json")
SYSTEM_PROMPT = "You are a helpful assistant that responds in Portuguese. Your tone of voice is friendly, engaging and informative. Your answers should be concise and take no more than 50 words. No need to use emojis!"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_db(path=DB_PATH):
	"""Loads the database from a JSON file."""
	if os.path.exists(path):
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)
	return {"interactions": [], "summaries": []}

def save_db(db, path=DB_PATH):
	"""Saves the database to a JSON file."""
	with open(path, "w", encoding="utf-8") as f:
		json.dump(db, f, ensure_ascii=False, indent=2)


def build_prompt(short_memory: list, long_memory: list, user_input: str) -> str:
	"""Builds the prompt including system prompt, long-term and short-term memory, and user input."""
	prompt = TIMESTAMP + "\n" + SYSTEM_PROMPT + "\n"
	if long_memory:
		prompt += "Long-term memory (summaries):\n"
		for item in long_memory:
			s = item.get("summary") if isinstance(item, dict) else str(item)
			prompt += f"- {s}\n"
		prompt += "\n"
	if short_memory:
		prompt += "Recent interactions:\n"
		for interaction in short_memory:
			prompt += f"User: {interaction['user']}\nAssistant: {interaction['assistant']}\n"
		prompt += "\n"
	prompt += f"User: {user_input}\nAssistant:"
	return prompt

def generate_summary(client, db, long_window):
	"""Generates a summary of the conversation every last 10 interactions and updates the database and long-term memory."""
	last_10 = db.get("interactions", [])[-10:]
	if not last_10:
		return None
	summary_prompt = (
		"Sum in Portuguese and concisely the main themes of the following conversation exchanges between user and assistant: " + "\n".join(f"User: {it['user']}\nAssistant: {it['assistant']}" for it in last_10)
		+ "\nSummary:"
	)
	response = client.models.generate_content(
		model="gemini-2.5-flash",
		contents=summary_prompt,
		config=types.GenerateContentConfig(temperature=0.0)
	)
	record = History(summary=response.text).model_dump()
	db.setdefault("summaries", []).append(record)
	long_window.append(record)
	return response.text

def persistent_chatbot() -> None:
	"""Initializes a chatbot with persistent memory, returning a summary every last 10 interactions."""
	client = genai.Client(api_key=GEMINI_API_KEY)
	db = load_db() # loads my database based on the path passed on the DB_PATH variable (set on load_db function)
	short_window = deque(maxlen=5) #maximum of 5 interactions stored
	long_window = deque(maxlen=10) #maximum of 10 interactions stored

	for it in db.get("interactions", [])[-5:]:
		short_window.append(it)
	for s in db.get("summaries", [])[-10:]:
		long_window.append(s)

	# Start chat loop
	while True:
		try:
			user_input = input("Q: ")
		except (EOFError, KeyboardInterrupt):
			print("\nA: Bye!.")
			break

		# Avoid empty prompts (better UX and API usage)
		if not user_input.strip():
			print("Digite algo (ou 'bye' para sair).")
			continue	
		# Normalize and verifies exit commands
		clean = user_input.lower().strip().strip(string.punctuation)
		if clean in {"bye", "exit", "tchau", "sair"}:
			print("A: Bye!.")
			break
		
		# Build prompt mixing long and short term memory
		short_memory = list(short_window)
		long_memory = list(long_window)
		prompt = build_prompt(short_memory, long_memory, user_input)

		# Try to get response with exponential backoff
		try:
			response = client.models.generate_content(
				model="gemini-2.5-flash",
				contents=prompt,
		   		config=types.GenerateContentConfig(temperature=0.0)
			)
		except Exception as e:
			print(f"ERROR. {type(e).__name__} - 429 RESOURCE_EXHAUSTED.\nA: Try again later.")
			break
		print(f'A: {response.text}')

		# Append the current interaction to short-term memory and database
		interaction = History(user=user_input, assistant=response.text).model_dump()
		db.setdefault("interactions", []).append(interaction)
		short_window.append(interaction)

		# Quando o total de interações for múltiplo de 10, gera resumo das últimas 10
		if len(db["interactions"]) % 10 == 0:
			summary_text = generate_summary(client, db, long_window)
			if summary_text:
				print(f"\n_ _ _\nHello! This is the Summary of last 10 interactions:\n {summary_text}\n_ _ _\n")
		save_db(db)

	save_db(db)


if __name__ == "__main__":
	persistent_chatbot()



#deque: double-ended queue, allows appending and popping from both ends. Good for managing a fixed-size history of interactions.