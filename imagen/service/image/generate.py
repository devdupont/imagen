from enum import StrEnum
from pathlib import Path

from openai import AsyncOpenAI

from imagen.config import cfg
from imagen.utils.download_utils import download_image_from_url

client = AsyncOpenAI(api_key=cfg.openai_api_key)


class Sizes(StrEnum):
    SQUARE = "1024x1024"
    PORTRAIT = "1024x1792"
    LANDSCAPE = "1792x1024"


async def generate_image(prompt: str, number_of_images: int = 1, size: Sizes = Sizes.SQUARE) -> list[Path]:
    response = await client.images.generate(
        # model=cfg.openai_image_model,
        prompt=prompt,
        n=number_of_images,  # Number of images to generate
        size=size.value,  # Size of the generated image,
        response_format="url",
    )
    return [d for image in response.data if image.url and (d := await download_image_from_url(image.url))]


if __name__ == "__main__":
    import asyncio

    images = asyncio.run(generate_image("Generate an image of a futuristic spaceship flying past the planet of Saturn"))
    for im in images:
        print(im)
