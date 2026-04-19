import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("Location Stats")

if "owner_select_location_analytics" not in st.session_state:
    st.session_state["owner_select_location_analytics"] = None

company_id = 7  # replace later with logged-in owner's company id

API_BASE_COMPANY = "http://127.0.0.1:4000/api/company"


# -----------------------------
# API helpers
# -----------------------------
def get_company_locations(company_id):
    try:
        response = requests.get(f"{API_BASE_COMPANY}/{company_id}/locations", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching locations: {e}")
        st.error("Could not load company locations.")
        return []


def get_location_analytics(location_id):
    try:
        response = requests.get(f"{API_BASE_COMPANY}/location/{location_id}/analytics", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching location analytics: {e}")
        st.error("Could not load analytics for this location.")
        return []


def get_overall_rating(location_id):
    try:
        response = requests.get(f"{API_BASE_COMPANY}/location/{location_id}/overall-rating", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching overall rating: {e}")
        st.error("Could not load overall rating.")
        return {}


def get_location_by_id(locations, location_id):
    for loc in locations:
        if loc["location_id"] == location_id:
            return loc
    return None


# -----------------------------
# Load locations
# -----------------------------
locations = get_company_locations(company_id)

if not locations:
    st.warning("No restaurant locations found.")
    st.stop()

selected_location = None
saved_location_id = st.session_state["owner_select_location_analytics"]

if saved_location_id is not None:
    selected_location = get_location_by_id(locations, saved_location_id)

    if selected_location is None:
        st.warning("Saved location was not found. Please choose a location again.")
        st.session_state["owner_select_location_analytics"] = None

# -----------------------------
# Choose location
# -----------------------------
if st.session_state["owner_select_location_analytics"] is None:
    selected_location = st.selectbox(
        "Choose a restaurant location",
        locations,
        format_func=lambda loc: f'{loc.get("city", "")}'
    )
    location_id = selected_location["location_id"]
else:
    location_id = saved_location_id
    st.subheader(
        f'Selected Location: {selected_location.get("city", "")}'
    )

# -----------------------------
# Fetch analytics
# -----------------------------
overall_rating_data = get_overall_rating(location_id)
analytics_data = get_location_analytics(location_id)

overall_rating = overall_rating_data.get("overall_rating")

# -----------------------------
# Top metrics
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    if overall_rating is not None:
        st.metric("Overall Rating", f"{overall_rating}/5")
    else:
        st.metric("Overall Rating", "N/A")

with col2:
    st.metric("Number of Rating Categories", len(analytics_data))

st.divider()

# -----------------------------
# Category analytics
# -----------------------------
st.subheader("Category Ratings")

if not analytics_data:
    st.info("No category analytics available for this location.")
else:
    df = pd.DataFrame(analytics_data)

    # Make sure expected columns exist
    if "category" in df.columns and "avg_rating" in df.columns:
        chart_df = df.set_index("category")

        st.bar_chart(chart_df["avg_rating"])

        st.markdown("### Detailed Rating Breakdown")
        st.dataframe(
            df.rename(
                columns={
                    "category": "Category",
                    "avg_rating": "Average Rating"
                }
            ),
            use_container_width=True
        )
    else:
        st.warning("Analytics data format was not what the page expected.")