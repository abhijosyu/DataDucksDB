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
st.markdown("# Company Metrics")

API_BASE_COMPANY = "http://web-api:4000/api/company"

company_id = 7

def get_company_locations(company_id):
    try:
        response = requests.get(f"{API_BASE_COMPANY}/{company_id}/locations", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching company locations: {e}")
        st.error("Could not load company locations.")
        return []


def get_company_analytics(company_id):
    try:
        response = requests.get(f"{API_BASE_COMPANY}/{company_id}/analytics", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching company analytics: {e}")
        st.error("Could not load company analytics.")
        return []


def get_company_overall_rating(company_id):
    try:
        response = requests.get(f"{API_BASE_COMPANY}/{company_id}/overall-rating", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching company overall rating: {e}")
        st.error("Could not load company overall rating.")
        return {}


locations = get_company_locations(company_id)
analytics_data = get_company_analytics(company_id)
overall_rating_data = get_company_overall_rating(company_id)

overall_rating = overall_rating_data.get("overall_rating")
num_locations = len(locations)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Overall Company Rating", f"{overall_rating}/5" if overall_rating is not None else "N/A")

with col2:
    st.metric("Total Locations", num_locations)

with col3:
    st.metric("Rating Categories", len(analytics_data))

st.divider()


st.subheader("Company-Wide Category Ratings")

if not analytics_data:
    st.info("No analytics data available for this company.")
else:
    df = pd.DataFrame(analytics_data)

    if "category" in df.columns and "avg_rating" in df.columns:
        chart_df = df.set_index("category")

        st.bar_chart(chart_df["avg_rating"])

        st.markdown("### Detailed Breakdown")
        st.dataframe(
            df.rename(
                columns={
                    "category": "Category",
                    "avg_rating": "Average Rating"
                }
            ),
            use_container_width=True
        )

        st.markdown("### Rating Meters")
        for row in analytics_data:
            category = row["category"]
            rating = row["avg_rating"] if row["avg_rating"] is not None else 0

            st.write(f"**{category}** — {rating}/5")
            st.progress(min(float(rating) / 5, 1.0))
    else:
        st.warning("Analytics data format was not what the page expected.")


