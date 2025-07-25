from core.state import AgentState
from typing import Literal

def department_node(state: AgentState, department: Literal[
    "hematology", 
    "nutrition", 
    "immunology",
    "geriatrics",
    "general_medicine",
    "infectious_diseases"
]) -> AgentState:
    
    responses = {
        "hematology": (
            "\nLooks like your blood needs to be purified, just like your mind. "
            "\nYou have been referred to the Hematology department."
        ),
        "nutrition": (
            "\nYou need to eat more greens and less junk food. "
            "\nReferred to Nutrition and Dietetics department."
        ),
        "immunology": (
            "\nAhh, I'm surprised at how weak your immune system is. "
            "\nReferred to Immunology department."
        ),
        "geriatrics": (
            "\nWell, our GAS department would take care of you. "
            "\nReferred to Geriatrics department."
        ),
        "general_medicine": (
            "\nDon't worry much! Maybe something minor! "
            "\nReferred to General Medicine department."
        ),
        "infectious_diseases": (
            "\nIt seems you may have an infectious disease. "
            "\nReferred to Infectious Diseases department."
        )
    }
    
    return {
        "answer": responses[department],
        "department": department,
        **state 
    }