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
st.markdown("# Employee Reviews")

EMPLOYEE_API_BASE = "http://web-api:4000/api/employee"
REVIEWER_API_BASE = "http://web-api:4000/api/reviewer"

def get_locations():
    try:
        response = requests.get(f"{REVIEWER_API_BASE}/locations")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching locations: {e}")
        return []

def get_employee_reviews(location_id):
    try:
        response = requests.get(f"{EMPLOYEE_API_BASE}/locations/{location_id}/employee-reviews")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Employee reviews for location {location_id}: {e}")
        return []
    
locations = get_locations()

if "selected_location" not in st.session_state:
    st.info("No restaurant was selected from the previous page. Choose one below.")

    options = {
        f"{loc['restaurant_name']} ({loc['city']})": loc
        for loc in locations
    }

    selected_label = st.selectbox(
        "Choose a restaurant",
        options=list(options.keys())
    )

    loc = options[selected_label]
else:
    loc = st.session_state["selected_location"]

st.session_state.pop('selected_location', None)

st.markdown(
    f"<h1 style='text-align: center;'>{loc['restaurant_name']}</h2>",
    unsafe_allow_html=True
)
st.markdown(
    f"<h4 style='text-align: center;'>{loc['address']}</h4>",
    unsafe_allow_html=True
)

reviews = get_employee_reviews(loc["location_id"])

st.markdown("## Employee Reviews")

if not reviews:
    st.info("No employee reviews yet for this restaurant.")
else:
    for review in reviews:
        employee_name = review["employee_name"]
        review_text = review["review_text"]
        review_date = review["review_date"]
        avg_score = review["avg_score"] if review["avg_score"] is not None else "N/A"
        
       

        with st.container():
            st.markdown(f"### {employee_name}")
            st.write(f"{review_date}")
            col3, col4 = st.columns([3, 1])
            with col3:
                st.write(review_text)

            with col4:
                st.write(f"**Average Score:** {avg_score}")
                reviewer_id = review["user_id"]
                if reviewer_id == 1:
                    if st.button("Edit", key=f"edit_{review['emp_review_id']}"):
                        st.session_state["emp_review_id"] = f'{review["emp_review_id"]}'
                        st.session_state["location_id"] = f'{loc["location_id"]}'
                        st.switch_page("pages/12_Employee_Write.py")                
            st.divider()

cols = st.columns(2)
with cols[0]:
    if st.button("✍️ Write an Employee Review", use_container_width=True, type="primary"):
        st.switch_page("pages/13_Employee_Write.py")
with cols[1]:
    if st.button("📢 Submit a Complaint", use_container_width=True):
        st.switch_page("pages/14_Employee_Complaint.py")
