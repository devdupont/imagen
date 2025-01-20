"""Model classes for the image search service."""

from typing import Self

from pydantic import BaseModel, Field

from imagen.model.error import Error
from imagen.model.image import Image


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
    def from_image(cls, image: Image) -> Self:
        """Convert image objects to SearchResponse objects."""
        return cls(
            name=image.name,
            description=image.description,
            url=f"/image/{image.name}",
            distance=image.distance,
        )

    @classmethod
    def from_images(cls, images: list[Image]) -> list["SearchResponse"]:
        """Convert search results to SearchResponse objects."""
        return [cls.from_image(image) for image in images]


class UploadResponse(BaseModel):
    """Upload response payload."""

    name: str = Field(..., description="The image name")
    path: str = Field(..., description="The image file path")
    output: bool | Error = Field(..., description="Upload status")
