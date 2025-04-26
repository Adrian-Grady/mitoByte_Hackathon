import streamlit as st
from dotenv import load_dotenv
import PyPDF2
import io

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Resume Tailoring",
    page_icon="✂️",
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
    .section-box {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        background-color: #fff;
    }
    .highlight {
        background-color: #fff3cd;
        padding: 2px 5px;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("Resume Tailoring Assistant ✂️")
st.markdown("""
Upload your resume and a job description to get a tailored version optimized for the specific role.
The AI will analyze both documents and suggest improvements to make your resume stand out.
""")

# Create two columns for the main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Step 1: Upload Your Resume")
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="resume_upload")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        st.markdown("### Step 2: Enter Job Description")
        job_description = st.text_area(
            "Paste the job description here",
            height=300,
            placeholder="Paste the full job description including requirements and responsibilities..."
        )
        
        if job_description:
            st.markdown("### Step 3: Customize Tailoring")
            with st.expander("Advanced Options", expanded=False):
                st.checkbox("Emphasize matching skills", value=True)
                st.checkbox("Prioritize relevant experience", value=True)
                st.checkbox("Add missing keywords", value=True)
                st.checkbox("Optimize for ATS", value=True)
            
            if st.button("Generate Tailored Resume", type="primary"):
                with st.spinner("Analyzing and tailoring your resume..."):
                    # Here you would call your resume tailoring function
                    st.success("Resume tailored successfully!")
                    
                    # Display the tailored resume
                    st.markdown("### Your Tailored Resume")
                    st.markdown('<div class="section-box">', unsafe_allow_html=True)
                    st.text_area("Preview", height=400, value="Your tailored resume will appear here...")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add download button
                    st.download_button(
                        label="Download Tailored Resume",
                        data="Your tailored resume content",
                        file_name="tailored_resume.txt",
                        mime="text/plain"
                    )

with col2:
    if uploaded_file is not None and 'job_description' in locals():
        st.markdown("### Analysis & Suggestions")
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        
        # Key Skills Matching
        st.markdown("#### Key Skills Matching")
        st.progress(75)
        st.markdown("""
        - Strong match: Python, Machine Learning
        - Partial match: Data Analysis, SQL
        - Missing: AWS, Docker
        """)
        
        # Experience Alignment
        st.markdown("#### Experience Alignment")
        st.progress(60)
        st.markdown("""
        - Highly relevant: Data Science projects
        - Moderately relevant: Software Development
        - Less relevant: Customer Service
        """)
        
        # Keyword Optimization
        st.markdown("#### Keyword Optimization")
        st.progress(85)
        st.markdown("""
        - Found: 15/20 key terms
        - Missing: 5 key terms
        - Suggested additions: Cloud Computing, CI/CD
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Improvement Suggestions
        st.markdown("### Suggested Improvements")
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown("""
        1. **Add Technical Skills**
           - Include AWS and Docker in your skills section
           - Add specific cloud computing experience
        
        2. **Enhance Experience Descriptions**
           - Quantify achievements with metrics
           - Use more action verbs from the job description
        
        3. **Optimize Summary**
           - Add a targeted professional summary
           - Highlight relevant certifications
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# Add a back button
if st.button("← Back to Main Menu"):
    st.switch_page("app.py") 