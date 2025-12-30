from tavily import TavilyClient
from typing import Dict, List, Any, Optional
from agents.utils.job_scraper import JobScraper
from memory.embedding_utils import EmbeddingUtils
from memory.miras_memory import MIRASMemory
from llm.groq_client import GroqClient
import config

class OpportunityDiscoveryAgent:
    def __init__(self, memory: Optional[MIRASMemory] = None):
        self.tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)
        self.job_scraper = JobScraper()
        self.embedding_utils = EmbeddingUtils()
        self.llm_client = GroqClient()
        self.memory = memory or MIRASMemory()
    
    def search_jobs(self, query: str, max_results: int = None) -> List[Dict[str, Any]]:
        max_res = max_results or config.JOB_SEARCH_PARAMS['max_results']
        
        search_query = f"job openings {query}"
        
        try:
            response = self.tavily_client.search(
                query=search_query,
                max_results=max_res,
                search_depth=config.JOB_SEARCH_PARAMS['search_depth']
            )
            
            jobs = []
            for result in response.get('results', []):
                job_data = {
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'content': result.get('content', ''),
                    'score': result.get('score', 0)
                }
                jobs.append(job_data)
            
            self.memory.add_memory(
                f"Job search '{query}' returned {len(jobs)} results",
                metadata={'type': 'job_search', 'query': query, 'count': len(jobs)}
            )
            
            return jobs
        except Exception as e:
            return [{'error': str(e)}]
    
    def match_jobs_to_profile(self, jobs: List[Dict[str, Any]], profile_embedding, profile_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        matched_jobs = []
        
        for job in jobs:
            if 'error' in job:
                continue
            
            job_text = f"{job['title']} {job['content']}"
            job_embedding = self.embedding_utils.generate_embedding(job_text)
            
            similarity = self.embedding_utils.cosine_similarity(profile_embedding, job_embedding)
            
            job_skills = self._extract_job_skills(job_text)
            skill_match = self._calculate_skill_match(profile_data, job_skills)
            
            combined_score = (similarity * 0.6) + (skill_match * 0.4)
            
            matched_jobs.append({
                'job': job,
                'similarity_score': round(similarity, 3),
                'skill_match_score': round(skill_match, 3),
                'combined_score': round(combined_score, 3),
                'required_skills': job_skills
            })
        
        matched_jobs.sort(key=lambda x: x['combined_score'], reverse=True)
        return matched_jobs
    
    def _extract_job_skills(self, job_text: str) -> List[str]:
        parsed_job = self.job_scraper.parse_job_description(job_text)
        return parsed_job.get('required_skills', [])
    
    def _calculate_skill_match(self, profile_data: Dict[str, Any], job_skills: List[str]) -> float:
        if not job_skills:
            return 0.5
        
        user_skills = set()
        for category_skills in profile_data.get('skills', {}).values():
            for skill, _ in category_skills:
                user_skills.add(skill.lower())
        
        matched_skills = 0
        for job_skill in job_skills:
            if job_skill.lower() in user_skills:
                matched_skills += 1
        
        return matched_skills / len(job_skills) if job_skills else 0
    
    def generate_job_recommendations(self, matched_jobs: List[Dict[str, Any]], top_n: int = 5) -> str:
        top_jobs = matched_jobs[:top_n]
        
        recommendations = []
        for idx, match in enumerate(top_jobs, 1):
            job = match['job']
            recommendations.append(
                f"{idx}. {job['title']}\n"
                f"   Match Score: {match['combined_score']}\n"
                f"   URL: {job['url']}\n"
                f"   Required Skills: {', '.join(match['required_skills'][:5])}"
            )
        
        recommendations_text = "\n\n".join(recommendations)
        
        messages = [
            {
                "role": "system",
                "content": "You are a career advisor. Provide brief insights on job recommendations."
            },
            {
                "role": "user",
                "content": f"Here are the top job matches:\n{recommendations_text}\n\nProvide a brief summary and advice."
            }
        ]
        
        llm_advice = self.llm_client.chat_completion(messages, temperature=0.7)
        return llm_advice
    
    def analyze_skill_match_detailed(self, profile_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        user_skills_dict = profile_data.get('skills', {})
        user_skills = set()
        for category_skills in user_skills_dict.values():
            for skill, _ in category_skills:
                user_skills.add(skill.lower())
        
        required_skills = job_data.get('required_skills', [])
        required_tech = job_data.get('technologies', [])
        all_required = list(set(required_skills + required_tech))
        
        matching_skills = []
        missing_skills = []
        
        for req_skill in all_required:
            if req_skill.lower() in user_skills:
                matching_skills.append(req_skill)
            else:
                missing_skills.append(req_skill)
        
        match_percentage = (len(matching_skills) / len(all_required) * 100) if all_required else 0
        
        return {
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'total_required': len(all_required),
            'total_matching': len(matching_skills),
            'total_missing': len(missing_skills),
            'match_percentage': round(match_percentage, 2),
            'skill_matrix': {
                'strong_match': [s for s in matching_skills if s in ['Python', 'LLM', 'RAG', 'LangChain', 'Docker', 'AWS']],
                'partial_match': [s for s in matching_skills if s not in ['Python', 'LLM', 'RAG', 'LangChain', 'Docker', 'AWS']],
                'critical_gaps': missing_skills[:5]
            }
        }
