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

class Mixtral8x7B_Instruct:
    def __init__(self,
                 builder,
                 model_config):
        self.builder = builder
        self.model_config = model_config
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_config["model_name"], trust_remote_code=True)
        
    # @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def ask(self, 
            question,
            system_prompt=None):
        timer = Timer()
        
        ### CREATE MESSAGES
        messages = self.builder.ContextEngineering.instruct_prompt_template(question, system_prompt=system_prompt)
        if self.builder.verbose:
            for message in messages:
                lab_print(message)
                
        ### FORMAT INPUT
        formatted_messages = self.format_messages(messages)
        
        json_payload = json.dumps({
            "inputs": formatted_messages, 
            "parameters": {
                "max_new_tokens": self.builder.max_tokens, 
                "do_sample": False
            }
        })

        ### SEND TO RUNPOD MIXTRAL 8x7B
        if self.builder.streaming:
            endpoint = "/generate_stream"
        else:
            endpoint = "/generate"
        try:
            curl_command = f"""
            curl -s {self.model_config['model_url']}{endpoint} \
                -X POST \
                -d '{json_payload}' \
                -H 'Content-Type: application/json'
            """
            response = subprocess.run(curl_command, shell=True, check=True, stdout=subprocess.PIPE)
            time_taken = timer.get_elapsed_time()
    
            ### DECODE RESPONSE
            response = response.stdout.decode()
            text_response = json.loads(response).get("generated_text", "No generated text found")
            response_message = {"role": "assistant", "content": text_response}
            messages.append(response_message)
            if self.builder.verbose:
                lab_print(response_message)
    
    
            ### TRACK COMPLETION METADATA
            time_taken = timer.get_elapsed_time()
            metadata = self.builder.Utilities.compile_metadata(
                ingress=messages,
                egress=text_response, 
                time_taken=time_taken, 
                model_name=self.model_config["model_name"]
            )
            return messages, metadata

        ## OR RETURN ERROR
        except subprocess.CalledProcessError as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return None

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
