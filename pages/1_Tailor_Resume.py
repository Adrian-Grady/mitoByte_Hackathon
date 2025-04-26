import streamlit as st
from dotenv import load_dotenv
import PyPDF2
import io
import json
import os
from datetime import datetime
from fpdf import FPDF
from resume_agent import tailor_resume, generate_tailored_resume_text
import requests
from pathlib import Path
import unicodedata

# Load environment variables
load_dotenv()

def ensure_font_exists():
    """Ensure the font exists in the fonts directory."""
    font_dir = Path("fonts")
    font_dir.mkdir(exist_ok=True)
    
    # Roboto font files
    font_files = {
        "Roboto-Regular.ttf": "https://fonts.googleapis.com/css2?family=Roboto:wght@400&display=swap",
        "Roboto-Bold.ttf": "https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap",
        "Roboto-Italic.ttf": "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@1,400&display=swap"
    }
    
    for font_file, url in font_files.items():
        font_path = font_dir / font_file
        if not font_path.exists():
            try:
                # Download the font from Google Fonts
                response = requests.get(url)
                response.raise_for_status()
                
                # Extract the actual font URL from the CSS
                font_url = response.text.split('url(')[1].split(')')[0].strip('"\'')
                font_response = requests.get(font_url)
                font_response.raise_for_status()
                
                with open(font_path, "wb") as f:
                    f.write(font_response.content)
            except Exception as e:
                st.error(f"Failed to download font {font_file}: {str(e)}")
                return None
    
    return str(font_dir)

def sanitize_text(text):
    """Sanitize text to handle problematic characters."""
    # Replace problematic characters with their ASCII equivalents
    replacements = {
        '\u2013': '-',  # en-dash
        '\u2014': '--', # em-dash
        '\u2018': "'",  # left single quote
        '\u2019': "'",  # right single quote
        '\u201C': '"',  # left double quote
        '\u201D': '"',  # right double quote
        '\u2026': '...' # ellipsis
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text

# Create Resume folder if it doesn't exist
RESUME_FOLDER = "Resume"
if not os.path.exists(RESUME_FOLDER):
    os.makedirs(RESUME_FOLDER)

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

# Initialize session state for resume text and job description
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'tailored_resume' not in st.session_state:
    st.session_state.tailored_resume = ""
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# Title and description
st.title("Resume Tailoring Assistant ✂️")
st.markdown("""
Upload your resume and a job description to get a tailored version optimized for the specific role.
The AI will analyze both documents and suggest improvements to make your resume stand out.
""")

# Create two columns for the main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Upload Your Resume")
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="resume_upload")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
            
            st.session_state.resume_text = resume_text
            st.markdown("### Extracted Resume Text")
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.text_area("Resume Content", value=resume_text, height=400, key="resume_text_area")
            st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### Enter Job Description")
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="Paste the full job description including requirements and responsibilities...",
        key="job_description_input"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if job_description:
        st.session_state.job_description = job_description
        st.markdown("### Customize Tailoring")
        with st.expander("Advanced Options", expanded=False):
            st.session_state.emphasize_skills = st.checkbox("Emphasize matching skills", value=True)
            st.session_state.prioritize_experience = st.checkbox("Prioritize relevant experience", value=True)
            st.session_state.add_keywords = st.checkbox("Add missing keywords", value=True)
            st.session_state.optimize_ats = st.checkbox("Optimize for ATS", value=True)

# Analysis and tailoring section (only show if both resume and job description are provided)
if st.session_state.resume_text and st.session_state.job_description:
    st.markdown("---")
    
    if st.button("Generate Tailored Resume", type="primary"):
        with st.spinner("Analyzing and tailoring your resume..."):
            # Get the analysis
            analysis = tailor_resume(
                st.session_state.resume_text,
                st.session_state.job_description,
                {
                    "emphasize_matching_skills": st.session_state.get("emphasize_skills", True),
                    "prioritize_relevant_experience": st.session_state.get("prioritize_experience", True),
                    "add_missing_keywords": st.session_state.get("add_keywords", True),
                    "optimize_for_ats": st.session_state.get("optimize_ats", True)
                }
            )
            
            # Generate the tailored resume
            tailored_resume = generate_tailored_resume_text(
                st.session_state.resume_text,
                st.session_state.job_description,
                analysis
            )
            
            # Store results in session state
            st.session_state.analysis_result = analysis
            st.session_state.tailored_resume = tailored_resume
            
            # Create timestamped folder
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            user_name = st.session_state.get("user_name", "Anonymous")
            resume_folder = os.path.join(RESUME_FOLDER, f"{timestamp}_{user_name}")
            os.makedirs(resume_folder, exist_ok=True)
            
            # Save JSON version
            resume_data = {
                "original_resume": st.session_state.resume_text,
                "job_description": st.session_state.job_description,
                "tailored_resume": tailored_resume,
                "analysis": analysis,
                "timestamp": timestamp,
                "user_name": user_name
            }
            
            json_path = os.path.join(resume_folder, "resume_data.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(resume_data, f, indent=4, ensure_ascii=False)
            
            # Generate PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Set professional colors
            primary_color = (0, 51, 102)  # Dark blue
            secondary_color = (102, 102, 102)  # Gray
            accent_color = (0, 102, 153)  # Light blue
            
            # Add Google Fonts
            font_dir = ensure_font_exists()
            if font_dir:
                try:
                    pdf.add_font('Roboto', '', str(Path(font_dir) / 'Roboto-Regular.ttf'), uni=True)
                    pdf.add_font('Roboto', 'B', str(Path(font_dir) / 'Roboto-Bold.ttf'), uni=True)
                    pdf.add_font('Roboto', 'I', str(Path(font_dir) / 'Roboto-Italic.ttf'), uni=True)
                    pdf.set_font('Roboto', '', 12)
                except Exception as e:
                    st.error(f"Failed to load font: {str(e)}")
                    pdf.set_font("Arial", size=12)
            else:
                pdf.set_font("Arial", size=12)
            
            # Get the resume text from the analysis result
            resume_text = st.session_state.tailored_resume
            
            if resume_text:
                # Split into sections
                sections = [s.strip() for s in resume_text.split("\n\n") if s.strip()]
                
                # Process each section
                for section in sections:
                    if not section.strip():
                        continue
                    
                    # Extract section header and content
                    lines = section.split("\n")
                    header = lines[0].strip()
                    content = "\n".join(lines[1:]).strip()
                    
                    # Skip Skills section
                    if any(skill_keyword in header.upper() for skill_keyword in ["SKILLS", "TECHNICAL SKILLS", "PROFESSIONAL SKILLS", "CORE SKILLS"]):
                        continue
                    
                    # Format section header
                    pdf.set_font('Roboto', 'B', 14)
                    pdf.set_text_color(*primary_color)
                    pdf.cell(0, 10, txt=header, ln=True)
                    pdf.ln(2)
                    
                    # Process content based on section type
                    if "EXPERIENCE" in header.upper() or "WORK EXPERIENCE" in header.upper():
                        # Process experience entries
                        entries = content.split("\n")
                        current_entry = []
                        
                        for line in entries:
                            if line.strip():
                                if line.strip().startswith(("-", "•", "*")):
                                    # Process previous entry if exists
                                    if current_entry:
                                        process_experience_entry(pdf, current_entry, primary_color, secondary_color)
                                        current_entry = []
                                    current_entry.append(line)
                                else:
                                    current_entry.append(line)
                        
                        # Process last entry
                        if current_entry:
                            process_experience_entry(pdf, current_entry, primary_color, secondary_color)
                    
                    else:
                        # Process other sections
                        pdf.set_font('Roboto', '', 11)
                        pdf.set_text_color(0, 0, 0)
                        for line in content.split("\n"):
                            if line.strip():
                                pdf.multi_cell(0, 8, txt=line.strip())
                        pdf.ln(5)
                
                # Add subtle footer
                pdf.ln(10)
                pdf.set_font('Roboto', 'I', 8)
                pdf.set_text_color(*secondary_color)
                pdf.cell(0, 5, txt=f"Generated on {datetime.now().strftime('%B %d, %Y')}", ln=True, align="C")
            else:
                st.error("No resume content available to generate PDF")
            
            # Save PDF
            pdf_path = os.path.join(resume_folder, "tailored_resume.pdf")
            pdf.output(pdf_path)
            
            st.success("Resume tailored successfully and saved!")
            
            # Add download button for PDF
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download Tailored Resume (PDF)",
                    data=f,
                    file_name="tailored_resume.pdf",
                    mime="application/pdf"
                )
    
    # Display results if available
    if st.session_state.analysis_result and st.session_state.tailored_resume:
        # Create two columns for results
        result_col1, result_col2 = st.columns([1, 1])
        
        with result_col1:
            # Display the tailored resume
            st.markdown("### Your Tailored Resume")
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.text_area("Preview", value=st.session_state.tailored_resume, height=400, key="tailored_resume_preview")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with result_col2:
            st.markdown("### Analysis & Suggestions")
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            
            # Display analysis results
            analysis = st.session_state.analysis_result
            
            # Key Skills Matching
            st.markdown("#### Key Skills Matching")
            st.progress(analysis["skills_analysis"]["match_score"])
            st.markdown(f"""
            - Strong matches: {', '.join(analysis["skills_analysis"]["matching_skills"])}
            - Missing skills: {', '.join(analysis["skills_analysis"]["missing_skills"])}
            """)
            
            # Experience Alignment
            st.markdown("#### Experience Alignment")
            st.progress(analysis["experience_analysis"]["match_score"])
            st.markdown(f"""
            - Relevant experiences: {', '.join(analysis["experience_analysis"]["relevant_experiences"])}
            - Less relevant: {', '.join(analysis["experience_analysis"]["irrelevant_experiences"])}
            """)
            
            # Keyword Optimization
            st.markdown("#### Keyword Optimization")
            st.progress(analysis["keyword_analysis"]["match_score"])
            st.markdown(f"""
            - Found keywords: {', '.join(analysis["keyword_analysis"]["found_keywords"])}
            - Missing keywords: {', '.join(analysis["keyword_analysis"]["missing_keywords"])}
            """)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Improvement Suggestions
            st.markdown("### Suggested Improvements")
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            for i, suggestion in enumerate(analysis["improvement_suggestions"], 1):
                st.markdown(f"{i}. {suggestion}")
            st.markdown('</div>', unsafe_allow_html=True)

# Add a back button
if st.button("← Back to Main Menu"):
    st.switch_page("app.py")

def process_experience_entry(pdf, entry, primary_color, secondary_color):
    """Helper function to process and format an experience entry"""
    if not entry:
        return
    
    # Extract title and company
    title_company = entry[0].split("|")
    title = title_company[0].strip()
    company = title_company[1].strip() if len(title_company) > 1 else ""
    
    # Print title and company
    pdf.set_font('Roboto', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, txt=f"{title} | {company}", ln=True)
    
    # Print dates and location if available
    if len(entry) > 1:
        pdf.set_font('Roboto', 'I', 10)
        pdf.set_text_color(*secondary_color)
        pdf.cell(0, 6, txt=entry[1], ln=True)
    
    # Print bullet points
    pdf.set_font('Roboto', '', 11)
    pdf.set_text_color(0, 0, 0)
    for bullet in entry[2:]:
        pdf.cell(5)
        pdf.cell(5, 8, txt="•", ln=0)
        pdf.multi_cell(0, 8, txt=bullet.lstrip("-•*").strip())
    
    pdf.ln(5) 