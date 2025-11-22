import os
from typing import List, Dict, Optional
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

class VectorStoreFAISS:
    """
    Manages FAISS vector store for semantic search of research papers.
    """
    
    def __init__(self, index_path: Optional[str] = None):
        """
        Initialize vector store manager.
        
        Args:
            index_path: Path to save/load FAISS index
        """
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        self.index_path = index_path or "backend/memory/faiss_index"
        self.vector_store = None
        
        # Try to load existing index
        if os.path.exists(self.index_path):
            self.load_index()
    
    def add(self, texts: List[str], metadatas: List[str] = None) -> None:
        """
        Add texts to vector store (used by pipeline_graph.py)
        
        Args:
            texts: List of text strings to add
            metadatas: List of metadata (paper IDs) for each text
        """
        if not texts:
            return
        
        if metadatas is None:
            metadatas = [{"id": str(i)} for i in range(len(texts))]
        else:
            metadatas = [{"paper_id": mid} for mid in metadatas]
        
        documents = [Document(page_content=text, metadata=meta) 
                    for text, meta in zip(texts, metadatas)]
        
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)
        
        print(f"[VECTOR STORE] Added {len(documents)} items to index")
    
    def add_papers(self, papers: List[Dict]) -> None:
        """
        Add research papers to the vector store.
        
        Args:
            papers: List of paper dictionaries from search_api
        """
        if not papers:
            return
        
        documents = []
        for paper in papers:
            # Create document with paper content
            content = f"""
            Title: {paper['title']}
            Authors: {', '.join(paper['authors'])}
            Published: {paper.get('published', 'N/A')}
            Categories: {', '.join(paper.get('categories', []))}
            Summary: {paper['summary']}
            """
            
            metadata = {
                "title": paper['title'],
                "authors": paper['authors'],
                "pdf_url": paper['pdf_url'],
                "entry_id": paper.get('entry_id', ''),
                "published": paper.get('published', ''),
                "categories": paper.get('categories', [])
            }
            
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)
        
        # Create or update vector store
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)
        
        print(f"[VECTOR STORE] Added {len(documents)} papers to index")
    
    def similarity_search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Perform semantic similarity search.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of matching papers with metadata
        """
        if self.vector_store is None:
            print("[VECTOR STORE] No papers in index yet")
            return []
        
        results = self.vector_store.similarity_search(query, k=k)
        
        papers = []
        for doc in results:
            papers.append(doc.metadata)
        
        return papers
    
    def similarity_search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """
        Perform semantic search with relevance scores.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of tuples (paper_metadata, score)
        """
        if self.vector_store is None:
            print("[VECTOR STORE] No papers in index yet")
            return []
        
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        papers_with_scores = []
        for doc, score in results:
            papers_with_scores.append((doc.metadata, score))
        
        return papers_with_scores
    
    def save_index(self) -> None:
        """Save FAISS index to disk."""
        if self.vector_store is not None:
            self.vector_store.save_local(self.index_path)
            print(f"[VECTOR STORE] Index saved to {self.index_path}")
    
    def load_index(self) -> None:
        """Load FAISS index from disk."""
        try:
            self.vector_store = FAISS.load_local(
                self.index_path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"[VECTOR STORE] Index loaded from {self.index_path}")
        except Exception as e:
            print(f"[VECTOR STORE] Could not load index: {e}")
    
    def clear_index(self) -> None:
        """Clear the vector store."""
        self.vector_store = None
        print("[VECTOR STORE] Index cleared")
