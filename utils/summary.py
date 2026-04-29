from typing import List
from llm import call_llama

def generate_summary(log_lines: List[str]) -> str:
    log_text = "\n".join(log_lines)

    prompt = f"""
        Analise a execução de um fluxo LangGraph abaixo.

        {log_text}

        Gere um resumo objetivo contendo:
        - Tipo de fluxo executado
        - Caminho seguido
        - Comportamento geral do sistema
        """
    # return "teste-resumo"
    return call_llama(prompt)