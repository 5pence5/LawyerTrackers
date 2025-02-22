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
        with st.expander("Client Management"):
            new_client = st.text_input("Add New Client")
            if st.button("Add Client"):
                if new_client:
                    data_manager.add_client(new_client)
                    st.success(f"Added client: {new_client}")
        
        # Matter Management
        with st.expander("Matter Management"):
            selected_client = st.selectbox(
                "Select Client",
                data_manager.get_clients()
            )
            new_matter = st.text_input("Add New Matter")
            if st.button("Add Matter"):
                if selected_client and new_matter:
                    data_manager.add_matter(selected_client, new_matter)
                    st.success(f"Added matter: {new_matter} for client: {selected_client}")

if __name__ == "__main__":
    main()
