import sys
import time
from datetime import datetime

sys.path.append('/workspace/ai-builder/src')
from bin.utilities import *
from bin.keys import set_keys
from chat_templates.prompt_engineering import *
from openai_inference.openai_gpt4_instruct import *
from openai_inference.openai_gpt4_vision import *
from runpod_inference.mixtral8x7b_instruct import *
from runpod_inference.llava_vision import *

class AIBuilder:
    def __init__(self,
                 verbose=True,
                 streaming=False):
        ### INITIALIZATION
        set_keys(self)
        self.verbose = verbose
        self.streaming = streaming
        self.timestamp = datetime.now().isoformat(timespec='minutes')
        self.ai_name = "Indra"
        self.home = "/workspace/ai-builder/"
        self.prompt_templates_dir = f"{self.home}src/chat_templates/templates/"
        self.Utilities = Utilities(self)
        self.ContextEngineering = ContextEngineering(self)

        ### HYPERPARAMETERS
        self.max_tokens = 2400

        ### INSTANTIATE MODEL CONNECTIONS
        self.init_llms()

    #############################
    ### CONNECT TO ALL MODELS ###
    #############################
    def init_llms(self):
        ### LOAD ALL AVAILABLE MODELS
        with open(f'{self.home}available-models.json', 'r') as file:
            self.all_available_models = json.load(file)

        ### OPENAI MODELS
        openai_models = self.all_available_models["OpenAI"].items()
        for module_name, model_config in openai_models:
            ### IMPORT CLASS FROM FILE
            try:
                builder_module = importlib.import_module(f"openai_inference.{module_name}")
            except:
                print(f"[Error] Unable to import module for `openai_inference.{module_name}`.")
                continue

            ### SET AIBUILDER ATTRIBUTE
            builder_class_name = model_config["builder_class"]
            builder_class = getattr(builder_module, builder_class_name)
            instance = builder_class(self, model_config)
            setattr(self, builder_class_name, instance)
            print(f"[Success] Connected to the {builder_class_name} API.")

        ### RUNPOD-HOSTED MODELS
        successful_connections = []
        runpod_models = self.all_available_models["Runpod"].items()
        for module_name, model_config in runpod_models:
            ### LOAD MODEL CONFIG
            model_name = model_config.get("model_name", None)
            runpod_id = model_config.get("runpod_id", None)
            runpod_port = model_config.get("runpod_port", None)
            builder_class_name = model_config.get("builder_class", None)
            if None in [model_name, runpod_id, runpod_port, builder_class_name]:
                print(f"[Error] Missing required model configuration parameters for {module_name}.")
                continue
            
            ### IMPORT CLASS FROM FILE
            try:
                builder_module = importlib.import_module(f"runpod_inference.{module_name}")
            except:
                print(f"[Error] Unable to import module for `runpod_inference.{module_name}`.")
                continue

            ### TEST API
            model_url = f"https://{runpod_id}-{runpod_port}.proxy.runpod.net"
            if not self.Utilities.test_api_up(model_url):
                print(f"[Error] API is not responding to {builder_class_name}.")
                continue
            model_config["model_url"] = model_url # add only when successful

            ### SAVE RESPONDING ENDPOINTS AS SUBMODULE
            builder_class = getattr(builder_module, builder_class_name)
            instance = builder_class(self, model_config)
            setattr(self, builder_class_name, instance)
            print(f"[Success] Connected to your {builder_class_name} API.")







    