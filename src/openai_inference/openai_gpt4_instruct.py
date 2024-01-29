import json
import time
import requests
import sys
import os
import subprocess
from openai import OpenAI
import importlib
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
import tiktoken

sys.path.append('/workspace/ai-builder/src')
from bin.utilities import *

class OpenAI_Instruct:
    def __init__(self,
                 builder,
                 model_config):
        self.builder = builder
        self.model_config = model_config
        self.client = OpenAI()
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    # @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def ask(self, 
            question,
            system_prompt=None):
        timer = Timer()
        messages = self.builder.ContextEngineering.instruct_prompt_template(question, system_prompt=system_prompt)
        if self.builder.verbose:
            for message in messages:
                lab_print(message)

        ### GENERATE RESPONSE
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model_config["model_name"]
        )
        response_message = {
            "role": "assistant",
            "content": response.choices[0].message.content
        }
        if self.builder.verbose:
            lab_print(response_message)
        messages.append(response_message)

        ### TRACK COMPLETION METADATA
        time_taken = timer.get_elapsed_time()
        tokens_generated = len(self.tokenizer.encode(text_response))
        tokens_per_second = tokens_generated / time_taken if time_taken > 0 else 0
        print(f"Total Time Taken: {time_taken:.2f} seconds")
        print(f"Tokens per Second: {tokens_per_second:.2f}")
        return messages

