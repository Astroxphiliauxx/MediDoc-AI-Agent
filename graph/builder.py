from langgraph.graph import StateGraph, END
from core.state import AgentState
from nodes.classifications import classify_symptoms  # Fixed import
from nodes.departments.departmentss import department_node  # Fixed import
from nodes.input_output import get_symptoms

def build_medical_graph():
    """Constructs and compiles the medical diagnosis workflow graph"""
    
    builder = StateGraph(AgentState)
    
    # --- Add Nodes ---
    builder.add_node("get_symptoms", get_symptoms)
    builder.add_node("classify_symptoms", classify_symptoms)
    
    # Department nodes configuration
    departments = {
        "hematology": {
            "node_name": "hematology_department",
            "key": "hematology"
        },
        "nutrition": {
            "node_name": "nutrition_department", 
            "key": "nutrition"
        },
        "immunology": {
            "node_name": "immunology_department",
            "key": "immunology"
        },
        "geriatrics": {
            "node_name": "geriatrics_department",
            "key": "geriatrics"
        },
        "general_medicine": {
            "node_name": "general_medicine_department",
            "key": "general_medicine"
        },
        "infectious_diseases": {
            "node_name": "infectious_diseases_department",
            "key": "infectious_diseases"
        }
    }
    
    # Add department nodes
    for dept in departments.values():
        builder.add_node(
            dept["node_name"],
            lambda state, key=dept["key"]: department_node(state, key)
        )

    # --- Define Workflow ---
    builder.set_entry_point("get_symptoms")
    builder.add_edge("get_symptoms", "classify_symptoms")
    
    # Conditional routing
    builder.add_conditional_edges(
        "classify_symptoms",
        lambda state: symptom_router(state),
        {dept["key"]: dept["node_name"] for dept in departments.values()}
    )
    
    # Connect all departments to END
    for dept in departments.values():
        builder.add_edge(dept["node_name"], END)

    return builder.compile()

def symptom_router(state: AgentState) -> str:
   
    # Validate state
    if not state.get("category") or not state.get("ward"):
        return "general_medicine"  # Default fallback
    
    category = state["category"].lower()
    ward = state["ward"].lower()
    
    if "blood" in category and "icu" in ward:
        return "hematology"
    elif "deficiency" in category:
        return "nutrition"
    elif "allerg" in category:  # Matches allergy/allergies
        return "immunology"
    elif "degenerative" in category:
        return "geriatrics"
    elif "infectious" in category:
        return "infectious_diseases"
    
    return "general_medicine"