from openai import OpenAI
from app.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)

BATCH_SIZE = 50


def embed_query(query: str):
    """Embeds a single query using OpenAI embeddings."""

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    return response.data[0].embedding


def embed_texts(texts: list[str]):
    """Embeds a list of text strings in batches using OpenAI."""

    all_embeddings = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch
        )

        embeddings = [
            item.embedding
            for item in response.data
        ]

        all_embeddings.extend(embeddings)

    return all_embeddings