import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("My Restaurants")

if st.button('View My Restaurants',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_Restauraunts_List.py')

if st.button('View Restaurant Analytics',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_Reviewer_Restaurant_Reviews.py')


if st.button('View Restaurant Reviews',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_Reviewer_Restaurant_Reviews.py')

if st.button('View Restaurant Complaints',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_Reviewer_Restaurant_Reviews.py')
