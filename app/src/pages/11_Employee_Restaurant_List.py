import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.markdown('# List Of Restaurants')
st.session_state.pop('selected_location', None)
st.session_state.pop('review_id', None)
st.session_state.pop('location_id', None)

API_BASE = "http://web-api:4000/api/employee"


def get_locations():
    try:
        response = requests.get(f"{API_BASE}/locations")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching locations: {e}")
        return []


locations = get_locations()

if not locations:
    st.warning("No restaurant locations found.")
else:
    valid_scores = []

    for loc in locations:
        scores = [
            loc.get("avg_pay"),
            loc.get("avg_management"),
            loc.get("avg_work_life_balance")
        ]
        for score in scores:
            if score is not None:
                valid_scores.append(float(score))

    if valid_scores:
        max_score = float(max(valid_scores))

        selected_range = st.slider(
            "Filter by workplace score",
            min_value=0.0,
            max_value=5.0,
            value=(0.0, max_score),
            step=0.5
        )

        filtered_locations = []
        for loc in locations:
            scores = [
                loc.get("avg_pay"),
                loc.get("avg_management"),
                loc.get("avg_work_life_balance")
            ]

            numeric_scores = [float(s) for s in scores if s is not None]

            if not numeric_scores:
                continue

            overall_work_score = sum(numeric_scores) / len(numeric_scores)

            if selected_range[0] <= overall_work_score <= selected_range[1]:
                loc["overall_work_score"] = round(overall_work_score, 1)
                filtered_locations.append(loc)
    else:
        st.info("No workplace scores available yet.")
        filtered_locations = locations

    if not filtered_locations:
        st.warning("No restaurants match that score range.")
    else:
        for loc in filtered_locations:
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"### {loc['restaurant_name']}")
                st.caption(f"{loc['address']}, {loc['city']}")

            with col2:
                pay = loc.get("avg_pay", "N/A")
                management = loc.get("avg_management", "N/A")
                work_life = loc.get("avg_work_life_balance", "N/A")

                st.markdown(f"""
                **💵 Pay:** {pay}  
                **👔 Management:** {management}  
                **⚖️ Work-Life Balance:** {work_life}
                """)

                if st.button("View", key=f"view_{loc['location_id']}"):
                    st.session_state["selected_location"] = loc
                    st.switch_page("pages/12_Employee_Restaurant_Reviews.py")

            st.divider()