import json
import time
import requests
import sys
import os

sys.path.append('/workspace/ai-builder/src')
from bin.utilities import *

class ContextEngineering:
    def __init__(self,
                 builder):
        self.builder = builder
        self.prompt_templates_dir = f"{self.builder.home}src/chat_templates/templates/"

    def instruct_prompt_template(self,
                                 question,
                                 system_prompt=None):
        ### SYSTEM PROMPT
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            with open(f"{self.prompt_templates_dir}instruct_system_template.txt", 'r') as file:
                system_prompt = file.read()
            messages.append({"role": "system", "content": system_prompt})

        ### RETURN WITH QUESTION
        messages.append({"role": "user", "content": question})
        return messages

    def summarize_prompt_template(self,
                                  question,
                                  system_prompt=None):
        ### SYSTEM PROMPT
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            with open(f"{self.prompt_templates_dir}summarize_system_template.txt", 'r') as file:
                system_prompt = file.read()
            messages.append({"role": "system", "content": system_prompt})

        ### RETURN WITH QUESTION
        messages.append({"role": "user", "content": question})
        return messages


