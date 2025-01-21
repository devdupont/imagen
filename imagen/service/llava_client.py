"""Client for the LLAVA service."""

from pathlib import Path

import aiohttp

from imagen.config import cfg
from imagen.utils.image import encode_image


async def describe(image_path: Path, prompt: str = "What is in this picture?") -> str:
    """Create a description for an image at the given path using a specified prompt."""
    data = {
        "model": "llava",
        "prompt": prompt,
        "stream": False,
        "images": [encode_image(image_path)],
    }
    resp = await _post(data, "generate")
    text: str = resp["response"]
    return text


async def embeddings(image_path: Path, description: str) -> list[float]:
    """Create embeddings for an image at the given path using a specified description."""
    data = {"model": "llava", "prompt": description, "images": encode_image(image_path)}
    resp = await _post(data, "embeddings")
    vector: list[float] = resp["embedding"]
    return vector


async def _post(data: dict, route: str) -> dict:
    """Make a POST request and just return the value of the key from the response."""
    url = f"{cfg.ollama_base_url}/{route}"
    async with aiohttp.ClientSession() as session, session.post(url, json=data) as resp:
        output: dict = await resp.json()
    return output


if __name__ == "__main__":
    import asyncio
    import sys

    images_path = Path("./images")
    if not images_path.exists():
        images_path = Path("./multimodal_experiments/images")
        if not images_path.exists():
            print("Cannot find the images", file=sys.stderr)
            sys.exit(1)

    for im in images_path.glob("*.png"):
        print(f""" ===== {im.name} =====""")
        description = asyncio.run(describe(im))
        print(description)
        print()
        if description is not None:
            embs = asyncio.run(embeddings(im, description))
            print("Embeddings length: ", len(embs))
