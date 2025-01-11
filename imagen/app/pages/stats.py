import streamlit as st

from imagen.app.navbar import nav
from imagen.vdb.lancedb_info import basic_info, col_info

st.set_page_config(layout="wide")
st.header("Database stats")

# Display the menu
nav("Stats")

count, _ = basic_info()
column_info = col_info()

st.markdown(
    f"""Here are some informations about the image database:
- Number of rows: {count}
- Number of columns: {len(column_info)}

Here are the columns information:
- {"- ".join([c[0] + f": {c[1]}\n" for c in column_info])}
"""
)
