import arxiv
from typing import List, Dict, Optional

def search_papers(query: str, max_results: int = 5) -> List[Dict[str, any]]:
    """
    Search arXiv for academic papers.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        List of paper dictionaries containing title, authors, summary, etc.
    """
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        papers = []
        for paper in search.results():
            papers.append({
                "title": paper.title,
                "authors": [a.name for a in paper.authors],
                "summary": paper.summary,
                "published": paper.published.strftime("%Y-%m-%d") if paper.published else None,
                "pdf_url": paper.pdf_url,
                "entry_id": paper.entry_id,
                "categories": paper.categories,
                "primary_category": paper.primary_category
            })
        return papers
    except Exception as e:
        print(f"Error searching arXiv: {e}")
        return []
