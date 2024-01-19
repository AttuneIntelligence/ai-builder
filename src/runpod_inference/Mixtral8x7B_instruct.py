import json
import time
import requests
import sys
from transformers import AutoTokenizer
import os
import subprocess
from tenacity import retry, wait_random_exponential, stop_after_attempt

sys.path.append('/workspace/ai-builder/src')
from bin.utilities import *

class Mixtral7x8B_Instruct:
    def __init__(self,
                 assistant):
        ### SETUP LLAVA PARAMETERS
        self.assistant = assistant
        self.runpod_port = "8080"
        self.model_path = f"https://{self.assistant.instruct_runpod_id}-{self.runpod_port}.proxy.runpod.net"
        self.tokenizer = AutoTokenizer.from_pretrained(self.assistant.instruct_model_name, trust_remote_code=True)

    def format_messages(self,
                        messages):
        B_SYS = "<<SYS>>\n"
        E_SYS = "\n<</SYS>>\n\n"
        B_INST = "[INST] "
        E_INST = " [/INST]\n\n"
        BOS_token = "<s>"
        EOS_token = "</s>"

        formatted_string = ''
        formatted_string += BOS_token
        formatted_string += B_INST
    
        for message in messages:
            if message['role'] == 'system':
                formatted_string += B_SYS
                formatted_string += message['content']
                formatted_string += E_SYS
            elif message['role'] in ['user']:
                formatted_string += message['content']
                formatted_string += E_INST
            elif message['role'] in ['assistant']:
                formatted_string += message['content']
                formatted_string += EOS_token
                formatted_string += BOS_token
                formatted_string += B_INST
        return formatted_string
        
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def text_completion(self, 
                        question=None,
                        system_prompt=None):
        timer = Timer()
        
        ### CREATE MESSAGES
        if question == None:
            question = self.assistant.question
        messages = self.assistant.ContextEngineering.instruct_prompt_template(question, system_prompt=system_prompt)

        ### FORMAT INPUT
        formatted_messages = self.format_messages(messages)
        json_payload = json.dumps({
            "inputs": formatted_messages, 
            "parameters": {
                "max_new_tokens": self.assistant.max_tokens, 
                "do_sample": False
            }
        })

        ### SEND TO RUNPOD MIXTRAL 7x8B
        try:
            curl_command = f"""
            curl -s {self.model_path}/generate \
                -X POST \
                -d '{json_payload}' \
                -H 'Content-Type: application/json'
            """
            response = subprocess.run(curl_command, shell=True, check=True, stdout=subprocess.PIPE)
            time_taken = timer.get_elapsed_time()

            ### DECODE RESPONSE
            response = response.stdout.decode()
            text_response = json.loads(response).get("generated_text", "No generated text found")
            messages.append({"role": "assistant", "content": text_response})

            ### TRACK COMPLETION METADATA
            tokens_generated = len(response)/4 
            tokens_per_second = tokens_generated / time_taken if time_taken > 0 else 0
            print(f"Total Time Taken: {time_taken:.2f} seconds")
            print(f"Tokens per Second: {tokens_per_second:.2f}")
            self.assistant.Utilities.pretty_print_conversation(messages)
            return text_response

        ### OR RETURN ERROR
        except subprocess.CalledProcessError as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return None