import json
import time
import requests
import sys

sys.path.append('/workspace/ai-builder/src')
from bin.utilities import *

class LLaVA_Vision:
    def __init__(self,
                 assistant):
        self.assistant = assistant
        
        ### RUNPOD CONNECTION
        self.runpod_port = "5000"
        self.model_path = f"https://{self.assistant.vision_runpod_id}-{self.runpod_port}.proxy.runpod.net"
        self.max_tokens = 512
        self.temperature = 0.2

    def llm_vision(self, 
                   question, 
                   image_path,
                   temperature=0.2):
        ### SEND TO RUNPOD LLAVA MODEL
        payload = {
            'model_path': self.assistant.vision_model_name,
            'image_base64': self.assistant.Utilities.encode_image_to_base64(image_path),
            'prompt': f"{question}\nYou should be descript, precise, and comprehensive in your response.",
            'temperature': temperature,
            'max_new_tokens': self.assistant.max_tokens
        }
        timer = Timer()
        r = requests.post(
            f'{self.model_path}/inference',
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

