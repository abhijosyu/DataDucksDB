import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()



# set up the page
st.markdown("# Restaurant Reviews")

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

def get_location_reviews(location_id):
    try:
        response = requests.get(f"{API_BASE}/locations/{location_id}/reviews")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching reviews for location {location_id}: {e}")
        return []

if "selected_location" not in st.session_state:
    st.info("No restaurant was selected from the previous page. Choose one below.")

    options = {
        f"{loc['restaurant_name']} ({loc['city']})": loc
        for loc in locations
    }

    selected_label = st.selectbox(
        "Choose a restaurant",
        options=list(options.keys())
    )

    loc = options[selected_label]
else:
    loc = st.session_state["selected_location"]

st.markdown(
    f"<h1 style='text-align: center;'>{loc['restaurant_name']}</h2>",
    unsafe_allow_html=True
)
st.markdown(
    f"<h4 style='text-align: center;'>{loc['address']}</h4>",
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(
    f"<h5 style='text-align: center;'> price range: {loc['price_range']}</h5>",
    unsafe_allow_html=True
    )

with col2:
    rating = loc["avg_rating"] if loc["avg_rating"] is not None else "No ratings yet"
    st.markdown(
    f"<h5 style='text-align: center;'> price range: {rating}</h5>",
    unsafe_allow_html=True
    )

reviews = get_location_reviews(loc["location_id"])

st.markdown("## Reviews")

if not reviews:
    st.info("No reviews yet for this restaurant.")
else:
    for review in reviews:
        reviewer_name = review["reviewer_name"]
        review_text = review["review_text"]
        review_date = review["review_date"]
        avg_score = review["avg_score"] if review["avg_score"] is not None else "N/A"

        with st.container():
            st.markdown(f"### {reviewer_name}")
            st.write(f"**Date:** {review_date}")
            st.write(f"**Average Score:** {avg_score}")
            st.write(review_text)
            st.divider()