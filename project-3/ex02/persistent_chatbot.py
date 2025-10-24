from google import genai
from google.genai import types
from dotenv import load_dotenv
import string
import os
import json
from collections import deque
from datetime import datetime

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_PATH = "./chat_history.json"
SYSTEM_PROMPT = "You are a helpful assistant that responds in Portuguese. Your answers are always concise and take no more than 50 words."
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_db(path=DB_PATH):
	if os.path.exists(path):
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)
	return {"interactions": [], "summaries": []}

def save_db(db, path=DB_PATH):
	with open(path, "w", encoding="utf-8") as f:
		json.dump(db, f, ensure_ascii=False, indent=2)


def build_prompt(short_memory: list, long_memory: list, user_input: str) -> str:
	prompt = TIMESTAMP + "\n" + SYSTEM_PROMPT + "\n"
	if long_memory:
		prompt += "Long-term memory:\n"
		for item in long_memory:
			prompt += f"- {item}\n"
		prompt += "\n"
	if short_memory:
		prompt += "Recent interactions:\n"
		for interaction in short_memory:
			prompt += f"User: {interaction['user']}\nAssistant: {interaction['assistant']}\n"
		prompt += "\n"
	prompt += f"User: {user_input}\nAssistant:"
	return prompt

def print_summary(interaction_count: int) -> None:
		# Build summary prompt
		summary_prompt = "Summarize the following interactions in Portuguese, focusing on key points. Keep it under 50 words.\n\n"
		for it in list(short_window):
			summary_prompt += f"User: {it['user']}\nAssistant: {it['assistant']}\n"
		# Get summary from the model
		summary_response = client.models.generate_content(
			model="gemini-2.5-flash",
			contents=summary_prompt,
		   	config=types.GenerateContentConfig(temperature=0.0)
		)
		summary_text = summary_response.text.strip()
		print(f"\n[Summary Generated]: {summary_text}\n")
		# Update long-term memory and database
		long_window.append(summary_text)
		db["summaries"].append(summary_text)

def persistent_chatbot() -> None:
	"""Initializes a chatbot with persistent memory, returning a summary every last 10 interactions."""
	client = genai.Client(api_key=GEMINI_API_KEY)
	db = load_db()
	short_window = deque(maxlen=5) #maximum of 5 interactions stored
	long_window = deque(maxlen=10) #maximum of 10 interactions stored

	for it in db.get("interactions", [])[-5:]:
		short_window.append(it)
	for s in db.get("summaries", [])[-10:]:
		long_window.append(s)

	interaction_since_last_summary = 0

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
			print(f"ERROR. {type(e).__name__} - 429 RESOURCE_EXHAUSTED.\n")
			break
		print(f'A: {response.text}')

		# Append the current interaction to short-term memory and database
		interaction = {"user": user_input, "assistant": response.text}
		db["interactions"].append(interaction)
		short_window.append(interaction)
		
		# interaction_since_last_summary += 1
		interaction_since_last_summary = len(db.get("interactions", [])) % 10
		# Every 10 interactions, generate a summary and update long-term memory
		if interaction_since_last_summary >= 10:
			print_summary()
		
		
		save_db(db)
	
	save_db(db)



if __name__ == "__main__":
	persistent_chatbot()



#deque: double-ended queue, allows appending and popping from both ends. Good for managing a fixed-size history of interactions.