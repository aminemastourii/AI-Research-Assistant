"""Test the complete pipeline from pipeline_graph.py"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from backend.graph.pipeline_graph import create_pipeline
from backend.memory.vector_store import VectorStoreFAISS

def test_pipeline():
    """Test the complete research pipeline"""
    print("=" * 80)
    print("TESTING RESEARCH PIPELINE")
    print("=" * 80)
    
    # Create vector store
    print("\n[1/5] Initializing FAISS vector store...")
    vector_store = VectorStoreFAISS(index_path="backend/memory/pipeline_faiss_index")
    
    # Create pipeline
    print("[2/5] Building research pipeline graph...")
    pipeline = create_pipeline(vector_store)
    
    # Test query
    query = "quantum computing algorithms"
    print(f"\n[3/5] Running pipeline with query: '{query}'")
    print("-" * 80)
    
    # Run the pipeline
    print("\n[4/5] Executing pipeline stages:")
    print("  → Search Agent: Searching arXiv...")
    search_node = pipeline.nodes[0]
    papers = search_node.run(query)
    print(f"  ✓ Found {len(papers)} papers")
    
    print("\n  → Extraction Agent: Extracting key information...")
    extract_node = pipeline.nodes[1]
    extractions = extract_node.run(papers[:3])  # Limit to 3 papers for speed
    print(f"  ✓ Extracted info from {len(extractions)} papers")
    
    print("\n  → Analysis Agent: Performing deep analysis...")
    analysis_node = pipeline.nodes[2]
    analyses = analysis_node.run(extractions)
    print(f"  ✓ Analyzed {len(analyses)} papers")
    
    print("\n  → FAISS Memory: Storing in vector database...")
    memory_node = pipeline.nodes[3]
    stored = memory_node.run(analyses)
    print(f"  ✓ Stored {len(stored)} analyses in vector store")
    
    print("\n  → Final Report Generator: Creating literature review...")
    report_node = pipeline.nodes[4]
    final_report = report_node.run(analyses)
    print("  ✓ Generated final report")
    
    # Display results
    print("\n[5/5] FINAL LITERATURE REVIEW:")
    print("=" * 80)
    print(final_report)
    print("=" * 80)
    
    # Show what's in vector store
    print(f"\n✓ Vector store now contains {len(analyses)} analyzed papers")
    print("  You can perform semantic search on these analyses")
    
    # Save the index
    vector_store.save_index()
    print(f"✓ Index saved to {vector_store.index_path}")
    
    print("\n" + "=" * 80)
    print("PIPELINE TEST COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    test_pipeline()
