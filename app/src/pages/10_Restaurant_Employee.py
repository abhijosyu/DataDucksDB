import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Restauraunt Employee, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('View Restauraunt List',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_Restauraunts_List.py')

if st.button('View Restauraunt Employee Reviews',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/03_Employee_Restaurant_Reviews.py')

if st.button('Write Employee Review',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/04_Employee_Write.py')

    if st.button('Write Employee Complaint', type='primary', use_container_width=True):
        st.switch_page('pages/05_Employee_Complaint.py')
