"""Client for the LLAVA service."""

from pathlib import Path

import aiohttp

from imagen.config import cfg
from imagen.model.error import Error
from imagen.utils.image import encode_image


async def describe(image_path: Path, prompt: str = "What is in this picture?") -> str | Error:
    """Create a description for an image at the given path using a specified prompt."""
    data = {
        "model": "llava",
        "prompt": prompt,
        "stream": False,
        "images": [encode_image(image_path)],
    }
    generate_url = f"{cfg.ollama_base_url}/generate"
    return await _post(data, generate_url, "response")


async def embeddings(image_path: Path, description: str) -> list[float] | Error:
    """Create embeddings for an image at the given path using a specified description."""
    data = {"model": "llava", "prompt": description, "images": encode_image(image_path)}
    embeddings_url = f"{cfg.ollama_base_url}/embeddings"
    return await _post(data, embeddings_url, "embedding")


async def _post(data: dict, url: str, key: str) -> list[float] | str | Error:
    """Make a POST request and just return the value of the key from the response."""
    async with aiohttp.ClientSession() as session, session.post(url, json=data) as resp:
        if resp.status >= 200 and resp.status < 300:
            json_res = await resp.json()
            if key in json_res:
                return json_res[key]
            return Error(code=resp.status, message="Failed to extract response")
        return Error(code=resp.status, message=await resp.text())


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
            if type(embs) != Error:
                print("Embeddings length: ", len(embs))
