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
st.markdown("# Complaints")

API_BASE = "http://web-api:4000/api/admin"

def get_complaints():
    try:
        response = requests.get(f"{API_BASE}/complaints")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching complaints: {e}")
        st.error("Could not load complaints.")
        return []
    
def delete_complaint(complaint_id):
    try:
        response = requests.delete(f"{API_BASE}/complaints/{complaint_id}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting complaint {complaint_id}: {e}")
        st.error(f"Could not delete complaint #{complaint_id}.")
        return False

complaints = get_complaints()

if not complaints:
    st.info("No complaints found.")
else:
    for complaint in complaints:
        complaint_id = complaint.get("complaint_id", "N/A")
        user_id = complaint.get("user_id", "N/A")
        description = complaint.get("description", "")
        status = complaint.get("status", "N/A")

        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"### Complaint #{complaint_id}")
            st.write(f"**User:** {complaint.get('name', '')}")
            st.write(f"**Email:** {complaint.get('email', '')}")
            st.write(f"**Role:** {complaint.get('role', '')}")
            st.write(f"**Description:** {complaint.get('description', '')}")

        with col2:
            st.write(f"**Status:** {status}")

            if st.button("Delete", key=f"delete_{complaint_id}"):
                if delete_complaint(complaint_id):
                    st.success(f"Complaint #{complaint_id} deleted.")
                    st.rerun()

        st.divider()

