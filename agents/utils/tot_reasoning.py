from typing import List, Dict, Any
from llm.groq_client import GroqClient
import json

class TreeOfThoughtsReasoning:
    def __init__(self):
        self.llm_client = GroqClient()
    
    def generate_hypotheses(self, context: str, problem: str) -> List[str]:
        messages = [
            {
                "role": "system",
                "content": "You are an expert career analyst. Generate multiple hypotheses for why a job application might be rejected."
            },
            {
                "role": "user",
                "content": f"Context: {context}\nProblem: {problem}\n\nGenerate 5 distinct hypotheses for the rejection. Return as JSON array of strings."
            }
        ]
        
        response = self.llm_client.chat_completion(messages, temperature=0.9)
        
        try:
            hypotheses = json.loads(response)
            if isinstance(hypotheses, list):
                return hypotheses
        except:
            pass
        
        return [
            "Skill gap in required technologies",
            "Insufficient years of experience",
            "Resume formatting or clarity issues",
            "Lack of relevant project experience",
            "Missing certifications or qualifications"
        ]
    
    def evaluate_hypothesis(self, hypothesis: str, evidence: Dict[str, Any]) -> Dict[str, Any]:
        messages = [
            {
                "role": "system",
                "content": "You are an expert evaluator. Assess the likelihood of a hypothesis given evidence."
            },
            {
                "role": "user",
                "content": f"Hypothesis: {hypothesis}\n\nEvidence: {json.dumps(evidence, indent=2)}\n\nProvide:\n1. Likelihood score (0-1)\n2. Supporting evidence\n3. Counter evidence\n\nReturn as JSON with keys: likelihood, supporting, counter"
            }
        ]
        
        response = self.llm_client.chat_completion(messages, temperature=0.5)
        
        try:
            evaluation = json.loads(response)
            return evaluation
        except:
            return {
                "likelihood": 0.5,
                "supporting": "Unable to parse evidence",
                "counter": "Insufficient data"
            }
    
    def select_best_hypothesis(self, evaluated_hypotheses: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not evaluated_hypotheses:
            return None
        
        best = max(evaluated_hypotheses, key=lambda x: x.get('evaluation', {}).get('likelihood', 0))
        return best
    
    def reason_through_problem(self, context: str, problem: str, evidence: Dict[str, Any]) -> Dict[str, Any]:
        hypotheses = self.generate_hypotheses(context, problem)
        
        evaluated = []
        for hypothesis in hypotheses:
            evaluation = self.evaluate_hypothesis(hypothesis, evidence)
            evaluated.append({
                'hypothesis': hypothesis,
                'evaluation': evaluation
            })
        
        best_hypothesis = self.select_best_hypothesis(evaluated)
        
        return {
            'all_hypotheses': evaluated,
            'best_hypothesis': best_hypothesis,
            'reasoning_path': self._generate_reasoning_path(evaluated, best_hypothesis)
        }
    
    def _generate_reasoning_path(self, evaluated_hypotheses: List[Dict[str, Any]], best: Dict[str, Any]) -> str:
        path = "Reasoning Process:\n\n"
        
        for idx, item in enumerate(evaluated_hypotheses, 1):
            likelihood = item['evaluation'].get('likelihood', 0)
            path += f"{idx}. {item['hypothesis']} (Likelihood: {likelihood})\n"
        
        if best:
            path += f"\nMost Likely Cause: {best['hypothesis']}\n"
            path += f"Supporting Evidence: {best['evaluation'].get('supporting', 'N/A')}\n"
        
        return path
