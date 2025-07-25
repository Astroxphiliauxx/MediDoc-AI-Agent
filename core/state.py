from typing import TypedDict

class AgentState(TypedDict):
    symptoms: str
    response: str
    category: str
    ward: str
    answer: str