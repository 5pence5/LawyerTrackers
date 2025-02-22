import streamlit as st

def apply_custom_style():
    """Apply custom styling to the application"""
    st.markdown("""
        <style>
        .stButton > button {
            width: 100%;
        }
        
        .reportview-container {
            background: #ffffff
        }
        
        .main .block-container {
            padding-top: 2rem;
        }
        
        h1 {
            color: #2c3e50;
            padding-bottom: 1rem;
        }
        
        h2 {
            color: #34495e;
            padding-bottom: 0.5rem;
        }
        
        .stMetric {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }
        
        .stSelectbox {
            margin-bottom: 1rem;
        }
        
        .stTextArea {
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
