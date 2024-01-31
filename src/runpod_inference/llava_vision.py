import json
import time
import requests
import sys

sys.path.append('/workspace/ai-builder/src')
from bin.utilities import *

class LLaVA_Vision:
    def __init__(self,
                 builder,
                 model_config):
        self.builder = builder
        self.model_config = model_config

    def ask(self, 
            question, 
            image_path,
            system_prompt=None):
        ### SEND TO RUNPOD LLAVA MODEL
        payload = {
            'model_path': f"https://{runpod_id}-{runpod_port}.proxy.runpod.net",
            'image_base64': self.builder.Utilities.encode_image_to_base64(image_path),
            'prompt': f"{question}",
            'temperature': 0.1,
            'max_new_tokens': self.builder.max_tokens
        }
        timer = Timer()
        r = requests.post(
            f'{self.model_config["model_url"]}/inference',
            json=payload,
        )

        ### HANDLE RESPONSE
        time_taken = timer.get_elapsed_time()
        if r.status_code == 200:
            text_response = r.json()["response"]
            print(f'Total time taken for API call: {time_taken} seconds')
            return text_response
        else:
            print(f"Failed to get a valid response, status code: {r.status_code}")
            print(f"Response content: {r.text}")
            return None

