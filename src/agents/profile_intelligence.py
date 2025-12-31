from typing import Dict, Any, Optional
from src.agents.utils.resume_parser import ResumeParser
from src.agents.utils.github_analyzer import GitHubAnalyzer
from src.agents.utils.skill_extractor import SkillExtractor
from src.memory.miras_memory import MIRASMemory
from src.llm.groq_client import GroqClient
import json

class ProfileIntelligenceAgent:
    def __init__(self, memory: Optional[MIRASMemory] = None):
        self.resume_parser = ResumeParser()
        self.github_analyzer = GitHubAnalyzer()
        self.skill_extractor = SkillExtractor()
        self.memory = memory or MIRASMemory()
        self.llm_client = GroqClient()

    def analyze_profile(self, pdf_path: str = None, github_username: str = None) -> Dict[str, Any]:
        resume_data = {}
        if pdf_path:
            resume_data = self.resume_parser.parse_resume(pdf_path)
            # Store in memory
            self.memory.add_memory(f"Resume Content: {resume_data.get('raw_text', '')[:1000]}...", importance=0.8)

        github_data = {}
        if github_username:
            github_data = self.github_analyzer.analyze_user(github_username)
            # Store in memory
            self.memory.add_memory(f"GitHub Analysis for {github_username}: {json.dumps(github_data)}", importance=0.6)

        # Extract skills from resume text
        extracted_skills = {}
        if resume_data.get('raw_text'):
             # Simplify skill extraction call
             extracted_skills = self.skill_extractor.extract_skills(resume_data['raw_text'])

        return {
            'resume_data': resume_data,
            'github_data': github_data,
            'skills': extracted_skills
        }
