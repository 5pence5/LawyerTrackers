import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from data_manager import DataManager
from components import (
    render_timer,
    render_time_entry_form,
    render_daily_log,
    render_reports
)
from style import apply_custom_style
from utils import initialize_session_state

def main():
    st.set_page_config(
        page_title="Legal Time Tracker",
        page_icon="⚖️",
        layout="wide"
    )

    apply_custom_style()

    # Initialize data manager
    data_manager = DataManager()

    # Initialize session state
    initialize_session_state()

    # Main title
    st.title("⚖️ Legal Time Tracker")

    # Sidebar navigation
    page = st.sidebar.radio(
        "Navigation",
        ["Time Entry", "Daily Log", "Reports", "Client/Matter Management"]
    )

    if page == "Time Entry":
        col1, col2 = st.columns([2, 1])
        with col1:
            render_time_entry_form(data_manager)
        with col2:
            render_timer()

    elif page == "Daily Log":
        render_daily_log(data_manager)

    elif page == "Reports":
        render_reports(data_manager)

    elif page == "Client/Matter Management":
        st.header("Client/Matter Management")

        # Client Management
        with st.expander("Client Management", expanded=True):
            st.subheader("Add New Client")
            new_client = st.text_input("Client Name", key="new_client")
            if st.button("Add Client"):
                if new_client:
                    success, message = data_manager.add_client(new_client)
                    if success:
                        st.success(message)
                        st.session_state.new_client = ""  # Clear the input
                    else:
                        st.error(message)
                else:
                    st.error("Please enter a client name")

            st.subheader("Existing Clients")
            clients = data_manager.get_clients()
            if clients:
                st.table(pd.DataFrame(clients, columns=["Client Name"]))
            else:
                st.info("No clients added yet")

        # Matter Management
        with st.expander("Matter Management", expanded=True):
            st.subheader("Add New Matter")
            selected_client = st.selectbox(
                "Select Client",
                [""] + data_manager.get_clients(),
                key="matter_client"
            )

            if selected_client:
                new_matter = st.text_input("Matter Name", key="new_matter")
                if st.button("Add Matter"):
                    if new_matter:
                        success, message = data_manager.add_matter(selected_client, new_matter)
                        if success:
                            st.success(message)
                            st.session_state.new_matter = ""  # Clear the input
                        else:
                            st.error(message)
                    else:
                        st.error("Please enter a matter name")

                st.subheader("Existing Matters")
                matters = data_manager.get_matters(selected_client)
                if matters:
                    st.table(pd.DataFrame(matters, columns=["Matter Name"]))
                else:
                    st.info("No matters added yet for this client")
            else:
                st.info("Please select a client to add or view matters")

if __name__ == "__main__":
    main()