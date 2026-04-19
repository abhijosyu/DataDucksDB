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
st.markdown("# Write A User Review")



API_BASE = "http://127.0.0.1:4000/api/reviewer"

def fetch_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {url}: {e}")
        st.error(f"Could not load data from: {url}")
        return []
    except ValueError:
        logger.error(f"Non-JSON response from {url}")
        st.error(f"Server returned invalid JSON for: {url}")
        return []

locations = fetch_json(f"{API_BASE}/locations")

if not locations:
    st.stop()



selected_location = st.selectbox(
    "Choose restaurant",
    locations,
    format_func=lambda loc: f"{loc['restaurant_name']} ({loc['city']})"
)

review_text = st.text_area("Write your review")

st.markdown("### Category Ratings")

ratings = []

food = st.slider(
        'food',
        1, 5, 3,
        key=f"5"
    )

price = st.slider(
        'price',
        1, 3, 2,
        key=f"6"
    )

service = st.slider(
        'price',
        1, 3, 2,
        key=f"7"
    )


if st.button("Submit Review"):
    ratings.append({
        "category_id": 5,
        "score": food
    })
    ratings.append({
        "category_id": 6,
        "score": price
    })
    ratings.append({
        "category_id": 7,
        "score": service
    })
    payload = {
        "location_id": selected_location["location_id"],
        "user_id": 1,
        "review_text": review_text,
        "ratings": ratings
    }

    try:
        response = requests.post(
            f"{API_BASE}/reviews",
            json=payload
        )

        if response.status_code == 201:
            st.success("Review submitted successfully!")
        else:
            try:
                st.error(f"Failed: {response.json()}")
            except ValueError:
                st.error(f"Failed: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error submitting review: {e}")
        st.error("Could not submit review.")

