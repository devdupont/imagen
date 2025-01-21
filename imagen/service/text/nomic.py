import aiohttp

from imagen.config import cfg
from imagen.log import logger


async def text_embeddings(prompt: str) -> list[float]:
    """
    Asynchronously creates text embeddings using a specified model.

    Args:
    prompt (str): The text prompt to create embeddings for.

    Returns:
    Union[List[float], None]: A list of float embeddings if successful, None otherwise.
    """
    url = f"{cfg.ollama_base_url}/embeddings"
    data = {"model": cfg.nomic_embed_model, "prompt": prompt}
    logger.debug("embeddings input: %s", data)
    async with aiohttp.ClientSession() as session, session.post(url, json=data) as resp:
        response_json: dict = await resp.json()
        embeddings: list[float] = response_json["embedding"]
        return embeddings


if __name__ == "__main__":
    import asyncio

    embeddings = asyncio.run(text_embeddings("is a large context length text encoder that surpasses OpenAI"))

    assert isinstance(embeddings, list)
    print("size", len(embeddings))
