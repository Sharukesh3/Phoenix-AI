import re
from typing import Dict, List, Tuple
from src.llm.groq_client import GroqClient
import json

class SkillExtractor:
    def __init__(self):
        self.llm_client = GroqClient()

    def extract_skills(self, text: str) -> Dict[str, any]:
        prompt = """
        You are an expert technical recruiter. Analyze the following resume text and extract a structured list of technical skills.
        
        Output EXCLUSIVELY a JSON object with the following schema:
        {
            "technical_skills": {
                "programming_languages": [["Skill", proficiency_0_to_1], ...],
                "machine_learning_frameworks": [["Skill", proficiency_0_to_1], ...],
                "databases": [["Skill", proficiency_0_to_1], ...],
                "web_and_mobile": [["Skill", proficiency_0_to_1], ...],
                "devops": [["Skill", proficiency_0_to_1], ...],
                "cloud": [["Skill", proficiency_0_to_1], ...],
                "tools": [["Skill", proficiency_0_to_1], ...]
            },
            "soft_skills": ["List of soft skills"]
        }
        
        Resume Text:
        """ + text[:4000]

        messages = [
            {"role": "system", "content": "You are a precise JSON extractor. Output only valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.llm_client.chat_completion(messages)
            # Response is already the content string
            content = response or '{}'
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                return json.loads(content[start:end])
            return {"technical_skills": {}}
        except Exception as e:
            print(f"Skill extraction error: {e}")
            return {"technical_skills": {}}
