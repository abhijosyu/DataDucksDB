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
st.session_state.pop('owner_select_location', None)
st.session_state.pop('owner_select_location_reviews', None)


API_BASE = "http://web-api:4000/api/company"


company_id = 7  

def get_company_name(company_id):
    response = requests.get(f"{API_BASE}/{company_id}")
    response.raise_for_status()
    return response.json()

def get_company_locations(company_id):
    response = requests.get(f"{API_BASE}/{company_id}/locations")
    response.raise_for_status()
    return response.json()

locations = get_company_locations(company_id)

name = get_company_name(company_id)
st.markdown(f'# {name["name"]} Restauraunts List')
for loc in locations:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"### {loc['address']}, {loc['city']}")

        st.divider()
