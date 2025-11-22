from backend.tools.search_api import search_papers

class SearchAgentNode:
    """Search agent node for the pipeline - searches arXiv for papers"""
    
    def __init__(self):
        pass
    
    def run(self, query):
        """
        Search for papers on arXiv
        Args:
            query: str - search query
        Returns:
            list of paper dictionaries
        """
        results = search_papers(query, max_results=10)
        return results
