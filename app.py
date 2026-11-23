import streamlit as st
import sqlite3
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
import streamlit as st

import sqlite3

# Connect to database
conn = sqlite3.connect("campuspilot.db", check_same_thread=False)

cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    event_name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    feedback TEXT,
    rating TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    category TEXT,
    complaint TEXT
)
""")

conn.commit()

# CUSTOM CSS
st.markdown("""
<style>
.stApp {
    background-color: #F4F7FC;
    color: #172554 !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #F4F7FC;
}

[data-testid="stMarkdownContainer"] p {
    color: #334155 !important;
}

h1, h2, h3, h4 {
    color: #172554 !important;
}

[data-testid="stSidebar"] {
    background-color: #172554;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

.hero {
    background: linear-gradient(120deg, #2563EB, #7C3AED);
    padding: 35px;
    border-radius: 20px;
    margin-bottom: 25px;
}

.hero h1, .hero p {
    color: #FFFFFF !important;
}

.feature-card {
    background: #FFFFFF;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #DCE4F2;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
}

.feature-card h3 {
    color: #1D4ED8 !important;
}

.feature-card p {
    color: #475569 !important;
}

label {
    color: #172554 !important;
}

[data-testid="stMetricLabel"] {
    color: #475569 !important;
}

[data-testid="stMetricValue"] {
    color: #1D4ED8 !important;
}

.stButton > button {
    background-color: #2563EB;
    color: white !important;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# SIDEBAR
st.sidebar.markdown("# 🎓 CampusPilot")
st.sidebar.caption("SMART CAMPUS PLATFORM")

page = st.sidebar.radio(
    "MAIN MENU",
    [
        "Dashboard",
        "Academic Assistant",
        "Campus Events",
        "Study Resources",
        "Student Support",
        "Admin Dashboard"
    ]
)

st.sidebar.divider()
st.sidebar.write("🚀 Your Smart Campus Partner")
st.sidebar.caption("Version 1.0")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
# LOGIN SYSTEM
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🎓 CampusPilot Login")
    st.write("Welcome to your Smart Campus Platform")

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if username == "student" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    st.stop()


# HEADER
st.markdown("""
<div class="hero">
    <h1>🎓 CampusPilot AI</h1>
    <p>Your Intelligent Campus Assistant</p>
    <p>Making campus life smarter, easier and better.</p>
</div>
""", unsafe_allow_html=True)


# DASHBOARD
if page == "Dashboard":

    st.markdown(
        '<div class="section-title">Welcome to Your Dashboard 👋</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Campus Services", "04")
    col2.metric("Assistant Status", "Active")
    col3.metric("Platform Status", "Online")

    st.write("")

    st.markdown(
        '<div class="section-title">Explore Our Services</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Academic Assistant</h3>
            <p>Ask questions and get academic guidance
            through your smart campus assistant.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>📖 Study Resources</h3>
            <p>Explore study materials, programming
            resources and learning notes.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <h3>📅 Campus Events</h3>
            <p>Discover technical workshops,
            hackathons and cultural activities.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>💬 Student Support</h3>
            <p>Find assistance for academic,
            technical and general enquiries.</p>
        </div>
        """, unsafe_allow_html=True)



# ACADEMIC ASSISTANT
elif page == "Academic Assistant":

    st.header("🤖 CampusPilot AI Chatbot")
    st.write("Your personal academic assistant.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask me anything about your campus...")

    if question:
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        q = question.lower()

        if "course" in q:
            answer = "Our campus offers various academic courses."

        elif "library" in q:
            answer = "The library provides books and study resources."

        elif "exam" in q:
            answer = "Please check your college notice board for exam updates."

        elif "event" in q:
            answer = "Our campus conducts technical and cultural events."

        elif "faculty" in q or "teacher" in q:
            answer = "Contact your department faculty for academic support."

        elif "hello" in q or "hi" in q:
            answer = "Hello! Welcome to CampusPilot AI. How can I help you?"

        else:
            answer = "I am still learning. Please ask me a campus-related question."

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        st.rerun()

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

          

# CAMPUS EVENTS
elif page == "Campus Events":

    st.header("📅 Campus Events")
    st.write("Discover activities happening on your campus!")

    events = [
        {
            "name": "Hackathon 2026",
            "description": "Build innovative projects and showcase your coding skills.",
            "date": "Coming Soon",
            "icon": "💻"
        },
        {
            "name": "Technical Workshop",
            "description": "Learn new technologies from industry experts.",
            "date": "Coming Soon",
            "icon": "⚙️"
        },
        {
            "name": "Cultural Fest",
            "description": "Celebrate creativity, music and culture.",
            "date": "Coming Soon",
            "icon": "🎭"
        },
        {
            "name": "Coding Competition",
            "description": "Test your programming and problem-solving skills.",
            "date": "Coming Soon",
            "icon": "🏆"
        }
    ]

    col1, col2 = st.columns(2)

    for i, event in enumerate(events):

        with [col1, col2][i % 2]:

            st.markdown(f"""
            <div class="feature-card">
                <h3>{event['icon']} {event['name']}</h3>
                <p>{event['description']}</p>
                <p><b>Date:</b> {event['date']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.subheader("📝 Event Registration")

    student_name = st.text_input("Enter your name")

    selected_event = st.selectbox(
        "Select an event",
        [event["name"] for event in events]
    )

    if st.button("Register Now"):
        if student_name.strip():
            cursor.execute(
            "INSERT INTO registrations (student_name, event_name) VALUES (?, ?)",
            (student_name, selected_event)
        )
        conn.commit()

        st.success(
            f"Congratulations {student_name}! "
            f"You have registered for {selected_event}."
        )
    else:
        st.warning("Please enter your name.")


# STUDY RESOURCES
elif page == "Study Resources":

    st.header("📚 Study Resources")
    st.write("Learn smarter with CampusPilot AI!")

    st.subheader("📖 Explore Subjects")

    subjects = {
        "Python Programming": [
            "Introduction to Python",
            "Variables and Data Types",
            "Conditional Statements",
            "Loops and Functions",
            "Lists and Dictionaries"
        ],
        "Data Structures": [
            "Arrays",
            "Linked Lists",
            "Stacks and Queues",
            "Trees",
            "Graphs"
        ],
        "Artificial Intelligence": [
            "Introduction to AI",
            "Machine Learning",
            "Deep Learning",
            "Neural Networks",
            "Natural Language Processing"
        ],
        "Web Development": [
            "HTML Basics",
            "CSS Styling",
            "JavaScript",
            "Frontend Development",
            "Backend Development"
        ]
    }

    subject = st.selectbox(
        "Choose your subject",
        list(subjects.keys())
    )

    st.subheader(f"Topics in {subject}")

    for topic in subjects[subject]:
        st.markdown(f"📘 {topic}")

    st.divider()

    st.subheader("📤 Upload Study Materials")

    uploaded_file = st.file_uploader(
        "Upload your notes (PDF)",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.success("File uploaded successfully!")

        st.download_button(
            label="⬇️ Download Notes",
            data=uploaded_file.getvalue(),
            file_name=uploaded_file.name,
            mime="application/pdf"
        )


# STUDENT SUPPORT
elif page == "Student Support":

    st.header("💬 Student Support")
    st.write("We are here to help you!")

    tab1, tab2, tab3 = st.tabs([
        "📝 Feedback",
        "⚠️ Complaints",
        "📞 Contact"
    ])

    with tab1:

        st.subheader("Share Your Feedback")

        name = st.text_input("Your Name", key="feedback_name")

        feedback = st.text_area(
            "Write your feedback",
            key="feedback_text"
        )

        rating = st.select_slider(
            "Rate our platform",
            options=["Poor", "Average", "Good", "Excellent"]
        )

    if st.button("Submit Feedback"):

        if name.strip() and feedback.strip():

            cursor.execute(
            "INSERT INTO feedback (student_name, feedback, rating) VALUES (?, ?, ?)",
            (name, feedback, rating)
        )

        conn.commit()

        st.success("Thank you! Your feedback has been saved.")

    else:
        st.warning("Please complete all fields.")

    with tab2:

        st.subheader("Submit a Complaint")

        student = st.text_input(
            "Student Name",
            key="complaint_name"
        )

        category = st.selectbox(
            "Complaint Category",
            [
                "Academic",
                "Library",
                "Infrastructure",
                "Technical",
                "Other"
            ]
        )

        complaint = st.text_area(
            "Describe Your Complaint"
        )

    if st.button("Submit Complaint"):

        if student.strip() and complaint.strip():

            cursor.execute(
            "INSERT INTO complaints (student_name, category, complaint) VALUES (?, ?, ?)",
            (student, category, complaint)
        )

        conn.commit()

        st.success("Your complaint has been saved successfully!")

    else:
        st.warning("Please fill in all details.")

    with tab3:

        st.subheader("Contact Information")

        st.info("🎓 Academic Support - Contact your department.")
        st.info("💻 Technical Support - Report technical issues.")
        st.info("🏫 General Enquiries - Contact the college office.")

        st.write("Thank you for using CampusPilot AI!")

# ADMIN DASHBOARD
elif page == "Admin Dashboard":

    st.header("🔐 Admin Dashboard")
    st.write("Manage student activities and information.")

    # Student Registrations
    st.subheader("📅 Student Registrations")

    registrations = cursor.execute(
        "SELECT * FROM registrations"
    ).fetchall()

    st.write("Total Registrations:", len(registrations))

    if registrations:
        st.dataframe(
            registrations,
            column_config={
                0: "ID",
                1: "Student Name",
                2: "Event Name"
            },
            hide_index=True
        )
    else:
        st.info("No registrations available.")

    st.divider()

    # Student Feedback
    st.subheader("📝 Student Feedback")

    feedback_data = cursor.execute(
        "SELECT * FROM feedback"
    ).fetchall()

    st.write("Total Feedback:", len(feedback_data))

    if feedback_data:
        st.dataframe(feedback_data)
    else:
        st.info("No feedback available.")

    st.divider()

    # Student Complaints
    st.subheader("⚠️ Student Complaints")

    complaints_data = cursor.execute(
        "SELECT * FROM complaints"
    ).fetchall()

    st.write("Total Complaints:", len(complaints_data))

    if complaints_data:
        st.dataframe(complaints_data)
    else:
        st.info("No complaints available.")


# FOOTER
st.divider()

st.caption(
    "© 2026 CampusPilot AI | Smart Campus Experience"
)