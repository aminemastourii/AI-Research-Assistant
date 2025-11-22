# Streamlit UI Guide

## Quick Start

### Running the Application

```bash
# Activate virtual environment and run
source venv/bin/activate
streamlit run app.py
```

The app will open in your browser at `http://localhost:8502`

## Features

### 🔍 Research Tab
- **Query Input**: Enter your research question or topic
- **Model Selection**: Choose between Gemini 2.5 Flash or Pro
- **Max Papers**: Control how many papers to analyze (1-10)
- **Example Queries**: Click to try pre-configured research topics:
  - Quantum computing and cryptography
  - Machine learning in healthcare
  - Climate change mitigation strategies

### 📄 Papers Tab
- View all analyzed papers with:
  - Title, authors, publication date
  - Extracted key findings
  - Analysis insights
  - Expandable full details

### 🗄️ Vector Store Tab
- **Semantic Search**: Query the knowledge base
- **Top K Results**: Control number of similar results (1-10)
- **View Statistics**: See total stored papers
- **Clear Storage**: Reset the vector database

## Sidebar

### Settings
- **GEMINI_API_KEY**: Enter your Google Gemini API key
- **Model Selection**: Choose between Flash (faster) or Pro (better quality)
- **Max Papers**: Adjust result count

### Search History
- View previous queries
- Click to rerun past searches

## Workflow

1. **Enter API Key** in sidebar settings
2. **Type Research Query** in Research tab
3. **Configure Settings** (optional):
   - Select model (Flash recommended for speed)
   - Set max papers (3-5 recommended)
4. **Click "Start Research"**
5. **Monitor Progress**:
   - Searching papers...
   - Extracting findings...
   - Analyzing insights...
   - Generating report...
6. **View Results**:
   - Final report in Research tab
   - Individual papers in Papers tab
   - Semantic search in Vector Store tab

## Tips

### Performance
- **Gemini 2.5 Flash**: Faster, good for most tasks
- **Gemini 2.5 Pro**: Higher quality, slower
- **Max Papers 3-5**: Good balance of depth vs. speed
- **Max Papers 1-2**: Quick overviews
- **Max Papers 8-10**: Comprehensive research (slower)

### Best Practices
- Start with specific queries for better results
- Use 3-5 papers for balanced analysis
- Check Papers tab for individual insights
- Use Vector Store for follow-up questions
- Save your API key in sidebar for session

### Troubleshooting

**Module not found errors?**
```bash
# Always activate venv first
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

**Port already in use?**
```bash
# Streamlit will auto-increment port (8502, 8503, etc.)
# Or specify custom port:
streamlit run app.py --server.port 8080
```

**API errors?**
- Verify GEMINI_API_KEY is correct
- Check internet connection
- Ensure Gemini API is enabled in Google Cloud

## Architecture

The Streamlit app integrates with the LangGraph pipeline:

```
User Query (Streamlit)
    ↓
StateGraph Pipeline
    ↓
├── Search Node → ArXiv papers
├── Extraction Node → Key findings
├── Analysis Node → Insights
├── Memory Node → Vector storage
└── Report Node → Final summary
    ↓
Results Display (Streamlit)
```

## Keyboard Shortcuts

- **Ctrl+S**: Save (auto-saves in session state)
- **Ctrl+R**: Rerun app
- **Ctrl+C**: Stop server (in terminal)

## Session State

The app maintains:
- Current query and results
- All analyzed papers
- Vector store instance
- Search history (up to 10 queries)
- User settings (API key, model choice)

Session persists until browser refresh or server restart.

## Next Steps

After running research:
1. Review the final report
2. Check individual papers for details
3. Use semantic search for related concepts
4. Export results (copy/paste report)
5. Run new queries or refine existing ones

---

**Need help?** Check the main README.md for project overview and architecture details.
