import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.7
)

# Create a prompt template for the greeting
greeting_template = """
You are a friendly greeter whose purpose is to welcome everyone with warmth and positivity.
You love making people feel welcome and appreciated.

Task: Create a warm greeting for the world.

Your greeting:
"""

prompt = PromptTemplate(
    input_variables=[],
    template=greeting_template
)

# Create the chain using the new pattern
greeting_chain = prompt | llm | RunnablePassthrough()

def run_hello_world():
    result = greeting_chain.invoke({})
    print(result.content)
    return result.content

# Run if this file is executed directly
if __name__ == "__main__":
    run_hello_world()
