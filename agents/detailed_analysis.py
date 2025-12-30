from typing import Dict, List, Any, Optional
from llm.groq_client import GroqClient
from memory.miras_memory import MIRASMemory
import json

class DetailedAnalysisAgent:
    def __init__(self, memory: Optional[MIRASMemory] = None):
        self.llm_client = GroqClient()
        self.memory = memory or MIRASMemory()
    
    def analyze_skill_gap_detailed(self, profile_data: Dict[str, Any], job_data: Dict[str, Any], 
                                   skill_match: Dict[str, Any]) -> Dict[str, Any]:
        
        user_skills = profile_data.get('skills', {})
        github_data = profile_data.get('github_data', {})
        
        analysis = {
            'your_level': self._assess_current_level(user_skills, github_data),
            'industry_expectations': self._define_industry_expectations(job_data),
            'gap_analysis': self._detailed_gap_analysis(skill_match, user_skills, github_data),
            'improvement_roadmap': self._generate_improvement_roadmap(skill_match),
            'competitive_analysis': self._competitive_positioning(user_skills, github_data)
        }
        
        self.memory.add_memory(
            f"Detailed analysis: {analysis['your_level']['overall_rating']}/10 current level, {len(skill_match['missing_skills'])} critical gaps",
            metadata={'type': 'detailed_analysis'}
        )
        
        return analysis
    
    def _assess_current_level(self, skills: Dict[str, Any], github: Dict[str, Any]) -> Dict[str, Any]:
        total_skills = sum(len(skill_list) for skill_list in skills.values())
        
        github_score = 0
        if github.get('public_repos', 0) > 15:
            github_score += 2
        if github.get('activity_metrics', {}).get('total_commits', 0) > 500:
            github_score += 2
        if github.get('followers', 0) > 5:
            github_score += 1
        
        skill_score = min(5, total_skills // 5)
        
        overall_rating = min(10, skill_score + github_score)
        
        level_map = {
            (0, 3): "Junior",
            (4, 6): "Mid-Level",
            (7, 8): "Senior",
            (9, 10): "Expert"
        }
        
        level = "Junior"
        for (low, high), label in level_map.items():
            if low <= overall_rating <= high:
                level = label
                break
        
        return {
            'overall_rating': overall_rating,
            'level': level,
            'total_skills': total_skills,
            'github_activity': github.get('activity_metrics', {}).get('total_commits', 0),
            'github_repos': github.get('public_repos', 0),
            'strengths': self._identify_strengths(skills),
            'weaknesses': self._identify_weaknesses(skills)
        }
    
    def _identify_strengths(self, skills: Dict[str, Any]) -> List[str]:
        strengths = []
        for category, skill_list in skills.items():
            if len(skill_list) >= 3:
                top_skills = [s[0] for s in skill_list[:3]]
                strengths.extend(top_skills)
        return strengths[:8]
    
    def _identify_weaknesses(self, skills: Dict[str, Any]) -> List[str]:
        weak_categories = []
        for category, skill_list in skills.items():
            if len(skill_list) < 2:
                weak_categories.append(category.replace('_', ' ').title())
        return weak_categories
    
    def _define_industry_expectations(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        required_skills = job_data.get('required_skills', [])
        technologies = job_data.get('technologies', [])
        
        return {
            'expected_level': 'Senior',
            'years_experience': '3-5 years',
            'must_have_skills': required_skills[:5],
            'nice_to_have_skills': technologies[:5],
            'total_requirements': len(required_skills) + len(technologies),
            'industry_standards': {
                'GitHub Activity': '1000+ commits',
                'Open Source': '5+ contributions',
                'Projects': '10+ repositories',
                'Technical Depth': 'Multiple AI frameworks'
            }
        }
    
    def _detailed_gap_analysis(self, skill_match: Dict[str, Any], skills: Dict[str, Any], 
                               github: Dict[str, Any]) -> Dict[str, Any]:
        
        missing_skills = skill_match.get('missing_skills', [])
        
        critical_gaps = []
        moderate_gaps = []
        minor_gaps = []
        
        critical_keywords = ['LLM', 'RAG', 'LangChain', 'Vector Database', 'Fine-tuning']
        
        for skill in missing_skills:
            if any(keyword.lower() in skill.lower() for keyword in critical_keywords):
                critical_gaps.append(skill)
            elif len(critical_gaps) < 3:
                moderate_gaps.append(skill)
            else:
                minor_gaps.append(skill)
        
        github_gaps = []
        if github.get('activity_metrics', {}).get('total_commits', 0) < 1000:
            github_gaps.append('Increase GitHub activity (target: 1000+ commits)')
        if github.get('public_repos', 0) < 15:
            github_gaps.append('Build more projects (target: 15+ repos)')
        if github.get('followers', 0) < 10:
            github_gaps.append('Grow community presence (target: 10+ followers)')
        
        return {
            'critical_gaps': critical_gaps,
            'moderate_gaps': moderate_gaps,
            'minor_gaps': minor_gaps,
            'github_improvement_areas': github_gaps,
            'priority_order': critical_gaps + moderate_gaps[:2]
        }
    
    def _generate_improvement_roadmap(self, skill_match: Dict[str, Any]) -> Dict[str, Any]:
        missing = skill_match.get('missing_skills', [])
        
        return {
            'immediate_focus': missing[:2],
            'short_term': missing[2:4],
            'long_term': missing[4:],
            'learning_approach': [
                'Start with official documentation',
                'Build hands-on projects',
                'Contribute to open-source',
                'Write technical blog posts'
            ]
        }
    
    def _competitive_positioning(self, skills: Dict[str, Any], github: Dict[str, Any]) -> Dict[str, Any]:
        total_skills = sum(len(skill_list) for skill_list in skills.values())
        commits = github.get('activity_metrics', {}).get('total_commits', 0)
        
        percentile = 50
        if total_skills > 30 and commits > 500:
            percentile = 75
        elif total_skills > 20 and commits > 300:
            percentile = 60
        
        return {
            'market_percentile': percentile,
            'competitive_advantage': self._identify_strengths(skills)[:3],
            'areas_to_improve': ['Fine-tuning', 'Vector Databases', 'Production ML'],
            'recommendation': f"You're in the top {100-percentile}% of candidates. Focus on missing skills to reach top 10%."
        }
