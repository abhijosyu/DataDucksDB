# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has functions to add links to the left sidebar based on the user's role.

import streamlit as st


# ---- General ----------------------------------------------------------------

def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🍽️")


def about_page_nav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🐤")


# ---- Role: reviewer ------------------------------------------------

def reviewer_home_nav():
    st.sidebar.page_link(
        "pages/00_Reviewer_Home.py", label="Reviewer Home", icon="👤"
    )


def reviewer_restaurant_list():
    st.sidebar.page_link(
        "pages/01_Restauraunts_List.py", label="Restauraunts List", icon="📋"
    )

def reviewer_user_reviews():
    st.sidebar.page_link(
        "pages/02_Reviewer_Restaurant_Reviews.py", label="User Reviews", icon="⭐️"
    )

def reviewer_write_review():
    st.sidebar.page_link(
        "pages/03_Reviewer_Write.py", label="Write Reviews", icon="✏️"
    )




# ---- Role: employee -----------------------------------------------------

def employee_restauraunt_reviews():
    st.sidebar.page_link(
        "pages/03_Employee_Restaurant_Reviews.py", label="Employee Reviews", icon="⭐️"
    )


def employee_write_review():
    st.sidebar.page_link(
        "pages/04_Employee_Write.py", label="Write Review", icon="✏️"
    )


def employee_write_complaint():
    st.sidebar.page_link("pages/05_Employee_Complaint.py", label="Write a Complaint", icon="⚠️")

# ---- Role: company owner ----------------------------------------------------

def owner_home_nav():
    st.sidebar.page_link("pages/11_Owner_Home.py", label="Owner Home", icon="🏠")


def local_stats():
    st.sidebar.page_link(
        "pages/12_Restaraunt_Stats.py", label="Local Restaurant Analytics", icon="📊"
    )

def global_stats():
    st.sidebar.page_link(
        "pages/13_Global_Restaurant_Stats.py", label="Global Restaurant Analytics", icon="🌎"
    )

def local_reviews():
    st.sidebar.page_link(
        "pages/14_Local_Restaurant_Reviews.py", label="Local Restaurant Reviews", icon="🗒️"
    )



# ---- Role: administrator ----------------------------------------------------

def admin_home_nav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")


def ml_model_mgmt_nav():
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )


# ---- Sidebar assembly -------------------------------------------------------

def SideBarLinks(show_home=False):
    """
    Renders sidebar navigation links based on the logged-in user's role.
    The role is stored in st.session_state when the user logs in on Home.py.
    """

    # Logo appears at the top of the sidebar on every page
    st.sidebar.image("assets/logo.png", width=300)

    # If no one is logged in, send them to the Home (login) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        home_nav()

    if st.session_state["authenticated"]:

        if st.session_state["role"] == "reviewer":
            reviewer_home_nav()
            reviewer_restaurant_list()
            reviewer_user_reviews()
            reviewer_write_review()

        if st.session_state["role"] == "employee":
            reviewer_restaurant_list()
            employee_restauraunt_reviews()
            employee_write_review()
            employee_write_complaint()

        if st.session_state["role"] == "owner":
            owner_home_nav()
            local_stats()
            global_stats()
            local_reviews()

        if st.session_state["role"] == "administrator":
            reviewer_home_nav()

    # About link appears at the bottom for all roles
    about_page_nav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
