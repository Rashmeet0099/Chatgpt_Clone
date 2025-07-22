import streamlit as st
import requests

API_BASE = "http://localhost:8000"

# Session state management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar navigation - in correct order
page = st.sidebar.radio("Navigation", ["Register", "Login", "Chat"])

# ---------------- Register Page ----------------
if page == "Register":
    st.title("🧑‍💻 Create an Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("🔐 Register"):
        if username and password:
            response = requests.post(f"{API_BASE}/users/register", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                st.success("✅ Registered successfully!")
            else:
                st.error(f"❌ Registration failed: {response.text}")
        else:
            st.warning("Please enter both username and password.")

# ---------------- Login Page ----------------
elif page == "Login":
    st.title("🔓 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("➡ Login"):
        if username and password:
            response = requests.post(f"{API_BASE}/users/login", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Logged in successfully!")
            else:
                st.error(f"❌ Login failed: {response.text}")
        else:
            st.warning("Please enter both username and password.")

# ---------------- Chat Page ----------------
elif page == "Chat":
    st.title("💬 Chat with your AI Assistant")

    if not st.session_state.logged_in:
        st.warning("⚠ Please log in to access the chat.")
    else:
        st.subheader(f"👋 Welcome, {st.session_state.username}")
        message = st.text_input("✍️ Enter your message:")
        topic = st.selectbox("📚 Select a topic:", ["General", "Weather", "Science", "Tech", "News"])

        if st.button("🚀 Send"):
            if message:
                try:
                    headers = {"X-Username": st.session_state.username}
                    st.write("DEBUG HEADERS:", headers)  # Optional debug line

                    response = requests.post(
                        f"{API_BASE}/chat",
                        json={"message": message, "topic": topic},
                        headers=headers
                    )

                    if response.status_code == 200:
                        reply = response.json().get("response")
                        st.session_state.chat_history.append(("You", message))
                        st.session_state.chat_history.append(("AI", reply))
                    else:
                        st.error(f"❌ Chat failed: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"🔌 Connection error: {e}")
            else:
                st.warning("Please enter a message before sending.")

        # Show chat history
        st.subheader("🕓 Chat History")
        for sender, msg in st.session_state.chat_history:
            if sender == "You":
                st.markdown(f"**🧑‍💻 You:** {msg}")
            else:
                st.markdown(f"**🤖 AI:** {msg}")
