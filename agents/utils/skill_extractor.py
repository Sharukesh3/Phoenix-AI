import re
from typing import Dict, List, Tuple
from llm.groq_client import GroqClient
import json

class SkillExtractor:
    def __init__(self):
        self.llm_client = GroqClient()
    
    def extract_skills(self, text: str) -> Dict[str, List[Tuple[str, float]]]:
        messages = [
            {
                "role": "system",
                "content": """You are an expert at extracting skills from resumes. 
Extract ALL skills mentioned and categorize them logically (e.g., programming_languages, frameworks, databases, cloud, tools, etc.).
For each skill, estimate proficiency (0.0-1.0) based on context clues like "expert", "proficient", years of experience, or frequency.
Return ONLY a JSON object with this structure:
{
  "category_name": [["skill", proficiency], ["skill2", proficiency], ...],
  ...
}"""
            },
            {
                "role": "user",
                "content": f"Extract all skills with proficiency scores from this resume:\n\n{text[:3000]}"
            }
        ]
        
        try:
            response = self.llm_client.chat_completion(messages, temperature=0.3)
            
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                skills_dict = json.loads(json_match.group(0))
                
                formatted_skills = {}
                for category, skills in skills_dict.items():
                    if isinstance(skills, list):
                        formatted_skills[category] = [
                            (skill[0], float(skill[1])) if isinstance(skill, list) and len(skill) == 2 
                            else (skill, 0.5) if isinstance(skill, str)
                            else (str(skill), 0.5)
                            for skill in skills
                        ]
                
                return formatted_skills
            
            return self._fallback_extraction(text)
            
        except Exception as e:
            return self._fallback_extraction(text)
    
    def _fallback_extraction(self, text: str) -> Dict[str, List[Tuple[str, float]]]:
        text_lower = text.lower()
        
        common_skills = {
            "programming_languages": ["Python", "Java", "JavaScript", "C++", "Go", "TypeScript", "R"],
            "frameworks": ["React", "Django", "Flask", "TensorFlow", "PyTorch", "LangChain"],
            "databases": ["PostgreSQL", "MongoDB", "Redis", "MySQL"],
            "cloud": ["AWS", "Azure", "Docker", "Kubernetes"],
            "tools": ["Git", "Jupyter Notebook"]
        }
        
        found_skills = {}
        for category, skills in common_skills.items():
            category_skills = []
            for skill in skills:
                if skill.lower() in text_lower:
                    proficiency = min(text_lower.count(skill.lower()) * 0.2, 0.6)
                    category_skills.append((skill, proficiency))
            
            if category_skills:
                found_skills[category] = category_skills
        
        return found_skills
    
    def _calculate_proficiency(self, text: str, skill: str) -> float:
        text_lower = text.lower()
        skill_lower = skill.lower()
        
        count = text_lower.count(skill_lower)
        base_score = min(count * 0.2, 0.6)
        
        context_score = 0.0
        
        expert_patterns = [
            r'expert\s+(?:in|with|at)\s+' + re.escape(skill_lower),
            r'advanced\s+' + re.escape(skill_lower),
            r'proficient\s+(?:in|with)\s+' + re.escape(skill_lower),
            r'\d+\+?\s+years?\s+(?:of\s+)?(?:experience\s+)?(?:with\s+)?' + re.escape(skill_lower)
        ]
        
        for pattern in expert_patterns:
            if re.search(pattern, text_lower):
                context_score = 0.4
                break
        
        if context_score == 0.0:
            intermediate_patterns = [
                r'experience\s+(?:with|in)\s+' + re.escape(skill_lower),
                r'worked\s+(?:with|on)\s+' + re.escape(skill_lower),
                r'used\s+' + re.escape(skill_lower)
            ]
            for pattern in intermediate_patterns:
                if re.search(pattern, text_lower):
                    context_score = 0.2
                    break
        
        total_score = min(base_score + context_score, 1.0)
        return round(total_score, 2)
    
    def get_top_skills(self, skills_dict: Dict[str, List[Tuple[str, float]]], top_n: int = 10) -> List[Tuple[str, float]]:
        all_skills_flat = []
        for category_skills in skills_dict.values():
            all_skills_flat.extend(category_skills)
        
        all_skills_flat.sort(key=lambda x: x[1], reverse=True)
        return all_skills_flat[:top_n]
