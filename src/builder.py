import sys
import time
from datetime import datetime

sys.path.append('/workspace/ai-builder/src')
from bin.keys import set_keys
from bin.utilities import *
from chat_templates.prompt_engineering import *
from runpod_inference.LLaVA_vision import *
from runpod_inference.Mixtral8x7B_instruct import *
from runpod_inference.Mixtral8x7B_summarization_64k import *
from openai_inference.OpenAI_gpt_4_vision import *
from openai_inference.OpenAI_instruct import *

class AIBuilder:
    def __init__(self,
                 instruct_model=None,
                 vision_model=None,
                 verbose=False):
        ### INITIALIZATION
        self.instruct_model = instruct_model
        self.vision_model = vision_model
        self.verbose = verbose
        set_keys(self)
        self.timestamp = datetime.now().isoformat(timespec='minutes')
        self.ai_name = "Indra"
        self.home = "/workspace/ai-builder/"
        self.Utilities = Utilities(self)
        self.ContextEngineering = ContextEngineering(self)
        
        ### HYPERPARAMETERS
        self.max_tokens = 2400
        self.streaming = True

        #############################
        ### MODEL API CONNECTIONS ###
        #############################
        self.available_models = {
            "Mixtral8x7B-Instruct": {
                "model_name": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "runpod_id": "",
                "runpod_port": "8080",
                "server_template": "server-docs/instruct-models/Mixtral8x7B_Instruct_README.md",
                "builder_class": Mixtral7x8B_Instruct,
                "multimodal": False
            },
            "LLaVA-Vision": {
                "model_name": "liuhaotian/llava-v1.5-7b",
                "runpod_id": "",
                "runpod_port": "5000",
                "server_template": "server-docs/vision-models/LLaVA_README.md",
                "builder_class": LLaVA_Vision,
                "multimodal": True
            }
        }

        ### GPT MODELS
        self.gpt_model = "gpt-4-0125-preview"
        self.gpt_vision_model = "gpt-4-vision-preview"
        self.ask_gpt4 = OpenAI_Instruct(self)
        self.ask_gpt4_vision = OpenAI_Vision(self)

    def personalize_message_thread(self,
                                   user_json):
        self.human_name = user_json["full_name"]
        self.question = user_json["question"]
        
    #########################
    ### CONNECT TO MODELS ###
    #########################
    def instantiate_model(self,
                          model_key):
        if self.model_key not in self.available_models:
            return f"[ERROR] unsupported model name provided {self.instruct_model_name}"
        else:
            runpod_id = self.available_instruct_models[self.instruct_model]["runpod_id"]
            model_name = self.available_instruct_models[self.instruct_model]["model_name"]
            model_port = self.available_instruct_models[self.instruct_model]["runpod_port"]
            model_url = f"https://{self.instruct_runpod_id}-{self.instruct_model_port}.proxy.runpod.net"
            model_class = self.available_instruct_models[self.instruct_model]["builder_class"]
            ### TEST API
            if self.Utilities.test_api_up(model_url):
                return model_class

    def instantiate_vision_model(self):
        ### DEFAULT TO OPENAI
        if not self.instruct_model:   
            self.Instruct = OpenAI_Instruct(self)
            print(f"=> Instruct Model: {self.gpt_model}")
        else:
            ### IDENTIFY MODEL
            if self.instruct_model not in self.available_instruct_models:
                self.Instruct = OpenAI_Instruct(self)
                print(f"=> Instruct Model: {self.gpt_model} (unsupported model name provided {self.instruct_model_name})")
            else:
                self.instruct_runpod_id = self.available_instruct_models[self.instruct_model]["runpod_id"]
                self.instruct_model_name = self.available_instruct_models[self.instruct_model]["model_name"]
                self.instruct_model_port = self.available_instruct_models[self.instruct_model]["runpod_port"]
                self.instruct_model_url = f"https://{self.instruct_runpod_id}-{self.instruct_model_port}.proxy.runpod.net"
                ### TEST API
                if self.Utilities.test_api_up(self.instruct_model_url):
                    self.Instruct = LLaVA_Vision(self)
                    print(f"=> Instruct Model: {self.instruct_model_name}")
                else:
                    self.Instruct = OpenAI_Instruct(self)
                    print(f"=> Instruct Model: {self.gpt_model} (failed to connect to {self.instruct_model_name})")


    