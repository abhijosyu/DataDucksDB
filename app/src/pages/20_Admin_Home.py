import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Restaurant Reviewer, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('View Restauraunt List',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_Restauraunts_List.py')

if st.button('View Restauraunt Reviews',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_Reviewer_Restaurant_Reviews.py')
