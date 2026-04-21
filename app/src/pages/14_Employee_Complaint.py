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
st.markdown("# Write An Employee Complaint")
st.session_state.pop('selected_location', None)

if "emp_review_id" not in st.session_state:
    st.session_state["emp_review_id"] = None
if "location_id" not in st.session_state:
    st.session_state["location_id"] = None

EMPLOYEE_API_BASE = "http://web-api:4000/api/employee"
REVIEWER_API_BASE = "http://web-api:4000/api/reviewer"

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

def get_locations():
    return fetch_json(f"{REVIEWER_API_BASE}/locations")

locations = get_locations()

selected_location = st.selectbox(
    "Choose restaurant",
    locations,
    format_func=lambda loc: f"{loc['restaurant_name']} ({loc['city']})"
)

complaint_text = st.text_area("Write your complaint")

if st.button("Submit Complaint"):
    if not complaint_text.strip():
        st.warning("Please write a complaint before submitting.")
    payload = {
        "location_id": selected_location["location_id"],
        "user_id": 1,
        "review_text": complaint_text,
    }

    try:
        response = requests.post(
            f"http://web-api:4000/api/complaints",
            json=payload
        )

        if response.status_code == 201:
            st.success("Complaint submitted successfully!")
        else:
            try:
                st.error(f"Failed: {response.json()}")
            except ValueError:
                st.error(f"Failed: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error submitting complaint: {e}")
        st.error("Could not submit complaint.")

