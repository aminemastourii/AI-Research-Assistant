from typing import TypedDict, List, Dict, Annotated
from langgraph.graph import StateGraph, END
from backend.agents.search_agent import SearchAgentNode
from backend.agents.extraction_agent import ExtractionAgentNode
from backend.agents.analysis_agent import AnalysisAgentNode
from backend.memory.vector_store import VectorStoreFAISS
from backend.llm_client import ask_standard

# Define the state that flows through the pipeline
class PipelineState(TypedDict):
    """State that flows through the research pipeline"""
    query: str
    papers: List[Dict]
    extractions: List[Dict]
    analyses: List[Dict]
    final_report: str

def search_node(state: PipelineState) -> PipelineState:
    """Search for papers on arXiv"""
    agent = SearchAgentNode()
    papers = agent.run(state["query"])
    return {"papers": papers}

def extraction_node(state: PipelineState) -> PipelineState:
    """Extract key information from papers"""
    agent = ExtractionAgentNode()
    extractions = agent.run(state["papers"])
    return {"extractions": extractions}

def analysis_node(state: PipelineState) -> PipelineState:
    """Perform critical analysis of papers"""
    agent = AnalysisAgentNode()
    analyses = agent.run(state["extractions"])
    return {"analyses": analyses}

def memory_node(state: PipelineState, vector_store: VectorStoreFAISS) -> PipelineState:
    """Store analyses in vector database"""
    for item in state["analyses"]:
        text = item['analysis']
        vector_store.add([text], [item['paper_id']])
    return {}

def report_node(state: PipelineState) -> PipelineState:
    """Generate final literature review"""
    combined = "\n\n".join([a['analysis'] for a in state["analyses"]])
    final_report = ask_standard(f"Produce a final literature review:\n{combined}")
    return {"final_report": final_report}

def create_pipeline(vector_store: VectorStoreFAISS):
    """
    Create a LangGraph pipeline for research workflow.
    
    Args:
        vector_store: FAISS vector store instance
        
    Returns:
        Compiled LangGraph workflow
    """
    # Create the graph
    workflow = StateGraph(PipelineState)
    
    # Add nodes
    workflow.add_node("search", search_node)
    workflow.add_node("extract", extraction_node)
    workflow.add_node("analyze", analysis_node)
    workflow.add_node("memory", lambda state: memory_node(state, vector_store))
    workflow.add_node("report", report_node)
    
    # Define edges (pipeline flow)
    workflow.set_entry_point("search")
    workflow.add_edge("search", "extract")
    workflow.add_edge("extract", "analyze")
    workflow.add_edge("analyze", "memory")
    workflow.add_edge("memory", "report")
    workflow.add_edge("report", END)
    
    # Compile the graph
    return workflow.compile()
