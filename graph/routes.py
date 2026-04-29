from typing import Literal
from .state import FlowState

def route_complexity(state: FlowState) -> Literal["simple_process", "complex_process"]:
    return "simple_process" if state["complexity"] == "baixo" else "complex_process"

def route_parity(state: FlowState) -> Literal["call_tool", "retry"]:
    return "call_tool" if state["value"] % 2 == 0 else "retry"