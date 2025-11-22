from backend.llm_client import ask_mini

class AnalysisAgentNode:
    """Analysis agent node - performs deep analysis of extracted information"""
    
    def __init__(self):
        pass
    
    def run(self, extractions):
        """
        Analyze extracted information from papers
        Args:
            extractions: list of extracted paper information
        Returns:
            list of papers with analysis
        """
        analyses = []
        for item in extractions:
            prompt = f"""
Perform a critical analysis of this research paper:

Title: {item['title']}
Authors: {', '.join(item['authors'])}

Extracted Information:
{item['extraction']}

Provide:
1. Strengths of the research
2. Limitations and weaknesses
3. Significance and impact
4. How it relates to the broader field
5. Future research directions suggested

Be analytical and constructive.
"""
            analysis = ask_mini(prompt)
            analyses.append({
                'paper_id': item['paper_id'],
                'title': item['title'],
                'authors': item['authors'],
                'extraction': item['extraction'],
                'analysis': analysis,
                'pdf_url': item['pdf_url'],
                'published': item['published']
            })
        return analyses
