import os
from dotenv import load_dotenv

def set_keys(builder):
    ### LOOK FOR .ENV
    try:
        load_dotenv()
    except:
        pass

    ### SET KEYS
    builder.HUGGING_FACE_HUB_TOKEN = os.getenv("HUGGING_FACE_HUB_TOKEN")
    builder.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
