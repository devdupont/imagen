""""""

from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile


async def create_temp_file(file: UploadFile, tmp: NamedTemporaryFile) -> Path:
    """Create a temporary file from an uploaded file."""
    content = await file.read()  # Read the file content
    tmp.write(content)  # Write the file content to a temporary file
    return Path(tmp.name)  # Get the temporary file path
