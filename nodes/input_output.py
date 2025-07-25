from core.state import AgentState
from typing import Optional, Dict, Any
import sys
import time
import datetime
from llm.prompts import CLASSIFICATION_PROMPT

def get_symptoms(state: Optional[AgentState] = None) -> AgentState:
    
   
    
    while True:
        try:
            symptoms = input("\nPlease describe your symptoms (or type 'help' for examples, 'quit' to exit):\n> ").strip()
            time.sleep(3) 
            if symptoms.lower() == 'quit':
                print("\nThank you for using our service. Take Care!")
                sys.exit(0)
                
            elif symptoms.lower() == 'help':
                show_symptom_examples()
                continue
                
            elif not symptoms:
                print("⚠️ Please enter at least one symptom")
                continue
                
            elif len(symptoms.split()) < 2:
                print("⚠️ For better accuracy, please describe your symptoms in more detail")
                continue
                
            return {
                "symptoms": symptoms,
                "response": "",
                "category": "",
                "ward": "",
                "answer": ""
            }
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            sys.exit(1)

def show_symptom_examples():
    """Displays examples of well-formatted symptom descriptions"""
    examples = [
        "Headache with fever and stiff neck",
        "Chest pain radiating to left arm",
        "Persistent cough with yellow phlegm for 3 weeks",
        "Joint pain and fatigue in mornings",
        "Abdominal pain with diarrhea after eating"
    ]
    
    print("\nExamples of good symptom descriptions:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
        time.sleep(0.5)
    print("\nTip: Include duration, severity, and related symptoms when possible.")

def format_final_output(state: AgentState) -> Dict[str, Any]:
    
    
    department_art = {
        "hematology": r"""
         ____
        /    \
       | BLOOD |
        \____/ 
          ||     Hematology Department
         \||/
          \/
        """,
        "nutrition": r"""
         _______
        / FRUIT \
       | VEGGIES |   Nutrition Clinic
        \_______/
          🥗🥕
        """,
        "immunology": r"""
         ⚕️ 
        /|__|\    Immunology Center
       | ALLERGY |
        \😷🤧/
        """,
        "geriatrics": r"""
         👵🏻👴🏻
        / SILVER \   Geriatrics Care
       |  CARE   |
        \_______/
        """,
        "general_medicine": r"""
         ⚕️ 
        /____\     General Medicine
       |  🩺  |
        \____/
        """,
        "infectious_diseases": r"""
         ☣️ 
        /    \    Infectious Diseases
       | ISOLN |
        \____/
        """,
        "orthopedic": r"""
         🦴
        /|__|\    Orthopedics
       | SPLINT |
        \____/
        """
    }

    # Map categories to departments
    category_map = {
        "blood": "hematology",
        "deficiency": "nutrition",
        "allerg": "immunology",
        "degenerative": "geriatrics",
        "infectious": "infectious_diseases",
        "orthopedic": "orthopedic"
    }

    # Determine department
    dept = "general_medicine"  # default
    category = state.get("category", "").lower()
    for key, value in category_map.items():
        if key in category:
            dept = value
            break

    # Prepare structured output
    return {
        "diagnosis": state.get("answer", "No diagnosis available"),
        "category": state.get("category", "Unknown"),
        "ward": state.get("ward", "Unknown"),
        "original_symptoms": state.get("symptoms", ""),
        "ascii_art": department_art.get(dept, department_art["general_medicine"]),
        "department": dept.upper(),
        "timestamp": datetime.datetime.now().isoformat()
    }