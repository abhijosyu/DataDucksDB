import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("Location Stats")

company_id = 7  # example

def get_company_locations(company_id):
    response = requests.get(f"http://127.0.0.1:5000/companies/{company_id}/locations")
    response.raise_for_status()
    return response.json()

locations = get_company_locations(company_id)


selected_location = st.selectbox(
    "Choose a restaurant location",
    locations,
    format_func=lambda loc: f'{loc["name"]} - {loc["city"]}'
)


def get_location_analytics(location_id):
    response = requests.get(f"http://127.0.0.1:5000/analytics/location/{location_id}")
    response.raise_for_status()
    return response.json()

if selected_location:
    analytics = get_location_analytics(selected_location["location_id"])

    st.subheader("Location Analytics")
    st.write("Average Rating:", analytics["average_rating"])
    st.write("Review Count:", analytics["review_count"])
    st.write("Trend:", analytics["positive_trend"])
    st.write("Common Complaint:", analytics["common_complaint"])