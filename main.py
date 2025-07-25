# import os
# from langgraph.graph import StateGraph, END
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_google_genai import HarmBlockThreshold, HarmCategory
# from langchain_core.messages import HumanMessage
# from dotenv import load_dotenv
# from typing import TypedDict, Annotated
# import operator
# import time



# # Using a TypedDict is a best practice for defining state in LangGraph
# class AgentState(TypedDict):
#     symptoms: str
#     response: str
#     category: str
#     ward: str
#     answer: str



# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")


# # LLM Initialization
# llm = ChatGoogleGenerativeAI(
#     model="models/gemini-1.5-flash",
#     api_key=api_key,
#     temperature=0.5,
#     safety_settings={
#         HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,

#     }
# )


# #Node Functions

# def get_symptoms(state: AgentState) -> AgentState:
    
#     symptoms = input("Welcome to the AI Agent, please enter your symptoms: ")
#     return {"symptoms": symptoms}


# def classify_symptoms(state: AgentState) -> AgentState:
#     print("-> Classifying symptoms...")
#     time.sleep(3)
#     prompt = (
#         "You are a medical expert. Classify the following symptoms into one of the following categories: 'Blood Diseases', 'Deficiency Diseases', 'Allergies', 'Degenerative Diseases', 'Non-infectious Diseases', 'Infectious Diseases'.\n"
#         "On the basis of the symptoms provided, classify them into one of the wards in hospital: "
#         "'general ward', 'emergency ward', 'ICU', 'maternity ward', 'pediatric ward', 'orthopedic ward', 'ENT ward', 'ophthalmology ward', 'dermatology ward', 'neurology ward'.\n"
#         f"Symptoms: {state['symptoms']}\n\n"
#         "Respond with the category and ward in the following format ONLY:\n"
#         "Category: <category>\n"
#         "Ward: <ward>"
#     )
#     try:
#         response = llm.invoke([HumanMessage(content=prompt)])
#         response_text = response.content
#         # print(f"LLM Response:\n{response_text}")

        
#         category = response_text.split("Category:")[1].split("\n")[0].strip()
#         ward = response_text.split("Ward:")[1].split("\n")[0].strip()

#         return {
#             "response": response_text,
#             "category": category,
#             "ward": ward,
#             "answer": f"After analysing your symptoms, I have classified them as follows:\nCategory: {category}\nWard: {ward}\n"
#         }
#     except (IndexError, AttributeError) as e:
#         print(f"Error parsing LLM response: {e}")
#         # Handle cases where the LLM response is not in the expected format
#         return {
#             "response": "Could not classify symptoms based on the response.",
#             "category": "Unknown",
#             "ward": "Unknown",
#             "answer": "I was unable to classify your symptoms. Please try rephrasing them."
#         }


# def hematology_department(state: AgentState) -> AgentState:
#     """Node for the Hematology department."""
#     return {"answer": "\nLooks like your blood needs to be purified, just like your mind. \nYou have been referred to the Hematology department for further evaluation and treatment."}

# def nutrition_department(state: AgentState) -> AgentState:
#     """Node for the Nutrition and Dietetics department."""
#     return {"answer": "\nYou need to eat more greens and less junk food. \nYou have been referred to the Nutrition and Dietetics department for further evaluation and treatment."}

# def immunology_department(state: AgentState) -> AgentState:
#     """Node for the Immunology department."""
#     return {"answer": "\nAhh, I'm surprised that how weak your immune system is. \nYou have been referred to the Immunology department for further evaluation and treatment."}

# def geriatrics_department(state: AgentState) -> AgentState:
#     """Node for the Geriatrics department."""
#     return {"answer": "\nWell, our GAS department would take care of you. \nYou have been referred to the Geriatrics department for further evaluation and treatment."}

# def general_medicine_department(state: AgentState) -> AgentState:
#     """Node for the General Medicine department."""
#     return {"answer": "\nDon't worry much! Maybe something minor! You have been referred to the General Medicine department for further evaluation and treatment."}

# def infectious_diseases_department(state: AgentState) -> AgentState:
#     """Node for the Infectious Diseases department."""
#     return {"answer": "\nIt seems you may have an infectious disease. \nYou have been referred to the Infectious Diseases department for further evaluation and treatment."}


# #Conditional Router

# def symptom_router(state: AgentState) -> str:
#     """
#     This function inspects the state and returns a string key that
#     matches a key in the conditional edge mapping. It does NOT modify the state.
#     """
#     print("-> Routing based on classification...")
#     category = state["category"].lower()
#     ward = state["ward"].lower()

#     if "blood diseases" in category and "icu" in ward:
#         return "Hematology"
#     elif "deficiency diseases" in category:
#         return "Nutrition and Dietetics"
#     elif "allergies" in category:
#         return "Immunology"
#     elif "degenerative diseases" in category:
#         return "Geriatrics"
#     elif "infectious diseases" in category:
#         return "Infectious Diseases"
#     else:
#         # Default for all other cases
#         return "General Medicine"


# # --- Build the Graph ---

# builder = StateGraph(AgentState)

# builder.add_node("get_symptoms", get_symptoms)
# builder.add_node("classify_symptoms", classify_symptoms)
# builder.add_node("hematology_department", hematology_department)
# builder.add_node("nutrition_department", nutrition_department)
# builder.add_node("immunology_department", immunology_department)
# builder.add_node("geriatrics_department", geriatrics_department)
# builder.add_node("general_medicine_department", general_medicine_department)
# builder.add_node("infectious_diseases_department", infectious_diseases_department) # Added new node

# # Define the graph's flow
# builder.set_entry_point("get_symptoms")
# builder.add_edge("get_symptoms", "classify_symptoms")

# # Add the conditional routing
# builder.add_conditional_edges(
#     "classify_symptoms",
#     symptom_router,
#     {
#         "Hematology": "hematology_department",
#         "Nutrition and Dietetics": "nutrition_department",
#         "Immunology": "immunology_department",
#         "Geriatrics": "geriatrics_department",
#         "Infectious Diseases": "infectious_diseases_department",
#         "General Medicine": "general_medicine_department"
#     }
# )

# # Connect the final nodes to the end state
# builder.add_edge("hematology_department", END)
# builder.add_edge("nutrition_department", END)
# builder.add_edge("immunology_department", END)
# builder.add_edge("geriatrics_department", END)
# builder.add_edge("general_medicine_department", END)
# builder.add_edge("infectious_diseases_department", END)

# # Compile the graph
# graph = builder.compile()


# if __name__ == "__main__":
    
#     initial_state = {
#         "symptoms": "",
#         "response": "",
#         "category": "",
#         "ward": "",
#         "answer": ""  # Explicitly initialize answer
#     }

#     final_state = graph.invoke(initial_state)

#     print("\n AI Agent:")
#     print(final_state.get("answer", "No final answer was generated."))
    
  

#!/usr/bin/env python3


import sys
import time
from typing import Dict, Any
from dotenv import load_dotenv
from langgraph.graph import END
from graph.builder import build_medical_graph
from nodes.input_output import get_symptoms, format_final_output


MAX_ATTEMPTS = 3
VERSION = "1.0.0"

def display_welcome() -> None:
    
    print("\n" + "=" * 60)
    print(f" MEDICAL DIAGNOSIS AI AGENT (v{VERSION}) ".center(60, "="))
    print("=" * 60)
    print("\nNote: This AI assistant provides preliminary health guidance")
    print("and should NOT replace professional medical advice.\n")

def initialize_system() -> Any:
    
    load_dotenv() 
    
    try:
        medical_graph = build_medical_graph()
        time.sleep(1)
        print("\nInitializing system...")
        val = 3
        for i in range(val):
            print(f"{val-i}...")
            time.sleep(1)
        print(" System initialized successfully...")
        return medical_graph
    
    except Exception as e:
        print(f" Failed to initialize system: {str(e)}")
        sys.exit(1)

def main_loop(graph: Any) -> None:
   
    attempt = 0
    
    while attempt < MAX_ATTEMPTS:
        try:
           
            final_state = graph.invoke({})
            
           
            results = format_final_output(final_state)
            print("\n" + "=" * 50)
            print(" DIAGNOSIS RESULTS ".center(50, "="))
            print("=" * 50)
            print(results.get("ascii_art", ""))
            print(results["diagnosis"])
            print("Category:", results["category"])
            print("Ward:", results["ward"])
            print("Answer:", results["answer"])
            print("Session Stats:", results.get("session_stats", {}))
            print("\nTimestamp:", results["timestamp"])
            print("Duration:", results["duration"], "seconds")
            print("Consultation Count:", results["consultation_count"])
            
            print("\nOriginal symptoms:", results["original_symptoms"])
            print("=" * 50)
            
            # Prompt for next action
            choice = input("\nPress Enter to continue or 'q' to quit: ").strip().lower()
            if choice == 'q':
                break
                
            attempt = 0  # Reset on success
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            attempt += 1
            print(f"\n Error occurred (attempt {attempt}/{MAX_ATTEMPTS}): {str(e)}")
            if attempt >= MAX_ATTEMPTS:
                print("Maximum attempts reached. Please try again later.")
                break

def graceful_exit() -> None:
    """Handle system shutdown"""
    print("\n" + "=" * 50)
    print(" Thank you for using Medical Diagnosis AI ".center(50, "="))
    print("=" * 50 + "\n")
    sys.exit(0)

if __name__ == "__main__":
    display_welcome()
    medical_graph = initialize_system()
    main_loop(medical_graph)
    graceful_exit()
