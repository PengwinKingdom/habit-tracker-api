import streamlit as st
from pathlib import Path
from src.styles import load_all_styles
from src.utils.state import initialize_session_state, get_api_client
from src.pages.habits import render_habits_page
from src.pages.today import render_today_page
from src.pages.analytics import render_analytics_page

# Configuración de página
st.set_page_config(
    page_title="Habit Tracker",
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estado
initialize_session_state()

# Cargar CSS
load_all_styles()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.title("Configuración")
    
    # User ID
    user_id_input = st.number_input(
        "User ID",
        min_value=1,
        value=st.session_state.user_id if st.session_state.user_id else 1,
        help="Ingresa tu ID de usuario"
    )
    
    # API Base URL
    api_url_input = st.text_input(
        "API Base URL",
        value=st.session_state.api_base_url,
        help="Endpoint del backend API"
    )
    
    if st.button("Guardar Configuración", use_container_width=True):
        st.session_state.user_id = user_id_input
        st.session_state.api_base_url = api_url_input.rstrip('/')
        st.success("Configuración guardada!")
        st.rerun()
    
    st.divider()
    
    # Navegación
    st.subheader("📍 Navegación")
    
    if st.button(
        "Hábitos",
        use_container_width=True,
        type="primary" if st.session_state.page == "Habits" else "secondary"
    ):
        st.session_state.page = "Habits"
        st.rerun()
    
    if st.button(
        "Hoy",
        use_container_width=True,
        type="primary" if st.session_state.page == "Today" else "secondary"
    ):
        st.session_state.page = "Today"
        st.rerun()
    
    if st.button(
        "Analytics",
        use_container_width=True,
        type="primary" if st.session_state.page == "Analytics" else "secondary"
    ):
        st.session_state.page = "Analytics"
        st.rerun()
    
    st.divider()
    
    # Estado de conexión
    if st.session_state.user_id:
        st.success(f"✓ User ID: {st.session_state.user_id}")
        
        # Health check
        api = get_api_client()
        if api.health_check():
            st.success("✓ Backend conectado")
        else:
            st.error("✗ Backend no disponible")
    else:
        st.warning("⚠ Configura tu User ID")

# ==================== MAIN CONTENT ====================
if st.session_state.page == "Habits":
    render_habits_page()
elif st.session_state.page == "Today":
    render_today_page()
elif st.session_state.page == "Analytics":
    render_analytics_page()