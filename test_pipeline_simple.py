"""Test the pipeline using LangGraph"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from backend.graph.pipeline_graph import create_pipeline
from backend.memory.vector_store import VectorStoreFAISS

def test_pipeline_langgraph():
    """Test the complete research pipeline with LangGraph"""
    print("=" * 80)
    print("TESTING RESEARCH PIPELINE (LangGraph)")
    print("=" * 80)
    
    # Initialize vector store
    print("\n[1/2] Initializing FAISS vector store...")
    vector_store = VectorStoreFAISS(index_path="backend/memory/pipeline_faiss_index")
    
    # Create pipeline
    print("[2/2] Building LangGraph pipeline...")
    pipeline = create_pipeline(vector_store)
    print("✓ LangGraph workflow compiled")
    
    # Test query
    query = "quantum computing algorithms"
    print(f"\nQuery: '{query}'")
    print("-" * 80)
    
    # Run the pipeline with LangGraph
    print("\nExecuting LangGraph pipeline (all stages automatic)...")
    result = pipeline.invoke({
        "query": query,
        "papers": [],
        "extractions": [],
        "analyses": [],
        "final_report": ""
    })
    
    # Display results
    print("\n✓ Pipeline execution complete!")
    print(f"\nProcessed {len(result.get('papers', []))} papers")
    print(f"Generated {len(result.get('analyses', []))} analyses")
    
    print("\n" + "=" * 80)
    print("FINAL LITERATURE REVIEW")
    print("=" * 80)
    print(result["final_report"])
    print("=" * 80)
    
    # Save the index
    vector_store.save_index()
    print(f"\n✓ Index saved to {vector_store.index_path}")
    
    print("\n" + "=" * 80)
    print("✅ LANGGRAPH PIPELINE TEST COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    test_pipeline_langgraph()
    print(final_report)
    print("=" * 80)
    
    print("\n" + "=" * 80)
    print("✅ PIPELINE TEST COMPLETE!")
    print("=" * 80)
    print(f"\nProcessed {len(analyses)} papers through all 5 stages:")
    print("  1. ✅ Search (arXiv)")
    print("  2. ✅ Extraction (AI-powered)")
    print("  3. ✅ Analysis (AI-powered)")
    print("  4. ✅ Memory Storage")
    print("  5. ✅ Final Report Generation")

if __name__ == "__main__":
    test_pipeline_no_vector()
