from typing import TypedDict, List

class FlowState(TypedDict):
    value: int
    complexity: str
    result: str
    execution_path: List[str]
    llm_logs: List[str]