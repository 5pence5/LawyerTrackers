import streamlit as st
from datetime import datetime, timedelta
import time

def render_timer():
    """Render the running timer component"""
    st.subheader("Timer")

    # Initialize timer state if not exists
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = timedelta()
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Timer" if not st.session_state.timer_running else "Stop Timer"):
            if not st.session_state.timer_running:
                # Start the timer
                st.session_state.timer_running = True
                st.session_state.start_time = datetime.now()
                st.session_state.last_update = datetime.now()
                st.rerun()
            else:
                # Stop the timer
                st.session_state.timer_running = False
                st.session_state.elapsed_time = datetime.now() - st.session_state.start_time
                st.session_state.start_time = None
                st.session_state.last_update = None
                st.rerun()

    with col2:
        if st.button("Reset"):
            st.session_state.timer_running = False
            st.session_state.start_time = None
            st.session_state.elapsed_time = timedelta()
            st.session_state.last_update = None
            if 'current_duration' in st.session_state:
                del st.session_state.current_duration
            st.rerun()

    # Update timer display
    if st.session_state.timer_running and st.session_state.start_time:
        current_time = datetime.now()
        elapsed = current_time - st.session_state.start_time

        # Display the timer
        hours = elapsed.seconds // 3600
        minutes = (elapsed.seconds % 3600) // 60
        st.metric("Time Elapsed", f"{hours:02d}:{minutes:02d}")

        # Store formatted time for auto-fill
        st.session_state.current_duration = f"{hours:02d}:{minutes:02d}"

        # Force a rerun every second to update the display
        if (st.session_state.last_update is None or 
            (current_time - st.session_state.last_update).seconds >= 1):
            st.session_state.last_update = current_time
            time.sleep(0.1)  # Small delay to prevent excessive reruns
            st.rerun()

    elif st.session_state.elapsed_time:
        hours = st.session_state.elapsed_time.seconds // 3600
        minutes = (st.session_state.elapsed_time.seconds % 3600) // 60
        st.metric("Time Elapsed", f"{hours:02d}:{minutes:02d}")
        st.session_state.current_duration = f"{hours:02d}:{minutes:02d}"

def render_time_entry_form(data_manager):
    """Render the time entry form"""
    st.subheader("Time Entry")

    with st.form("time_entry_form"):
        # Get and display available clients
        clients = data_manager.get_clients()
        if not clients:
            st.error("No clients available. Please add a client first.")
            return

        client = st.selectbox("Client", options=clients, key="client_select")

        # Get matters for selected client
        matters = data_manager.get_matters(client) if client else []
        if not matters and client:
            st.warning(f"No matters found for client: {client}")

        matter = st.selectbox("Matter", options=matters if matters else ["No matters available"], key="matter_select")

        # Auto-fill duration from timer if available
        default_duration = st.session_state.get('current_duration', "01:00")
        duration = st.text_input("Duration (HH:MM)", default_duration)
        narrative = st.text_area("Narrative", height=100)

        submitted = st.form_submit_button("Submit Time Entry")

        if submitted:
            if matter == "No matters available":
                st.error("Please select a valid matter before submitting")
                return

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
                st.session_state.last_update = None
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