import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import time

def render_timer():
    """Render the running timer component"""
    st.subheader("Timer")

    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
        st.session_state.start_time = None
        st.session_state.elapsed_time = timedelta()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Timer" if not st.session_state.timer_running else "Stop Timer"):
            if not st.session_state.timer_running:
                st.session_state.timer_running = True
                st.session_state.start_time = datetime.now()
            else:
                st.session_state.timer_running = False
                if st.session_state.start_time:
                    st.session_state.elapsed_time = datetime.now() - st.session_state.start_time

    with col2:
        if st.button("Reset"):
            st.session_state.timer_running = False
            st.session_state.start_time = None
            st.session_state.elapsed_time = timedelta()

    if st.session_state.timer_running and st.session_state.start_time:
        elapsed = datetime.now() - st.session_state.start_time
        st.metric("Time Elapsed", f"{elapsed.seconds // 3600:02d}:{(elapsed.seconds // 60) % 60:02d}")
        # Store formatted time for auto-fill
        st.session_state.current_duration = f"{elapsed.seconds // 3600:02d}:{(elapsed.seconds // 60) % 60:02d}"
    elif st.session_state.elapsed_time:
        st.metric("Time Elapsed", f"{st.session_state.elapsed_time.seconds // 3600:02d}:{(st.session_state.elapsed_time.seconds // 60) % 60:02d}")
        # Store formatted time for auto-fill
        st.session_state.current_duration = f"{st.session_state.elapsed_time.seconds // 3600:02d}:{(st.session_state.elapsed_time.seconds // 60) % 60:02d}"

def render_time_entry_form(data_manager):
    """Render the time entry form"""
    st.subheader("Time Entry")

    with st.form("time_entry_form"):
        client = st.selectbox("Client", data_manager.get_clients())

        matters = data_manager.get_matters(client) if client else []
        matter = st.selectbox("Matter", matters)

        # Auto-fill duration from timer if available
        default_duration = st.session_state.get('current_duration', "01:00")
        duration = st.text_input("Duration (HH:MM)", default_duration)
        narrative = st.text_area("Narrative", height=100)

        submitted = st.form_submit_button("Submit Time Entry")

        if submitted:
            try:
                hours, minutes = map(int, duration.split(":"))
                if hours < 0 or minutes < 0 or minutes >= 60:
                    st.error("Invalid duration format")
                    return

                entry = {
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'client': client,
                    'matter': matter,
                    'duration': duration,
                    'narrative': narrative
                }

                data_manager.add_time_entry(entry)
                st.success("Time entry added successfully!")

                # Reset timer after successful submission
                st.session_state.timer_running = False
                st.session_state.start_time = None
                st.session_state.elapsed_time = timedelta()
                if 'current_duration' in st.session_state:
                    del st.session_state.current_duration
                st.rerun()

            except ValueError:
                st.error("Please enter duration in HH:MM format")

def render_daily_log(data_manager):
    """Render the daily time log view"""
    st.subheader("Daily Time Log")

    selected_date = st.date_input("Select Date", datetime.now())

    entries = data_manager.get_daily_entries(selected_date)
    if not entries.empty:
        st.dataframe(entries)

        total_hours = sum(
            sum(int(x) * (60 if i == 0 else 1) for i, x in enumerate(duration.split(":")))
            for duration in entries['duration']
        ) / 60

        st.metric("Total Hours", f"{total_hours:.2f}")
    else:
        st.info("No entries for selected date")

def render_reports(data_manager):
    """Render the reporting view"""
    st.subheader("Reports")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())

    if start_date <= end_date:
        df = data_manager.get_report_data(start_date, end_date)

        if not df.empty:
            # Summary by client
            st.subheader("Summary by Client")
            client_summary = df.groupby('client')['duration'].agg(lambda x: sum(
                sum(int(t) * (60 if i == 0 else 1) for i, t in enumerate(d.split(":")))
                for d in x
            ) / 60).reset_index()
            client_summary.columns = ['Client', 'Total Hours']
            st.dataframe(client_summary)

            # Summary by matter
            st.subheader("Summary by Matter")
            matter_summary = df.groupby(['client', 'matter'])['duration'].agg(lambda x: sum(
                sum(int(t) * (60 if i == 0 else 1) for i, t in enumerate(d.split(":")))
                for d in x
            ) / 60).reset_index()
            matter_summary.columns = ['Client', 'Matter', 'Total Hours']
            st.dataframe(matter_summary)

            # Export option
            if st.button("Export to CSV"):
                df.to_csv("time_entries_export.csv", index=False)
                st.success("Data exported to time_entries_export.csv")
        else:
            st.info("No entries found for selected date range")
    else:
        st.error("End date must be after start date")