import time
import base64
import json
from termcolor import colored
from IPython.display import Markdown, display
import requests
import os, sys
import importlib.util
import pkgutil
import tiktoken
from transformers import AutoTokenizer
from PIL import Image as PIL_Image
from io import BytesIO
from math import ceil
import math

class Utilities:
    def __init__(self,
                 builder):
        self.builder = builder
            
    ###################
    ### API TESTING ###
    ###################
    def test_api_up(self,
                    url):
        ### TEST RUNPOD API STATUS
        test_payload = json.dumps({"inputs": "Test", "parameters": {"max_new_tokens": 1, "do_sample": False}})
    
        try:
            response = requests.post(url, data=test_payload, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                # print("API is up and running.")
                return True
            else:
                # print(f"API is not responding as expected. Status Code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            # print(f"Error while checking API status: {e}")
            return False
            
    ####################
    ### VISION TOOLS ###
    ####################
    def encode_image_to_base64(self,
                               image_path):
        with open(image_path, 'rb') as image_file:
            return str(base64.b64encode(image_file.read()).decode('utf-8'))

    ##########################
    ### METADATA FUNCTIONS ###
    ##########################
    def compile_metadata(self,
                         ingress,
                         egress,
                         time_taken,
                         model_name,
                         b64_image=None):
        ### CALCULATE COST
        if "gpt" in model_name:
            tokenizer = tiktoken.get_encoding("cl100k_base")
            cost = self.openai_costs(ingress, egress, model_name, b64_image)
        else:
            tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            cost = None

        ### TOKEN METRICS
        ingress_tokens = sum([len(tokenizer.encode(message["content"])) for message in ingress])
        egress_tokens = len(tokenizer.encode(egress))
        tokens_per_second = egress_tokens / time_taken if time_taken > 0 else 0
        if self.builder.verbose:
            print(f"Total Time Taken: {time_taken:.2f} seconds")
            print(f"Tokens per Second: {tokens_per_second:.2f}")
            if cost:
                print(f"Cost ($): {cost:.3f}")
        return {
            "time (s)": time_taken,
            "ingress_tokens": ingress_tokens,
            "egress_tokens": egress_tokens,
            "tokens_per_second": round(tokens_per_second, 2),
            "cost ($)": cost,
            "model": model_name
        }
        
    def openai_costs(self,
                     ingress,
                     egress,
                     model,
                     b64_image):
        tokenizer = tiktoken.get_encoding("cl100k_base")
        
        ### INGRESS IS MESSAGE LIST / EGRESS IS RESPONSE STRING
        ingress_tokens = sum([len(tokenizer.encode(message["content"])) for message in ingress])
        egress_tokens = len(tokenizer.encode(egress))
                            
        if model in ["gpt-4-0125-preview", "gpt-4-1106-preview", "gpt-4-vision-preview"]:
            prompt_cost = (ingress_tokens / 1000)*0.01
            response_cost = (egress_tokens / 1000)*0.03

        elif model in ["gpt-4"]:
            prompt_cost = (egress_tokens / 1000)*0.03
            response_cost = (egress_tokens / 1000)*0.06

        elif model in ["gpt-4-32k"]:
            prompt_cost = (egress_tokens / 1000)*0.06
            response_cost = (egress_tokens / 1000)*0.12

        elif model in ["gpt-3.5-turbo-1106"]:
            prompt_cost = (egress_tokens / 1000)*0.0010
            response_cost = (egress_tokens / 1000)*0.0020

        elif model in ["gpt-3.5-turbo-instruct"]:
            prompt_cost = (egress_tokens / 1000)*0.0015
            response_cost = (egress_tokens / 1000)*0.0020

        ### ADD VISION COST IF NECESSARY
        if b64_image:
            image_cost = self.calculate_vision_pricing(b64_image)
        else:
            image_cost = 0
            
        return round(prompt_cost+response_cost+image_cost, 4)

    def calculate_vision_pricing(self, 
                                 base64_image_data):
        ### CONSTANTS
        TILE_SIZE = 512
        BASE_TOKENS = 85
        TOKENS_PER_TILE = 170
        PRICE_PER_1K_TOKENS = 0.01

        ### DECODE BASE64 IMAGE DATA
        image_bytes = base64.b64decode(base64_image_data)
        image = PIL_Image.open(BytesIO(image_bytes))
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


#######################
### UNIVERSAL TIMER ###
#######################
class Timer:
    def __init__(self):
        self.start = time.time()

    def restart(self):
        self.start = time.time()

    def get_elapsed_time(self):
        end = time.time()
        return round(end - self.start, 1)

#########################
### PRINT IN MARKDOWN ###
#########################
def printmd(string):
    display(Markdown(string))

def lab_print(message):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "tool": "magenta",
        "function": "magenta",
    }
    color = role_to_color.get(message["role"], "black")
    
    ### BUILD HTML WITH COLOR
    content = message.get("content", "")
    if message["role"] == "assistant" and message.get("function_call"):
        content = message["function_call"]
    content = content.replace("\n", "<br>")
    header_content = f"<span style='color: {color};'><strong>{message['role'].upper()}</strong></span>"
    html_content = f"<span style='color: {color};'>{content}</span>"
    
    ### DISPLAY AS COLORED MARKDOWN
    display(Markdown(header_content))
    display(Markdown(html_content))

def pretty_print(message):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "tool": "magenta",
        "function": "magenta",
    }
    if message["role"] == "system":
        print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
    elif message["role"] == "user":
        print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
    elif message["role"] == "assistant" and message.get("function_call"):
        print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
    elif message["role"] == "assistant" and not message.get("function_call"):
        print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
    elif message["role"] == "tool" or message["role"] == "function":
        print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))