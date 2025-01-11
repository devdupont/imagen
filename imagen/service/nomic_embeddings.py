import aiohttp

from imagen.config import cfg
from imagen.log import logger


async def nomic_create_text_embeddings(prompt: str) -> list[float] | None:
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

    # Use aiohttp.ClientSession for making HTTP requests
    async with aiohttp.ClientSession() as session, session.post(url, json=data) as response:
        # Check if the request was successful
        if response.status == 200:
            response_json: dict = await response.json()
            # Extract the embeddings key
            return response_json.get("embedding")
        logger.error(f"Error: Received response code {response.status}")
        return None


if __name__ == "__main__":
    import asyncio

    embeddings = asyncio.run(
        nomic_create_text_embeddings("is a large context length text encoder that surpasses OpenAI")
    )

    assert isinstance(embeddings, list)
    print("size", len(embeddings))
