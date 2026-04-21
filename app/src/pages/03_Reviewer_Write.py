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
st.session_state.pop('selected_location', None)

if "review_id" not in st.session_state:
    st.session_state["review_id"] = None
if "location_id" not in st.session_state:
    st.session_state["location_id"] = None

API_BASE = "http://web-api:4000/api/reviewer"


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

def get_specific_review(review_id, location_id):
    total_reviews = get_location_reviews(location_id)
    for rev in total_reviews:
        if int(rev["review_id"]) == int(review_id):
            return rev

if st.session_state["review_id"] != None and st.session_state["location_id"] != None:
    review_id = st.session_state["review_id"]
    location_id = st.session_state["location_id"]
    review_info = get_specific_review(review_id, location_id)
    
    
    review_text = st.text_area("Write your review",  value=review_info["review_text"])

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


    if st.button("Edit Review"):
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
            "location_id": location_id,
            "user_id": st.session_state["user_id"],
            "review_text": review_text,
            "ratings": ratings
        }

        try:
            response = requests.put(
                f"{API_BASE}/reviews/{review_id}",
                json=payload
            )

            if response.status_code == 200:
                st.success("Review edited successfully!")
            else:
                try:
                    st.error(f"Failed: {response.json()}")
                except ValueError:
                    st.error(f"Failed: {response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error submitting review: {e}")
            st.error("Could not submit review.")

        


else:
    st.session_state.pop('review_state', None)
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
            "user_id": st.session_state["user_id"],
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

