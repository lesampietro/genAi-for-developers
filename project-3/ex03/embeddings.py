import sys
from sentence_transformers import SentenceTransformer
import numpy as np


SENTENCES = [
    "O cachorro correu pelo parque atrás da bola azul.",
    "Ontem a bolsa de valores fechou em queda após anúncio do governo.",
    "O vulcão entrou em erupção, iluminando o céu noturno com lava.",
    "Aprender programação em Python pode abrir muitas portas no mercado de trabalho.",
    "O café recém-moído tem um aroma que desperta memórias da infância.",
    "Cientistas descobriram uma nova espécie de peixe em águas profundas.",
    "A final da Copa foi decidida nos pênaltis, com muita emoção na torcida.",
    "O conceito de buracos negros desafia nossa compreensão do espaço-tempo.",
    "O artista usou realidade aumentada para criar uma exposição interativa.",
    "A meditação diária ajuda a reduzir o estresse e aumentar a concentração."
]


def main():
    if len(sys.argv) < 2:
        print('ERROR. Usage: python3 embeddings.py "<term>"')
        sys.exit(1)

    query = " ".join(sys.argv[1:]).strip()

    # Loads the model. This download can be slow on first execution.
    model = SentenceTransformer("all-mpnet-base-v2")

    # Encode and normalize embeddings to use dot product as cosine_similarity
    texts = SENTENCES + [query]
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

    sentences_embeds = embeddings[:-1]
    query_embeds = embeddings[-1]

    # Similarity by internal product (vectors already normalized -> cosine)
    sims = np.dot(sentences_embeds, query_embeds)

    # Top-k
    k = min(3, len(SENTENCES))
    top_idx = np.argsort(-sims)[:k]

    for idx in top_idx:
        print(f"{SENTENCES[int(idx)]} (score: {sims[int(idx)]:.4f})")


if __name__ == "__main__":
    main()