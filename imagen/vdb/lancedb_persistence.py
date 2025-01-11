from enum import StrEnum
from pathlib import Path

import lancedb
import numpy as np

from imagen.config import cfg
from imagen.log import logger
from imagen.model.error import Error, ErrorCode
from imagen.model.image_data import ImageData, convert_to_pyarrow
from imagen.service.conversion_service import (
    convert_single_image,
)
from imagen.utils.file_utils import unlink_file
from imagen.vdb.imagedb_schema import (
    FIELD_CREATE_TIMESTAMP,
    FIELD_IMAGE_DESCRIPTION,
    FIELD_IMAGE_NAME,
    FIELD_IMAGE_VECTOR,
    FIELD_TEXT_VECTOR,
    FIELD_UPDATE_TIMESTAMP,
    schema,
)


class DISTANCE(StrEnum):
    EUCLIDEAN = "l2"
    COSINE = "cosine"
    DOT = "dot"


def execute_knn_search(
    embedding: list[float],
    vector_column_name: str,
    limit: int = 10,
    distance: str = DISTANCE.EUCLIDEAN,
) -> list[dict]:
    return (
        tbl.search(embedding, query_type="vector", vector_column_name=vector_column_name)
        .metric(distance)
        .limit(limit)
        .to_list()
    )


def init_image_vector_table() -> lancedb.table.LanceTable:
    db = lancedb.connect(cfg.lance_db_location)
    table_name = cfg.lance_table_image
    try:
        return db.open_table(table_name)
    except FileNotFoundError:
        logger.warning("Could not open database. It does not exist.")
        return db.create_table(table_name, schema=schema)


tbl = init_image_vector_table()


def sql_escape(text: str) -> str:
    return text.replace("'", "''")


def convert_vec_to_literal(float_list: list[float]) -> list[str]:
    return [str(v) for v in float_list]


def save_image(image_data: ImageData, *, ignore_update: bool = False) -> bool:
    results = execute_knn_search(image_data.image_embedding, FIELD_IMAGE_VECTOR, 1)
    image_available = False
    if len(results) > 0:
        first_result = results[0]
        image_available = np.array_equal(first_result[FIELD_IMAGE_VECTOR], image_data.image_embedding)
    if not image_available:  # insert
        logger.info("Creating %s", image_data.file_name)
        pa_table = convert_to_pyarrow(image_data, None)
        tbl.add(pa_table)
        return True
    logger.info("Updating %s", image_data.file_name)
    first_result = results[0]
    if not ignore_update:
        create_timestamp = first_result[FIELD_CREATE_TIMESTAMP]
        pa_table = convert_to_pyarrow(image_data, create_timestamp)

        single_value = {
            FIELD_TEXT_VECTOR: convert_vec_to_literal(first_result[FIELD_TEXT_VECTOR]),
            FIELD_IMAGE_DESCRIPTION: sql_escape(first_result[FIELD_IMAGE_DESCRIPTION]),
            FIELD_IMAGE_VECTOR: convert_vec_to_literal(first_result[FIELD_IMAGE_VECTOR]),
            FIELD_UPDATE_TIMESTAMP: first_result[FIELD_UPDATE_TIMESTAMP],
        }
        filter_expression = f"{FIELD_IMAGE_NAME} = '{first_result[FIELD_IMAGE_NAME]}'"
        if image_data.image_path:
            # The file was uploaded again. Keep the old file to avoid dups.
            unlink_file(cfg.image_storage_folder / image_data.file_name)
        tbl.update(where=filter_expression, values=single_value)
    return False


async def save_image_from_path(image_path: Path) -> bool | Error:
    if not image_path.exists():
        return Error(
            code=ErrorCode.NOT_FOUND,
            message=f"Could not find original image path: {image_path}",
        )
    image_data = await convert_single_image(image_path)
    if image_data is None:
        return Error(
            ErrorCode.DESCRIPTION_MISSING,
            f"Image description is missing for {image_path}",
        )
    return save_image(image_data)
