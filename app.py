import streamlit as st
import time
import os
from dotenv import load_dotenv
from resume_agent import process_resume_input, generate_resume
import PyPDF2
import io

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(page_title="Resume Tailoring Assistant", page_icon="📝", layout="centered")

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
    st.session_state.current_step = "upload"

if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

# App title and description
st.title("Resume Tailoring Assistant 📝")
st.markdown("Upload your existing resume and a job description, and I'll help you tailor your resume to match the job requirements.")

# Function to add a message to the chat
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.getvalue()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to process the uploaded resume
def process_uploaded_resume(resume_text, job_description):
    # Add user message to chat
    add_message("user", "I've uploaded my resume and job description")
    
    # Display thinking indicator
    with st.status("Analyzing your resume and job description...", expanded=False) as status:
        try:
            # Process the resume and job description
            response = process_resume_input(
                user_input=f"Resume: {resume_text}\nJob Description: {job_description}",
                current_resume=st.session_state.resume_data,
                current_step="analysis"
            )
            
            # Update resume data
            st.session_state.resume_data = response["updated_resume"]
            
            # Add assistant response to chat
            add_message("assistant", response["content"])
            
            # Get and display the next question
            with st.chat_message("assistant"):
                st.write(response["content"])
            
        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            add_message("assistant", error_message)
            st.error(error_message)
        
        status.update(label="Done!", state="complete", expanded=False)

# Function to generate the tailored resume
def generate_tailored_resume():
    st.session_state.is_generating = True
    with st.status("Generating your tailored resume...", expanded=False) as status:
        try:
            final_resume = generate_resume(st.session_state.resume_data)
            
            # Display the resume in a nice format
            st.markdown("### Your Tailored Resume")
            st.text_area("Resume Preview", value=final_resume, height=400)
            
            # Add download button
            st.download_button(
                label="Download Tailored Resume",
                data=final_resume,
                file_name="tailored_resume.txt",
                mime="text/plain"
            )
            
            add_message("assistant", "I've generated your tailored resume! You can preview it above and download it using the button.")
            
        except Exception as e:
            error_message = f"Sorry, I encountered an error while generating your resume: {str(e)}"
            add_message("assistant", error_message)
            st.error(error_message)
        
        status.update(label="Done!", state="complete", expanded=False)
        st.session_state.is_generating = False

# Create a clean chat interface
st.markdown("### Resume Tailoring Process")

# File upload section
st.markdown("#### Step 1: Upload Your Resume")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Job description input
st.markdown("#### Step 2: Enter Job Description")
job_description = st.text_area("Paste the job description here", height=200)

# Process button
if st.button("Analyze Resume"):
    if uploaded_file is not None and job_description:
        resume_text = extract_text_from_pdf(uploaded_file)
        st.session_state.job_description = job_description
        process_uploaded_resume(resume_text, job_description)
    else:
        st.warning("Please upload a resume and enter a job description first.")

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

# Generate tailored resume button
if st.session_state.messages and not st.session_state.is_generating:
    if st.button("Generate Tailored Resume"):
        generate_tailored_resume()

# Add a reset button
if st.button("Start Over"):
    st.session_state.messages = []
    st.session_state.resume_data = {
        "personal_info": {},
        "education": [],
        "experience": [],
        "skills": [],
        "projects": [],
        "certifications": []
    }
    st.session_state.current_step = "upload"
    st.session_state.is_generating = False
    st.session_state.job_description = ""
    st.rerun()

# Hidden state for debugging (can be accessed via st.session_state in the Streamlit app)
if "debug_mode" in st.session_state and st.session_state.debug_mode:
    with st.expander("Debug: Current Resume Data", expanded=False):
        st.json(st.session_state.resume_data)
