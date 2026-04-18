import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

import requests

st.set_page_config(layout='wide')

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.markdown('# List Of Restaurants')

def get_locations():
    try:
        response = requests.get("http://127.0.0.1:5000/locations") # change route once done
        return response.json()
    except requests.exceptions.RequestException:
        return []

locations = get_locations()

if not locations:
    st.warning("No restaurant locations found.")
else:
    for loc in locations:
        st.subheader(loc["name"])
        st.write(f'City: {loc["city"]}')
        st.write(f'Address: {loc["address"]}')
        st.divider()


