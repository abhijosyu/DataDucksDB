import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

# set up the page
st.markdown("# Restaurant Reviews")


if locations:
    selected_location = st.selectbox(
        "Choose a restaurant location",
        locations,
        format_func=lambda loc: f'{loc["name"]} - {loc["city"]}'
    )

    st.write("Selected location:")
    st.write(selected_location)
else:
    st.warning("No locations found.")