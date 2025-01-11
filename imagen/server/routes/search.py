"""Search routes for the API."""

from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, Form, UploadFile

from imagen.server.model import SearchRequest, SearchResponse
from imagen.server.util import api_tempfile
from imagen.vdb.image_search_helper import image_search
from imagen.vdb.result_combiner import combine_results
from imagen.vdb.text_search import text_search

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/text")
async def search_text(request: SearchRequest) -> list[SearchResponse]:
    res = await text_search(request.search, request.limit)
    return SearchResponse.from_searches(res)


@router.post("/image")
async def search_image(file: UploadFile = File(...), limit: int = Form(default=10)) -> list[SearchResponse]:  # noqa: B008
    with NamedTemporaryFile(delete=False) as tmp:
        tmp_path = await api_tempfile(file, tmp)
        res = image_search(tmp_path, limit)
    return SearchResponse.from_searches(res)


@router.post("/text_image")
async def search_text_image(file: UploadFile = File(...), search: str = Form(...)):  # noqa: B008
    limit = 5
    res_image = await search_image(file, limit=limit)
    res_text = await search_text(SearchRequest(search=search, limit=limit))
    return combine_results(res_image, res_text, limit)
