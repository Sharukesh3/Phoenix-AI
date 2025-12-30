from typing import Dict, Any, Optional
from agents.utils.resume_parser import ResumeParser
from agents.utils.github_analyzer import GitHubAnalyzer
from agents.utils.skill_extractor import SkillExtractor
from memory.embedding_utils import EmbeddingUtils
from memory.miras_memory import MIRASMemory
from llm.groq_client import GroqClient
import json

class ProfileIntelligenceAgent:
    def __init__(self, memory: Optional[MIRASMemory] = None):
        self.resume_parser = ResumeParser()
        self.github_analyzer = GitHubAnalyzer()
        self.skill_extractor = SkillExtractor()
        self.embedding_utils = EmbeddingUtils()
        self.llm_client = GroqClient()
        self.memory = memory or MIRASMemory()
    
    def analyze_profile(self, resume_path: Optional[str] = None, github_username: Optional[str] = None) -> Dict[str, Any]:
        profile_data = {
            'resume_data': None,
            'github_data': None,
            'skills': {},
            'profile_summary': None,
            'profile_embedding': None
        }
        
        if resume_path:
            resume_data = self.resume_parser.parse_resume(resume_path)
            profile_data['resume_data'] = resume_data
            
            resume_text = resume_data['raw_text']
            skills_from_resume = self.skill_extractor.extract_skills(resume_text)
            profile_data['skills'] = skills_from_resume
            
            if not github_username and 'github' in resume_data.get('contact_info', {}):
                github_username = resume_data['contact_info']['github']
            
            self.memory.add_memory(
                f"Resume analyzed with {len(skills_from_resume)} skill categories",
                metadata={'type': 'resume_analysis', 'source': 'pdf'}
            )
        
        if github_username:
            github_data = self.github_analyzer.analyze_user(github_username)
            profile_data['github_data'] = github_data
            
            self.memory.add_memory(
                f"GitHub profile {github_username}: {github_data.get('public_repos', 0)} repos, {len(github_data.get('languages', {}))} languages",
                metadata={'type': 'github_analysis', 'username': github_username}
            )
            
            if 'languages' in github_data:
                github_skills = list(github_data['languages'].keys())
                for lang in github_skills:
                    if lang not in [s[0] for category in profile_data['skills'].values() for s in category]:
                        if 'programming_languages' not in profile_data['skills']:
                            profile_data['skills']['programming_languages'] = []
                        profile_data['skills']['programming_languages'].append((lang, 0.5))
        
        profile_summary = self._generate_profile_summary(profile_data)
        profile_data['profile_summary'] = profile_summary
        
        profile_embedding = self.embedding_utils.generate_embedding(profile_summary)
        profile_data['profile_embedding'] = profile_embedding
        
        return profile_data
    
    def _generate_profile_summary(self, profile_data: Dict[str, Any]) -> str:
        summary_parts = []
        
        if profile_data['resume_data']:
            resume_sections = profile_data['resume_data']['sections']
            if 'summary' in resume_sections:
                summary_parts.append(f"Professional Summary: {resume_sections['summary'][:200]}")
        
        if profile_data['skills']:
            top_skills = self.skill_extractor.get_top_skills(profile_data['skills'], top_n=10)
            skills_str = ", ".join([f"{skill} ({score})" for skill, score in top_skills])
            summary_parts.append(f"Top Skills: {skills_str}")
        
        if profile_data['github_data'] and 'languages' in profile_data['github_data']:
            langs = profile_data['github_data']['languages']
            top_langs = list(langs.items())[:5]
            langs_str = ", ".join([f"{lang} ({pct}%)" for lang, pct in top_langs])
            summary_parts.append(f"GitHub Languages: {langs_str}")
        
        summary = " | ".join(summary_parts)
        
        messages = [
            {
                "role": "system",
                "content": "You are a professional career analyst. Create a concise professional profile summary."
            },
            {
                "role": "user",
                "content": f"Create a professional profile summary from this data:\n{summary}\n\nProvide a 2-3 sentence summary."
            }
        ]
        
        llm_summary = self.llm_client.chat_completion(messages, temperature=0.7)
        return llm_summary
    
    def get_skill_gaps(self, profile_data: Dict[str, Any], required_skills: list) -> Dict[str, Any]:
        user_skills = set()
        for category_skills in profile_data['skills'].values():
            for skill, _ in category_skills:
                user_skills.add(skill.lower())
        
        missing_skills = []
        present_skills = []
        
        for req_skill in required_skills:
            if req_skill.lower() in user_skills:
                present_skills.append(req_skill)
            else:
                missing_skills.append(req_skill)
        
        return {
            'missing_skills': missing_skills,
            'present_skills': present_skills,
            'match_percentage': round((len(present_skills) / len(required_skills)) * 100, 2) if required_skills else 0
        }
