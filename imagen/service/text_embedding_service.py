from imagen.config import cfg
from imagen.service.nomic_embeddings import nomic_create_text_embeddings
from imagen.service.openai_embeddings import openai_create_text_embeddings


async def create_text_embeddings(text: str) -> list[float]:
    if cfg.openai_embeddings_model:
        return openai_create_text_embeddings(text)
    return await nomic_create_text_embeddings(text)
