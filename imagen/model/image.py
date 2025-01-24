import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Self

import numpy as np
import pyarrow as pa

from imagen.config import cfg


@dataclass
class ImageFields:
    """Fields for the image table."""

    name = "name"
    description = "description"
    image_vector = "image_vector"
    text_vector = "text_vector"
    created = "created"
    updated = "updated"

    @property
    def all(self) -> list[str]:
        return [
            self.name,
            self.description,
            self.image_vector,
            self.text_vector,
            self.created,
            self.updated,
        ]

    @property
    def info(self) -> list[str]:
        return [
            self.name,
            self.description,
            self.created,
            self.updated,
        ]


FIELD = ImageFields()
SCHEMA = pa.schema(
    [
        pa.field(FIELD.name, pa.string()),
        pa.field(FIELD.description, pa.string()),
        pa.field(FIELD.image_vector, pa.list_(pa.float32(), cfg.image_vector_size)),
        pa.field(FIELD.text_vector, pa.list_(pa.float32(), cfg.text_vector_size)),
        pa.field(FIELD.created, pa.timestamp("ms")),
        pa.field(FIELD.updated, pa.timestamp("ms")),
    ]
)


@dataclass
class Image:
    """Image data object."""

    name: str
    description: str
    image_embedding: list[float]
    text_embedding: list[float]

    image_path: Path | None = None
    created: int | None = None
    updated: int | None = None
    distance: float | None = None

    field: ClassVar[ImageFields] = FIELD
    schema: ClassVar[pa.Schema] = SCHEMA

    @classmethod
    def from_vdb(cls, data: dict) -> Self:
        """Create an image object from a database entry."""
        return cls(
            name=data[FIELD.name],
            description=data[FIELD.description],
            image_embedding=data[FIELD.image_vector],
            text_embedding=data[FIELD.text_vector],
            created=data[FIELD.created],
            updated=data[FIELD.updated],
        )

    def to_pyarrow(self, create_timestamp: int | None = None) -> pa.lib.Table:
        """Convert the image object to a pyarrow table."""
        current_timestamp = int(dt.datetime.now(dt.UTC).timestamp() * 1_000)
        elements = [
            pa.array([self.name]),
            pa.array([self.description]),
            pa.array([self.image_embedding], pa.list_(pa.float32(), cfg.image_vector_size)),
            pa.array([self.text_embedding], pa.list_(pa.float32(), cfg.text_vector_size)),
        ]

        if create_timestamp:
            elements.append(pa.array([create_timestamp]))
        else:
            elements.append(pa.array([current_timestamp]))
        elements.append(pa.array([current_timestamp]))

        return pa.Table.from_arrays(elements, FIELD.all)  # type: ignore

    def matching_vector(self, image: "Image") -> bool:
        """Check if the image vectors match."""
        return np.array_equal(self.image_embedding, image.image_embedding)
