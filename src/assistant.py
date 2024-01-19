import sys
import time
from datetime import datetime

sys.path.append('/workspace/ai-builder/src')
from bin.keys import set_keys
from bin.utilities import *
from chat_templates.prompt_engineering import *
from chat_templates.memory import *
from functions.toolkit import *
from runpod_inference.LLaVA_vision import *
from runpod_inference.Mixtral8x7B_function_calling import *
from runpod_inference.Mixtral8x7B_instruct import *
from runpod_inference.Mixtral8x7B_summarization_64k import *
from openai_inference.OpenAI_function_calling import *
from openai_inference.OpenAI_gpt_4_vision import *
from openai_inference.OpenAI_instruct import *

class DigitalAgent:
    def __init__(self,
                 try_self_hosted=True,
                 verbose=False):
        ### INITIALIZATION
        self.try_self_hosted = try_self_hosted
        self.verbose = verbose
        set_keys(self)
        self.timestamp = datetime.now().isoformat(timespec='minutes')
        self.ai_name = "Indra"
        self.home = "/workspace/ai-builder/"
        self.Utilities = Utilities(self)
        self.ContextEngineering = ContextEngineering(self)
        self.Toolkit = Toolkit(self)

        ### START CONVERSATION MEMORY
        self.Memory = Memory(self)
        self.Memory.start_mongo_container()
        
        ### HYPERPARAMETERS
        self.max_tokens = 2400
        self.max_agent_iterations = 3
        self.memory_context_len = 3
        self.streaming = True

        #############################
        ### MODEL API CONNECTIONS ###
        #############################
        ### RUNPOD AGENT
        self.agent_runpod_id = "0j95403wwm9397"
        self.agent_model_name = "Trelis/Mixtral-8x7B-Instruct-v0.1-function-calling-v3"
        self.agent_model_url = f"https://{self.agent_runpod_id}-8080.proxy.runpod.net"

        ### RUNPOD VISION
        self.vision_runpod_id = "9ngplbfr3cqaiq"
        self.vision_model_name = "liuhaotian/llava-v1.5-7b"
        self.vision_model_url = f"https://{self.vision_runpod_id}-5000.proxy.runpod.net"

        ### RUNPOD INSTRUCT
        self.instruct_runpod_id = "d5eqjxunt7a8p0"
        self.instruct_model_name = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.instruct_model_url = f"https://{self.instruct_runpod_id}-8080.proxy.runpod.net"

        ### OPENAI INFERENCE
        self.gpt_model = "gpt-4-1106-preview"
        self.gpt_vision_model = "gpt-4-vision-preview"

        ### INITIALIZE CLASS WITH MODELS
        self.instantiate_model_apis()

    def personalize_message_thread(self,
                                   user_json):
        self.human_name = user_json["full_name"]
        self.username = user_json["username"]
        self.question = user_json["question"]
        
    #########################
    ### CONNECT TO MODELS ###
    #########################
    def instantiate_model_apis(self):
        print(f"Connecting to LLM APIs...")
        ### ATTEMPT RUNPOD CONNECTION...
        if self.try_self_hosted:
            ### AGENT
            if self.Utilities.test_api_up(self.agent_model_url):
                self.Agent = Mixtral7x8B_Agent(self)
                print(f"=> Agent Model: {self.agent_model_name}")
            else:
                self.Agent = OpenAI_Agent(self)
                print(f"=> Agent Model: {self.gpt_model} (failed to connect to {self.agent_model_name}")
                
            ### INSTRUCT
            if self.Utilities.test_api_up(self.instruct_model_url):
                self.Instruct = Mixtral7x8B_Instruct(self)
                print(f"=> Instruct Model: {self.instruct_model_name}")
            else:
                self.Instruct = OpenAI_Completion(self)
                print(f"=> Instruct Model: {self.gpt_model} (failed to connect to {self.instruct_model_name})")
                
            ### VISION
            if self.Utilities.test_api_up(self.vision_model_url):
                self.Vision = LLaVA_Vision(self)
                print(f"=> Vision Model: {self.vision_model_name}")
            else:
                self.Vision = OpenAI_Vision(self)
                print(f"=> Vision Model: {self.gpt_vision_model} (failed to connect to {self.vision_model_name})")


        ### ...OR JUST CONNECT TO OPENAI
        else:
            self.Agent = OpenAI_Agent(self)
            self.Instruct = OpenAI_Instruct(self)
            self.Vision = OpenAI_Vision(self)
            print(f"=> Agent Model: {self.gpt_model}")
            print(f"=> Vision Model: {self.gpt_vision_model}")
            print(f"=> Instruct Model: {self.gpt_model}")





    