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

class CodeLlama_Instruct:
    def __init__(self,
                 builder,
                 model_config):
        self.builder = builder
        self.model_config = model_config