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

    def instruct_prompt_template(self,
                                 question,
                                 system_prompt=None):
        ### SYSTEM PROMPT
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            with open(f"{self.builder.prompt_templates_dir}instruct_system_template.txt", 'r') as file:
                system_prompt = file.read()
            messages.append({"role": "system", "content": system_prompt})

        ### RETURN WITH QUESTION
        question = question.replace("'", "").replace('"', "")
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
            with open(f"{self.builder.prompt_templates_dir}summarize_system_template.txt", 'r') as file:
                system_prompt = file.read()
            messages.append({"role": "system", "content": system_prompt})

        ### RETURN WITH QUESTION
        question = question.replace("'", "").replace('"', "")
        messages.append({"role": "user", "content": question})
        return messages
        
    def vision_prompt_template(self,
                               question,
                               system_prompt=None):
        ### SYSTEM PROMPT
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            with open(f"{self.builder.prompt_templates_dir}vision_system_template.txt", 'r') as file:
                system_prompt = file.read()
            messages.append({"role": "system", "content": system_prompt})

        ### RETURN WITH QUESTION
        question = question.replace("'", "").replace('"', "")
        messages.append({"role": "user", "content": question})
        return messages

