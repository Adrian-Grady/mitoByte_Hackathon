import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Verify API key is set
if not os.getenv("OPENAI_API_KEY"):
    st.error("OpenAI API key not found. Please set it in your .env file.")
    st.stop()

# Set page configuration
st.set_page_config(
    page_title="Resume Assistant",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .mode-card {
        padding: 2rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .mode-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .mode-title {
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .mode-description {
        color: #666;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("Resume Assistant 📝")
st.markdown("""
Welcome to your AI-powered resume assistant! Choose from three powerful modes to enhance your job search:
""")

# Create three columns for the modes
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="mode-card">
        <h3 class="mode-title">Resume Tailoring</h3>
        <p class="mode-description">Upload your resume and a job description to get a tailored version optimized for the specific role.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Tailoring Mode", key="tailor"):
        st.switch_page("pages/1_Tailor_Resume.py")

with col2:
    st.markdown("""
    <div class="mode-card">
        <h3 class="mode-title">Job Hunting Assistant</h3>
        <p class="mode-description">Get personalized job search recommendations and interview preparation based on your resume.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Job Hunting Mode", key="hunt"):
        st.switch_page("pages/2_Job_Hunting.py")

with col3:
    st.markdown("""
    <div class="mode-card">
        <h3 class="mode-title">Resume Chat</h3>
        <p class="mode-description">Chat with your resume to get insights, suggestions, and answers to your career questions.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Chat Mode", key="chat"):
        st.switch_page("pages/3_Resume_Chat.py")

# Add a footer with instructions
st.markdown("---")
st.markdown("""
### How to Use
1. **Resume Tailoring**: Upload your resume and a job description to get a customized version
2. **Job Hunting**: Get personalized job search strategies and interview preparation
3. **Resume Chat**: Have a conversation with your resume to get career insights

Each mode requires you to upload your resume first. Your resume will be securely stored and can be accessed across all modes.
""")
