import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any
import re

class JobScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def parse_job_description(self, html_content: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        
        job_data = {
            'raw_text': text,
            'required_skills': self._extract_skills(text),
            'experience_required': self._extract_experience(text),
            'education_required': self._extract_education(text)
        }
        
        return job_data
    
    def _extract_skills(self, text: str) -> List[str]:
        from llm.groq_client import GroqClient
        
        llm_client = GroqClient()
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert at analyzing job descriptions. Extract ALL required skills, technologies, tools, and qualifications from the job description. Return ONLY a JSON array of strings, nothing else."
            },
            {
                "role": "user",
                "content": f"Extract all required skills from this job description:\n\n{text}\n\nReturn as JSON array: [\"skill1\", \"skill2\", ...]"
            }
        ]
        
        try:
            response = llm_client.chat_completion(messages, temperature=0.3)
            
            import json
            import re
            
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                skills = json.loads(json_match.group(0))
                return skills if isinstance(skills, list) else []
            
            return []
        except Exception as e:
            return []
    
    def _extract_experience(self, text: str) -> str:
        exp_patterns = [
            r'(\d+)\+?\s*(?:to|\-)\s*(\d+)\s*years?',
            r'(\d+)\+?\s*years?',
            r'minimum\s*(\d+)\s*years?'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return "Not specified"
    
    def _extract_education(self, text: str) -> str:
        education_keywords = ['Bachelor', 'Master', 'PhD', 'B.Tech', 'M.Tech', 'BS', 'MS']
        
        for keyword in education_keywords:
            if keyword.lower() in text.lower():
                return keyword
        
        return "Not specified"
    
    def scrape_url(self, url: str) -> Dict[str, Any]:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return self.parse_job_description(response.text)
        except Exception as e:
            return {'error': str(e)}
    
    def parse_job_description_file(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            job_data = {
                'raw_text': text,
                'required_skills': self._extract_skills(text),
                'experience_required': self._extract_experience(text),
                'education_required': self._extract_education(text),
                'responsibilities': self._extract_responsibilities(text),
                'technologies': self._extract_technologies(text)
            }
            
            return job_data
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        responsibilities = []
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 20 and ('develop' in line.lower() or 'build' in line.lower() or 
                                   'design' in line.lower() or 'implement' in line.lower() or
                                   'create' in line.lower() or 'manage' in line.lower()):
                responsibilities.append(line)
        return responsibilities[:10]
    
    def _extract_technologies(self, text: str) -> List[str]:
        from llm.groq_client import GroqClient
        
        llm_client = GroqClient()
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert at analyzing job descriptions. Extract ALL technologies, frameworks, tools, and platforms mentioned. Return ONLY a JSON array of strings."
            },
            {
                "role": "user",
                "content": f"Extract all technologies and tools from this job description:\n\n{text}\n\nReturn as JSON array: [\"tech1\", \"tech2\", ...]"
            }
        ]
        
        try:
            response = llm_client.chat_completion(messages, temperature=0.3)
            
            import json
            import re
            
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                technologies = json.loads(json_match.group(0))
                return technologies if isinstance(technologies, list) else []
            
            return []
        except Exception as e:
            return []
