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
st.markdown("# Write An Employee Review")
st.session_state.pop('selected_location', None)

if "emp_review_id" not in st.session_state:
    st.session_state["emp_review_id"] = None
if "location_id" not in st.session_state:
    st.session_state["location_id"] = None

EMPLOYEE_API_BASE = "http://web-api:4000/api/employee"
REVIEWER_API_BASE = "http://web-api:4000/api/reviewer"


def get_locations():
    return fetch_json(f"{REVIEWER_API_BASE}/locations")

def get_employee_reviews(location_id):
    return fetch_json(f"{EMPLOYEE_API_BASE}/locations/{location_id}/employee-reviews")

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

locations = get_locations()

if not locations:
    st.stop()


if st.session_state["emp_review_id"] != None and st.session_state["location_id"] != None:
    emp_review_id = st.session_state["emp_review_id"]
    location_id = st.session_state["location_id"]
    #review_info = get_specific_review(review_id, location_id)
    
    
   # review_text = st.text_area("Write your review",  value=review_info["review_text"])

    st.markdown("### Category Ratings")

    ratings = []
    
    management = st.slider("Management", 1, 5, 3, key="new_management")
    pay = st.slider("Pay", 1, 5, 3, key="new_pay")
    work_life_balance = st.slider("Work-Life Balance", 1, 5, 3, key="new_wlb")

    col1, col2 = st.columns(2)      


    if st.button("Edit Review"):
        ratings.append({
            "category_id": 1,
            "score": pay
        })
        ratings.append({
            "category_id": 2,
            "score": management
        })
        ratings.append({
            "category_id": 3,
            "score": work_life_balance
        })
        payload = {
            "location_id": location_id,
            "user_id": st.session_state["user_id"],
            "review_text": "",
            "ratings": ratings
        }

        try:
            response = requests.put(
                f"{EMPLOYEE_API_BASE}/employee-reviews/{emp_review_id}",
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


    pay = st.slider(
            'pay',
            1, 5, 3,
            key=f"1"
        )
    management = st.slider(
            'management',
            1, 5, 3,
            key=f"2"
        )
    work_life_balance = st.slider(
            'work_life_balance',
            1, 5, 3,
            key=f"3"
        )
    
    if st.button("Submit Review"):
        ratings.append({
            "category_id": 1,
            "score": pay
        })
        ratings.append({
            "category_id": 2,
            "score": management
        })
        ratings.append({
            "category_id": 3,
            "score": work_life_balance
        })
        payload = {
            "location_id": selected_location["location_id"],
            "user_id": st.session_state["user_id"],
            "review_text": review_text,
            "ratings": ratings
        }

        try:
            response = requests.post(
                f"{EMPLOYEE_API_BASE}/employee-reviews",
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



