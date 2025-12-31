import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any
import re
from src.llm.groq_client import GroqClient
import json

class JobScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.llm_client = GroqClient()

    def parse_job_description(self, html_content: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        
        messages = [
            {
                "role": "system",
                "content": "Extract all technologies and tools from this job description. Return JSON array of strings."
            },
            {
                "role": "user",
                "content": text[:4000]
            }
        ]
        
        try:
            response = self.llm_client.chat_completion(messages, temperature=0.3)
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                technologies = json.loads(json_match.group(0))
                return {'required_skills': technologies if isinstance(technologies, list) else []}
            return {'required_skills': []}
        except Exception:
            return {'required_skills': []}
