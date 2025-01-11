"""Model classes for the image search service."""

from typing import Self

from pydantic import BaseModel, Field

from imagen.model.error import Error
from imagen.vdb.imagedb_schema import FIELD_IMAGE_DESCRIPTION, FIELD_IMAGE_NAME


class SearchRequest(BaseModel):
    """Search request payload."""

    search: str = Field(..., description="The search expression")
    limit: int = Field(default=10, description="The amount of results")


class SearchResponse(BaseModel):
    """Search response payload."""

    name: str = Field(..., description="The image name")
    description: str = Field(..., description="The image description")
    url: str = Field(..., description="The image URL")
    distance: float = Field(..., description="The distance to the search query")

    @classmethod
    def from_search(cls, search: dict) -> Self:
        """Convert search results to SearchResponse objects."""
        return cls(
            name=search[FIELD_IMAGE_NAME],
            description=search[FIELD_IMAGE_DESCRIPTION],
            url=f"/image/{search[FIELD_IMAGE_NAME]}",
            distance=search["_distance"],
        )

    @classmethod
    def from_searches(cls, searches: list[dict]) -> list["SearchResponse"]:
        """Convert search results to SearchResponse objects."""
        return [cls.from_search(search) for search in searches]


class UploadResponse(BaseModel):
    """Upload response payload."""

    name: str = Field(..., description="The image name")
    path: str = Field(..., description="The image file path")
    output: bool | Error = Field(..., description="Upload status")
