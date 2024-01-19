import json
from openai import OpenAI
import requests
import os, re
import sys
import importlib
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

sys.path.append('/workspace/ai-builder/src')
from bin.utilities import *

class OpenAI_Agent:
    def __init__(self,
                 assistant):
        self.assistant = assistant
        self.client = OpenAI()
        
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def agent_interaction(self,
                          question=None):
        ### CREATE MESSAGES
        if question == None:
            question = self.assistant.question
        messages = self.assistant.ContextEngineering.agent_prompt_template(question)
        if self.assistant.verbose:
            for message in messages:
                pretty_print(message)

        ### LOAD TOOLS
        toolset_metadata = self.assistant.Toolkit.load_tool_metadata()
        all_functions = self.assistant.Toolkit.load_tools()
    
        ### FUNCTION-CALLING INFERENCE
        n_function_calls = 0
        final_answer = None
        while n_function_calls < self.assistant.max_agent_iterations:
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.assistant.gpt_model,
                functions=toolset_metadata,
                function_call="auto",
            )
            response_message = response.choices[0].message
            tool_call = response_message.function_call
            
            ### NO FUNCTIONS CALLED, RETURN RESPONSE
            if not tool_call:
                agent_response_message = {
                    "role": "assistant",
                    "content": response_message.content
                }
                if self.assistant.verbose:
                    pretty_print(agent_response_message)
                messages.append(agent_response_message)
                return messages
    
            ### OTHERWISE ENTER FUNCTION LOOP
            else:
                if tool_call.name is not None:
                    ### CALL A FUNCTION
                    function_call_json = {
                        "name": tool_call.name,
                        "arguments": json.loads(tool_call.arguments)
                    }
                    function_response = self.assistant.Toolkit.execute_function_call(function_call_json, all_functions)
                    if not isinstance(function_response, str):
                        function_response = json.dumps(function_response, indent=4)
    
                    ### ADD TO MESSAGES
                    function_message = {
                        "role": "function",
                        "name": tool_call.name,
                        "content": function_response
                    }
                    if self.assistant.verbose:
                        pretty_print(function_message)
                    messages.append(function_message)

                    ### REMIND GPT THE DIRECTIONS
                    reminder_message = {
                        "role": "system",
                        "content": "Remember, you should now either compile a Final Answer or take another function action..."
                    }
                    messages.append(reminder_message)
                    if self.assistant.verbose:
                        pretty_print(reminder_message)

                    ### LOOP BACK TO CALL ANOTHER FUNCTION OR RESPOND
                    n_function_calls += 1
        
    def parse_function_response(self,
                                message):
        function_call = message["function_call"]
        function_name = function_call["name"]
    
        print("GPT: Called function " + function_name )
    
        try:
            arguments = json.loads(function_call["arguments"])
    
            if hasattr(gpt_functions, function_name):
                function_response = getattr(gpt_functions, function_name)(**arguments)
            else:
                function_response = "ERROR: Called unknown function"
        except:
            function_response = "ERROR: Invalid arguments"
    
        return (function_name, function_response)