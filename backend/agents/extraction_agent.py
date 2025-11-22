from backend.llm_client import ask_mini

class ExtractionAgentNode:
    """Extraction agent node - extracts key information from papers"""
    
    def __init__(self):
        pass
    
    def run(self, papers):
        """
        Extract key information from each paper
        Args:
            papers: list of paper dictionaries
        Returns:
            list of papers with extracted information
        """
        extracted = []
        for paper in papers:
            prompt = f"""
Extract the key information from this research paper:

Title: {paper['title']}
Authors: {', '.join(paper['authors'])}
Summary: {paper['summary']}

Provide:
1. Main research question
2. Methodology
3. Key findings
4. Contributions

Be concise and structured.
"""
            extraction = ask_mini(prompt)
            extracted.append({
                'paper_id': paper['entry_id'],
                'title': paper['title'],
                'authors': paper['authors'],
                'extraction': extraction,
                'pdf_url': paper['pdf_url'],
                'published': paper['published']
            })
        return extracted
