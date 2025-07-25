from typing import Dict, Any
from graph.builder import build_medical_graph
from nodes.input_output import format_final_output

class MedicalAgent:
   
    
    def __init__(self):
        self.graph = build_medical_graph()
        self.session_stats = {
            'total_consultations': 0,
            'last_category': None
        }
    
    def diagnose(self, symptoms: str) -> Dict[str, Any]:
       
        try:
            # Execute the graph
            state = self.graph.invoke({
                "symptoms": symptoms,
                "response": "",
                "category": "",
                "ward": "",
                "answer": ""
            })
            
            # Update session stats
            self.session_stats['total_consultations'] += 1
            self.session_stats['last_category'] = state.get('category')
            
            # Format output
            return {
                **format_final_output(state),
                'session_stats': self.session_stats
            }
            
        except Exception as e:
            return {
                'diagnosis': f"Error processing request: {str(e)}",
                'category': 'error',
                'ward': 'error',
                'original_symptoms': symptoms,
                'session_stats': self.session_stats
            }
    
    def reset_session(self) -> None:
        """Clear consultation history"""
        self.session_stats = {
            'total_consultations': 0,
            'last_category': None
        }