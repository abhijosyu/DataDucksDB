import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
from datetime import datetime
import requests


st.set_page_config(layout='wide')

SideBarLinks()

st.title("All Reviews")
st.write("### Reviews submitted by reviewers and employees")

API_BASE = "http://web-api:4000/api/admin"


def get_all_reviews():
    try:
        response = requests.get(f"{API_BASE}/all_reviews")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching reviews: {e}")
        st.error("Could not load reviews.")
        return []

def delete_customer_review(review_id):
    try:
        response = requests.delete(f"{API_BASE}/customer_reviews/{review_id}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting customer review {review_id}: {e}")
        st.error(f"Could not delete customer review #{review_id}.")
        return False


def delete_employee_review(review_id):
    try:
        response = requests.delete(f"{API_BASE}/employee_reviews/{review_id}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting employee review {review_id}: {e}")
        st.error(f"Could not delete employee review #{review_id}.")
        return False


reviews = get_all_reviews()

review_filter = st.selectbox(
    "Filter by review type",
    ["All", "Customer", "Employee"]
)

if review_filter == "Customer":
    reviews = [r for r in reviews if r.get("review_type") == "customer"]
elif review_filter == "Employee":
    reviews = [r for r in reviews if r.get("review_type") == "employee"]

st.write(f"### {len(reviews)} review(s) found")

if not reviews:
    st.info("No reviews found.")
else:
    for review in reviews:
        review_id = review.get("review_id", "N/A")
        review_text = review.get("review_text", "")
        review_date = review.get("review_date", "")
        user_name = review.get("name", "Unknown User")
        email = review.get("email", "")
        restaurant_name = review.get("restaurant_name", "Unknown Restaurant")
        address = review.get("address", "")
        city = review.get("city", "")
        review_type = review.get("review_type", "")

        formatted_date = review_date
        try:
            formatted_date = datetime.fromisoformat(str(review_date)).strftime("%B %d, %Y")
        except Exception:
            pass

        col1, col2 = st.columns([5, 1])

        with col1:
            st.markdown(f"### {review_type.capitalize()} Review")
            st.markdown(f"**{user_name}**")
            if email:
                st.caption(email)

            st.markdown(f"📍 **{restaurant_name}**")
            if address or city:
                location_line = f"{address}, {city}" if address and city else address or city
                st.caption(location_line)

            st.markdown(f"**Date:** :blue[{formatted_date}]")
            st.write(f"**Review:** {review_text}")

        with col2:
            st.write(f"**Type:** {review_type.capitalize()}")

            if review_type == "customer":
                if st.button("Delete", key=f"delete_customer_{review_id}"):
                    if delete_customer_review(review_id):
                        st.success(f"Customer review #{review_id} deleted.")
                        st.rerun()

            elif review_type == "employee":
                if st.button("Delete", key=f"delete_employee_{review_id}"):
                    if delete_employee_review(review_id):
                        st.success(f"Employee review #{review_id} deleted.")
                        st.rerun()

        st.divider()