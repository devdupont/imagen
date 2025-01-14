"""Command line interface for the database."""

from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import typer

from imagen.config import cfg

if TYPE_CHECKING:
    import pandas as pd

app = typer.Typer()


@app.command()
async def init(
    path: Annotated[
        Path,
        typer.Option(cfg.image_load_path, exists=True, help="Can supply a non-default image location"),
    ],
) -> None:
    """Initialize the database."""
    from imagen.service.conversion_service import create_image_embeddings
    from imagen.vdb.lancedb_persistence import save_image, tbl

    async for image_data in create_image_embeddings(path):
        save_image(image_data)
        print("Saved", image_data.file_name)

    print(f"Table {tbl} has {tbl.count_rows()} rows.")


@app.command()
async def add(path: Annotated[Path, typer.Option(exists=True, help="Image path to add")]) -> None:
    """Add an image to the database."""
    from imagen.vdb.lancedb_persistence import save_image_from_path

    print("Processing", path)
    await save_image_from_path(path)


@app.command()
def count() -> None:
    """Count the number of rows in the database."""
    from imagen.vdb.lancedb_info import basic_info

    count, names = basic_info()
    print(f"Table has {count} rows.")
    print("Columns", names)


@app.command()
def export() -> None:
    """Export image data to CSV."""
    from imagen.vdb.lancedb_persistence import tbl

    df: pd.DataFrame = tbl.to_pandas()
    df.to_csv("images_data.csv")


@app.command()
def clean() -> None:
    """Cleanup images and database."""
    from imagen.vdb.synchronize_images import syncronize_db

    syncronize_db()


if __name__ == "__main__":
    typer.run(app)
