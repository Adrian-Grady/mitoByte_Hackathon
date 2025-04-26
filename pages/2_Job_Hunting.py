import streamlit as st
from dotenv import load_dotenv
import PyPDF2
import io

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Job Hunting Assistant",
    page_icon="🔍",
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
    .job-card {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        background-color: #fff;
        transition: all 0.3s ease;
    }
    .job-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("Job Hunting Assistant 🔍")
st.markdown("""
Get personalized job search recommendations and interview preparation based on your resume.
The AI will analyze your skills and experience to suggest the best job opportunities and help you prepare.
""")

# Create two columns for the main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Step 1: Upload Your Resume")
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="resume_upload")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        st.markdown("### Step 2: Job Search Preferences")
        with st.expander("Search Criteria", expanded=True):
            job_title = st.text_input("Desired Job Title")
            location = st.text_input("Preferred Location")
            experience_level = st.selectbox(
                "Experience Level",
                ["Entry Level", "Mid Level", "Senior Level", "Executive"]
            )
            industry = st.multiselect(
                "Industry",
                ["Technology", "Finance", "Healthcare", "Education", "Manufacturing", "Other"]
            )
        
        if st.button("Find Jobs", type="primary"):
            with st.spinner("Analyzing your profile and finding matching jobs..."):
                # Here you would call your job search function
                st.success("Found matching jobs!")

with col2:
    if uploaded_file is not None:
        st.markdown("### Recommended Jobs")
        
        # Sample job cards (replace with actual job data)
        st.markdown('<div class="job-card">', unsafe_allow_html=True)
        st.markdown("""
        #### Senior Software Engineer
        **Company:** TechCorp Inc.
        **Location:** Remote
        **Match Score:** 92%
        
        - Strong match with your Python and Machine Learning experience
        - Aligns with your 5+ years of experience
        - Matches your preferred remote work setup
        """)
        st.button("View Details", key="job1")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="job-card">', unsafe_allow_html=True)
        st.markdown("""
        #### Data Science Lead
        **Company:** DataFlow Solutions
        **Location:** New York, NY
        **Match Score:** 88%
        
        - Excellent match with your data analysis skills
        - Leadership experience preferred
        - Competitive salary and benefits
        """)
        st.button("View Details", key="job2")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Interview Preparation Section
        st.markdown("### Interview Preparation")
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown("""
        #### Common Questions to Expect
        1. Tell me about your experience with Python and Machine Learning
        2. How do you handle large datasets?
        3. Describe a challenging project you've worked on
        
        #### Technical Skills to Highlight
        - Python programming
        - Machine Learning algorithms
        - Data analysis and visualization
        - Cloud computing experience
        
        #### Soft Skills to Emphasize
        - Problem-solving
        - Team collaboration
        - Communication
        - Leadership
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# Add a back button
if st.button("← Back to Main Menu"):
    st.switch_page("app.py") 