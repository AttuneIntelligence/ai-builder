import json
import time
import requests
import sys
import os

sys.path.append('/workspace/ai-builder/src')
from bin.utilities import *

class ContextEngineering:
    def __init__(self,
                 assistant):
        self.assistant = assistant
        self.prompt_templates_dir = f"{self.assistant.home}src/chat_templates/templates/"

    def agent_prompt_template(self,
                              question):
        messages = []
        if self.assistant.try_self_hosted:
            ### TOOLSET METADATA FOR OPEN AGENT
            toolset_metadata = self.assistant.Toolkit.load_tool_metadata()
            messages.append({"role": "function_metadata", "content": toolset_metadata})
        
        ### SYSTEM PROMPT
        with open(f"{self.prompt_templates_dir}agent_system_template.txt", 'r') as file:
            system_prompt = file.read()
        messages.append({"role": "system", "content": system_prompt})

        ### RETURN WITH QUESTION
        messages.append({"role": "user", "content": question})
        return messages

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


