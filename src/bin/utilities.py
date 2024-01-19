import time
import base64
import json
from termcolor import colored
from IPython.display import Markdown, display
import requests

class Utilities:
    def __init__(self,
                 assistant):
        self.assistant = assistant
            
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