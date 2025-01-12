"""Image processing routes for the API."""

import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from imagen.config import cfg
from imagen.server.model import UploadResponse
from imagen.utils.file_utils import get_temp_file
from imagen.utils.time_utils import generate_file_timestamp
from imagen.vdb.lancedb_persistence import save_image_from_path

router = APIRouter(prefix="/image", tags=["image"])


@router.post("/")
async def create_upload_file(file: UploadFile = File(...)) -> UploadResponse:  # noqa: B008
    """Upload an image file to the server."""
    with get_temp_file(await file.read()) as tmp:
        formatted_timestamp = generate_file_timestamp()
        file_copy = tmp.parent / f"{formatted_timestamp}_{file.filename}"
        shutil.copyfile(tmp, file_copy)
        output = await save_image_from_path(file_copy)

    return UploadResponse(name=file.filename or "upload", path=tmp.as_posix(), output=output)


@router.get("/{image_name}")
async def get_image(image_name: str) -> FileResponse:
    """Get an image by name."""
    # Define the path to the image folder
    image_path = cfg.image_storage_folder / image_name

    # Check if the image exists
    if not image_path.exists():
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found")

    # Return the image as a streaming response
    return FileResponse(image_path)
