import shutil
import uuid
from collections.abc import AsyncIterator
from pathlib import Path

from PIL import Image as PILImage

from imagen.config import cfg
from imagen.log import logger
from imagen.model.error import Error, ErrorCode
from imagen.model.image import Image
from imagen.service.image_embeddings.embedding_query import get_image_emb
from imagen.service.llava_client import describe
from imagen.service.text_embedding_service import create_text_embeddings


async def create_image_embeddings(images_path: Path, glob_expression: str = "*.png") -> AsyncIterator[Image]:
    if not images_path.exists():
        return
    for im in images_path.glob(glob_expression):
        yield await convert_single_image(im)


async def convert_single_image(im: Path) -> Image | None:
    logger.info(f""" ===== {im.as_posix()} =====""")
    logger.info(f"Image exists: {im.exists()}")

    new_image_path = copy_image_to_images_folder(im)
    if not new_image_path.exists():
        return Error(
            code=ErrorCode.NOT_FOUND,
            message=f"Could not find new image path: {im}",
        )

    description = await describe(new_image_path)
    logger.info(f"description: {description}\n")

    if description is not None and type(description) is not Error:
        image_embedding = get_image_emb(im)
        embedding = await create_text_embeddings(description)
        return Image(new_image_path.name, description, image_embedding, embedding, new_image_path)
    return None


NAME_LIMIT = 100
NAME_TRANS = str.maketrans(",+;", "   ")


def copy_image_to_images_folder(im: Path) -> Path:
    """Copy an image to the image storage folder."""
    logger.info("Original image name: %s", im)
    name = f"{uuid.uuid4()}_{im.name}"
    if len(im.stem) > NAME_LIMIT:
        name = f"{im.stem[:NAME_LIMIT]}{im.suffix}"
    new_image: Path = cfg.image_path / name.translate(NAME_TRANS)
    if new_image.suffix == ".webp":
        new_image = new_image.parent / f"{new_image.stem}.png"
        logger.info("New image name: %s", new_image)
        convert_webp_to_png(im, new_image)
    else:
        logger.info("New image name: %s", new_image)
        shutil.copyfile(im, new_image)
    return new_image


def convert_webp_to_png(im: Path, new_image: Path) -> None:
    """Convert a WebP image to PNG format."""
    with PILImage.open(im) as img:
        # Convert the image to PNG and save it
        img.save(new_image, "PNG")


if __name__ == "__main__":
    import asyncio as aio

    from imagen.config import cfg

    async def test_convert() -> None:
        async for image in create_image_embeddings(cfg.image_load_path):
            res = image.to_pyarrow()
            print(type(res))
            break

    aio.run(test_convert())
