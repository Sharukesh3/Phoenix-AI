from typing import TypedDict, Annotated, Any, Dict, List
import operator

class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    user_input: Dict[str, Any]
    profile_data: Dict[str, Any]
    job_matches: List[Dict[str, Any]]
    diagnosis: Dict[str, Any]
    recovery_strategy: Dict[str, Any]
    final_output: Dict[str, Any]
    current_step: str
    error: str
