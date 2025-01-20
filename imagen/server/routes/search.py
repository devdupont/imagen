"""Search routes for the API."""

import asyncio as aio

from fastapi import APIRouter, File, Form, UploadFile

from imagen.model.image import Image
from imagen.server.model import SearchRequest, SearchResponse
from imagen.utils.combine import combine_results
from imagen.utils.file_utils import get_temp_file
from imagen.vdb.image_search_helper import image_search
from imagen.vdb.text_search import text_search

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/text")
async def search_text(request: SearchRequest) -> list[SearchResponse]:
    """Search for images based on a text query."""
    res = await text_search(request.search, request.limit)
    return SearchResponse.from_images(res)


async def _search_image(file: UploadFile, limit: int) -> list[Image]:
    with get_temp_file(file.file, delete=False) as tmp:  # type: ignore
        return image_search(tmp, limit)


@router.post("/image")
async def search_image(file: UploadFile = File(...), limit: int = Form(default=10)) -> list[SearchResponse]:  # noqa: B008
    """Search for images based on an uploaded image."""
    return SearchResponse.from_images(await _search_image(file, limit))


LIMIT = 5


@router.post("/text_image")
async def search_text_image(file: UploadFile = File(...), search: str = Form(...)) -> list[SearchResponse]:  # noqa: B008
    """Search for images based on an uploaded image and a text query."""
    res_image, res_text = await aio.gather(_search_image(file, LIMIT), text_search(search, LIMIT))
    return SearchResponse.from_images(combine_results(res_image, res_text, LIMIT))
