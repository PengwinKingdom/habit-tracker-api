import streamlit as st
import requests
from src.utils.state import initialize_session_state

def render_weekly_reports_page():
    initialize_session_state()
    API_BASE = st.session_state.api_base_url

    st.title("Weekly Reports")

    user_id = st.number_input(
        "User ID",
        min_value=1,
        step=1,
        value=st.session_state.user_id or 2
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Weekly Report"):
            r = requests.post(f"{API_BASE}/users/{user_id}/insights/weekly-summary")
            if r.status_code == 200:
                st.success("Weekly report generated and saved ✅")
                st.session_state["latest_report"] = r.json()
            else:
                st.error(f"Error {r.status_code}: {r.text}")

    with col2:
        if st.button("Refresh"):
            st.session_state.pop("latest_report", None)

    st.divider()

    # -------- Latest report --------
    st.subheader("Latest Report")

    latest = None
    if "latest_report" in st.session_state:
        latest = st.session_state["latest_report"]
    else:
        r = requests.get(f"{API_BASE}/users/{user_id}/reports/weekly/latest")
        if r.status_code == 200:
            latest = r.json()

    if latest:
        week_start = latest.get("WeekStartDate") or latest.get("week_start")
        week_end = latest.get("WeekEndDate") or latest.get("week_end")
        tone = latest.get("tone") or latest.get("Tone") or "supportive"
        summary = latest.get("summary") or latest.get("Summary")
        highlights = latest.get("highlights") or latest.get("Highlights", [])
        next_actions = latest.get("next_actions") or latest.get("NextActions", [])

        st.write(f"**Week:** {week_start} → {week_end}")
        st.write(f"**Tone:** {tone}")

        st.write("### Summary")
        st.info(summary)

        st.write("### Highlights")
        for h in highlights:
            st.write(f"✅ {h}")

        st.write("### Next actions")
        for a in next_actions:
            st.write(f"➡️ {a}")
    else:
        st.warning("No reports found yet. Generate one!")

    st.divider()

    # -------- History --------
    st.subheader("Report History")

    r = requests.get(f"{API_BASE}/users/{user_id}/reports/weekly?limit=12")
    if r.status_code != 200:
        st.error(f"Error loading history: {r.status_code} {r.text}")
        st.stop()

    items = r.json().get("items", [])
    if not items:
        st.info("No reports in history yet.")
        st.stop()

    options = [
        f"#{it['ReportId']} | {it['WeekStartDate']} → {it['WeekEndDate']}"
        for it in items
    ]
    selected = st.selectbox("Select a report", options)

    selected_id = int(selected.split("|")[0].replace("#", "").strip())

    detail = requests.get(f"{API_BASE}/users/{user_id}/reports/weekly/{selected_id}")
    if detail.status_code != 200:
        st.error(f"Error loading report: {detail.status_code} {detail.text}")
        st.stop()

    rep = detail.json()

    st.subheader("Selected Report")
    st.write(f"**Created At:** {rep['CreatedAt']}")

    st.write("### Summary")
    st.info(rep["summary"])

    st.write("### Highlights")
    for h in rep["highlights"]:
        st.write(f"✅ {h}")

    st.write("### Next actions")
    for a in rep["next_actions"]:
        st.write(f"➡️ {a}")