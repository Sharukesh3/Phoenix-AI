from typing import Dict, List, Any, Optional
from tavily import TavilyClient
from memory.miras_memory import MIRASMemory
import config
import re

class YouTubeTutorialAgent:
    def __init__(self, memory: Optional[MIRASMemory] = None):
        self.tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)
        self.memory = memory or MIRASMemory()
    
    def find_tutorials(self, missing_skills: List[str]) -> Dict[str, List[Dict[str, str]]]:
        tutorials = {}
        
        for skill in missing_skills[:8]:
            skill_tutorials = self._search_youtube_tutorials(skill)
            if skill_tutorials:
                tutorials[skill] = skill_tutorials
        
        self.memory.add_memory(
            f"Found YouTube tutorials for {len(tutorials)} skills",
            metadata={'type': 'tutorial_search', 'skills_count': len(tutorials)}
        )
        
        return tutorials
    
    def _search_youtube_tutorials(self, skill: str) -> List[Dict[str, str]]:
        queries = [
            f"{skill} tutorial for beginners site:youtube.com",
            f"{skill} crash course site:youtube.com",
            f"learn {skill} step by step site:youtube.com"
        ]
        
        all_results = []
        
        for query in queries[:1]:
            try:
                response = self.tavily_client.search(
                    query=query,
                    max_results=3,
                    search_depth="basic"
                )
                
                for result in response.get('results', []):
                    url = result.get('url', '')
                    if 'youtube.com' in url or 'youtu.be' in url:
                        all_results.append({
                            'title': result.get('title', ''),
                            'url': url,
                            'description': result.get('content', '')[:150]
                        })
                
                if len(all_results) >= 3:
                    break
                    
            except Exception as e:
                continue
        
        if not all_results:
            all_results = self._get_curated_tutorials(skill)
        
        return all_results[:3]
    
    def _get_curated_tutorials(self, skill: str) -> List[Dict[str, str]]:
        curated_map = {
            'LangChain': [
                {
                    'title': 'LangChain Crash Course - Build Apps with Language Models',
                    'url': 'https://www.youtube.com/watch?v=LbT1yp6quS8',
                    'description': 'Complete beginner tutorial for LangChain'
                },
                {
                    'title': 'LangChain Explained in 13 Minutes',
                    'url': 'https://www.youtube.com/watch?v=aywZrzNaKjs',
                    'description': 'Quick overview of LangChain concepts'
                }
            ],
            'LlamaIndex': [
                {
                    'title': 'LlamaIndex Tutorial - Build RAG Applications',
                    'url': 'https://www.youtube.com/results?search_query=llamaindex+tutorial',
                    'description': 'Learn to build RAG apps with LlamaIndex'
                }
            ],
            'CrewAI': [
                {
                    'title': 'CrewAI Tutorial - Multi-Agent Systems',
                    'url': 'https://www.youtube.com/results?search_query=crewai+tutorial',
                    'description': 'Build multi-agent systems with CrewAI'
                }
            ],
            'Fine-tuning': [
                {
                    'title': 'Fine-Tuning Large Language Models',
                    'url': 'https://www.youtube.com/watch?v=eC6Hd1hFvos',
                    'description': 'Complete guide to LLM fine-tuning'
                },
                {
                    'title': 'LoRA and QLoRA Explained',
                    'url': 'https://www.youtube.com/results?search_query=lora+qlora+fine+tuning',
                    'description': 'Efficient fine-tuning techniques'
                }
            ],
            'Vector Database': [
                {
                    'title': 'Vector Databases Explained',
                    'url': 'https://www.youtube.com/watch?v=klTvEwg3oJ4',
                    'description': 'Understanding vector databases and embeddings'
                }
            ],
            'ChromaDB': [
                {
                    'title': 'ChromaDB Tutorial - Vector Database for AI',
                    'url': 'https://www.youtube.com/results?search_query=chromadb+tutorial',
                    'description': 'Getting started with ChromaDB'
                }
            ],
            'Pinecone': [
                {
                    'title': 'Pinecone Vector Database Tutorial',
                    'url': 'https://www.youtube.com/results?search_query=pinecone+tutorial',
                    'description': 'Build semantic search with Pinecone'
                }
            ],
            'Knowledge Graph': [
                {
                    'title': 'Knowledge Graphs for RAG Applications',
                    'url': 'https://www.youtube.com/results?search_query=knowledge+graph+rag',
                    'description': 'Enhance RAG with knowledge graphs'
                }
            ],
            'Machine Learning': [
                {
                    'title': 'Machine Learning Course - Full Tutorial',
                    'url': 'https://www.youtube.com/watch?v=Gv9_4yMHFhI',
                    'description': 'Complete ML fundamentals course'
                }
            ]
        }
        
        if skill in curated_map:
            return curated_map[skill]
        
        return [{
            'title': f'{skill} Tutorial',
            'url': f'https://www.youtube.com/results?search_query={skill.replace(" ", "+")}+tutorial',
            'description': f'Search results for {skill} tutorials'
        }]
    
    def generate_learning_playlist(self, tutorials: Dict[str, List[Dict[str, str]]]) -> Dict[str, Any]:
        playlist = {
            'total_videos': sum(len(vids) for vids in tutorials.values()),
            'estimated_hours': sum(len(vids) * 0.5 for vids in tutorials.values()),
            'by_skill': tutorials,
            'recommended_order': list(tutorials.keys())
        }
        
        return playlist
