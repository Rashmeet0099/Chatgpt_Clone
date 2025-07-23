import streamlit as st
import requests
from datetime import datetime

API_BASE = "http://localhost:8000"

# ---------- Session State Setup ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "page" not in st.session_state:
    st.session_state.page = "Register"
if "show_logout_confirm" not in st.session_state:
    st.session_state.show_logout_confirm = False

# ---------- Navigation Helper ----------
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ---------- Register Page ----------
if st.session_state.page == "Register":
    st.title("🧑‍💻 Create an Account")
    username = st.text_input("Username", key="register_username")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("🔐 Register"):
        if username and password:
            response = requests.post(f"{API_BASE}/users/register", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                st.success("✅ Registered successfully! Please log in.")
                go_to("Login")
            else:
                st.error(f"❌ Registration failed: {response.text}")
        else:
            st.warning("Please enter both username and password.")

    if st.button("➡ Go to Login"):
        go_to("Login")

# ---------- Login Page ----------
elif st.session_state.page == "Login":
    st.title("🔓 Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("➡ Login"):
        if username and password:
            response = requests.post(f"{API_BASE}/users/login", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "Chat"
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error(f"❌ Login failed: {response.text}")
        else:
            st.warning("Please enter both username and password.")

    if st.button("⬅ Go to Register"):
        go_to("Register")

# ---------- Chat Page ----------
elif st.session_state.page == "Chat":
    if not st.session_state.logged_in:
        st.warning("⚠ Please log in first.")
        go_to("Login")
    else:
        st.title("💬 Chat with your AI Assistant")
        st.markdown(f"👋 Welcome, **{st.session_state.username}**")

        # Input layout
        col1, col2 = st.columns([4, 1])
        with col1:
            message = st.text_input("✍️ Your message here...", label_visibility="collapsed")
        with col2:
            topic = st.selectbox("📚 Topic", ["General", "Weather", "Science", "Tech", "News"])

        send_col, logout_col = st.columns([1, 1])
        with send_col:
            if st.button("🚀 Send"):
                if message:
                    try:
                        headers = {"X-Username": st.session_state.username}
                        response = requests.post(
                            f"{API_BASE}/chat",
                            json={"message": message, "topic": topic},
                            headers=headers
                        )
                        if response.status_code == 200:
                            reply = response.json().get("response")
                            now = datetime.now().strftime("%H:%M:%S")
                            st.session_state.chat_history.append(("You", message, now))
                            st.session_state.chat_history.append(("AI", reply, now))
                        else:
                            st.error(f"❌ Chat failed: {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"🔌 Connection error: {e}")
                else:
                    st.warning("Please type a message first.")

        with logout_col:
            if st.button("🔒 Logout"):
                st.session_state.show_logout_confirm = True

        # ---------- Logout Confirmation ----------
        if st.session_state.show_logout_confirm:
            st.warning("Lock kar diya jaye?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Haan, Lock karo"):
                    st.session_state.logged_in = False
                    st.session_state.username = ""
                    st.session_state.chat_history = []
                    st.session_state.show_logout_confirm = False
                    go_to("Login")
            with col2:
                if st.button("Firse sochta hoon"):
                    st.session_state.show_logout_confirm = False

        # ---------- Chat History ----------
        st.markdown("### 🕓 Chat History")
        with st.container():
            for sender, msg, time in reversed(st.session_state.chat_history):
                with st.chat_message("user" if sender == "You" else "assistant"):
                    st.markdown(f"**{sender} ({time}):** {msg}")
