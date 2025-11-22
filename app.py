"""
Streamlit Web Interface for AI Research Assistant
"""
import streamlit as st
import sys
import os
from typing import Dict, List

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from backend.graph.pipeline_graph import create_pipeline
from backend.memory.vector_store import VectorStoreFAISS

# Page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Robotic Theme
st.markdown("""
<style>
    /* Robotic Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
        background-attachment: fixed;
    }
    
    /* Animated circuit pattern overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0, 255, 255, 0.03) 2px, rgba(0, 255, 255, 0.03) 4px),
            repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(0, 255, 255, 0.03) 2px, rgba(0, 255, 255, 0.03) 4px);
        pointer-events: none;
        z-index: 1;
    }
    
    /* Main title styling */
    .main-header {
        font-size: 5rem;
        font-weight: 900;
        text-align: center;
        margin: 4rem 0 1rem 0;
        background: linear-gradient(90deg, #00f5ff 0%, #00d4ff 25%, #0099ff 50%, #00d4ff 75%, #00f5ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% auto;
        animation: shine 3s linear infinite;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
        letter-spacing: 4px;
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
    }
    
    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #00d4ff;
        margin-bottom: 3rem;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    /* Search container */
    .search-container {
        max-width: 800px;
        margin: 0 auto 3rem auto;
        padding: 2rem;
        background: rgba(10, 20, 40, 0.8);
        border: 2px solid #00d4ff;
        border-radius: 15px;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.3), inset 0 0 20px rgba(0, 212, 255, 0.1);
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        background-color: rgba(15, 25, 45, 0.9) !important;
        color: #00f5ff !important;
        border: 2px solid #00d4ff !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
        font-family: 'Courier New', monospace !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #00f5ff !important;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.5) !important;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%) !important;
        color: #000 !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        border: 2px solid #00f5ff !important;
        font-size: 1.1rem !important;
        font-family: 'Arial', 'Helvetica', sans-serif !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #00f5ff 0%, #00d4ff 100%) !important;
        box-shadow: 0 0 30px rgba(0, 245, 255, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Paper cards */
    .paper-card {
        padding: 1.5rem;
        border-left: 4px solid #00d4ff;
        background: rgba(15, 25, 45, 0.8);
        margin: 1rem 0;
        border-radius: 10px;
        border: 1px solid rgba(0, 212, 255, 0.3);
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    }
    
    .paper-card h4 {
        color: #00f5ff;
    }
    
    .paper-card p {
        color: #b0c4de;
    }
    
    .paper-card a {
        color: #00d4ff;
        text-decoration: none;
        font-weight: bold;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%) !important;
        border-right: 2px solid #00d4ff !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #b0c4de !important;
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #00f5ff !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(15, 25, 45, 0.6);
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #00d4ff !important;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 212, 255, 0.2) !important;
        border-bottom: 3px solid #00f5ff !important;
    }
    
    /* Text colors */
    h1, h2, h3, h4, h5, h6 {
        color: #00f5ff !important;
    }
    
    p, span, div {
        color: #b0c4de !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00f5ff !important;
        font-family: 'Courier New', monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
    st.session_state.vector_store = None
    st.session_state.result = None
    st.session_state.processing = False
    st.session_state.pipeline_initialized = False

def initialize_pipeline():
    """Initialize the research pipeline (called automatically on first research)"""
    if st.session_state.pipeline is None:
        st.session_state.vector_store = VectorStoreFAISS(
            index_path="backend/memory/streamlit_faiss_index"
        )
        st.session_state.pipeline = create_pipeline(st.session_state.vector_store)
        st.session_state.pipeline_initialized = True

def run_research(query: str):
    """Run the research pipeline"""
    st.session_state.processing = True
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Auto-initialize pipeline on first run
        if st.session_state.pipeline is None:
            status_text.text("🔧 Initializing pipeline (first time only)...")
            progress_bar.progress(5)
            initialize_pipeline()
        
        # Stage 1: Execute pipeline
        status_text.text("🔍 Searching papers...")
        progress_bar.progress(20)
        
        result = st.session_state.pipeline.invoke({
            "query": query,
            "papers": [],
            "extractions": [],
            "analyses": [],
            "final_report": ""
        })
        
        progress_bar.progress(100)
        status_text.text("✅ Research complete!")
        
        st.session_state.result = result
        
        # Save vector store
        if st.session_state.vector_store:
            st.session_state.vector_store.save_index()
        
    except Exception as e:
        st.error(f"❌ Error during research: {str(e)}")
        st.session_state.result = None
    
    finally:
        st.session_state.processing = False

def display_papers(papers: List[Dict]):
    """Display found papers"""
    st.markdown("### 📚 Found Papers")
    
    for i, paper in enumerate(papers[:10], 1):
        with st.container():
            st.markdown(f"""
            <div class="paper-card">
                <h4>{i}. {paper['title']}</h4>
                <p><strong>Authors:</strong> {', '.join(paper['authors'][:5])}{'...' if len(paper['authors']) > 5 else ''}</p>
                <p><strong>Published:</strong> {paper.get('published', 'N/A')}</p>
                <p><strong>Categories:</strong> {', '.join(paper.get('categories', [])[:3])}</p>
                <p><strong>Abstract:</strong> {paper['summary'][:300]}...</p>
                <a href="{paper['pdf_url']}" target="_blank">📄 View PDF</a>
            </div>
            """, unsafe_allow_html=True)

def display_analyses(analyses: List[Dict]):
    """Display analyses"""
    st.markdown("### 🔬 Critical Analyses")
    
    tabs = st.tabs([f"Paper {i+1}" for i in range(min(len(analyses), 5))])
    
    for i, (tab, analysis) in enumerate(zip(tabs, analyses[:5])):
        with tab:
            st.markdown(f"**Title:** {analysis['title']}")
            st.markdown(f"**Authors:** {', '.join(analysis['authors'][:3])}...")
            
            with st.expander("📊 Extracted Information", expanded=True):
                st.write(analysis['extraction'])
            
            with st.expander("🔍 Critical Analysis", expanded=True):
                st.write(analysis['analysis'])

# Main UI
def main():
    # Header - Centered and prominent
    st.markdown('<p class="main-header">🤖 AI Research Assistant</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="subtitle">
    [ POWERED BY ADVANCED AI • SEARCH • ANALYZE • SYNTHESIZE ]
    </p>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=100)
        st.title("Settings")
        
        st.markdown("---")
        
        # API Status
        st.markdown("### 🔑 API Status")
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            st.success("✅ OpenAI API configured")
        else:
            st.error("❌ OpenAI API key not found")
            st.info("Add OPENAI_API_KEY to .env file")
        
        st.markdown("---")
        
        # About
        with st.expander("ℹ️ About"):
            st.markdown("""
            This AI Research Assistant automatically searches, analyzes, 
            and synthesizes academic papers using AI.
            
            **Features:**
            - 🔍 Search arXiv papers
            - 📊 Extract key information
            - 🔬 Perform critical analysis
            - 📝 Generate literature reviews
            """)
        
        # Clear results
        if st.button("🗑️ Clear Results"):
            st.session_state.result = None
            st.rerun()
    
    # Centered search container
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Research query input - centered
    st.markdown("### 🔍 Enter Research Query")
    
    query = st.text_input(
        "Research Topic",
        placeholder="Enter your research topic (e.g., quantum computing, neural networks, AI ethics)...",
        label_visibility="collapsed",
        key="main_query"
    )
    
    # Search button - full width in container
    search_button = st.button("🔬 START RESEARCH")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick examples
    st.markdown("**Quick Examples:**")
    example_cols = st.columns(3)
    
    examples = [
        "quantum computing algorithms",
        "transformer neural networks",
        "reinforcement learning robotics"
    ]
    
    for col, example in zip(example_cols, examples):
        with col:
            if st.button(f"💡 {example}", key=f"example_{example}"):
                run_research(example)
    
    # Execute research
    if search_button and query:
        run_research(query)
    
    st.markdown("---")
    
    # Display results
    if st.session_state.result:
        result = st.session_state.result
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Final Report", 
            "📚 Papers Found", 
            "🔬 Analyses",
            "📈 Statistics"
        ])
        
        with tab1:
            st.markdown("### 📊 Literature Review")
            st.markdown(result.get("final_report", "No report generated"))
            
            # Download button
            if result.get("final_report"):
                st.download_button(
                    label="📥 Download Report",
                    data=result["final_report"],
                    file_name=f"literature_review_{query.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
        
        with tab2:
            if result.get("papers"):
                display_papers(result["papers"])
            else:
                st.info("No papers found")
        
        with tab3:
            if result.get("analyses"):
                display_analyses(result["analyses"])
            else:
                st.info("No analyses available")
        
        with tab4:
            st.markdown("### 📈 Research Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Papers Found", len(result.get("papers", [])))
            
            with col2:
                st.metric("Extractions", len(result.get("extractions", [])))
            
            with col3:
                st.metric("Analyses", len(result.get("analyses", [])))
            
            with col4:
                report_words = len(result.get("final_report", "").split())
                st.metric("Report Words", report_words)
            
            # Paper categories
            if result.get("papers"):
                st.markdown("#### 📊 Paper Categories")
                categories = {}
                for paper in result["papers"]:
                    for cat in paper.get("categories", []):
                        categories[cat] = categories.get(cat, 0) + 1
                
                # Display top categories
                sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]
                for cat, count in sorted_cats:
                    st.write(f"- **{cat}**: {count} papers")

if __name__ == "__main__":
    main()
