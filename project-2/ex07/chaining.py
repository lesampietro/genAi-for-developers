from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_detailed_description_prompt(product: str) -> str:
	"""Builds and returns a detailed description based on a system role, examples, instructions and a product as input, using XML tags."""
	SYSTEM_PROMPT = """
		You are a creative salesperson. Given a product name provided by the user, generate a detailed and engaging description that highlights its features, benefits, and potential uses. The description should be persuasive and tailored to attract potential buyers.
		"""
	EXAMPLES = """
		INPUT: "fone de ouvido sem fio"
		OUTPUT: Descubra o futuro do som com nossos Fones de Ouvido Sem Fio, desenvolvidos para quem busca qualidade de áudio excepcional e total liberdade de movimento. Com tecnologia Bluetooth 5.0 avançada para conexões rápidas e estáveis, esses fones oferecem até 20 horas de reprodução contínua e um som imersivo de alta fidelidade. Com cancelamento ativo de ruído, almofadas auriculares ergonômicas e um design leve e ajustável, você aproveita um áudio nítido e envolvente por horas sem desconforto. O microfone embutido garante chamadas com clareza cristalina, enquanto os controles por toque permitem ajustar o volume, trocar faixas e atender chamadas com facilidade. Além disso, sua resistência à água e ao suor (IPX5) os torna perfeitos para treinos e atividades ao ar livre. Seja para trabalhar, se exercitar, viajar ou relaxar, esses fones de ouvido sem fio são o companheiro ideal. Elegantes, modernos e versáteis, oferecem o equilíbrio perfeito entre conforto, estilo e desempenho para qualquer ocasião. Adquira o seu hoje mesmo e experimente o som sem limites!
		"""
	INSTRUCTIONS = """
		Now follow theses rules to generate the product description:
		- Return ONLY a paragraph of plain text.
		- DO NOT separate the text in topics or use bullet points.
		- DO NOT use special characters to highlight parts of the text.
		- Correct spelling and grammar.
		- If the input is in any other language than Portuguese, return the translated output in Portuguese.
		- If the input is empty or nonsensical, return (NO CONTENT).
		""".strip()
	return f"""<system_prompt>{SYSTEM_PROMPT}</system_prompt><examples>{EXAMPLES}</examples><instructions>{INSTRUCTIONS}</instructions><input>{product}</input>"""

def generate_short_ad_prompt(description: str) -> str:
	"""Builds and returns a short ad text based on a system role, examples and a detailed description as input, using XML tags."""
	SYSTEM_PROMPT = """You are an advertiser. Your job is to convert the given detailed description into a short and creative advertising text."""
	EXAMPLES = """
	INPUT: Liberte-se dos fios e mergulhe em uma experiência sonora incomparável com nossos Fones de Ouvido Sem Fio de última geração. Projetados para o audiófilo moderno, eles contam com a avançada tecnologia Bluetooth 5.3, garantindo uma conexão ultrarrápida e estável, com zero latência para suas músicas, podcasts e chamadas. Desfrute de um áudio cristalino e graves profundos, impulsionado por drivers de alta performance, enquanto o cancelamento ativo de ruído superior o isola do mundo exterior, permitindo que você se concentre totalmente no que importa. Com uma bateria de longa duração que oferece até 30 horas de reprodução contínua e um estojo de carregamento compacto que adiciona horas extras, sua música nunca mais irá parar. O design ergonômico, leve e com almofadas macias proporciona conforto excepcional para uso prolongado, e os controles por toque intuitivos permitem gerenciar suas faixas, volume e chamadas sem esforço. Equipados com microfones duplos para chamadas em HD e certificação IPX7 de resistência à água e ao suor, são o companheiro perfeito para seus treinos intensos, viagens diárias ou momentos de relaxamento. Escolha a liberdade, o conforto e a qualidade de som premium que você merece.

	OUTPUT: Experimente a liberdade sem fio com nossos Fones de Ouvido Sem Fio de última geração. Com Bluetooth 5.3, áudio cristalino e até 30 horas de reprodução, eles são perfeitos para qualquer ocasião.
	""".strip()
	return f"""<system_prompt>{SYSTEM_PROMPT}</system_prompt><examples>{EXAMPLES}</examples><input>{description}</input>"""

def generate_translated_output(description: str) -> str:
	"""Builds and returns a translated text based on examples, instructions and a short advertising text as input, using XML tags."""
	EXAMPLES = """
	INPUT: Experimente a liberdade sem fio com nossos Fones de Ouvido Sem Fio de última geração. Com Bluetooth 5.3, áudio cristalino e até 30 horas de reprodução, eles são perfeitos para qualquer ocasião.

	OUTPUT: Experience the wireless freedom with our next-generation Wireless Earbuds. With Bluetooth 5.3, crystal-clear audio, and up to 30 hours of playback, they're perfect for any occasion.
	""".strip()
	INSTRUCTIONS = """
		Now follow theses rules to translate the input text:
		- Return ONLY the translated text in English, without "OUTPUT:".
		- DO NOT create or add any text.
		- DO NOT use special characters to highlight parts of the text.
		- Correct spelling and grammar.
		""".strip()
	return f"""<examples>{EXAMPLES}</examples><instructions>{INSTRUCTIONS}</instructions><input>{description}</input>"""

def chained_prompts(prompt: str) -> None:
	"""Generates advertisement content based on chained prompting technique."""
	client = genai.Client(api_key=GEMINI_API_KEY)
	first_prompt = generate_detailed_description_prompt(prompt)
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