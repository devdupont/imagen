import asyncio
import shutil

import streamlit as st

from imagen.app.navbar import Page, nav
from imagen.config import cfg
from imagen.log import logger
from imagen.utils.file_utils import get_temp_file
from imagen.utils.time_utils import generate_file_timestamp
from imagen.vdb.lancedb_persistence import save_image_from_path

st.set_page_config(layout="wide")
st.header("Image Upload")

# Display the menu
nav(Page.UPLOAD)

st.markdown("""This page allows you to upload an image to the vector database.""")

with st.form(key="image_upload_form"):
    # File uploader widget
    uploaded_file = st.file_uploader("Choose a file", type=cfg.supported_file_formats)

    # Submit button for the form
    submit_button = st.form_submit_button(label="Upload")

if submit_button:
    if uploaded_file is None:
        # Display a message prompting the user to fill out the upload file
        st.error("Please upload an image")
    else:
        with st.spinner("Uploading file... Please wait."):
            output = None
            with get_temp_file(uploaded_file.getbuffer()) as tmp:
                file_copy = tmp.parent / f"{generate_file_timestamp()}_{uploaded_file.name}"
                logger.info("file_copy %s", file_copy)
                shutil.copyfile(tmp, file_copy)
                logger.info("file_copy exists %s", file_copy.exists())
                output = asyncio.run(save_image_from_path(file_copy))

                # if type(output) == Error:
                #     st.error(f"Image upload failed due to {output.message}")
                # else:
                st.info(f"Image {uploaded_file.name} successfully {'created' if output else 'updated'}")
