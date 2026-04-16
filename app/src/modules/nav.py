# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has functions to add links to the left sidebar based on the user's role.

import streamlit as st


# ---- General ----------------------------------------------------------------

def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🍽️")


def about_page_nav():
    st.sidebar.page_link("pages/40_About.py", label="About", icon="🐤")


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

def employee_home_nav():
    st.sidebar.page_link(
        "pages/10_Employee_Home.py", label="Employee Home", icon="🏠"
    )

def employee_restauraunt_reviews():
    st.sidebar.page_link(
        "pages/11_Employee_Restaurant_Reviews.py", label="Employee Reviews", icon="⭐️"
    )


def employee_write_review():
    st.sidebar.page_link(
        "pages/12_Employee_Write.py", label="Write Review", icon="✏️"
    )


def employee_write_complaint():
    st.sidebar.page_link("pages/13_Employee_Complaint.py", label="Write a Complaint", icon="⚠️")

# ---- Role: company owner ----------------------------------------------------

def owner_home_nav():
    st.sidebar.page_link("pages/20_Owner_Home.py", label="Owner Home", icon="🏠")


def owner_my_restauraunts():
    st.sidebar.page_link("pages/24_Owner_Restauraunts.py", label="My Restauraunts", icon="🍽️")

def local_stats():
    st.sidebar.page_link(
        "pages/21_Restaraunt_Stats.py", label="Local Restaurant Analytics", icon="📊"
    )

def global_stats():
    st.sidebar.page_link(
        "pages/22_Global_Restaurant_Stats.py", label="Global Restaurant Analytics", icon="🌎"
    )

def local_reviews():
    st.sidebar.page_link(
        "pages/23_Local_Restaurant_Reviews.py", label="Local Restaurant Reviews", icon="🗒️"
    )



# ---- Role: administrator ----------------------------------------------------

def admin_home_nav():
    st.sidebar.page_link("pages/30_Admin_Home.py", label="Admin Home", icon="🏠")

def admin_users_list():
    st.sidebar.page_link("pages/33_Users_List.py", label="Users List", icon="👤")

def admin_view_complaints():
    st.sidebar.page_link("pages/32_View_Complaints.py", label="View Complaints", icon="⚠️")

def admin_message_user():
    st.sidebar.page_link("pages/31_Message_User.py", label="Message User", icon="🧑‍💻")




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
            employee_home_nav()
            reviewer_restaurant_list()
            employee_restauraunt_reviews()
            employee_write_review()
            employee_write_complaint()

        if st.session_state["role"] == "owner":
            owner_home_nav()
            owner_my_restauraunts()
            local_stats()
            global_stats()
            local_reviews()

        if st.session_state["role"] == "administrator":
            admin_home_nav()
            admin_users_list()
            admin_view_complaints()
            admin_message_user()

    # About link appears at the bottom for all roles
    about_page_nav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
