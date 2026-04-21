import logging
import requests

logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

API_BASE = "http://web-api:4000/api/admin"

def get_users():
    try:
        response = requests.get(f"{API_BASE}/users")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching users: {e}")
        return []

users = get_users()

if not users:
    st.warning("No users found.")
else:
    st.markdown("# List of Users")

    for user in users:
        st.markdown(f"### {user['name']}")
        st.write(f"Email: {user['email']}")
        st.write(f"Role: {user['role']}")
        st.divider()

