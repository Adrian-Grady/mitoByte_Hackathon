import streamlit as st
from dotenv import load_dotenv
import PyPDF2
import io

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Resume Chat",
    page_icon="💬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .upload-box {
        border: 2px dashed #ccc;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
        background-color: #f8f9fa;
    }
    .chat-container {
        height: 500px;
        overflow-y: auto;
        padding: 20px;
        border-radius: 5px;
        background-color: #f8f9fa;
        margin-bottom: 20px;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .assistant-message {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 80%;
    }
    .suggestion-chip {
        display: inline-block;
        padding: 5px 10px;
        margin: 5px;
        background-color: #e3f2fd;
        border-radius: 15px;
        cursor: pointer;
    }
    .suggestion-chip:hover {
        background-color: #bbdefb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title and description
st.title("Resume Chat Assistant 💬")
st.markdown("""
Chat with your resume to get insights, suggestions, and answers to your career questions.
The AI will analyze your resume and provide personalized advice.
""")

# Create two columns for the main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Step 1: Upload Your Resume")
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="resume_upload")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        st.markdown("### Step 2: Start Chatting")
        st.markdown("""
        Ask questions about:
        - Career advice
        - Skill development
        - Job search strategies
        - Resume improvements
        """)
        
        # Quick suggestion chips
        st.markdown("### Quick Suggestions")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="suggestion-chip">How can I improve my skills section?</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="suggestion-chip">What jobs am I qualified for?</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="suggestion-chip">How can I make my experience stand out?</div>', unsafe_allow_html=True)

with col2:
    if uploaded_file is not None:
        st.markdown("### Chat History")
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_input("Type your message here...", key="chat_input")
        if st.button("Send", type="primary"):
            if user_input:
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Here you would call your chat function
                # For now, we'll add a sample response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Based on your resume, I can see you have strong experience in Python and Machine Learning. Here are some suggestions..."
                })
                
                # Clear the input
                st.experimental_rerun()

# Add a back button
if st.button("← Back to Main Menu"):
    st.switch_page("app.py") 