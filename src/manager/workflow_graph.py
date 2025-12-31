from langgraph.graph import StateGraph, END
from src.manager.state import AgentState
from src.agents.profile_intelligence import ProfileIntelligenceAgent
from src.agents.opportunity_discovery import OpportunityDiscoveryAgent
from src.agents.recovery_strategist import RecoveryStrategistAgent
from src.memory.miras_memory import MIRASMemory
from typing import Dict, Any, List, Optional

class WorkflowGraph:
    def __init__(self, memory: MIRASMemory = None):
        self.memory = memory or MIRASMemory()
        self.profile_agent = ProfileIntelligenceAgent(memory=self.memory)
        self.opportunity_agent = OpportunityDiscoveryAgent(memory=self.memory)
        self.recovery_agent = RecoveryStrategistAgent(memory=self.memory)
        
        self.graph = self._build_graph()

    def _profile_analysis_node(self, state: AgentState) -> AgentState:
        user_input = state['user_input']
        
        # Determine if we have a resume path or github
        pdf_path = user_input.get('resume_path')
        github_username = user_input.get('github_username')
        
        # Direct Injection (from DB)
        if user_input.get('resume_text'):
            # Construct a stub profile response
            # Note: This bypasses fresh analysis. If we want fresh analysis on old text,
            # we need to adapt ProfileIntelligenceAgent to accept text.
            # For now, we trust the injected 'existing_skills'
            skills = user_input.get('existing_skills', {})
            profile_data = {
                'resume_data': {'raw_text': user_input.get('resume_text')},
                'skills': {'technical_skills': skills},
                'github_data': {} # We could injection this too if needed
            }
        else:
            profile_data = self.profile_agent.analyze_profile(pdf_path, github_username)
            
        state['profile_data'] = profile_data
        state['messages'].append("Profile analysis complete.")
        state['current_step'] = 'profile_analysis_complete'
        return state

    def _opportunity_discovery_node(self, state: AgentState) -> AgentState:
        # Stub logic for flow compatibility
        state['job_matches'] = []
        state['messages'].append("Opportunity discovery complete.")
        state['current_step'] = 'opportunity_discovery_complete'
        return state

    def _recovery_strategy_node(self, state: AgentState) -> AgentState:
        user_input = state['user_input']
        if user_input.get('rejection_scenario'):
             diagnosis = self.recovery_agent.diagnose_rejection(
                 state['profile_data'], 
                 user_input.get('rejected_job', {}), 
                 user_input.get('rejection_context', '')
             )
             strategy = self.recovery_agent.generate_recovery_strategy(
                 diagnosis, 
                 state['profile_data'],
                 user_input.get('rejected_job', {})
             )
             state['diagnosis'] = diagnosis
             state['recovery_strategy'] = strategy
             state['messages'].append("Recovery strategy generated.")
        
        state['current_step'] = 'recovery_strategy_complete'
        return state

    def _finalize_node(self, state: AgentState) -> AgentState:
        state['final_output'] = {
            'profile_summary': state['profile_data'],
            'recovery': state.get('recovery_strategy'),
            'diagnosis': state.get('diagnosis')
        }
        state['current_step'] = 'complete'
        return state

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
