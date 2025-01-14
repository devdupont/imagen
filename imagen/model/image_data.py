import datetime as dt
from dataclasses import dataclass
from pathlib import Path

import pyarrow as pa

from imagen.config import cfg
from imagen.vdb.imagedb_schema import (
    FIELD_CREATE_TIMESTAMP,
    FIELD_IMAGE_DESCRIPTION,
    FIELD_IMAGE_NAME,
    FIELD_IMAGE_VECTOR,
    FIELD_TEXT_VECTOR,
    FIELD_UPDATE_TIMESTAMP,
)


@dataclass
class ImageData:
    file_name: str
    description: str
    image_embedding: list[float]
    text_embedding: list[float]
    image_path: Path | None = None


def convert_to_pyarrow(image_data: ImageData, create_timestamp: int | None) -> pa.lib.Table:
    current_timestamp = int(dt.datetime.now(dt.UTC).timestamp() * 1_000)
    vector_size = cfg.image_vector_size
    elements = [
        pa.array([image_data.image_embedding], pa.list_(pa.float32(), vector_size)),
        pa.array([image_data.text_embedding], pa.list_(pa.float32(), cfg.text_vector_size)),
        pa.array([image_data.file_name]),
        pa.array([image_data.description]),
    ]

    if create_timestamp:
        elements.append(pa.array([create_timestamp]))
    else:
        elements.append(pa.array([current_timestamp]))
    elements.append(pa.array([current_timestamp]))

    return pa.Table.from_arrays(
        elements,  # type: ignore
        [
            FIELD_IMAGE_VECTOR,
            FIELD_TEXT_VECTOR,
            FIELD_IMAGE_NAME,
            FIELD_IMAGE_DESCRIPTION,
            FIELD_CREATE_TIMESTAMP,
            FIELD_UPDATE_TIMESTAMP,
        ],
    )
