from google import genai
from google.genai import types
from dotenv import load_dotenv
import string
import os
from collections import deque
from datetime import datetime

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def first_chatbot() -> None:
	"""Initializes a chatbot session saving the history of last 5 interactions."""
	client = genai.Client(api_key=GEMINI_API_KEY)
	chat = client.chats.create(model="gemini-2.5-flash")
	history = deque(maxlen=5) #maximum of 5 interactions stored
	system_prompt = "You are a helpful assistant that responds in Portuguese. Your answers are always concise and take no more than 50 words."
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	while True:
		try:
			user_input = input("Q: ")
		except (EOFError, KeyboardInterrupt):
			print("\nA: Bye!.")
			break

		# Avoid empty prompts (better UX and API usage)
		user_input = user_input.strip()
		if not user_input:
			print("Digite algo (ou 'bye' para sair).")
			continue
		
		# Normalize and verifies exit commands
		clean = user_input.lower().strip().strip(string.punctuation)
		if clean in {"bye", "exit", "tchau", "sair"}:
			print("A: Bye!.")
			break
		
		user_input = f"{timestamp}\n{system_prompt}\nUser: {user_input}\nAssistant:"

		context_parts = [] #creating a list to hold context strings
		for item in history:
			context_parts.append(f"User: {item['user']}\nAssistant: {item['assistant']}")
			context_text = "\n".join(context_parts)
			if context_text:
				user_input = f"{timestamp}\n{system_prompt}\n{context_text}\nUser: {user_input}\nAssistant:"

		try:
			response = chat.send_message(user_input)
		except Exception as e:
			print(f"Error: {type(e).__name__} - 429 RESOURCE_EXHAUSTED.\nA: Please try again later.")
			break			
		print(f'A: {response.text}')

		# Append the current interaction to history
		history.append({
			"user": user_input,
			"assistant": response.text,
		})



if __name__ == "__main__":
	first_chatbot()



#deque: double-ended queue, allows appending and popping from both ends. Good for managing a fixed-size history of interactions.