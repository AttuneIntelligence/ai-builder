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

sys.path.append('/workspace/ai-builder/src')
from bin.utilities import *

class OpenAI_Instruct:
    def __init__(self,
                 builder):
        self.builder = builder
        self.client = OpenAI()

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def text_completion(self, 
                        question=None,
                        system_prompt=None):
        timer = Timer()
        
        ### CREATE MESSAGES
        if question == None:
            question = self.builder.question
        messages = self.builder.ContextEngineering.instruct_prompt_template(question, system_prompt=system_prompt)
        if self.builder.verbose:
            for message in messages:
                pretty_print(message)

        ### GENERATE RESPONSE
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.builder.gpt_model
        )
        response_message = {
            "role": "assistant",
            "content": response.choices[0].message.content
        }
        if self.builder.verbose:
            pretty_print(response_message)
        messages.append(response_message)
        return messages

