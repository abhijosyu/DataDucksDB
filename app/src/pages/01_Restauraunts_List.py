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
    valid_ratings = [
        float(loc["avg_rating"])
        for loc in locations
        if loc["avg_rating"] is not None
    ]

    if valid_ratings:
        min_rating = float(min(valid_ratings))
        max_rating = float(max(valid_ratings))

        selected_range = st.slider(
            "Filter by rating",
            max_value=5.0,
            value=(0.0, max_rating),
            step=0.5
        )

        filtered_locations = []
        for loc in locations:
            rating = loc["avg_rating"]
            if rating is None:
                continue
            rating = float(rating)
            if selected_range[0] <= rating <= selected_range[1]:
                filtered_locations.append(loc)
    else:
        st.info("No ratings available yet.")
        filtered_locations = locations

    if not filtered_locations:
        st.warning("No restaurants match that rating range.")
    else:
        for loc in filtered_locations:
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"### {loc['restaurant_name']}")
                st.caption(f"{loc['address']}, {loc['city']}")

            with col2:
                rating = loc["avg_rating"] if loc["avg_rating"] is not None else "N/A"
                st.markdown(f"""
                **💲 {loc['price_range']}**  
                **⭐ {rating}**
                """)
                if st.button("View", key=f"view_{loc}"):
                    st.session_state["selected_location"] = loc
                    st.switch_page("pages/02_Reviewer_Restaurant_Reviews.py")

            st.divider()


