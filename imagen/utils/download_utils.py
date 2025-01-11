from pathlib import Path
from urllib.parse import urlparse

import aiofiles
import aiohttp

from imagen.config import cfg
from imagen.log import logger


async def download_image_from_url(url: str) -> Path | None:
    parsed = urlparse(url)
    image_name = parsed.path.split("/")[-1]
    return await download_image(url, image_name)


async def download_image(url: str, image_name: str) -> Path | None:
    async with aiohttp.ClientSession() as session, session.get(url) as response:
        # Ensure the request was successful
        if response.status == 200:
            # Read the content of the response
            content = await response.read()
            filepath = cfg.image_storage_folder / image_name
            # Open a file in binary write mode and save the content to it
            async with aiofiles.open(filepath, "wb") as file:
                await file.write(content)
            return filepath
        logger.error(f"Failed to download image. Status code: {response.status}")
        return None
