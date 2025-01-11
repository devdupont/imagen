"""Configuration file for the project."""

from collections.abc import Callable
from pathlib import Path
from typing import Self

from dotenv import load_dotenv
from pydantic import DirectoryPath, Field, HttpUrl, ValidationError, model_validator
from pydantic_settings import BaseSettings

load_dotenv()


def default_dir(path_str: str) -> Callable[[], Path]:
    """Create a directory if it does not exist."""

    def default_dir_factory() -> Path:
        path = Path(path_str)
        path.mkdir(parents=True, exist_ok=True)
        return path

    return default_dir_factory


class Config(BaseSettings):
    """Configuration object for the project."""

    image_storage_folder: DirectoryPath = Field(default_factory=default_dir("./tmp/images"))

    openai_api_key: str = ""
    openai_embeddings_model: str | None = None
    openai_image_model: str = "clip-vit-base"

    ollama_base_url: HttpUrl = "http://localhost:11434/api"
    llava_model: str = "llava"
    nomic_embed_model: str = "nomic-embed-text"

    lance_db_location: DirectoryPath = Field(default_factory=default_dir("./tmp/.lancedb"))
    lance_table_image: str = "tbl_image"

    image_vector_size: int = 768
    text_vector_size: int = 768

    supported_file_formats: tuple[str] = ("png", "jpg", "jpeg", "webp",)

    testing: bool = False

    @model_validator(mode="after")
    def check_text_vector_size(self) -> Self:
        """Set the text vector size based on the embeddings model."""
        self.text_vector_size = 1536 if self.openai_embeddings_model is not None else 768  # nomic vector size
        return self

    @model_validator(mode="after")
    def check_openai_api_key(self) -> Self:
        """Check if the OpenAI API key is set."""
        if not self.openai_api_key or "<" in self.openai_api_key:
            msg = "OpenAI API key is not set"
            raise ValidationError(msg)
        return self


def get_image_folder() -> Path:
    import sys

    images_path = Path("./images")
    if not images_path.exists():
        images_path = Path("./multimodal_experiments/images")
        if not images_path.exists():
            print("Cannot find the images", file=sys.stderr)
            sys.exit(1)
    return images_path


cfg = Config()
