from pathlib import Path
from urllib.parse import urlparse

import aiofiles
import aiohttp

from imagen.config import cfg
from imagen.log import logger


async def download_image_from_url(url: str) -> Path | None:
    """Download an image from a URL."""
    parsed = urlparse(url)
    name = parsed.path.split("/")[-1]
    return await download_image(url, name)


async def download_image(url: str, name: str) -> Path | None:
    """Download an image from a URL."""
    async with aiohttp.ClientSession() as session, session.get(url) as response:
        # Ensure the request was successful
        if response.status == 200:
            # Read the content of the response
            content = await response.read()
            path = cfg.image_path / name
            # Open a file in binary write mode and save the content to it
            async with aiofiles.open(path, "wb") as file:
                await file.write(content)
            return path
        logger.error(f"Failed to download image. Status code: {response.status}")
        return None
