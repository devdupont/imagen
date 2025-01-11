import streamlit as st

from imagen.app.navbar import Page, nav
from imagen.vdb.lancedb_info import get_data

st.set_page_config(layout="wide")
st.header("Data")

# Display the menu
nav(Page.DATA)

image_metadata = get_data()

st.markdown("""Here you can see data contained in this database.""")

st.dataframe(image_metadata)
