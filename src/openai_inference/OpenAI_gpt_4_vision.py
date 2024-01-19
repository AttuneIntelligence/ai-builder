import base64
import sys
from openai import OpenAI
import requests
from math import ceil
import math
from PIL import Image
from io import BytesIO

sys.path.append('/workspace/ai-builder/src')
from bin.utilities import *

class OpenAI_Vision:
    def __init__(self,
                 assistant):
        self.assistant = assistant

    def vision_completion(self,
                          question, 
                          image_path):
        ### SETUP API CALL
        timer = Timer()
        client = OpenAI()
        prompt = f"{question}\nYou should be descript, precise, and comprehensive in your response."
        b64_image = self.assistant.Utilities.encode_image_to_base64(image_path)

        try:
            ### ATTEMPT THE API CALL
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.assistant.OPENAI_API_KEY}"
            }
            payload = {
                "model": self.assistant.gpt_vision_model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
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
                "max_tokens": self.assistant.max_tokens
            }
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            image_description = response.json()["choices"][0]["message"]["content"]

            ### TRACK COST
            time_taken = timer.get_elapsed_time()
            vision_cost = self.calculate_vision_pricing(b64_image)
            print(f'Total time taken for OpenAI API call: {time_taken} seconds')
            print(f'Total cost for GPT-Vision API call: ${vision_cost}')
            return image_description
        
        except Exception as e:
            if "Rate limit reached" in str(e):
                print("Rate Limited by GPT-4-vision!")
                return None
            else:
                print(f"Error running GPT-4-vision: {str(e)}")
                return None

    def calculate_vision_pricing(self, 
                                 base64_image_data):
        ### CONSTANTS
        TILE_SIZE = 512
        BASE_TOKENS = 85
        TOKENS_PER_TILE = 170
        PRICE_PER_1K_TOKENS = 0.01

        ### DECODE BASE64 IMAGE DATA
        image_bytes = base64.b64decode(base64_image_data)
        image = Image.open(BytesIO(image_bytes))
        width, height = image.size

        ### NUMBER OF TILES NEEDED
        tiles_x = math.ceil(width / TILE_SIZE)
        tiles_y = math.ceil(height / TILE_SIZE)
        total_tiles = tiles_x * tiles_y

        ### TOTAL TOKENS
        tile_tokens = total_tiles * TOKENS_PER_TILE
        total_tokens = BASE_TOKENS + tile_tokens

        ### TOTAL COST
        total_price = (total_tokens / 1000) * PRICE_PER_1K_TOKENS

        return total_price