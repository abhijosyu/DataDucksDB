import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome System Admin, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('Users List',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/31_Users_List.py')

if st.button('View Reviews',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_View_Reviews.py')

if st.button('View Complaints',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/33_View_Complaints.py')

if st.button('Message User',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/34_Message_User.py')
