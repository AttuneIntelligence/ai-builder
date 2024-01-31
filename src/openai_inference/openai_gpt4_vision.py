import base64
import sys
from openai import OpenAI
import requests
from math import ceil
import math
from IPython.display import Image, display

sys.path.append('/workspace/ai-builder/src')
from bin.utilities import *

class OpenAI_Vision:
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
        timer = Timer()

        ### CREATE PROMPT
        messages = self.builder.ContextEngineering.vision_prompt_template(question, system_prompt=system_prompt)
        b64_image = self.builder.Utilities.encode_image_to_base64(image_path)
        if self.builder.verbose:
            for message in messages:
                lab_print(message)
            display(Image(data=base64.b64decode(b64_image)))
                
        try:
            ### ATTEMPT THE API CALL
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.builder.OPENAI_API_KEY}"
            }
            payload = {
                "model": self.model_config["model_name"],
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": str(messages)
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{b64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": self.builder.max_tokens
            }
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            text_response = response.json()["choices"][0]["message"]["content"]
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
                b64_image = b64_image
            )
            if return_messages:
                return messages, metadata
            else:
                return text_response, metadata
                
        except Exception as e:
            if "Rate limit reached" in str(e):
                print("Rate Limited by GPT-4-vision!")
                return None
            else:
                print(f"Error running GPT-4-vision: {str(e)}")
                return None

