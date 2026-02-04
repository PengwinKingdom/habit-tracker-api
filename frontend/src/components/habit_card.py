import streamlit as st

def render_habit_card(habit: dict):
    """Renderizar una tarjeta de hábito"""
    status_class = "status-active" if habit.get('is_active', True) else "status-inactive"
    status_text = "Activo" if habit.get('is_active', True) else "Inactivo"
    
    created_date = habit.get('created_at', 'N/A')[:10]
    
    st.markdown(f"""
    <div class="habit-card">
        <div class="habit-title">{habit['title']}</div>
        <div class="habit-description">{habit.get('description', 'Sin descripción')}</div>
        <div class="habit-meta">
            <span class="status-badge {status_class}">{status_text}</span>
            &nbsp;&nbsp;•&nbsp;&nbsp;
            Creado: {created_date}
        </div>
    </div>
    """, unsafe_allow_html=True)