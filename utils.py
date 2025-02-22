import streamlit as st

def initialize_session_state():
    """Initialize session state variables"""
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = None
