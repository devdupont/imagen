"""Utility functions for the app."""

from pathlib import Path
from tempfile import _TemporaryFileWrapper

from streamlit.runtime.uploaded_file_manager import UploadedFile


def app_tempfile(file: UploadedFile, tmp: _TemporaryFileWrapper) -> Path:
    """Create a temporary file from an uploaded file."""
    content = file.getbuffer()
    tmp.write(content)
    return Path(tmp.name)
