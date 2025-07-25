from llm.setup import get_llm
from llm.prompts import CLASSIFICATION_PROMPT
from core.state import AgentState
from typing import Dict, Any

def classify_symptoms(state: AgentState) -> AgentState:
   
    llm = get_llm()
    
    try:
        
        response = llm.invoke(
            CLASSIFICATION_PROMPT.format(symptoms=state['symptoms'])
        )
        response_text = response.content

       
        category = "Unknown"
        ward = "Unknown"
        
        if "Category:" in response_text:
            category = response_text.split("Category:")[1].split("\n")[0].strip()
        if "Ward:" in response_text:
            ward = response_text.split("Ward:")[1].split("\n")[0].strip()

        return {
            **state,
            "response": response_text,
            "category": category,
            "ward": ward,
            "answer": f"Classification complete:\nCategory: {category}\nWard: {ward}"
        }

    except Exception as e:
        print(f"Classification error: {str(e)}")
        return {
            **state,
            "response": str(e),
            "category": "Error",
            "ward": "Error",
            "answer": "Failed to classify symptoms. Please try again."
        }