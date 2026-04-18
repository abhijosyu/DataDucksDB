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

API_BASE = "http://127.0.0.1:4000/api/reviewer"

def get_locations():
    try:
        response = requests.get(f"{API_BASE}/locations")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching locations: {e}")
        return []

locations = get_locations()

if not locations:
    st.warning("No restaurant locations found.")
else:
    for loc in locations:
        st.subheader(loc["restaurant_name"])
        st.write(f'Location ID: {loc["location_id"]}')
        st.write(f'City: {loc["city"]}')
        st.write(f'Address: {loc["address"]}')
        st.write(f'Price Range: {loc["price_range"]}')
        st.write(f'Average Rating: {loc["avg_rating"] if loc["avg_rating"] is not None else "No ratings yet"}')
        st.write(f'Review Count: {loc["review_count"]}')
        st.divider()


