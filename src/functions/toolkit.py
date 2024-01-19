import os
import re
import sys
import importlib
import subprocess
import json
import requests
import inspect
from termcolor import colored
from tenacity import retry, wait_random_exponential, stop_after_attempt
from transformers import AutoTokenizer

sys.path.append('/workspace/ai-builder/src')
from functions.search_scientific_literature import *

class Toolkit:
    def __init__(self,
                 assistant):
        self.assistant = assistant
        self.tools_dir = f"{self.assistant.home}src/functions/"
        self.tools_json = "tools.json"

    def load_tool_metadata(self):
        with open(f"{self.tools_dir}{self.tools_json}", 'r') as file:
            tools = json.load(file)   

        ### RETURN FUNCTION DEFINITIONS
        if self.assistant.try_self_hosted:
            return json.dumps(tools, indent=4)
        else:
            definitions = []
            for tool in tools:
                if tool["type"] == "function":
                    definitions.append(tool["function"])
            return definitions

    def load_tools(self):
        with open(f"{self.tools_dir}{self.tools_json}", 'r') as file:
            tools = json.load(file)

        ### RETURN AS A LIST OF DICTIONARIES
        all_functions = {
            tool["function"]["name"]: importlib.import_module(f"functions.{tool['function']['name']}").__dict__[tool["function"]["name"]]
            for tool in tools if tool["type"] == "function"
        }
        return all_functions

    def execute_function_call(self,
                              function_json,
                              all_functions):
        ### LOAD INPUTS AND TOOLS
        func_name = function_json.get("name")
        func_arguments = function_json.get("arguments", {})

        ### FUNCTION PARAMETERS
        if func_name not in all_functions:
            print(f"Error: function {func_name} does not exist")
            return None
        func = all_functions[func_name]
        expected_params = set(inspect.signature(func).parameters)

        ### CALL THE FUNCTION
        if set(func_arguments) <= expected_params:
            try:
                ### RETURN OUTPUT
                return func(**func_arguments)
            except TypeError as e:
                print(f"Error: Incorrect arguments provided. {e}")
                return None
        else:
            print(f"Error: Incorrect argument keys. Expected: {', '.join(expected_params)}")
            return None