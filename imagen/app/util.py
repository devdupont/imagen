import asyncio
from pathlib import Path

import streamlit as st

from imagen.log import logger
from imagen.utils.file_utils import unlink_file
from imagen.vdb.lancedb_persistence import save_image_from_path


def missing_prompt_error() -> None:
    st.error("The image prompt should have at least 5 characters")


def display_image(image: Path, prompt: str) -> None:
    st.info(f"Generated {image.name}")
    st.image(
        image.as_posix(),
        caption=prompt,
        use_container_width=True,
    )


def save_image(image: Path) -> bool:
    try:
        asyncio.run(save_image_from_path(image))
        st.info(f"Created {image.name}")
    except Exception as exc:  # noqa: BLE001
        logger.exception(f"Failed to create image {image.name}: {exc}")
        st.info(f"Failed to import {image.name} to vector database.")
        return False
    finally:
        unlink_file(image)
    return True
