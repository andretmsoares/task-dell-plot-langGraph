from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from config import ENDPOINT, MODEL_NAME, TOKEN

client = ChatCompletionsClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(TOKEN),
)

def call_llama(prompt: str) -> str:
    # print(f"MODEL_NAME: {MODEL_NAME}")
    # print(f"ENDPOINT: {ENDPOINT}")
    # print(f"TOKEN: {TOKEN}")
    try:
        response = client.complete(
            model=MODEL_NAME,
            messages=[
                SystemMessage(content="Responda sempre de forma curta, em 1 frase."),
                UserMessage(content=prompt),
            ],
            temperature=0.7,
            max_tokens=100,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"[Erro LLM] {str(e)}"