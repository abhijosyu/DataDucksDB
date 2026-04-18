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
st.markdown("# Restaurant List")


company = "Chipotle"  # example

response = requests.get(
    "http://127.0.0.1:5000/locations",
    params={"company": company}
)

locations = response.json()