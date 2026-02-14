import streamlit as st
from ..utils.state import get_api_client
from ..components.habit_card import render_habit_card

def render_habits_page():
    st.title("My Habits")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Please configure your User ID in the sidebar")
        return
    
    api = get_api_client()
    
    # Section: Add new habit
    with st.expander("Add new habit", expanded=False):
        with st.form("add_habit_form", clear_on_submit=True):
            title = st.text_input(
                "Title of the habit*"
            )
            description = st.text_area(
                "Description",
                placeholder="What is this habit about?",
                height=100
            )
            
            col1, col2 = st.columns([1, 5])
            with col1:
                submitted = st.form_submit_button("Create", use_container_width=True)
            
            if submitted:
                if not title.strip():
                    st.error("The title is required")
                else:
                    result = api.create_habit(
                        st.session_state.user_id,
                        title.strip(),
                        description.strip()
                    )
                    if result:
                        st.success(f"Habit '{title}' successfully created!")
                        st.rerun()
    
    st.divider()
    
    # Listar hábitos existentes
    habits = api.get_habits(st.session_state.user_id)
    
    if habits:
        st.subheader(f"Total Habits: {len(habits)}")
        
        for habit in habits:
            render_habit_card(habit)
    else:
        st.info("ℹYou don't have any habits yet. Create your first habit above!")