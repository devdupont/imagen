"""Text embedding services."""

from imagen.config import cfg
from imagen.service.text.nomic import text_embeddings as nomic_text_embeddings
from imagen.service.text.openai import text_embeddings as openai_text_embeddings


async def text_embeddings(text: str) -> list[float]:
    """Return text embeddings."""
    if cfg.openai_embeddings_model:
        return openai_text_embeddings(text)
    return await nomic_text_embeddings(text)
