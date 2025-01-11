"""Utility functions for the server."""

from pathlib import Path
from tempfile import _TemporaryFileWrapper

from fastapi import UploadFile


async def api_tempfile(file: UploadFile, tmp: _TemporaryFileWrapper) -> Path:
    """Create a temporary file from an uploaded file."""
    content = await file.read()  # Read the file content
    tmp.write(content)  # Write the file content to a temporary file
    return Path(tmp.name)  # Get the temporary file path
