from langgraph.graph import StateGraph, END
from manager.state import AgentState
from agents.profile_intelligence import ProfileIntelligenceAgent
from agents.opportunity_discovery import OpportunityDiscoveryAgent
from agents.recovery_strategist import RecoveryStrategistAgent
from memory.miras_memory import MIRASMemory
from typing import Dict, Any, List, Optional

class WorkflowGraph:
    def __init__(self, memory: MIRASMemory = None):
        self.memory = memory or MIRASMemory()
        self.profile_agent = ProfileIntelligenceAgent(memory=self.memory)
        self.opportunity_agent = OpportunityDiscoveryAgent(memory=self.memory)
        self.recovery_agent = RecoveryStrategistAgent(memory=self.memory)
        
        from agents.detailed_analysis import DetailedAnalysisAgent
        from agents.youtube_tutorial import YouTubeTutorialAgent
        self.analysis_agent = DetailedAnalysisAgent(memory=self.memory)
        self.tutorial_agent = YouTubeTutorialAgent(memory=self.memory)
        
        self.graph = self._build_graph()
    
    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("profile_analysis", self._profile_analysis_node)
        workflow.add_node("opportunity_discovery", self._opportunity_discovery_node)
        workflow.add_node("recovery_strategy", self._recovery_strategy_node)
        workflow.add_node("finalize", self._finalize_node)
        
        workflow.set_entry_point("profile_analysis")
        
        workflow.add_edge("profile_analysis", "opportunity_discovery")
        workflow.add_edge("opportunity_discovery", "recovery_strategy")
        workflow.add_edge("recovery_strategy", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    def _profile_analysis_node(self, state: AgentState) -> AgentState:
        user_input = state['user_input']
        
        resume_path = user_input.get('resume_path')
        github_username = user_input.get('github_username')
        
        profile_data = self.profile_agent.analyze_profile(resume_path, github_username)
        
        state['profile_data'] = profile_data
        state['current_step'] = 'profile_analysis_complete'
        state['messages'].append(f"Profile analysis complete. Found {len(profile_data.get('skills', {}))} skill categories.")
        
        return state
    
    def _opportunity_discovery_node(self, state: AgentState) -> AgentState:
        user_input = state['user_input']
        profile_data = state['profile_data']
        
        job_query = user_input.get('job_query', 'software engineer jobs')
        
        jobs = self.opportunity_agent.search_jobs(job_query)
        
        profile_embedding = profile_data.get('profile_embedding')
        matched_jobs = self.opportunity_agent.match_jobs_to_profile(jobs, profile_embedding, profile_data)
        
        state['job_matches'] = matched_jobs
        state['current_step'] = 'opportunity_discovery_complete'
        state['messages'].append(f"Found {len(matched_jobs)} job matches.")
        
        return state
    
    def _recovery_strategy_node(self, state: AgentState) -> AgentState:
        user_input = state['user_input']
        profile_data = state['profile_data']
        job_matches = state['job_matches']
        
        if user_input.get('rejection_scenario'):
            rejected_job = user_input.get('rejected_job', {})
            rejection_context = user_input.get('rejection_context', '')
            
            diagnosis = self.recovery_agent.diagnose_rejection(profile_data, rejected_job, rejection_context)
            recovery_strategy = self.recovery_agent.generate_recovery_strategy(diagnosis, profile_data)
            
            self.memory.add_memory(
                f"Recovery strategy generated for rejection: {diagnosis.get('root_cause', 'Unknown')}",
                metadata={'type': 'recovery_strategy'}
            )
            
            state['diagnosis'] = diagnosis
            state['recovery_strategy'] = recovery_strategy
            state['messages'].append(f"Recovery strategy created. Root cause: {diagnosis.get('root_cause', 'Unknown')}")
        else:
            state['messages'].append("No rejection scenario provided. Skipping recovery strategy.")
        
        state['current_step'] = 'recovery_strategy_complete'
        
        return state
    
    def _finalize_node(self, state: AgentState) -> AgentState:
        user_input = state['user_input']
        profile_data = state['profile_data']
        job_matches = state['job_matches']
        
        detailed_analysis = None
        youtube_tutorials = None
        
        if user_input.get('parsed_job_description') and profile_data:
            from agents.opportunity_discovery import OpportunityDiscoveryAgent
            opp_agent = OpportunityDiscoveryAgent(memory=self.memory)
            skill_match = opp_agent.analyze_skill_match_detailed(
                profile_data, 
                user_input['parsed_job_description']
            )
            
            detailed_analysis = self.analysis_agent.analyze_skill_gap_detailed(
                profile_data,
                user_input['parsed_job_description'],
                skill_match
            )
            
            missing_skills = skill_match.get('missing_skills', [])
            if missing_skills:
                youtube_tutorials = self.tutorial_agent.find_tutorials(missing_skills)
        
        final_output = {
            'profile_summary': profile_data.get('profile_summary'),
            'top_job_matches': job_matches[:5] if job_matches else [],
            'recovery_strategy': state.get('recovery_strategy'),
            'memory_stats': self.memory.get_stats(),
            'detailed_analysis': detailed_analysis,
            'youtube_tutorials': youtube_tutorials
        }
        
        state['final_output'] = final_output
        state['current_step'] = 'complete'
        state['messages'].append("Workflow complete with detailed analysis and tutorials.")
        
        return state
    
    def run(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        initial_state = {
            'messages': [],
            'user_input': user_input,
            'profile_data': {},
            'job_matches': [],
            'diagnosis': {},
            'recovery_strategy': {},
            'final_output': {},
            'current_step': 'initialized',
            'error': ''
        }
        
        final_state = self.graph.invoke(initial_state)
        
        return final_state
