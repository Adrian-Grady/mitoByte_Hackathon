import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7
)

# Define data models for resume sections
class PersonalInfo(BaseModel):
    name: str = Field(description="Full name of the person")
    email: str = Field(description="Email address")
    phone: str = Field(description="Phone number")
    linkedin: Optional[str] = Field(description="LinkedIn profile URL", default=None)
    location: Optional[str] = Field(description="City and state/country", default=None)

class Education(BaseModel):
    degree: str = Field(description="Degree obtained or in progress")
    institution: str = Field(description="Name of the educational institution")
    location: Optional[str] = Field(description="Location of the institution", default=None)
    graduation_date: str = Field(description="Graduation date or expected graduation date")
    gpa: Optional[str] = Field(description="GPA if relevant", default=None)
    highlights: Optional[List[str]] = Field(description="Notable achievements during education", default=None)

class Experience(BaseModel):
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    location: Optional[str] = Field(description="Job location", default=None)
    start_date: str = Field(description="Start date of employment")
    end_date: Optional[str] = Field(description="End date of employment, or 'Present' if current", default="Present")
    responsibilities: List[str] = Field(description="Key responsibilities and achievements")

class Project(BaseModel):
    name: str = Field(description="Project name")
    description: str = Field(description="Brief project description")
    technologies: List[str] = Field(description="Technologies used in the project")
    url: Optional[str] = Field(description="Project URL if available", default=None)

class Skill(BaseModel):
    category: str = Field(description="Skill category (e.g., Programming Languages, Tools)")
    skills: List[str] = Field(description="List of skills in this category")

class Certification(BaseModel):
    name: str = Field(description="Certification name")
    issuer: str = Field(description="Certification issuer")
    date: Optional[str] = Field(description="Date obtained", default=None)
    expiration: Optional[str] = Field(description="Expiration date if applicable", default=None)

class Resume(BaseModel):
    personal_info: PersonalInfo = Field(description="Personal and contact information")
    education: List[Education] = Field(description="Educational background")
    experience: List[Experience] = Field(description="Work experience")
    projects: Optional[List[Project]] = Field(description="Notable projects", default=None)
    skills: List[Skill] = Field(description="Skills organized by category")
    certifications: Optional[List[Certification]] = Field(description="Professional certifications", default=None)

# Create a prompt template for resume analysis and tailoring
resume_analysis_template = """
You are an expert resume consultant and career coach. Your task is to analyze the provided resume and job description, then provide specific recommendations for tailoring the resume to match the job requirements.

Resume Text:
{resume_text}

Job Description:
{job_description}

Current Resume Data:
{current_resume}

Please analyze the resume and job description, then:
1. Identify key skills and requirements from the job description
2. Highlight matching experiences and skills in the current resume
3. Suggest specific improvements to better align the resume with the job
4. Recommend which experiences to emphasize or de-emphasize
5. Suggest any missing keywords or skills that should be added
6. Provide specific examples of how to rephrase bullet points to better match the job requirements

Your response should be detailed and actionable, focusing on specific changes that will make the resume more compelling for this particular job.
"""

resume_analysis_prompt = PromptTemplate(
    input_variables=["resume_text", "job_description", "current_resume"],
    template=resume_analysis_template
)

# Create the chain for resume analysis
resume_analysis_chain = resume_analysis_prompt | llm | RunnablePassthrough()

def process_resume_input(user_input, current_resume, current_step):
    """
    Process the resume and job description to provide tailoring recommendations
    
    Args:
        user_input (str): The combined resume text and job description
        current_resume (dict): The current state of the resume
        current_step (str): The current step in the process
        
    Returns:
        dict: A dictionary containing:
            - content: The analysis and recommendations
            - next_step: The next step in the process
            - updated_resume: The updated resume data
    """
    # Split the input into resume text and job description
    parts = user_input.split("\nJob Description: ")
    resume_text = parts[0].replace("Resume: ", "")
    job_description = parts[1] if len(parts) > 1 else ""
    
    result = resume_analysis_chain.invoke({
        "resume_text": resume_text,
        "job_description": job_description,
        "current_resume": current_resume
    })
    
    return {
        "content": result.content,
        "next_step": "tailor",
        "updated_resume": current_resume
    }

def generate_resume(resume_data):
    """
    Generate a tailored resume based on the job description
    
    Args:
        resume_data (dict): The resume data to be tailored
        
    Returns:
        str: Formatted resume text optimized for the specific job
    """
    # Create a prompt for generating the tailored resume
    generate_template = """
    Create a professionally formatted resume using the following information:
    
    {resume_data}
    
    Format the resume following these guidelines:
    1. Use a clean, ATS-friendly layout that will pass through applicant tracking systems
    2. Include a compelling professional summary that highlights qualifications relevant to the job
    3. Emphasize experiences and skills that match the job requirements
    4. Use strong action verbs and industry-specific keywords from the job description
    5. Ensure consistent formatting throughout
    6. Prioritize and rephrase experiences to better align with the job requirements
    7. Optimize the skills section to highlight relevant technical and soft skills
    
    The final resume should be tailored specifically for the job and make the candidate stand out to recruiters.
    """
    
    generate_prompt = PromptTemplate(
        input_variables=["resume_data"],
        template=generate_template
    )
    
    generate_chain = generate_prompt | llm
    
    result = generate_chain.invoke({"resume_data": resume_data})
    return result.content

# Run if this file is executed directly
if __name__ == "__main__":
    # Example usage
    sample_resume = {
        "personal_info": {},
        "education": [],
        "experience": [],
        "skills": [],
        "projects": [],
        "certifications": []
    }
    
    response = process_resume_input(
        "Resume: John Doe\nSoftware Engineer\n5 years experience\n\nJob Description: Looking for a senior software engineer with Python experience",
        sample_resume,
        "analysis"
    )
    
    print(response)
