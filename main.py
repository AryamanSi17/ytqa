import streamlit as st
import youtube_loader as yl
from dotenv import load_dotenv
import textwrap

# 1) Page config
st.set_page_config(
    page_title="YTQA",
    page_icon="📺",
    layout="wide",
)

# 2) Custom CSS for nicer cards and spacing
st.markdown(
    """
    <style>
    .card {
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .sidebar .st-form {
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 style='text-align: center;'>📺 YTQA – Ask Videos Anything</h1>", unsafe_allow_html=True)
st.write("---")

with st.sidebar:
    st.markdown("## 🔎 Ask a YouTube Video")
    with st.form(key="ytqa_form"):
        youtube_url = st.text_input("Video URL", placeholder="https://youtu.be/…")
        query = st.text_input("Your Question", placeholder="e.g. What’s the main point?")
        submit_button = st.form_submit_button("▶️ Submit")

if submit_button and youtube_url and query:
    with st.spinner("Processing video…"):
        db = yl.vector_db_from_youtube(youtube_url)
        response, docs = yl.query_result(db, query)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.video(youtube_url)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 💬 Answer")
        st.write(textwrap.fill(response, width=85))

elif submit_button:
    st.error("Please enter both a valid YouTube URL and a question.")
