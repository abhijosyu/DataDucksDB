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
st.markdown("# Write A User Review")


locations = requests.get("http://127.0.0.1:5000/locations").json()

selected_location = st.selectbox(
    "Choose restaurant",
    locations,
    format_func=lambda loc: loc["name"]
)

rating = st.slider("Rating", 1, 5, 5)
title = st.text_input("Review title")
comment = st.text_area("Write your review")

if st.button("Submit Review"):
    payload = {
        "location_id": selected_location["location_id"],
        "user_id": 1, 
        "rating": rating,
        "title": title,
        "comment": comment
    }

    response = requests.post("http://127.0.0.1:5000/reviews", json=payload)

    if response.status_code == 201:
        st.success("Review submitted.")
    else:
        st.error("Failed to submit review.")