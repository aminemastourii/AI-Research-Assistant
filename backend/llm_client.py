import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

# Initialize LangChain LLM with Gemini
llm_flash = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

llm_pro = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-pro",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

def ask_flash(prompt: str) -> str:
    """
    Simple query using Gemini Flash model via LangChain.
    
    Args:
        prompt: User prompt/question
        
    Returns:
        LLM response
    """
    response = llm_flash.invoke(prompt)
    return response.content

def ask_pro(prompt: str) -> str:
    """
    Simple query using Gemini Pro model via LangChain.
    
    Args:
        prompt: User prompt/question
        
    Returns:
        LLM response
    """
    response = llm_pro.invoke(prompt)
    return response.content

def create_chain(template: str, llm=None):
    """
    Create a LangChain chain with a custom prompt template using LCEL.
    
    Args:
        template: Prompt template with variables
        llm: LLM instance (defaults to flash model)
        
    Returns:
        Runnable chain
    """
    if llm is None:
        llm = llm_flash
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    return chain

# Export LLM instances for direct use
__all__ = ['llm_flash', 'llm_pro', 'ask_flash', 'ask_pro', 'create_chain']
