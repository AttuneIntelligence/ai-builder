import os

def set_keys(assistant):
    assistant.HUGGING_FACE_HUB_TOKEN = os.getenv("HUGGING_FACE_HUB_TOKEN")
    assistant.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    assistant.SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
