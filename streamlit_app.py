import os
from datetime import date

import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


st.set_page_config(
    page_title="Elder Care Assistant",
    page_icon="ECA",
    layout="wide",
)


def api_request(method, path, *, json=None, params=None, auth=True):
    headers = {}
    if auth and st.session_state.get("token"):
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{path}",
            json=json,
            params=params,
            headers=headers,
            timeout=10,
        )
    except requests.RequestException as exc:
        return None, f"Could not reach API: {exc}"

    if response.ok:
        if response.content:
            return response.json(), None
        return {}, None

    try:
        detail = response.json().get("detail", response.text)
    except ValueError:
        detail = response.text
    return None, f"{response.status_code}: {detail}"


def require_login():
    if st.session_state.get("token"):
        return True
    st.info("Sign in or create an account to use this section.")
    return False


def render_status():
    data, error = api_request("GET", "/health", auth=False)
    if error:
        st.error(error)
        return
    st.success(f"API status: {data.get('status', 'unknown')}")


def render_auth():
    left, right = st.columns(2)

    with left:
        st.subheader("Sign In")
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Sign in")

        if submitted:
            data, error = api_request(
                "POST",
                "/api/v1/auth/login",
                params={"email": email, "password": password},
                auth=False,
            )
            if error:
                st.error(error)
            else:
                st.session_state.token = data["access_token"]
                st.success("Signed in.")
                st.rerun()

    with right:
        st.subheader("Create Account")
        with st.form("register_form"):
            first_name = st.text_input("First name")
            last_name = st.text_input("Last name")
            register_email = st.text_input("Email", key="register_email")
            register_password = st.text_input("Password", type="password", key="register_password")
            dob = st.date_input(
                "Date of birth",
                value=date(1960, 1, 1),
                min_value=date(1945, 1, 1),
                max_value=date(2000, 12, 31),
            )
            phone = st.text_input("Phone number")
            submitted = st.form_submit_button("Create account")

        if submitted:
            payload = {
                "email": register_email,
                "password": register_password,
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": dob.isoformat(),
                "phone_number": phone or None,
            }
            data, error = api_request("POST", "/api/v1/auth/register", json=payload, auth=False)
            if error:
                st.error(error)
            else:
                st.success(f"Account created for {data['first_name']} {data['last_name']}.")

    if st.session_state.get("token"):
        if st.button("Sign out"):
            st.session_state.pop("token", None)
            st.rerun()


def render_health():
    if not require_login():
        return

    left, right = st.columns([1, 1])
    with left:
        st.subheader("Add Reading")
        with st.form("health_form"):
            reading_type = st.selectbox(
                "Type",
                ["blood_pressure", "glucose", "temperature", "heart_rate", "oxygen"],
            )
            value = st.number_input("Primary value", min_value=0.0, step=1.0)
            secondary_value = st.number_input("Secondary value", min_value=0.0, step=1.0)
            unit = st.text_input("Unit", value="mmHg" if reading_type == "blood_pressure" else "")
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Save reading")

        if submitted:
            payload = {
                "reading_type": reading_type,
                "value": value,
                "secondary_value": secondary_value if secondary_value else None,
                "unit": unit,
                "notes": notes or None,
            }
            data, error = api_request("POST", "/api/v1/health/readings", json=payload)
            if error:
                st.error(error)
            else:
                st.success(f"Saved reading with status: {data.get('status')}")

    with right:
        st.subheader("Summary")
        data, error = api_request("GET", "/api/v1/health/summary")
        if error:
            st.error(error)
        else:
            st.json(data)


def render_reminders():
    if not require_login():
        return

    left, right = st.columns([1, 1])
    with left:
        st.subheader("Add Reminder")
        with st.form("reminder_form"):
            reminder_type = st.selectbox("Type", ["medication", "appointment", "activity", "hydration"])
            title = st.text_input("Title")
            description = st.text_area("Description")
            schedule_type = st.selectbox("Schedule", ["daily", "weekly", "once"])
            schedule_time = st.time_input("Time")
            submitted = st.form_submit_button("Create reminder")

        if submitted:
            payload = {
                "reminder_type": reminder_type,
                "title": title,
                "description": description or None,
                "schedule_type": schedule_type,
                "schedule_time": schedule_time.strftime("%H:%M"),
                "days_of_week": None,
                "reminder_minutes_before": 10,
            }
            data, error = api_request("POST", "/api/v1/reminders/", json=payload)
            if error:
                st.error(error)
            else:
                st.success(f"Created reminder: {data.get('title')}")

    with right:
        st.subheader("Upcoming")
        data, error = api_request("GET", "/api/v1/reminders/upcoming")
        if error:
            st.error(error)
        else:
            st.dataframe(data.get("upcoming", []), use_container_width=True)


def render_chat():
    if not require_login():
        return

    st.subheader("Medicine Information")
    with st.form("medicine_chat_form"):
        medicine_name = st.text_input("Medicine name")
        explain_medicine = st.form_submit_button("Explain medicine")

    if explain_medicine and medicine_name.strip():
        data, error = api_request(
            "POST",
            "/api/v1/chat/message",
            json={"message": f"Medicine name: {medicine_name}", "context": "medicine"},
        )
        if error:
            st.error(error)
        else:
            st.chat_message("user").write(medicine_name)
            st.chat_message("assistant").write(data["response"])

    message = st.chat_input("Send a message")
    if message:
        data, error = api_request(
            "POST",
            "/api/v1/chat/message",
            json={"message": message, "context": "general"},
        )
        if error:
            st.error(error)
        else:
            st.chat_message("user").write(message)
            st.chat_message("assistant").write(data["response"])

    data, error = api_request("GET", "/api/v1/chat/history")
    if not error and data:
        for item in data.get("messages", []):
            st.chat_message(item["role"]).write(item["content"])


def render_family():
    if not require_login():
        return

    left, right = st.columns([1, 1])
    with left:
        st.subheader("Add Family Member")
        with st.form("family_form"):
            family_email = st.text_input("Family email")
            relationship = st.text_input("Relationship")
            can_view_health = st.checkbox("Can view health", value=True)
            can_edit_reminders = st.checkbox("Can edit reminders")
            submitted = st.form_submit_button("Add family member")

        if submitted:
            payload = {
                "family_email": family_email,
                "relationship": relationship,
                "can_view_health": can_view_health,
                "can_edit_reminders": can_edit_reminders,
            }
            data, error = api_request("POST", "/api/v1/family/members", json=payload)
            if error:
                st.error(error)
            else:
                st.success(f"Added {data.get('family_email')}")

    with right:
        st.subheader("Members")
        data, error = api_request("GET", "/api/v1/family/members")
        if error:
            st.error(error)
        else:
            st.dataframe(data.get("members", []), use_container_width=True)


def render_emergency():
    if not require_login():
        return

    st.subheader("Emergency")
    emergency_type = st.selectbox("Type", ["general", "fall", "medical", "medication"])
    severity = st.selectbox("Severity", ["high", "critical"])
    if st.button("Activate emergency protocol", type="primary"):
        data, error = api_request(
            "POST",
            "/api/v1/emergency/activate",
            json={"type": emergency_type, "severity": severity},
        )
        if error:
            st.error(error)
        else:
            st.warning(data.get("message"))
            st.json(data)


st.title("Elder Care Assistant")

tabs = st.tabs(["Account", "Health", "Reminders", "Chat", "Family", "Emergency"])
with tabs[0]:
    render_auth()
with tabs[1]:
    render_health()
with tabs[2]:
    render_reminders()
with tabs[3]:
    render_chat()
with tabs[4]:
    render_family()
with tabs[5]:
    render_emergency()
