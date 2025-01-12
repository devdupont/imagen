"""Utility functions for the app."""

from collections.abc import Buffer, Generator
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any


def unlink_file(tmp_path: Path) -> None:
    if tmp_path is not None:
        # try:
        tmp_path.unlink()
        # except Exception as exc:
        #     logger.exception(f"Failed to delete {tmp_path}: {exc}")


@contextmanager
def get_temp_file(data: Buffer, *, delete: bool = True) -> Generator[Path, Any, Any]:
    """Create a temporary file from a buffer."""
    with NamedTemporaryFile(delete=delete) as tmp:
        tmp.write(data)
        yield Path(tmp.name)
