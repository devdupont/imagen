from enum import StrEnum
from pathlib import Path

import lancedb  # type: ignore

from imagen.config import cfg
from imagen.log import logger
from imagen.model.image import Image
from imagen.service.conversion_service import (
    convert_single_image,
)
from imagen.utils.file_utils import unlink_file

DB = lancedb.connect(cfg.lance_db_location)
try:
    TBL = DB.open_table(cfg.lance_table_image)
except FileNotFoundError:
    TBL = DB.create_table(cfg.lance_table_image, schema=Image.schema)


class DISTANCE(StrEnum):
    EUCLIDEAN = "l2"
    COSINE = "cosine"
    DOT = "dot"


def execute_knn_search(
    embedding: list[float],
    vector_column_name: str,
    limit: int = 10,
    distance: str = DISTANCE.EUCLIDEAN,
) -> list[Image]:
    data: list[dict] = (
        TBL.search(embedding, query_type="vector", vector_column_name=vector_column_name)
        .metric(distance)
        .limit(limit)
        .to_list()
    )
    return [Image.from_vdb(d) for d in data]


def sql_escape(text: str) -> str:
    return text.replace("'", "''")


def convert_vec_to_literal(float_list: list[float]) -> list[str]:
    return [str(v) for v in float_list]


def get_first_result(image: Image) -> Image | None:
    """Get the first result from the database."""
    try:
        return execute_knn_search(image.image_embedding, image.field.image_vector, 1)[0]
    except IndexError:
        return None


def save_image(image: Image, *, ignore_update: bool = False) -> bool:
    result = get_first_result(image)
    image_available = image.matching_vector(result) if result else False
    if not image_available:  # insert
        logger.info("Creating %s", image.name)
        TBL.add(image.to_pyarrow())
        return True
    logger.info("Updating %s", image.name)
    if result and not ignore_update:
        single_value = {
            image.field.text_vector: convert_vec_to_literal(result.text_embedding),
            image.field.description: sql_escape(result.description),
            image.field.image_vector: convert_vec_to_literal(result.image_embedding),
            image.field.updated: result.updated,
        }
        filter_expression = f"{image.field.name} = '{result.name}'"
        if image.image_path:
            # The file was uploaded again. Keep the old file to avoid dups.
            unlink_file(cfg.image_path / image.name)
        TBL.update(where=filter_expression, values=single_value)
    return False


async def save_image_from_path(image_path: Path) -> bool:
    if not image_path.exists():
        msg = f"Could not find original image path: {image_path}"
        raise FileNotFoundError(msg)
    image_data = await convert_single_image(image_path)
    if image_data is None:
        msg = f"Image description is missing for {image_path}"
        raise ValueError(msg)
    return save_image(image_data)
