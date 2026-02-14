import streamlit as st
from datetime import date
from ..utils.state import get_api_client
from ..utils.dates import format_date

def render_today_page():
    """Render the Daily Tracking page"""
    st.title("Today's Follow-up")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Please set your User ID in the sidebar")
        return
    
    api = get_api_client()
    
    # Select Date
    selected_date = st.date_input(
        "Select Date",
        value=date.today(),
        max_value=date.today(),
        help="You can record habits from previous days"
    )
    
    st.divider()
    
    # Get active habits
    habits = api.get_habits(st.session_state.user_id)
    active_habits = [h for h in (habits or []) if h.get('is_active', True)]
    
    if not active_habits:
        st.info("ℹ️ You don't have any active habits. Go to the Habits page to create one")
        return
    
    st.subheader(f"Active habits ({len(active_habits)})")
    
    log_date = format_date(selected_date)

    logs_by_habit = {}
    for h in active_habits:
        hid = h.get("id") or h.get("HabitId")
        if hid is None:
            continue

        logs = api.get_habit_logs(hid, days=30) or []
        found = None
        for lg in logs:
            d = lg.get("LogDate") or lg.get("log_date")
            if isinstance(d, str):
                d = d.split("T")[0]
            if d == log_date:
                found = lg
                break

        if found:
            logs_by_habit[hid] = found

    # Tracking each habit
    for habit in active_habits:
        habit_id = habit.get("id") or habit.get("HabitId") 

        if habit_id is None:
            continue

        existing = logs_by_habit.get(habit_id) 

        default_completed = bool(existing.get("Completed")) if existing else False
        default_notes = (existing.get("Notes") or "") if existing else ""

        with st.container():
            st.markdown(f"""
            <div class="habit-card today-habit-container">
                <div class="habit-title">{habit['title']}</div>
                <div class="habit-description">{habit.get('description', '')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                completed = st.checkbox(
                    "✓ Completed",
                    key=f"completed_{habit_id}_{log_date}", 
                    value=default_completed  
                )
            
            with col2:
                notes = st.text_input(
                    "Notes (optional)",
                    key=f"notes_{habit_id}_{log_date}",
                    value=default_notes, 
                    placeholder="Thoughts or reflections...",
                    label_visibility="collapsed"
                )
            
            with col3:
                if st.button("💾 Save", key=f"save_{habit_id}", use_container_width=True):
                    log_date = format_date(selected_date)
                    result = api.upsert_log(habit_id, log_date, completed, notes)

                    if result is not None:
                        st.success("✅ Saved!")
                        st.rerun()
            