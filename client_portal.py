import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_client_portal(data_manager, client_name):
    """Render the client portal interface"""
    st.title(f"Client Portal - {client_name}")
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=30)
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now()
        )
    
    if start_date <= end_date:
        # Get time entries for the client
        entries = data_manager.get_client_entries(client_name, start_date, end_date)
        
        if not entries.empty:
            # Summary statistics
            total_hours = sum(
                sum(int(x) * (60 if i == 0 else 1) for i, x in enumerate(duration.split(":")))
                for duration in entries['duration']
            ) / 60
            
            # Display summary metrics
            st.metric("Total Hours", f"{total_hours:.2f}")
            
            # Display detailed entries
            st.subheader("Time Entries")
            st.dataframe(
                entries[['date', 'matter', 'duration', 'narrative']],
                use_container_width=True
            )
            
            # Export option
            if st.button("Export to CSV"):
                entries.to_csv(f"time_entries_{client_name}.csv", index=False)
                st.success(f"Data exported to time_entries_{client_name}.csv")
        else:
            st.info("No time entries found for the selected date range")
    else:
        st.error("End date must be after start date")

def render_client_login():
    """Render the client login interface"""
    st.title("Client Portal Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            from client_auth import ClientAuth
            auth = ClientAuth()
            success, client_name = auth.authenticate_client(username, password)
            
            if success:
                st.session_state.client_logged_in = True
                st.session_state.client_name = client_name
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
