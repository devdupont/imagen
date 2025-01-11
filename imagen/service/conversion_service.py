import shutil
import uuid
from collections.abc import AsyncIterator
from pathlib import Path

from PIL import Image

from imagen.config import cfg
from imagen.log import logger
from imagen.model.error import Error, ErrorCode
from imagen.model.image_data import ImageData
from imagen.service.image_embeddings.embedding_query import get_image_emb
from imagen.service.llava_client import describe
from imagen.service.text_embedding_service import create_text_embeddings


async def create_image_embeddings(images_path: Path, glob_expression: str = "*.png") -> AsyncIterator[ImageData]:
    if not images_path.exists():
        return
    for im in images_path.glob(glob_expression):
        yield await convert_single_image(im)


async def convert_single_image(im: Path) -> ImageData | None:
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
        return ImageData(new_image_path.name, description, image_embedding, embedding, new_image_path)
    return None


def copy_image_to_images_folder(im: Path) -> Path:
    """Copy an image to the image storage folder."""
    logger.info("Original image name: %s", im)
    prefix = str(uuid.uuid4())
    image_name = f"{prefix}_{im.name}"

    image_name_limit = 100
    if len(im.stem) > image_name_limit:
        image_name = f"{im.stem[:image_name_limit]}{im.suffix}"
    translation_table = str.maketrans(",+;", "   ")
    replaced_string = image_name.translate(translation_table)

    new_image = cfg.image_storage_folder / replaced_string

    if new_image.suffix == ".webp":
        new_image = new_image.parent / f"{new_image.stem}.png"
        logger.info("New image name: %s", new_image)
        convert_webp_to_png(im, new_image)
    else:
        logger.info("New image name: %s", new_image)
        shutil.copyfile(im, new_image)
    return new_image


def convert_webp_to_png(im: Path, new_image: Path):
    """Convert a WebP image to PNG format."""
    with Image.open(im) as img:
        # Convert the image to PNG and save it
        img.save(new_image, "PNG")


if __name__ == "__main__":
    from imagen.config import get_image_folder
    from imagen.model.image_data import convert_to_pyarrow

    images_path = get_image_folder()

    for image_data in create_image_embeddings(images_path):
        res = convert_to_pyarrow(image_data, False)
        print(type(res))
        break
