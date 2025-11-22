"""
AI Research Assistant - Main Entry Point
Uses the pipeline from pipeline_graph.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from backend.graph.pipeline_graph import create_pipeline
from backend.memory.vector_store import VectorStoreFAISS

def main():
    """Run the AI Research Assistant pipeline"""
    print("=" * 80)
    print("AI RESEARCH ASSISTANT")
    print("=" * 80)
    
    # Initialize vector store
    print("\nInitializing vector store...")
    vector_store = VectorStoreFAISS(index_path="backend/memory/faiss_index")
    
    # Create pipeline
    print("Building research pipeline...")
    pipeline = create_pipeline(vector_store)
    
    # Get research query from user
    query = input("\nEnter research topic to explore: ").strip()
    if not query:
        query = "quantum computing algorithms"
        print(f"Using default query: '{query}'")
    
    print(f"\nProcessing query: '{query}'")
    print("-" * 80)
    
    # Execute pipeline with LangGraph
    print("\nExecuting LangGraph pipeline...")
    result = pipeline.invoke({
        "query": query,
        "papers": [],
        "extractions": [],
        "analyses": [],
        "final_report": ""
    })
    
    # Display final report
    print("\n" + "=" * 80)
    print("FINAL LITERATURE REVIEW")
    print("=" * 80)
    print(result["final_report"])
    print("=" * 80)
    
    # Save vector store
    vector_store.save_index()
    print(f"\n✓ Vector store saved to {vector_store.index_path}")
    print("\nResearch assistant session complete!")

if __name__ == "__main__":
    main()

