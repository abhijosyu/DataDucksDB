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
st.markdown("# Local Restaurant Reviews")

import streamlit as st

st.title("Restaurant Reviews")

company_id = 7  # example

locations = get_company_locations(company_id)

if not locations:
    st.warning("No restaurant locations found.")
else:
    selected_location = st.selectbox(
        "Choose a restaurant location",
        locations,
        format_func=lambda loc: f'{loc["name"]} - {loc["city"]}'
    )

    location_id = selected_location["location_id"]

    customer_reviews = get_customer_reviews(location_id)
    employee_reviews = get_employee_reviews(location_id)

    st.subheader("Customer Reviews")
    if not customer_reviews:
        st.info("No customer reviews found.")
    else:
        for review in customer_reviews:
            st.markdown(f'**Rating:** {review["rating"]}/5')
            st.markdown(f'**Title:** {review["title"]}')
            st.write(review["comment"])
            st.divider()

    st.subheader("Employee Reviews")
    if not employee_reviews:
        st.info("No employee reviews found.")
    else:
        for review in employee_reviews:
            st.markdown(f'**Rating:** {review["rating"]}/5')
            st.markdown(f'**Title:** {review["title"]}')
            st.write(review["comment"])
            st.divider()
