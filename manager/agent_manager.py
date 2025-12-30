from typing import Dict, Any, Optional
from manager.workflow_graph import WorkflowGraph
from memory.miras_memory import MIRASMemory
from llm.groq_client import GroqClient
import json

class AgentManager:
    def __init__(self, memory: Optional[MIRASMemory] = None):
        self.memory = memory or MIRASMemory()
        self.workflow = WorkflowGraph(memory=self.memory)
        self.llm_client = GroqClient()
    
    def execute_workflow(self, user_request: str, **kwargs) -> Dict[str, Any]:
        user_input = self._parse_user_request(user_request, **kwargs)
        
        result = self.workflow.run(user_input)
        
        formatted_result = self._format_result(result, user_input)
        
        return formatted_result
    
    def _parse_user_request(self, user_request: str, **kwargs) -> Dict[str, Any]:
        from agents.utils.job_scraper import JobScraper
        
        job_description_file = kwargs.get('job_description_file')
        parsed_jd = {}
        
        if job_description_file:
            scraper = JobScraper()
            parsed_jd = scraper.parse_job_description_file(job_description_file)
        
        user_input = {
            'raw_request': user_request,
            'resume_path': kwargs.get('resume_path'),
            'github_username': kwargs.get('github_username'),
            'job_query': kwargs.get('job_query', 'AI Engineer LLM RAG jobs'),
            'rejection_scenario': kwargs.get('rejection_scenario', False),
            'rejected_job': kwargs.get('rejected_job', parsed_jd),
            'rejection_context': kwargs.get('rejection_context', ''),
            'job_description_file': job_description_file,
            'parsed_job_description': parsed_jd
        }
        
        return user_input
    
    def _format_result(self, result: Dict[str, Any], user_input: Dict[str, Any]) -> Dict[str, Any]:
        final_output = result.get('final_output', {})
        
        formatted = {
            'status': 'success' if result.get('current_step') == 'complete' else 'incomplete',
            'profile_summary': final_output.get('profile_summary'),
            'top_jobs': [],
            'recovery_plan': None,
            'workflow_messages': result.get('messages', []),
            'memory_stats': final_output.get('memory_stats'),
            'skill_match_analysis': None,
            'github_data': result.get('profile_data', {}).get('github_data'),
            'extracted_skills': result.get('profile_data', {}).get('skills'),
            'detailed_analysis': final_output.get('detailed_analysis'),
            'youtube_tutorials': final_output.get('youtube_tutorials')
        }
        
        if user_input.get('parsed_job_description'):
            from agents.opportunity_discovery import OpportunityDiscoveryAgent
            from memory.miras_memory import MIRASMemory
            
            opp_agent = OpportunityDiscoveryAgent(memory=self.memory)
            profile_data = result.get('profile_data', {})
            jd_data = user_input['parsed_job_description']
            
            skill_analysis = opp_agent.analyze_skill_match_detailed(profile_data, jd_data)
            formatted['skill_match_analysis'] = skill_analysis
        
        for job_match in final_output.get('top_job_matches', []):
            formatted['top_jobs'].append({
                'title': job_match['job'].get('title'),
                'url': job_match['job'].get('url'),
                'match_score': job_match.get('combined_score'),
                'required_skills': job_match.get('required_skills', [])[:5]
            })
        
        if final_output.get('recovery_strategy'):
            recovery = final_output['recovery_strategy']
            formatted['recovery_plan'] = {
                'root_cause': recovery.get('root_cause'),
                'priority_actions': recovery.get('priority_actions', []),
                'timeline': recovery.get('timeline'),
                'resources': recovery.get('resources', {})
            }
        
        return formatted
    
    def get_conversational_summary(self, result: Dict[str, Any]) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful career assistant. Summarize the workflow results in a friendly, conversational manner."
            },
            {
                "role": "user",
                "content": f"Summarize these results for the user:\n{json.dumps(result, indent=2)}"
            }
        ]
        
        summary = self.llm_client.chat_completion(messages, temperature=0.7, max_tokens=500)
        return summary
