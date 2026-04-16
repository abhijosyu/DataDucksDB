import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title(f"Welcome Owner, {st.session_state['first_name']}.")

if st.button('View My Restauraunts',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/24_Owner_Restauraunts.py')

if st.button('View Local Restaurant Analytics',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/21_Restaraunt_Stats.py')


if st.button('View Global Restaurant Stats',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/22_Global_Restaurant_Stats.py')

if st.button('View Local Restaurant Reviews',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/23_Local_Restaurant_Reviews.py')
