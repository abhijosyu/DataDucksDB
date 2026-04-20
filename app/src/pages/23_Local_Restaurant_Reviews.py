import logging
import requests
import streamlit as st
from urllib.error import URLError
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Restaurant Reviews")

# ----------------------------
# Session state setup
# ----------------------------
st.session_state.pop("owner_select_location", None)

if "owner_select_location_reviews" not in st.session_state:
    st.session_state["owner_select_location_reviews"] = None

if "show_customer_reviews" not in st.session_state:
    st.session_state["show_customer_reviews"] = True

if "show_employee_reviews" not in st.session_state:
    st.session_state["show_employee_reviews"] = False

company_id = 7  # replace with logged-in owner's company id later

API_BASE_COMPANY = "http://web-api:4000/api/company"
API_BASE_REVIEWER = "http://web-api:4000/api/reviewer"
API_BASE_EMPLOYEE = "http://web-api:4000/api/employee"


# ----------------------------
# API helpers
# ----------------------------
def get_company_locations(company_id):
    try:
        response = requests.get(f"{API_BASE_COMPANY}/{company_id}/locations", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching company locations: {e}")
        st.error("Could not load restaurant locations.")
        return []


def get_customer_reviews(location_id):
    try:
        response = requests.get(f"{API_BASE_REVIEWER}/locations/{location_id}/reviews", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching customer reviews: {e}")
        st.error("Could not load customer reviews.")
        return []


def get_employee_reviews(location_id):
    try:
        response = requests.get(f"{API_BASE_EMPLOYEE}/locations/{location_id}/employee-reviews", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching employee reviews: {e}")
        st.error("Could not load employee reviews.")
        return []


def get_location_by_id(company_locations, location_id):
    for loc in company_locations:
        if loc["location_id"] == location_id:
            return loc
    return None


# ----------------------------
# Toggle handlers
# ----------------------------
def show_customer():
    st.session_state["show_customer_reviews"] = True
    st.session_state["show_employee_reviews"] = False


def show_employee():
    st.session_state["show_customer_reviews"] = False
    st.session_state["show_employee_reviews"] = True



locations = get_company_locations(company_id)


selected_location = None
selected_location_id = st.session_state["owner_select_location_reviews"]

if selected_location_id is not None:
    selected_location = get_location_by_id(locations, selected_location_id)

    if selected_location is None:
        st.warning("Choose a location")
        st.session_state["owner_select_location_reviews"] = None

if st.session_state["owner_select_location_reviews"] is None:
    selected_location = st.selectbox(
        "Choose a restaurant location",
        locations,
        format_func=lambda loc: f'{loc.get("name", "Location")} - {loc.get("city", "")}'
        if "name" in loc else f'Location {loc["location_id"]} - {loc.get("city", "")}'
    )
    location_id = selected_location["location_id"]
else:
    location_id = st.session_state["owner_select_location_reviews"]
    selected_location = st.selectbox(
        "change a restaurant location",
        locations,
        format_func=lambda loc: f'{loc.get("city", "")}'
        if "name" in loc else f'{loc.get("city", "")}'
    )
    location_id = selected_location["location_id"]

    if selected_location:
        st.subheader(
            f'Selected {selected_location.get("name", "Restaurant")} - {selected_location.get("city", "")}'
        )






col1, col2 = st.columns(2)

with col1:
    st.button("Customer Reviews", on_click=show_customer, use_container_width=True)

with col2:
    st.button("Employee Reviews", on_click=show_employee, use_container_width=True)



if st.session_state["show_customer_reviews"]:
    st.subheader("Customer Reviews")
    customer_reviews = get_customer_reviews(location_id)

    if not customer_reviews:
        st.info("No customer reviews found.")
    else:
        for review in customer_reviews:
            reviewer_name = review.get("reviewer_name", "Anonymous")
            avg_score = review.get("avg_score", "N/A")
            review_date = review.get("review_date", "")
            review_text = review.get("review_text", "")

            st.markdown(f"**Reviewer:** {reviewer_name}")
            st.markdown(f"**Average Score:** {avg_score}/5")
            st.markdown(f"**Date:** {review_date}")
            st.write(review_text)
            st.divider()

elif st.session_state["show_employee_reviews"]:
    st.subheader("Employee Reviews")
    employee_reviews = get_employee_reviews(location_id)

    if not employee_reviews:
        st.info("No employee reviews found.")
    else:
        for review in employee_reviews:
            employee_name = review.get("employee_name", "Anonymous")
            avg_score = review.get("avg_score", "N/A")
            review_date = review.get("review_date", "")
            review_text = review.get("review_text", "")

            st.markdown(f"**Employee:** {employee_name}")
            st.markdown(f"**Average Score:** {avg_score}/5")
            st.markdown(f"**Date:** {review_date}")
            st.write(review_text)
            st.divider()