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
    model_name="gpt-4o",
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

class Resume(BaseModel):
    personal_info: PersonalInfo = Field(description="Personal and contact information")
    education: List[Education] = Field(description="Educational background")
    experience: List[Experience] = Field(description="Work experience")
    projects: Optional[List[Project]] = Field(description="Notable projects", default=None)
    skills: List[Skill] = Field(description="Skills organized by category")

# Create a prompt template for resume building
resume_template = """
You are a professional resume builder assistant. Your goal is to help users create a well-structured, 
professional resume that highlights their strengths and experiences effectively.

Current Resume Information:
{current_resume}

User Input: {user_input}

Current Step: {current_step}

Based on the current step and user input, please help build or improve the resume.
If information is missing or unclear, ask specific questions to gather the necessary details.
Provide guidance on best practices for resume writing when appropriate.

Your response should be helpful, professional, and focused on creating an effective resume.
"""

resume_prompt = PromptTemplate(
    input_variables=["current_resume", "user_input", "current_step"],
    template=resume_template
)

# Create the chain using the new pattern
resume_chain = resume_prompt | llm | RunnablePassthrough()

def process_resume_input(user_input, current_resume, current_step):
    """
    Process user input for resume building based on the current step
    
    Args:
        user_input (str): The user's input text
        current_resume (dict): The current state of the resume
        current_step (str): The current step in the resume building process
        
    Returns:
        tuple: (response content, updated resume data)
    """
    result = resume_chain.invoke({
        "user_input": user_input,
        "current_resume": current_resume,
        "current_step": current_step
    })
    
    # Here you would add logic to update the resume based on the response
    # This is a simplified version - in a real implementation, you'd parse the response
    # and update the resume data structure accordingly
    
    return result.content

def generate_resume(resume_data):
    """
    Generate a formatted resume from the collected data
    
    Args:
        resume_data (dict): The complete resume data
        
    Returns:
        str: Formatted resume text
    """
    # Create a prompt for generating the final resume
    generate_template = """
    Create a professionally formatted resume using the following information:
    
    {resume_data}
    
    Format the resume in a clean, professional layout that would be suitable for printing or PDF conversion.
    Use appropriate sections, bullet points, and formatting to highlight the candidate's strengths.
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
        "projects": []
    }
    
    response = process_resume_input(
        "My name is John Doe and I'm a software engineer with 5 years of experience.",
        sample_resume,
        "personal_info"
    )
    
    print(response)
