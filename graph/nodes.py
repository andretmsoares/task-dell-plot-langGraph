from .state import FlowState
from llm import call_llama

def classify_node(state: FlowState) -> FlowState:
    path = state.get("execution_path", []) + ["classify"]
    logs = state.get("llm_logs", []).copy()

    v = state["value"]
    complexity = "baixo" if v < 50 else "alto"
    
    answer = call_llama(
        f"O valor {v} é {'baixo (< 50)' if complexity == 'baixo' else 'alto (>= 50)'}. Confirme em 1 frase."
    )
    # answer = "teste-classify"
    
    logs.append(f"classify -> {answer}")

    return {**state, "complexity": complexity, "result": answer, "execution_path": path, "llm_logs": logs}


def simple_process(state: FlowState) -> FlowState:
    path = state["execution_path"] + ["simple_process"]
    logs = state.get("llm_logs", []).copy()
    
    answer = call_llama(f"Valor {state['value']} é baixo. Dê 1 dica rápida de otimização.")
    # answer = "teste-simple-process"
    logs.append(f"simple_process -> {answer}")

    return {**state, "result": answer, "execution_path": path, "llm_logs": logs}


def complex_process(state: FlowState) -> FlowState:
    path = state["execution_path"] + ["complex_process"]
    logs = state.get("llm_logs", []).copy()

    answer = call_llama(f"Valor {state['value']} requer análise complexa. Descreva em 1 frase.")
    # answer = "teste-complex-process"
    logs.append(f"complex_process -> {answer}")

    return {**state, "result": answer, "execution_path": path, "llm_logs": logs}


def call_tool(state: FlowState) -> FlowState:
    path = state["execution_path"] + ["call_tool"]
    logs = state.get("llm_logs", []).copy()

    answer = call_llama(f"Simule chamada de ferramenta para valor par {state['value']}. 1 frase.")
    # answer = "teste-call-tool"
    logs.append(f"call_tool -> {answer}")

    return {**state, "result": answer, "execution_path": path, "llm_logs": logs}


def retry(state: FlowState) -> FlowState:
    path = state["execution_path"] + ["retry"]
    logs = state.get("llm_logs", []).copy()

    answer = call_llama(f"Valor ímpar {state['value']} acionou retry. Explique em 1 frase.")
    # answer = "teste-retry"
    logs.append(f"retry -> {answer}")

    return {**state, "result": answer, "execution_path": path, "llm_logs": logs}