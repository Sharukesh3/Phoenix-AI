from typing import Dict, List, Any, Optional
from src.agents.utils.tot_reasoning import TreeOfThoughtsReasoning
from src.memory.miras_memory import MIRASMemory
from src.llm.groq_client import GroqClient
import json
import re

class RecoveryStrategistAgent:
    def __init__(self, memory: Optional[MIRASMemory] = None):
        self.tot_reasoning = TreeOfThoughtsReasoning()
        self.llm_client = GroqClient()
        self.memory = memory or MIRASMemory()

    def _extract_json(self, text: str) -> Dict[str, Any]:
        try:
            # First try direct load
            return json.loads(text)
        except:
            # Try finding first { and last }
            try:
                match = re.search(r'\{.*\}', text, re.DOTALL)
                if match:
                    return json.loads(match.group(0))
            except:
                pass
        return {}

    def diagnose_rejection(self, profile_data: Dict[str, Any], rejected_job: Dict[str, Any], context: str) -> Dict[str, Any]:
        skills = profile_data.get('skills', {}).get('technical_skills', {})
        job_desc = rejected_job.get('description', '')
        
        system_prompt = """
        You are an expert Career Recovery Agent. Analyze the rejection context and job description against the user's skills.
        Identify the root cause of rejection and provide hypotheses.
        Output JSON: {"root_cause": "...", "hypotheses": ["...", "..."]}
        """
        
        user_prompt = f"""
        User Skills: {skills}
        Rejection Context: {context}
        Job Description: {job_desc}
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = self.llm_client.chat_completion(messages)
            data = self._extract_json(response)
            if not data:
                print(f"FAILED TO PARSE DIAGNOSIS JSON: {response}")
                return {'root_cause': 'Analysis Failed (JSON Error)', 'hypotheses': ['The agent output could not be parsed.']}
            return data
        except Exception as e:
            print(f"Diagnosis Error: {e}")
            return {'root_cause': 'Unknown', 'hypotheses': ['Server error during diagnosis.']}

    def generate_recovery_strategy(self, diagnosis: Dict, profile_data: Dict, rejected_job: Dict[str, Any] = None) -> Dict[str, Any]:
        skills = profile_data.get('skills', {}).get('technical_skills', {})
        # Note: rejected_job is passed here too, workflow graph handles this.
        
        system_prompt = """
        You are a Career Strategist. Generate a detailed recovery plan.
        The output MUST be a valid JSON object with this EXACT structure:
        {
            "roadmap": { "focus_area": "...", "timeline": "..." },
            "detailed_analysis": {
                "current_level": { "level": "...", "total_skills": 0, "github_commits": 0, "github_repos": 0 },
                "strengths": ["..."],
                "industry_expectations": { "level": "...", "experience": "...", "must_have": ["..."] },
                "github_improvement": ["..."],
                "competitive_positioning": { "percentile": "...", "insight": "..." }
            },
            "skill_analysis": {
                "missing_skills": ["..."]
            },
            "youtube_resources": [ {"title": "...", "url": "..."} ],
            "learning_path": {
                "nodes": [
                    { "id": "1", "label": "Topic Name", "type": "concept", "status": "pending", "resource_query": "best free resource to learn Topic Name" },
                    { "id": "2", "label": "Skill Name", "type": "practice", "status": "pending", "resource_query": "Skill Name practice exercises" }
                ],
                "edges": [
                    { "source": "1", "target": "2", "label": "leads to" }
                ]
            },
            "action_plan": ["...", "..."],
            "timeline": "..."
        }
        Populate 'youtube_resources' with REAL, existing high-quality YouTube video titles and URLs.
        Populate 'learning_path' with a branching dependency graph (DAG) of concepts/skills. 
        - It should NOT be a single linear line. 
        - Identify independent topics that can be learned in parallel (separate branches).
        - Identify advanced topics that merge branches.
        - The graph should look like a roadmap tree (e.g., NeetCode style).
        """
        
        user_prompt = f"""
        Diagnosis: {diagnosis}
        User Skills: {skills}
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = self.llm_client.chat_completion(messages)
            data = self._extract_json(response)
            if not data:
                 print(f"FAILED TO PARSE STRATEGY JSON: {response}")
                 # fallback
                 return {
                    'diagnosis': diagnosis,
                    'roadmap': {'focus_area': 'Error parsing plan', 'timeline': 'N/A'},
                    'detailed_analysis': {'strengths': [], 'industry_expectations': {'must_have': []}},
                    'action_plan': ['Retry analysis'],
                    'youtube_resources': []
                }

            data['diagnosis'] = diagnosis 
            return data
        except Exception as e:
            print(f"Strategy Error: {e}")
            # Fallback
            return {
                'diagnosis': diagnosis,
                'roadmap': {'focus_area': 'Error generating plan', 'timeline': 'N/A'},
                'detailed_analysis': {'strengths': [], 'industry_expectations': {'must_have': []}},
                'action_plan': ['Retry analysis'],
                'youtube_resources': []
            }
