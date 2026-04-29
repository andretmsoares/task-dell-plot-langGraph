import os
import datetime
import json

from config import OUTPUT_DIR, TOKEN
from graph.builder import build_graph
from visualization.plot import draw_flow
from utils.summary import generate_summary


ALL_EDGES = [
    ("__start__", "classify", ""),
    ("classify", "simple_process", "baixo"),
    ("classify", "complex_process", "alto"),
    ("simple_process", "__end__", ""),
    ("complex_process", "call_tool", "par"),
    ("complex_process", "retry", "impar"),
    ("call_tool", "__end__", ""),
    ("retry", "__end__", ""),
]

DISPLAY = {
    "__start__": "START", "classify": "CLASSIFY",
    "simple_process": "SIMPLE\nPROCESS", "complex_process": "COMPLEX\nPROCESS",
    "call_tool": "CALL\nTOOL", "retry": "RETRY", "__end__": "END",
}

def run_case(value, scenario):
    graph = build_graph()

    final = graph.invoke({
        "value": value,
        "complexity": "",
        "result": "",
        "execution_path": [],
        "llm_logs": []
    })

    path = final["execution_path"]

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    base_name = f"{scenario}_{value}_{timestamp}".replace(" ", "_")

    png_path = f"{OUTPUT_DIR}/{base_name}.png"

    draw_flow(
        path=path,
        edges=ALL_EDGES,
        out=png_path,
        value=value,
        scenario=scenario,
        display=DISPLAY
    )

    result_json = {
        "cenario": scenario,
        "valor": value,
        "caminho": path,
        "logs": final["llm_logs"],
        "resumo": generate_summary(final["llm_logs"])
    }

    with open(f"{OUTPUT_DIR}/{base_name}.json", "w") as f:
        json.dump(result_json, f, indent=2)


if __name__ == "__main__":
    
    # print(TOKEN)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    run_case(23, "Baixo")
    run_case(84, "Alto Par")
    run_case(77, "Alto Impar")