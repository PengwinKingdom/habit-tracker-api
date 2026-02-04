import streamlit as st

def initialize_session_state():
    """Inicializar todas las variables de session state"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'api_base_url' not in st.session_state:
        st.session_state.api_base_url = "http://127.0.0.1:8000"
    if 'page' not in st.session_state:
        st.session_state.page = "Habits"

def get_api_client():
    """Obtener instancia del cliente API"""
    from ..api.client import HabitTrackerAPI
    return HabitTrackerAPI(st.session_state.api_base_url)