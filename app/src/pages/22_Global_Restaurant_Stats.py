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
st.markdown("# Company Metrics")


def get_company_analytics(company_id):
    response = requests.get(f"http://127.0.0.1:5000/companies/{company_id}/analytics")
    response.raise_for_status()
    return response.json()

company_id = 7
analytics = get_company_analytics(company_id)

st.title("Company Analytics")

st.metric("Average Customer Rating", analytics["avg_customer_rating"])
st.metric("Average Employee Rating", analytics["avg_employee_rating"])
st.metric("Total Customer Reviews", analytics["total_customer_reviews"])
st.metric("Total Employee Reviews", analytics["total_employee_reviews"])

st.write("Top Complaint:", analytics["top_complaint"])
st.write("Top Strength:", analytics["top_strength"])


