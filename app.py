import streamlit as st
import time

# Set page configuration
st.set_page_config(page_title="Resume Builder Chatbot", page_icon="📝", layout="centered")

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

if "resume_data" not in st.session_state:
    st.session_state.resume_data = {
        "personal_info": {},
        "education": [],
        "experience": [],
        "skills": [],
        "projects": [],
        "certifications": []
    }

if "current_step" not in st.session_state:
    st.session_state.current_step = "intro"

# App title and description
st.title("Resume Builder Chatbot 📝")
st.markdown("Let me help you create a professional resume. I'll guide you through each section step by step.")

# Function to add a message to the chat
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# Function to handle the conversation flow
def process_user_input(user_input):
    # Add user message to chat
    add_message("user", user_input)
    
    # Display thinking indicator
    with st.status("Thinking...", expanded=False) as status:
        time.sleep(0.5)  # Simulate processing time
        
        if st.session_state.current_step == "intro":
            response = "Great! Let's start building your resume. First, I'll need some personal information. What's your full name?"
            st.session_state.current_step = "name"
        
        elif st.session_state.current_step == "name":
            st.session_state.resume_data["personal_info"]["name"] = user_input
            response = f"Nice to meet you, {user_input}! What's your email address?"
            st.session_state.current_step = "email"
        
        elif st.session_state.current_step == "email":
            st.session_state.resume_data["personal_info"]["email"] = user_input
            response = "What's your phone number?"
            st.session_state.current_step = "phone"
        
        elif st.session_state.current_step == "phone":
            st.session_state.resume_data["personal_info"]["phone"] = user_input
            response = "Do you have a LinkedIn profile? If yes, please provide the URL."
            st.session_state.current_step = "linkedin"
        
        elif st.session_state.current_step == "linkedin":
            st.session_state.resume_data["personal_info"]["linkedin"] = user_input
            response = "Now, let's add your education. What's your highest degree? (e.g., Bachelor's in Computer Science)"
            st.session_state.current_step = "education"
        
        # Add more steps for other resume sections
        
        else:
            response = "I'm not sure what to do next. Let's start over. What's your name?"
            st.session_state.current_step = "name"
        
        status.update(label="Done!", state="complete", expanded=False)
    
    # Add assistant response to chat
    add_message("assistant", response)

# Create a clean chat interface
st.markdown("### Chat with Resume Builder")

# Container for chat messages with fixed height
chat_container = st.container()
with chat_container:
    # Display chat messages in a scrollable area
    st.markdown("""
    <style>
    .chat-container {
        height: 400px;
        overflow-y: auto;
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f2f6;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        st.markdown('</div>', unsafe_allow_html=True)

# If this is the first time, add an initial message
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write("Hello! I'm your resume building assistant. I'll help you create a professional resume step by step. Ready to get started?")
    add_message("assistant", "Hello! I'm your resume building assistant. I'll help you create a professional resume step by step. Ready to get started?")

# Chat input
user_input = st.chat_input("Type your response here...")
if user_input:
    process_user_input(user_input)

# Hidden state for debugging (can be accessed via st.session_state in the Streamlit app)
if "debug_mode" in st.session_state and st.session_state.debug_mode:
    with st.expander("Debug: Current Resume Data", expanded=False):
        st.json(st.session_state.resume_data)
