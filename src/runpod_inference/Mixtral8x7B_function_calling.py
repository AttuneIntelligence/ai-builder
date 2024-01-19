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

class Mixtral7x8B_Agent:
    def __init__(self,
                 assistant):
        self.assistant = assistant
        self.tokenizer = AutoTokenizer.from_pretrained(self.assistant.agent_model_name, trust_remote_code=True)

    def agent_interaction(self,
                          question):
        ### CREATE MESSAGES
        if question == None:
            question = self.question
        messages = self.assistant.ContextEngineering.agent_prompt_template(question)

        ### FUNCTION-CALLING INFERENCE
        agent_response = self.agent_actions(messages)
        
        ### EXTRACT CITATIONS
        all_markdown_links = []
        functions_response = [message["content"] for message in agent_response if message["role"] == "function_response"]
        for func_call in functions_response:
            json_function_result = json.loads(func_call)
            for citation in json_function_result:
                all_markdown_links.append(json_function_result[citation]["markdown_link"])
        bulleted_citations = "\n".join(f"• {item}" for item in all_markdown_links)

        ### FORMULATE FINAL RESPONSE
        if agent_response[-1]["role"] == "assistant":
            final_answer = agent_response[-1]["content"]
            final_answer_with_citations = f"{final_answer}\n**REFERENCES**\n{bulleted_citations}"
            
        return final_answer_with_citations

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def agent_actions(self, 
                        messages,
                        n_actions_taken=0):
        ### LOAD TOOLS
        all_functions = self.assistant.Toolkit.load_tools()
        
        ### TEST API
        timer = Timer()
        if not self.assistant.Utilities.test_api_up(self.assistant.agent_model_url):
            print("Exiting due to API being down.")
            return None

        if n_actions_taken > self.assistant.max_agent_iterations:
            print("Maximum recursion depth reached")
            return messages
        
        ### FORMAT INPUT
        formatted_messages = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        json_payload = json.dumps(
            {"inputs": formatted_messages, 
             "parameters": {
                 "max_new_tokens": self.assistant.max_tokens, 
                 "do_sample": False
             }}
        )

        ### SEND TO RUNPOD MIXTRAL 7x8B AGENT
        curl_command = f"""
        curl {self.assistant.agent_model_url}/generate \
            -X POST \
            -d '{json_payload}' \
            -H 'Content-Type: application/json'
        """
        # try:
        response = subprocess.run(curl_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        response = response.stdout.decode()
        response = json.loads(response).get("generated_text", "No generated text found")
        print(f"{self.assistant.agent_model_name} Response:\n{response}")

        ### LOAD RESPONSE AS FUNCTION CALL
        function_call_json = None
        if response.startswith("```json") and response.endswith("```"):
            response = response[7:-3].strip()
        else:
            response = response        
        try:
            function_call_json = json.loads(response)
        except json.JSONDecodeError as e:
            ### NO FUNCTION CALLED
            if not isinstance(response, str):
                response = json.dumps(response, indent=4)
            messages.append({"role": "assistant", "content": response})
            return messages

        ### EXECUTE FUNCTION...
        if function_call_json.get("name") is not None:
            messages.append({"role": "function_call", "content": json.dumps(function_call_json, indent=4)})
            results = self.assistant.Toolkit.execute_function_call(function_call_json, all_functions)
            if not isinstance(results, str):
                results = json.dumps(results, indent=4)
            messages.append({"role": "function_response", "content": results})

            ### RUN AGAIN UNTIL FUNCTIONS COMPLETED
            return self.agent_actions(messages, n_actions_taken+1)
            
        else:
            print("ATTEMPTED FUNCTION CALL BUT WAS UNABLE...")
            messages.append({"role": "assistant", "content": response})
            return messages   
        

        # except subprocess.CalledProcessError as e:
        #     print("Unable to generate ChatCompletion response")
        #     print(f"Exception: {e}")
        #     return None


    # def compile_final_answer(self,
    #                          messages):
    #     final_prompt_messages = self.assistant.ContextEngineering.agent_final_answer_template(messages)
    #     formatted_messages = self.tokenizer.apply_chat_template(final_prompt_messages, tokenize=False, add_generation_prompt=True)
    #     print(f"GENERATING FINAL ANSWER: {formatted_messages}")
    #     json_payload = json.dumps(
    #         {"inputs": formatted_messages, 
    #          "parameters": {
    #              "max_new_tokens": self.assistant.max_tokens, 
    #              "do_sample": False
    #          }}
    #     )

    #     ### SEND TO RUNPOD MIXTRAL 7x8B AGENT
    #     curl_command = f"""
    #     curl {self.assistant.agent_model_url}/generate \
    #         -X POST \
    #         -d '{json_payload}' \
    #         -H 'Content-Type: application/json'
    #     """
    #     response = subprocess.run(curl_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    #     response = response.stdout.decode()
    #     response = json.loads(response).get("generated_text", "No generated text found")
    #     return response
