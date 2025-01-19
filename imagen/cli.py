"""Command line interface for the database."""

import asyncio as aio
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import typer

from imagen.config import cfg
from imagen.log import logger

if TYPE_CHECKING:
    import pandas as pd

app = typer.Typer()


@app.command()
def init(
    path: Annotated[
        Path,
        typer.Option(exists=True, help="Can supply a non-default image location"),
    ] = cfg.image_load_path,
) -> None:
    """Initialize the database."""
    from imagen.service.conversion_service import create_image_embeddings
    from imagen.vdb.lancedb_persistence import save_image, tbl

    async def load_images() -> None:
        async for image_data in create_image_embeddings(path):
            if image_data is None:
                logger.error("Could not process any images")
                return
            save_image(image_data)

    aio.run(load_images())
    print(f"Table {tbl} has {tbl.count_rows()} rows.")


@app.command()
def add(path: Annotated[Path, typer.Option(exists=True, help="Image path to add")]) -> None:
    """Add an image to the database."""
    from imagen.vdb.lancedb_persistence import save_image_from_path

    print("Processing", path)
    aio.run(save_image_from_path(path))


@app.command()
def count() -> None:
    """Count the number of rows in the database."""
    from imagen.vdb.lancedb_info import basic_info

    count, names = basic_info()
    print(f"Table has {count} rows.")
    print("Columns", names)


class FileFormats(StrEnum):
    """Supported file formats."""

    CSV = "csv"
    JSON = "json"


@app.command()
def export(fmt: Annotated[FileFormats, typer.Option(help="Output file format")] = FileFormats.JSON) -> None:
    """Export image data to CSV."""
    from imagen.vdb.lancedb_persistence import tbl

    df: pd.DataFrame = tbl.to_pandas()
    if fmt == FileFormats.CSV:
        df.to_csv("image_data.csv")
    else:
        df.to_json("image_data.json")


@app.command()
def clean() -> None:
    """Cleanup images and database."""
    from imagen.vdb.synchronize_images import syncronize_db

    syncronize_db()


if __name__ == "__main__":
    app()
