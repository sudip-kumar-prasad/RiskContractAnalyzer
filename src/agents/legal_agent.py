import enum
import json
import os
import re
from typing import List, Dict, Any, Optional
from utils.llm_client import LLMClient
from utils.retriever import get_relevant_guidelines
from src.agents.prompts import SYSTEM_PROMPT, ANALYSIS_TEMPLATE, REPORT_SUMMARY_TEMPLATE

class AgentState(enum.Enum):
    IDLE = "Idle"
    INITIALIZING = "Initializing"
    ANALYZING = "Analyzing Risks"
    RETRIEVING = "Retrieving Knowledge"
    REPORTING = "Generating Report"
    COMPLETED = "Completed"
    ERROR = "Error"

class LegalAgent:
    def __init__(self):
        self.state = AgentState.IDLE
        self.llm = LLMClient()
        self.history: List[Dict[str, str]] = []
        self.state_callback = None
        self.report = {}
        self.last_error = ""

    def _parse_json(self, text: str) -> Dict[str, Any]:
        try:
            cleaned = text.strip().strip('`').strip('json').strip()
            match = re.search(r'(\{.*\})', cleaned, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            return json.loads(cleaned)
        except Exception as e:
            self.last_error = str(e)
            return {}

    def set_state(self, state: AgentState):
        self.state = state
        if self.state_callback:
            self.state_callback(state)
        print(f"[Agent Status]: {state.value}")

    def generate_final_report(self, clauses: List[Dict[str, Any]]):
        try:
            self.set_state(AgentState.INITIALIZING)
            self.set_state(AgentState.RETRIEVING)
            for clause in clauses:
                if 'text' in clause:
                    guidelines = get_relevant_guidelines(clause['text'])
                    clause['relevant_guidelines'] = [g.get('content', '') for g in guidelines]
                    self.history.append({
                        "action": "retrieve_guidelines",
                        "clause_id": clause.get('id', 'unknown'),
                        "guidelines_found": len(guidelines)
                    })
            
            self.set_state(AgentState.ANALYZING)
            for clause in clauses:
                prompt = ANALYSIS_TEMPLATE.format(
                    clause_text=clause['text'],
                    guidelines="\n".join(clause['relevant_guidelines'])
                )
                parsed_data = self._parse_json(response_text)
                if parsed_data:
                    clause.update(parsed_data)
                else:
                    clause.update({
                        "risk_severity": "High",
                        "explanation": f"Significant risk detected. Analysis error: {response_text if 'Error' in response_text else self.last_error}",
                        "mitigation": "Manual legal review required."
                    })

            self.set_state(AgentState.REPORTING)
            self.report = self.generate_report(clauses)
            self.set_state(AgentState.COMPLETED)
            return self.report
        except Exception:
            self.set_state(AgentState.ERROR)
            return None

    def generate_report(self, clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
        clauses_data = json.dumps([{
            "text": c.get('text'),
            "risk_severity": c.get('risk_severity'),
            "explanation": c.get('explanation')
        } for c in clauses], indent=2)
        
        prompt = REPORT_SUMMARY_TEMPLATE.format(clauses_data=clauses_data)
        response_text = self.llm.generate_response(prompt, system_instruction=SYSTEM_PROMPT)
        
        report_meta = self._parse_json(response_text)
        if not report_meta:
            report_meta = {
                "contract_summary": f"AI Analysis incomplete: {response_text if 'Error' in response_text else self.last_error}",
                "legal_disclaimer": "AI usage disclaimer: Manual review required due to processing error."
            }
            
        final_report = {
            "contract_summary": report_meta.get("contract_summary", ""),
            "legal_disclaimer": report_meta.get("legal_disclaimer", ""),
            "clause_assessments": clauses,
            "analysis_history": self.history
        }
        
        os.makedirs("data/reports", exist_ok=True)
        report_path = "data/reports/analysis_report.json"
        with open(report_path, "w") as f:
            json.dump(final_report, f, indent=4)
        
        return final_report

if __name__ == "__main__":
    agent = LegalAgent()
    sample_clauses = [
        {"id": 1, "text": "The company shall not be liable for any damages."},
        {"id": 2, "text": "All disputes shall be settled in Mars."}
    ]
    report = agent.run_analysis("Mock contract", sample_clauses)
    if report:
        print("Analysis completed.")
