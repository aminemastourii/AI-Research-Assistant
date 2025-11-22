# AI Research Assistant

An intelligent research assistant that automatically searches, analyzes, and synthesizes academic papers using AI-powered workflows.

## Overview

This system uses a multi-stage AI pipeline to transform research queries into comprehensive literature reviews. It searches academic databases, extracts key information, performs critical analysis, and generates synthesis reports—all powered by OpenAI's GPT models and LangGraph workflow orchestration.

## Features

✨ **Automated Research Workflow**
- Search arXiv for relevant academic papers
- AI-powered information extraction
- Critical analysis and evaluation
- Vector-based semantic search
- Automated literature review generation

🤖 **AI-Powered Intelligence**
- GPT-4o-mini for fast processing (extraction & analysis)
- GPT-4o for high-quality synthesis (final reports)
- Semantic embeddings for intelligent paper matching

📊 **Advanced Capabilities**
- FAISS vector database for semantic search
- LangGraph state management and orchestration
- Persistent storage of analyzed papers
- Modular and extensible architecture

## Architecture

### System Flow

```
User Query
    ↓
┌─────────────────────────────────────┐
│   LangGraph Workflow Orchestration   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Stage 1: Search                    │
│  • Query arXiv API                  │
│  • Retrieve paper metadata          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Stage 2: Extraction                │
│  • Extract research questions       │
│  • Identify methodology             │
│  • Capture key findings             │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Stage 3: Analysis                  │
│  • Evaluate strengths/limitations   │
│  • Assess significance              │
│  • Identify future directions       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Stage 4: Vector Storage            │
│  • Generate embeddings              │
│  • Store in FAISS index             │
│  • Enable semantic search           │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Stage 5: Report Generation         │
│  • Synthesize all analyses          │
│  • Generate literature review       │
│  • Produce final report             │
└─────────────────────────────────────┘
    ↓
Final Literature Review
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | OpenAI GPT-4o/GPT-4o-mini | AI reasoning and generation |
| **Workflow** | LangGraph | State management and orchestration |
| **LLM Framework** | LangChain | LLM integration and tooling |
| **Vector DB** | FAISS | Semantic search and storage |
| **Embeddings** | OpenAI text-embedding-3-small | Text vectorization |
| **Paper Search** | arXiv API | Academic paper retrieval |

### Project Structure

```
AI-Research-Assistant/
│
├── backend/
│   ├── llm_client.py              # LangChain + OpenAI integration
│   ├── main.py                    # CLI entry point
│   │
│   ├── agents/                    # Processing agents
│   │   ├── search_agent.py        # arXiv search
│   │   ├── extraction_agent.py    # Information extraction
│   │   └── analysis_agent.py      # Critical analysis
│   │
│   ├── graph/                     # Workflow orchestration
│   │   └── pipeline_graph.py      # LangGraph pipeline
│   │
│   ├── memory/                    # Storage layer
│   │   └── vector_store.py        # FAISS vector database
│   │
│   └── tools/                     # Utilities
│       └── search_api.py          # arXiv API wrapper
│
├── test_pipeline_simple.py        # Pipeline test script
├── examples.py                    # Usage examples
├── requirements.txt               # Dependencies
└── .env                          # API keys
```

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd AI-Research-Assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

## Usage

### Quick Start

Run the main application:

```bash
python backend/main.py
```

You'll be prompted to enter a research topic:

```
Enter research topic to explore: quantum machine learning
```

The system will automatically:
1. Search for relevant papers
2. Extract key information
3. Perform critical analysis
4. Store in vector database
5. Generate comprehensive literature review

### Test the Pipeline

```bash
python test_pipeline_simple.py
```

### Programmatic Usage

```python
from backend.graph.pipeline_graph import create_pipeline
from backend.memory.vector_store import VectorStoreFAISS

# Initialize
vector_store = VectorStoreFAISS()
pipeline = create_pipeline(vector_store)

# Run pipeline
result = pipeline.invoke({
    "query": "neural networks",
    "papers": [],
    "extractions": [],
    "analyses": [],
    "final_report": ""
})

# Get final report
print(result["final_report"])
```

### Using Individual Components

```python
from backend.agents.search_agent import SearchAgentNode

# Search only
search_agent = SearchAgentNode()
papers = search_agent.run("quantum computing")

for paper in papers:
    print(f"{paper['title']}")
    print(f"  {paper['pdf_url']}")
```

## LangGraph Workflow

The pipeline uses LangGraph for state management and orchestration:

```python
# State flows through the workflow
PipelineState = {
    "query": str,           # Research query
    "papers": List[Dict],   # Found papers
    "extractions": List,    # Extracted information
    "analyses": List,       # Critical analyses
    "final_report": str     # Generated review
}

# Workflow automatically manages transitions
search → extract → analyze → store → report
```

### Benefits of LangGraph

- ✅ Automatic state management
- ✅ Clear workflow visualization
- ✅ Built-in error handling
- ✅ Easy to extend with branches/loops
- ✅ Checkpointing for long-running tasks

## Example Output

```
================================================================================
AI RESEARCH ASSISTANT
================================================================================

Initializing vector store...
Building research pipeline...

Enter research topic to explore: quantum computing algorithms

Processing query: 'quantum computing algorithms'
--------------------------------------------------------------------------------

Executing LangGraph pipeline...

================================================================================
FINAL LITERATURE REVIEW
================================================================================

This literature review examines recent advances in quantum computing algorithms,
with particular focus on three key areas...

[Comprehensive multi-paragraph analysis follows]

The reviewed papers demonstrate significant progress in quantum algorithm 
development, from theoretical frameworks to practical implementations...

================================================================================

✓ Vector store saved to backend/memory/faiss_index
Research assistant session complete!
```

## API Reference

### Pipeline Creation

```python
create_pipeline(vector_store: VectorStoreFAISS) -> CompiledGraph
```

Creates and compiles the LangGraph research pipeline.

### Pipeline Invocation

```python
pipeline.invoke(initial_state: Dict) -> Dict
```

Executes the full research workflow and returns final state.

### State Schema

```python
{
    "query": str,              # Research topic
    "papers": List[Dict],      # Paper metadata
    "extractions": List[Dict], # Extracted info
    "analyses": List[Dict],    # Critical analyses
    "final_report": str        # Final synthesis
}
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Yes |

### Pipeline Settings

Edit `backend/graph/pipeline_graph.py` to customize:
- Number of papers to process
- Analysis depth
- Report format
- Workflow stages

## Development

### Running Tests

```bash
python test_pipeline_simple.py
```

### Running Examples

```bash
python examples.py
```

### Adding Custom Stages

Add new nodes to the LangGraph workflow in `pipeline_graph.py`:

```python
def custom_node(state: PipelineState) -> PipelineState:
    # Your processing logic
    return {"new_field": result}

workflow.add_node("custom", custom_node)
workflow.add_edge("analyze", "custom")
workflow.add_edge("custom", "memory")
```

## Troubleshooting

### Quota Exceeded Error

If you hit the embedding API quota:
- Wait for quota reset
- Reduce number of papers processed
- Use the test script which processes fewer papers

### Import Errors

Ensure virtual environment is activated:
```bash
source venv/bin/activate
```

### No Papers Found

Try broader search terms or different keywords.

## Dependencies

Core dependencies:
- `langchain>=0.1.0` - LLM framework
- `langchain-openai>=0.0.5` - OpenAI integration
- `langgraph>=0.0.20` - Workflow orchestration
- `faiss-cpu>=1.7.4` - Vector search
- `arxiv>=2.1.0` - Paper search
- `python-dotenv>=1.0.0` - Environment management

## Performance

- **Search**: ~2-3 seconds per query
- **Extraction**: ~5-10 seconds per paper
- **Analysis**: ~5-10 seconds per paper
- **Report Generation**: ~10-15 seconds

Total pipeline: ~1-2 minutes for 3 papers

## Future Enhancements

- [ ] Web interface with Streamlit
- [ ] Support for additional paper sources (PubMed, Semantic Scholar)
- [ ] Citation graph analysis
- [ ] Export to PDF/LaTeX/Markdown
- [ ] Batch processing multiple queries
- [ ] Advanced semantic search features

## License

MIT

## Contributing

Contributions welcome! Areas for improvement:
- Additional paper sources
- Enhanced analysis prompts
- UI/UX improvements
- Performance optimizations
- Documentation

## Acknowledgments

Built with:
- LangChain & LangGraph by LangChain Inc.
- OpenAI API key
- FAISS by Meta AI Research
- arXiv API
