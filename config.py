import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = "https://models.github.ai/inference"
MODEL_NAME = "meta/Llama-3.3-70B-Instruct"
TOKEN = os.getenv("GITHUB_TOKEN")

OUTPUT_DIR = "./plots"