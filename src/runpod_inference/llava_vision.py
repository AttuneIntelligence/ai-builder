import json
import time
import requests
import sys
from IPython.display import Image, display

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
            system_prompt=None,
            return_messages=False):
        
        ### CREATE PROMPT
        messages = self.builder.ContextEngineering.vision_prompt_template(question, system_prompt=system_prompt)
        b64_image = self.builder.Utilities.encode_image_to_base64(image_path)
        if self.builder.verbose:
            for message in messages:
                lab_print(message)
            display(Image(data=base64.b64decode(b64_image)))
        
        ### SEND TO RUNPOD LLAVA MODEL
        payload = {
            'model_path': "liuhaotian/llava-v1.6-mistral-7b",
            'image_base64': b64_image,
            'prompt': str(messages),
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
            response_message = {
                "role": "assistant",
                "content": text_response
            }
            if self.builder.verbose:
                lab_print(response_message)
            messages.append(response_message)
            
            ### TRACK COMPLETION METADATA
            time_taken = timer.get_elapsed_time()
            metadata = self.builder.Utilities.compile_metadata(
                ingress=messages,
                egress=text_response, 
                time_taken=time_taken, 
                model_name=self.model_config["model_name"],
            )
            if return_messages:
                return messages, metadata
            else:
                return text_response, metadata

        else:
            print(f"Failed to get a valid response from LLaVA, status code: {r.status_code}")
            print(f"Response content: {r.text}")
            return None

    def test_api_up(self,
                    url,
                    model_name):
        ### TEST RUNPOD API STATUS
        test_image="/workspace/ai-builder/assets/images/ai-builder-small.png"
        test_payload = json.dumps({
            'model_path': model_name,
            'image_base64': self.builder.Utilities.encode_image_to_base64(test_image),
            'prompt': "What is this?",
            'temperature': 0.1,
            'max_new_tokens': 30
        })
    
        try:
            response = requests.post(f"{url}/inference", data=test_payload, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                # print("API is up and running.")
                return True
            else:
                # print(f"API is not responding as expected. Status Code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            # print(f"Error while checking API status: {e}")
            return False