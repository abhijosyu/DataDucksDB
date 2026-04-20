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
st.markdown("# Message User")


API_BASE = "http://web-api:4000/api/admin"

def get_users():
    try:
        response = requests.get(f"{API_BASE}/users")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching users: {e}")
        st.error("Could not load users.")
        return []

users = get_users()

if not users:
    st.warning("No users found.")
    st.stop()

selected_user = st.selectbox(
    "Choose a user",
    users,
    format_func=lambda u: f"{u.get('name', '')} ({u.get('role', 'Unknown')})"
)

message_text = st.text_area("Write your message")

if st.button("Send Message"):
    if not message_text.strip():
        st.warning("Please write a message before sending.")
    else:
        payload = {
            "admin_id": 1,
            "user_id": selected_user["user_id"],
            "message_text": message_text
        }

        try:
            response = requests.post(
                f"{API_BASE}/messages",
                json=payload
            )

            if response.status_code == 201:
                st.success("Message sent successfully!")
            else:
                try:
                    st.error(f"Failed: {response.json()}")
                except ValueError:
                    st.error(f"Failed: {response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message: {e}")
            st.error("Could not send message.")