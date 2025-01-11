from enum import StrEnum

import streamlit as st
from streamlit_option_menu import option_menu  # type: ignore


class Page(StrEnum):
    HOME = "Home"
    UPLOAD = "Upload"
    GENERATE = "Generate"
    # GENERATE_MIDJOURNEY = "Generate Midjourney"
    STATS = "Stats"
    DATA = "Data"


# Define the pages and their file paths
pages = {
    Page.HOME: "home.py",
    Page.UPLOAD: "pages/upload.py",
    Page.GENERATE: "pages/generate.py",
    # Page.GENERATE_MIDJOURNEY: "pages/generate_midjourney.py",
    Page.DATA: "pages/data.py",
    Page.STATS: "pages/stats.py",
}

# Create a list of the page names
page_list = list(pages.keys())


def nav(current_page: Page = Page.HOME) -> None:
    with st.sidebar:
        p = option_menu(
            "Main Menu",
            page_list,
            default_index=page_list.index(current_page),
            orientation="vertical",
        )

        if current_page != p:
            st.switch_page(pages[p])
