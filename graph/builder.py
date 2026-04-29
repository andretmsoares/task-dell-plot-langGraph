from langgraph.graph import StateGraph, START, END
from .state import FlowState
from .nodes import *
from .routes import *

def build_graph():
    g = StateGraph(FlowState)

    g.add_node("classify", classify_node)
    g.add_node("simple_process", simple_process)
    g.add_node("complex_process", complex_process)
    g.add_node("call_tool", call_tool)
    g.add_node("retry", retry)

    g.add_edge(START, "classify")

    g.add_conditional_edges("classify", route_complexity, {
        "simple_process": "simple_process",
        "complex_process": "complex_process"
    })

    g.add_edge("simple_process", END)

    g.add_conditional_edges("complex_process", route_parity, {
        "call_tool": "call_tool",
        "retry": "retry"
    })

    g.add_edge("call_tool", END)
    g.add_edge("retry", END)

    return g.compile()