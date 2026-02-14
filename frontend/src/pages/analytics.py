import streamlit as st
import pandas as pd
import plotly.express as px
from ..utils.state import get_api_client

def render_analytics_page():
    """Render the Analytics page"""
    st.title("Analytics and Insights")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Please set your User ID in the sidebar")
        return
    
    api = get_api_client()
    
    col1, col2 = st.columns([2, 4])
    with col1:
        days = st.selectbox(
            "Time period",
            options=[7, 30],
            format_func=lambda x: f"Last {x} days"
        )
    
    st.divider()
    
    # Get analytics data
    analytics = api.get_analytics(st.session_state.user_id, days)
    
    if not analytics:
        st.info("ℹNo data available yet. Start tracking your habits now!")
        return
    
    # Prepare DataFrame
    results = analytics.get("results", []) if isinstance(analytics, dict) else analytics
    
    if not results:
        st.info("There are no results for this period")
        return

    df = pd.DataFrame(results)


    if df.empty:
        st.info("There are no results for this period")
        return

    df["habit_title"] = df.get("habit_title", df.get("Title"))
    df["completion_rate"] = df.get("completion_rate", df.get("CompletionRate"))

    # convert to number for security
    df["completion_rate"] = pd.to_numeric(df["completion_rate"], errors="coerce").fillna(0.0)
    

    st.subheader("Completion Rates")
    
    cols = st.columns(min(len(df), 4))
    for idx, row in df.iterrows():
        with cols[idx % 4]:
            completion_rate = float(row["completion_rate"])
        
            st.metric(
                label=row['habit_title'],
                value=f"{completion_rate:.1f}%"
            )
    
    st.divider()
    
    # Detailed table
    st.subheader("Detailed Breakdown")
    
    display_df = df[['habit_title', 'completion_rate']].copy()
    display_df.columns = ['Habit', 'Rate (%)']

    display_df['Rate (%)'] = display_df['Rate (%)'].round(1)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    # Visualization
    st.subheader("Visual Progress")
    
    # Bar chart
    fig = px.bar(
        df,
        x='habit_title',
        y='completion_rate',
        labels={'habit_title': 'Habit', 'completion_rate': 'Completion Rate (%)'},
        color='completion_rate',
        color_continuous_scale='Blues',
        text='completion_rate'
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="",
        yaxis_title="Completion Rate (%)",
        yaxis_range=[0, 105]
    )
    
    st.plotly_chart(fig, use_container_width=True)