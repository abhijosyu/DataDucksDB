from datetime import datetime
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
st.title("Flagged Reviews")
st.write("### Reviews that have been flagged by admin")


API_BASE = "http://web-api:4000/api/admin"

def get_flags():
    try:
        response = requests.get(f"{API_BASE}/flags")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching flags: {e}")
        st.error("Could not load flagged reviews.")
        return []


def delete_flag(flag_id):
    try:
        response = requests.delete(f"{API_BASE}/flags/{flag_id}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting flag {flag_id}: {e}")
        st.error(f"Could not remove flag #{flag_id}.")
        return False


flags = get_flags()

st.write(f"### {len(flags)} flagged review(s) found")

if not flags:
    st.info("No flagged reviews found.")
else:
    for i, flag in enumerate(flags):

        flag_id = flag.get("flag_id", "N/A")
        review_id = flag.get("review_id", "N/A")

        reviewer_name = flag.get("reviewer_name", "Unknown Reviewer")
        reviewer_email = flag.get("reviewer_email", "")
        flagged_by_name = flag.get("flagged_by_name", "Unknown Admin")
        reason = flag.get("reason", "")
        review_text = flag.get("review_text", "")
        review_date = flag.get("review_date", "")
        restaurant_name = flag.get("restaurant_name", "Unknown Restaurant")
        address = flag.get("address", "")
        city = flag.get("city", "")
        review_type = flag.get("review_type", "")

        formatted_date = review_date
        try:
            formatted_date = datetime.fromisoformat(str(review_date)).strftime("%B %d, %Y")
        except Exception:
            pass

        col1, col2 = st.columns([5, 1])

        with col1:
            st.markdown(f"### Flag #{flag_id}")
            st.write(f"**Review Type:** {review_type.capitalize()}")

            st.write(f"**Reviewer:** {reviewer_name}")
            if reviewer_email:
                st.caption(reviewer_email)

            #st.write(f"**Flagged By:** {flagged_by_name}")

            st.write(f"**Reason:** {reason}")

            st.write(f"**Restaurant:** {restaurant_name}")

            if address or city:
                location_line = f"{address}, {city}" if address and city else address or city
                st.caption(location_line)

            st.write(f"**Date:** :blue[{formatted_date}]")
            st.write(f"**Review:** {review_text}")

        with col2:
            if st.button("Remove Flag", key=f"remove_flag_{flag_id}_{i}"):
                if delete_flag(flag_id):
                    st.success(f"Flag #{flag_id} removed.")
                    st.rerun()

        st.divider()