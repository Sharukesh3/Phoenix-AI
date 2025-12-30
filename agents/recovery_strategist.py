from typing import Dict, List, Any, Optional
from agents.utils.tot_reasoning import TreeOfThoughtsReasoning
from memory.miras_memory import MIRASMemory
from llm.groq_client import GroqClient
import json

class RecoveryStrategistAgent:
    def __init__(self, memory: Optional[MIRASMemory] = None):
        self.tot_reasoning = TreeOfThoughtsReasoning()
        self.llm_client = GroqClient()
        self.memory = memory or MIRASMemory()
    
    def diagnose_rejection(self, profile_data: Dict[str, Any], job_data: Dict[str, Any], rejection_context: str = "") -> Dict[str, Any]:
        context = self._build_context(profile_data, job_data)
        problem = f"Job application rejected. {rejection_context}"
        
        evidence = {
            'user_skills': self._extract_user_skills(profile_data),
            'required_skills': job_data.get('required_skills', []),
            'user_experience': self._extract_experience(profile_data),
            'required_experience': job_data.get('experience_required', 'Not specified'),
            'skill_match_percentage': self._calculate_match_percentage(profile_data, job_data)
        }
        
        diagnosis = self.tot_reasoning.reason_through_problem(context, problem, evidence)
        
        root_cause = diagnosis['best_hypothesis']['hypothesis'] if diagnosis['best_hypothesis'] else "Unknown"
        
        self.memory.add_memory(
            f"Rejection diagnosis: {root_cause} | Skill match: {evidence['skill_match_percentage']}%",
            metadata={'type': 'rejection_diagnosis', 'root_cause': root_cause}
        )
        
        return {
            'diagnosis': diagnosis,
            'evidence': evidence,
            'root_cause': root_cause
        }
    
    def generate_recovery_strategy(self, diagnosis: Dict[str, Any], profile_data: Dict[str, Any]) -> Dict[str, Any]:
        root_cause = diagnosis.get('root_cause', 'Unknown')
        evidence = diagnosis.get('evidence', {})
        
        missing_skills = list(set(evidence.get('required_skills', [])) - set(evidence.get('user_skills', [])))
        
        action_plan = self._create_action_plan(root_cause, missing_skills, evidence)
        
        timeline = self._estimate_timeline(action_plan)
        
        resources = self._recommend_resources(missing_skills)
        
        detailed_timeline = self.generate_detailed_timeline(missing_skills, action_plan)
        
        self.memory.add_memory(
            f"Recovery strategy: {len(action_plan)} actions, {timeline} timeline, {len(missing_skills)} skills to learn",
            metadata={'type': 'recovery_strategy', 'timeline': timeline, 'action_count': len(action_plan)}
        )
        
        return {
            'root_cause': root_cause,
            'action_plan': action_plan,
            'timeline': timeline,
            'resources': resources,
            'priority_actions': action_plan[:3] if len(action_plan) >= 3 else action_plan,
            'detailed_timeline': detailed_timeline
        }
    
    def _build_context(self, profile_data: Dict[str, Any], job_data: Dict[str, Any]) -> str:
        context_parts = []
        
        if profile_data.get('profile_summary'):
            context_parts.append(f"User Profile: {profile_data['profile_summary']}")
        
        if job_data.get('title'):
            context_parts.append(f"Job Title: {job_data['title']}")
        
        if job_data.get('required_skills'):
            context_parts.append(f"Required Skills: {', '.join(job_data['required_skills'][:10])}")
        
        return " | ".join(context_parts)
    
    def _extract_user_skills(self, profile_data: Dict[str, Any]) -> List[str]:
        skills = []
        for category_skills in profile_data.get('skills', {}).values():
            for skill, _ in category_skills:
                skills.append(skill)
        return skills
    
    def _extract_experience(self, profile_data: Dict[str, Any]) -> str:
        if profile_data.get('resume_data'):
            sections = profile_data['resume_data'].get('sections', {})
            exp_section = sections.get('experience', '')
            if exp_section:
                return exp_section[:200]
        return "Not specified"
    
    def _calculate_match_percentage(self, profile_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
        user_skills = set(self._extract_user_skills(profile_data))
        required_skills = set(job_data.get('required_skills', []))
        
        if not required_skills:
            return 0.0
        
        matched = len(user_skills.intersection(required_skills))
        return round((matched / len(required_skills)) * 100, 2)
    
    def _create_action_plan(self, root_cause: str, missing_skills: List[str], evidence: Dict[str, Any]) -> List[Dict[str, str]]:
        messages = [
            {
                "role": "system",
                "content": "You are a career recovery strategist. Create actionable steps to address job rejection causes."
            },
            {
                "role": "user",
                "content": f"Root Cause: {root_cause}\nMissing Skills: {', '.join(missing_skills)}\nEvidence: {json.dumps(evidence)}\n\nCreate 5-7 specific action items. Return as JSON array with objects containing 'action' and 'description' keys."
            }
        ]
        
        response = self.llm_client.chat_completion(messages, temperature=0.7)
        
        try:
            action_plan = json.loads(response)
            if isinstance(action_plan, list):
                return action_plan
        except:
            pass
        
        default_plan = []
        for skill in missing_skills[:5]:
            default_plan.append({
                'action': f'Learn {skill}',
                'description': f'Complete online courses and build projects using {skill}'
            })
        
        return default_plan
    
    def _estimate_timeline(self, action_plan: List[Dict[str, str]]) -> str:
        num_actions = len(action_plan)
        
        if num_actions <= 3:
            return "2-4 weeks"
        elif num_actions <= 5:
            return "1-2 months"
        else:
            return "2-3 months"
    
    def _recommend_resources(self, missing_skills: List[str]) -> Dict[str, List[str]]:
        resources = {}
        
        resource_map = {
            'LangChain': [
                'LangChain Documentation: https://python.langchain.com/docs/get_started/introduction',
                'DeepLearning.AI - LangChain Course (Free)',
                'Build LLM Apps with LangChain.js (Udemy)',
                'LangChain GitHub Examples: https://github.com/langchain-ai/langchain'
            ],
            'LlamaIndex': [
                'LlamaIndex Documentation: https://docs.llamaindex.ai/',
                'LlamaIndex Starter Tutorial',
                'Building RAG with LlamaIndex (YouTube)',
                'LlamaIndex GitHub: https://github.com/run-llama/llama_index'
            ],
            'CrewAI': [
                'CrewAI Documentation: https://docs.crewai.com/',
                'Multi-Agent Systems with CrewAI',
                'CrewAI GitHub: https://github.com/joaomdmoura/crewAI',
                'CrewAI Tutorial Series (YouTube)'
            ],
            'ChromaDB': [
                'ChromaDB Documentation: https://docs.trychroma.com/',
                'Vector Databases Crash Course',
                'ChromaDB GitHub: https://github.com/chroma-core/chroma'
            ],
            'Pinecone': [
                'Pinecone Documentation: https://docs.pinecone.io/',
                'Pinecone Free Tier Setup',
                'Building Semantic Search with Pinecone'
            ],
            'Qdrant': [
                'Qdrant Documentation: https://qdrant.tech/documentation/',
                'Qdrant Quickstart Guide',
                'Qdrant GitHub: https://github.com/qdrant/qdrant'
            ],
            'Vector Database': [
                'Vector Databases Explained (Pinecone Blog)',
                'Building with Vector Databases Course',
                'Embeddings and Vector Search Tutorial'
            ],
            'Knowledge Graph': [
                'Neo4j Graph Database Fundamentals',
                'Knowledge Graphs for RAG',
                'Building Knowledge Graphs with Python'
            ],
            'Fine-tuning': [
                'Hugging Face Fine-tuning Guide',
                'Fine-tuning LLMs with LoRA/QLoRA',
                'OpenAI Fine-tuning Documentation',
                'Practical Fine-tuning Course (DeepLearning.AI)'
            ],
            'Agent': [
                'LangChain Agents Documentation',
                'Building Autonomous Agents',
                'ReAct: Reasoning and Acting in LLMs (Paper)',
                'Agent Patterns and Best Practices'
            ],
            'Multi-agent': [
                'Multi-Agent Systems with AutoGen',
                'CrewAI Multi-Agent Tutorial',
                'Coordinating Multiple AI Agents',
                'Multi-Agent Collaboration Patterns'
            ]
        }
        
        for skill in missing_skills[:10]:
            if skill in resource_map:
                resources[skill] = resource_map[skill]
            else:
                resources[skill] = [
                    f"Coursera: Search for {skill} courses",
                    f"Udemy: {skill} tutorials",
                    f"Official {skill} documentation",
                    f"YouTube: {skill} crash course",
                    f"GitHub: {skill} sample projects"
                ]
        
        return resources
    
    def generate_detailed_timeline(self, missing_skills: List[str], action_plan: List[Dict[str, str]]) -> Dict[str, Any]:
        num_skills = len(missing_skills)
        
        if num_skills <= 3:
            weeks = 2
        elif num_skills <= 6:
            weeks = 4
        else:
            weeks = 6
        
        weekly_plan = {}
        skills_per_week = max(1, num_skills // weeks)
        
        for week in range(1, weeks + 1):
            start_idx = (week - 1) * skills_per_week
            end_idx = min(start_idx + skills_per_week, num_skills)
            week_skills = missing_skills[start_idx:end_idx]
            
            weekly_plan[f"Week {week}"] = {
                'focus_skills': week_skills,
                'goals': [f"Complete {skill} fundamentals" for skill in week_skills],
                'deliverables': [f"Build a mini-project using {skill}" for skill in week_skills[:1]],
                'time_commitment': '10-15 hours'
            }
        
        return {
            'total_weeks': weeks,
            'weekly_breakdown': weekly_plan,
            'final_project': 'Build an end-to-end RAG application using learned technologies',
            'success_metrics': [
                'Complete all tutorial exercises',
                'Build 2-3 portfolio projects',
                'Contribute to open-source projects',
                'Write technical blog posts'
            ]
        }
