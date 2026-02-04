import streamlit as st
from ..utils.state import get_api_client
from ..components.habit_card import render_habit_card

def render_habits_page():
    """Renderizar la página de Hábitos"""
    st.title("Mis Hábitos")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Por favor configura tu User ID en la barra lateral.")
        return
    
    api = get_api_client()
    
    # Sección: Agregar nuevo hábito
    with st.expander("Agregar Nuevo Hábito", expanded=False):
        with st.form("add_habit_form", clear_on_submit=True):
            title = st.text_input(
                "Título del Hábito*",
                placeholder="ej. Ejercicio matutino"
            )
            description = st.text_area(
                "Descripción",
                placeholder="¿En qué consiste este hábito?",
                height=100
            )
            
            col1, col2 = st.columns([1, 5])
            with col1:
                submitted = st.form_submit_button("Crear", use_container_width=True)
            
            if submitted:
                if not title.strip():
                    st.error("El título es obligatorio")
                else:
                    result = api.create_habit(
                        st.session_state.user_id,
                        title.strip(),
                        description.strip()
                    )
                    if result:
                        st.success(f"Hábito '{title}' creado exitosamente!")
                        st.rerun()
    
    st.divider()
    
    # Listar hábitos existentes
    habits = api.get_habits(st.session_state.user_id)
    
    if habits:
        st.subheader(f"Total de Hábitos: {len(habits)}")
        
        for habit in habits:
            render_habit_card(habit)
    else:
        st.info("ℹAún no tienes hábitos. ¡Crea tu primer hábito arriba!")