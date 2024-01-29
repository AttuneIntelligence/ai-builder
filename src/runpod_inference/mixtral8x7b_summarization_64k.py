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

class Mixtral7x8B_Summarization:
    def __init__(self,
                 builder):
        self.builder = builder

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def ask(self, 
            content,
            system_prompt=None):
        timer = Timer()
        
        ### CREATE MESSAGES
        if question == None:
            question = self.builder.question
        messages = self.builder.ContextEngineering.summarize_prompt_template(question, system_prompt=system_prompt)
        
        ### FORMAT INPUT
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, 
            trust_remote_code=True
        )
        formatted_messages = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        json_payload = json.dumps({
            "inputs": formatted_messages, 
            "parameters": {
                "max_new_tokens": self.assistant.max_tokens, 
                "do_sample": False
            }
        })

        ### SEND TO LONG-CONTEXT MIXTRAL
        try:
            curl_command = f"""
            curl -s {self.model_path} \
                -X POST \
                -d '{json_payload}' \
                -H 'Content-Type: application/json'
            """
            response = subprocess.run(curl_command, shell=True, check=True, stdout=subprocess.PIPE)
            time_taken = timer.get_elapsed_time()

            ### DECODE RESPONSE
            response = response.stdout.decode()
            text_response = json.loads(response)[0].get("generated_text", "No generated text found")
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