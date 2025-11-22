import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

# Initialize LangChain LLM with OpenAI
llm_mini = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

llm_standard = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

def ask_mini(prompt: str) -> str:
    """
    Simple query using GPT-4o-mini model via LangChain.
    
    Args:
        prompt: User prompt/question
        
    Returns:
        LLM response
    """
    response = llm_mini.invoke(prompt)
    return response.content

def ask_standard(prompt: str) -> str:
    """
    Simple query using GPT-4o model via LangChain.
    
    Args:
        prompt: User prompt/question
        
    Returns:
        LLM response
    """
    response = llm_standard.invoke(prompt)
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
        llm = llm_mini
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    return chain

# Export LLM instances for direct use
__all__ = ['llm_mini', 'llm_standard', 'ask_mini', 'ask_standard', 'create_chain']
