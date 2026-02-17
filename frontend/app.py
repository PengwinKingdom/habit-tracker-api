import streamlit as st
from pathlib import Path
from src.styles import load_all_styles
from src.utils.state import initialize_session_state, get_api_client
from src.pages.habits import render_habits_page
from src.pages.today import render_today_page
from src.pages.analytics import render_analytics_page
from src.pages.weekly_reports import render_weekly_reports_page

#  Configuration of the webpage
st.set_page_config(
    page_title="Habit Tracker",
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_session_state()
load_all_styles()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.title("Settings")

    api = get_api_client()

    # ---------------- Active user (dropdown) ----------------
    st.subheader("Active user")

    users_data = api.list_users(limit=50) or {"items": []}
    users = users_data.get("items", [])

    options = []
    id_map = {}

    for u in users:
        uid = u["UserId"]
        label = f"{uid} — {u['FullName']} ({u['Email']})"
        options.append(label)
        id_map[label] = uid

    selected_user_id = None
    if options:
        default_index = 0
        if st.session_state.user_id:
            for i, opt in enumerate(options):
                if id_map[opt] == st.session_state.user_id:
                    default_index = i
                    break

        selected = st.selectbox("Select a user", options, index=default_index)
        selected_user_id = id_map[selected]
        st.success("✓ User exists")
    else:
        st.info("No users yet. Create one below.")

    # ---------------- API Base URL ----------------
    api_url_input = st.text_input(
        "API Base URL",
        value=st.session_state.api_base_url,
        help="Backend API base URL"
    )

    if st.button("Set active user", use_container_width=True):
        if selected_user_id is None:
            st.error("Create a user first.")
        else:
            st.session_state.user_id = selected_user_id
            st.session_state.api_base_url = api_url_input.rstrip("/")
            st.success("Active user updated ✅")
            st.rerun()

    st.divider()

    # ---------------- Create user ----------------
    st.subheader("Create user")
    full_name = st.text_input("Full name", value="")
    email = st.text_input("Email", value="")

    if st.button("Create User", use_container_width=True):
        if not full_name.strip() or not email.strip():
            st.error("Full name and email are required.")
        else:
            created = api.create_user(full_name=full_name.strip(), email=email.strip())
            if created:
                new_id = created.get("UserId") or created.get("user_id") or created.get("id")
                if new_id:
                    st.session_state.user_id = int(new_id)
                    st.success(f"User created ✅ (User ID: {new_id})")
                    st.rerun()
                else:
                    st.warning("User created, but could not read the new user ID.")

    st.divider()

    # ---------------- Navigation ----------------
    st.subheader("📍 Navigation")

    if st.button(
        "Habits",
        use_container_width=True,
        type="primary" if st.session_state.page == "Habits" else "secondary"
    ):
        st.session_state.page = "Habits"
        st.rerun()

    if st.button(
        "Today",
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

    if st.button(
        "Weekly Reports",
        use_container_width=True,
        type="primary" if st.session_state.page == "Weekly Reports" else "secondary"
    ):
        st.session_state.page = "Weekly Reports"
        st.rerun()

    st.divider()

    # ---------------- Connection status ----------------
    if st.session_state.user_id:
        st.success(f"✓ Active User ID: {st.session_state.user_id}")
        if api.health_check():
            st.success("✓ Backend connected")
        else:
            st.error("✗ Backend not available")
    else:
        st.warning("⚠ Select or create a user")

# ==================== MAIN CONTENT ====================
if st.session_state.page == "Habits":
    render_habits_page()
elif st.session_state.page == "Today":
    render_today_page()
elif st.session_state.page == "Analytics":
    render_analytics_page()
elif st.session_state.page == "Weekly Reports":
    render_weekly_reports_page()