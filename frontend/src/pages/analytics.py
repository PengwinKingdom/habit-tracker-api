import streamlit as st
import pandas as pd
import plotly.express as px
from ..utils.state import get_api_client

def render_analytics_page():
    """Renderizar la página de Analytics"""
    st.title("Analytics e Insights")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Por favor configura tu User ID en la barra lateral.")
        return
    
    api = get_api_client()
    
    # Selector de período
    col1, col2 = st.columns([2, 4])
    with col1:
        days = st.selectbox(
            "Período de Tiempo",
            options=[7, 30],
            format_func=lambda x: f"Últimos {x} días"
        )
    
    st.divider()
    
    # Obtener datos de analytics
    analytics = api.get_analytics(st.session_state.user_id, days)
    
    if not analytics:
        st.info("ℹNo hay datos disponibles aún. ¡Comienza a registrar tus hábitos!")
        return
    
    # Preparar DataFrame
    results = analytics.get("results", []) if isinstance(analytics, dict) else analytics
    
    if not results:
        st.info("ℹNo hay resultados para este período.")
        return

    df = pd.DataFrame(results)


    if df.empty:
        st.info("ℹNo hay datos de analytics para este período.")
        return

    df["habit_title"] = df.get("habit_title", df.get("Title"))
    df["completion_rate"] = df.get("completion_rate", df.get("CompletionRate"))

    # convertir a número por seguridad
    df["completion_rate"] = pd.to_numeric(df["completion_rate"], errors="coerce").fillna(0.0)
    
    # Métricas de resumen
    st.subheader("Tasas de Completitud")
    
    cols = st.columns(min(len(df), 4))
    for idx, row in df.iterrows():
        with cols[idx % 4]:
            completion_rate = float(row["completion_rate"])
        
            st.metric(
                label=row['habit_title'],
                value=f"{completion_rate:.1f}%"
            )
    
    st.divider()
    
    # Tabla detallada
    st.subheader("Desglose Detallado")
    
    display_df = df[['habit_title', 'completion_rate']].copy()
    display_df.columns = ['Hábito', 'Tasa (%)']

    display_df['Tasa (%)'] = display_df['Tasa (%)'].round(1)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    # Visualización
    st.subheader("Progreso Visual")
    
    # Gráfico de barras
    fig = px.bar(
        df,
        x='habit_title',
        y='completion_rate',
        labels={'habit_title': 'Hábito', 'completion_rate': 'Tasa de Completitud (%)'},
        color='completion_rate',
        color_continuous_scale='Blues',
        text='completion_rate'
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="",
        yaxis_title="Tasa de Completitud (%)",
        yaxis_range=[0, 105]
    )
    
    st.plotly_chart(fig, use_container_width=True)