import os
from datetime import date

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL")

if not API_BASE_URL:
    st.warning(
        "API_BASE_URL is not configured. Please set the API_BASE_URL environment variable to your backend URL."
    )
    st.stop()

API_BASE_URL = API_BASE_URL.rstrip("/")

st.set_page_config(
    page_title="Elder Care Assistant",
    page_icon="🌿",
    layout="wide",
)

# ── Custom styles ────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">

<style>
/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
    background-color: #FAF7F2 !important;
    color: #2C2C2C !important;
}

/* ── Header banner ── */
.eca-header {
    background: linear-gradient(135deg, #1B3A5C 0%, #2E6B8A 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 18px;
}
.eca-header h1 {
    font-family: 'Playfair Display', serif !important;
    color: #FAF7F2 !important;
    font-size: 2.2rem !important;
    margin: 0 !important;
    letter-spacing: 0.02em;
}
.eca-header p {
    color: #E8D5B0 !important;
    margin: 4px 0 0 0 !important;
    font-size: 1rem;
    font-weight: 600;
}
.eca-icon {
    font-size: 3rem;
    line-height: 1;
}

/* ── Section headings ── */
h2, h3, .stSubheader {
    font-family: 'Playfair Display', serif !important;
    color: #1B3A5C !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #EDE8E0;
    border-radius: 12px;
    padding: 6px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    color: #1B3A5C !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    border: none !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: #1B3A5C !important;
    color: #FAF7F2 !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    background: #E8A838 !important;
    color: #1B3A5C !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-size: 0.95rem !important;
    transition: background 0.2s ease, transform 0.1s ease;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}
.stButton > button:hover {
    background: #D4922A !important;
    transform: translateY(-1px);
}
.stButton > button[kind="primary"] {
    background: #C0392B !important;
    color: #FAF7F2 !important;
}
.stButton > button[kind="primary"]:hover {
    background: #A93226 !important;
}

/* ── Form submit buttons ── */
.stFormSubmitButton > button {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    background: #3D8B8B !important;
    color: #FAF7F2 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-size: 0.95rem !important;
    transition: background 0.2s ease;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}
.stFormSubmitButton > button:hover {
    background: #2E6B6B !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    font-family: 'Nunito', sans-serif !important;
    border-radius: 10px !important;
    border: 2px solid #D4C9BB !important;
    background: #FFFFFF !important;
    color: #2C2C2C !important;
    font-size: 0.95rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #3D8B8B !important;
    box-shadow: 0 0 0 3px rgba(61,139,139,0.15) !important;
}

/* ── Labels ── */
label, .stSelectbox label, .stTextInput label, .stNumberInput label {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    color: #1B3A5C !important;
    font-size: 0.9rem !important;
}

/* ── Forms ── */
.stForm {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    padding: 20px !important;
    border: 1px solid #E8DDD2 !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06) !important;
}

/* ── Alerts ── */
.stSuccess, [data-testid="stNotification"] {
    border-radius: 10px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #1B3A5C !important;
}
section[data-testid="stSidebar"] * {
    color: #FAF7F2 !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #E8DDD2 !important;
}

/* ── Divider ── */
hr {
    border-color: #E8DDD2 !important;
    margin: 20px 0 !important;
}

/* ── Info / Warning boxes ── */
.stInfo, .stWarning, .stError {
    border-radius: 10px !important;
    font-family: 'Nunito', sans-serif !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border-radius: 12px !important;
    border: 1px solid #E8DDD2 !important;
    margin-bottom: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Top banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="eca-header">
    <div class="eca-icon">🌿</div>
    <div>
        <h1>Elder Care Assistant</h1>
        <p>Compassionate care, one step at a time</p>
    </div>
</div>
""", unsafe_allow_html=True)

if "localhost" in API_BASE_URL or "127.0.0.1" in API_BASE_URL:
    st.warning("Running on localhost. Set API_BASE_URL to your backend host for deployed environments.")


# ── API helper ───────────────────────────────────────────────────────────────
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
    st.info("👋 Please sign in or create an account to use this section.")
    return False


# ── Sections ─────────────────────────────────────────────────────────────────
def render_auth():
    left, right = st.columns(2)

    with left:
        st.subheader("Sign In")
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Sign in →")
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
                    st.success("✅ Signed in successfully!")
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
                min_value=date(1900, 1, 1),
                max_value=date(2000, 12, 31),
            )
            phone = st.text_input("Phone number", placeholder="+91XXXXXXXXXX")
            submitted = st.form_submit_button("Create account →")
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
                    st.success(f"🎉 Account created for {data['first_name']} {data['last_name']}!")

    if st.session_state.get("token"):
        st.divider()
        if st.button("Sign out"):
            st.session_state.pop("token", None)
            st.rerun()


def render_health():
    if not require_login():
        return

    left, right = st.columns([1, 1])

    with left:
        st.subheader("🩺 Add Health Reading")
        with st.form("health_form"):
            reading_type = st.selectbox(
                "Reading type",
                ["blood_pressure", "glucose", "temperature", "heart_rate", "oxygen"],
            )
            value = st.number_input("Primary value", min_value=0.0, step=1.0)
            secondary_value = st.number_input("Secondary value (if any)", min_value=0.0, step=1.0)
            unit = st.text_input("Unit", value="mmHg" if reading_type == "blood_pressure" else "")
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Save reading →")
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
                    st.success(f"✅ Reading saved — status: {data.get('status')}")

    with right:
        st.subheader("📊 Health Summary")
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
        st.subheader("⏰ Add Reminder")
        with st.form("reminder_form"):
            reminder_type = st.selectbox("Reminder type", ["medication", "appointment", "activity", "hydration"])
            title = st.text_input("Title")
            description = st.text_area("Description")
            schedule_type = st.selectbox("Schedule", ["daily", "weekly", "once"])
            schedule_time = st.time_input("Time")
            submitted = st.form_submit_button("Create reminder →")
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
                    st.success(f"✅ Reminder created: {data.get('title')}")

    with right:
        st.subheader("📋 Upcoming Reminders")
        data, error = api_request("GET", "/api/v1/reminders/upcoming")
        if error:
            st.error(error)
        else:
            st.dataframe(data.get("upcoming", []), use_container_width=True)


def render_chat():
    if not require_login():
        return

    st.subheader("💊 Medicine Information")
    with st.form("medicine_chat_form"):
        medicine_name = st.text_input("Enter medicine name")
        explain_medicine = st.form_submit_button("Explain this medicine →")
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

    st.divider()
    st.subheader("💬 Chat with Assistant")
    message = st.chat_input("Ask me anything...")
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

    if "family_phones" not in st.session_state:
        st.session_state.family_phones = {}

    left, right = st.columns([1, 1])

    with left:
        st.subheader("👨‍👩‍👧 Add Family Member")
        with st.form("family_form"):
            family_email = st.text_input("Family member's email")
            family_phone = st.text_input(
                "Phone number",
                placeholder="+91XXXXXXXXXX",
                help="Include country code, e.g. +919876543210",
            )
            relationship = st.text_input("Relationship (e.g. Son, Daughter)")
            can_view_health = st.checkbox("Can view health records", value=True)
            can_edit_reminders = st.checkbox("Can edit reminders")
            submitted = st.form_submit_button("Add family member →")
            if submitted:
                if not family_email:
                    st.warning("Please enter an email address.")
                else:
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
                        if family_phone:
                            st.session_state.family_phones[family_email] = family_phone
                        st.success(f"✅ Added {data.get('family_email')}")

    with right:
        st.subheader("👥 Members")
        data, error = api_request("GET", "/api/v1/family/members")
        if error:
            st.error(error)
        else:
            members = data.get("members", [])
            if members:
                for m in members:
                    email = m.get("family_email", "")
                    m["phone_number"] = st.session_state.family_phones.get(email, "—")
                st.dataframe(members, use_container_width=True)
            else:
                st.info("No family members added yet.")

        if st.session_state.family_phones:
            st.divider()
            st.subheader("📞 Phone Numbers")
            for email, phone in st.session_state.family_phones.items():
                st.markdown(f"**{email}** &nbsp;→&nbsp; `{phone}`")


def render_emergency():
    if not require_login():
        return

    st.subheader("🚨 Emergency Response")
    st.markdown(
        "<p style='color:#C0392B; font-weight:700; font-size:1rem;'>"
        "Use this only in a real emergency. This will alert your emergency contacts immediately."
        "</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        emergency_type = st.selectbox("Emergency type", ["general", "fall", "medical", "medication"])
    with col2:
        severity = st.selectbox("Severity", ["high", "critical"])

    if st.button("🚨 Activate Emergency Protocol", type="primary"):
        data, error = api_request(
            "POST",
            "/api/v1/emergency/activate",
            json={"type": emergency_type, "severity": severity},
        )
        if error:
            st.error(error)
        else:
            st.warning(f"⚠️ {data.get('message')}")
            st.json(data)


# ── App layout ────────────────────────────────────────────────────────────────
tabs = st.tabs(["👤 Account", "🩺 Health", "⏰ Reminders", "💬 Chat", "👨‍👩‍👧 Family", "🚨 Emergency"])

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

