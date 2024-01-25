# Mixtral 8x7B Instruct by Attune Engineering
---

## ONE-CLICK TEMPLATE
Deploy the model to Runpod to host your own inference-ready Large Language Model!

#### *[Template Link](https://runpod.io/gsc?template=ebyk7igygd&ref=zdeyr0zx)*

*Use Attune Engineering's [Runpod Affiliate Link](https://runpod.io?ref=zdeyr0zx) affiliate link to sign up for Runpod and help support our team to keep building and sharing systems with AI with free GPU credits!*

---

## ABOUT
Configured by [Reed Bender](https://reedbender.com) with [Attune Engineering](https://attuneengineering.com) as an open alternative to GPT-4's basic text-completion. This template is intended to simplify the process of deploying open-source instruction-following language models such as Mixtral 8x7B to Runpod GPUs and making them available via an API.

[Mixtral 8x7B](https://mistral.ai/news/mixtral-of-experts/) is a high-quality sparse mixture of experts model (SMoE) with fully open weights avaialble under [Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/), **allowing for commercial use.** It matches or outperforms GPT-3.5 on most all benchmarks and offers fast inference, making it an excellent model for self-hosted inference.

---

## DEPLOYMENT
This template will run the docker container for [text-generation-inference](https://huggingface.co/docs/text-generation-inference/index), allowing inference on any Huggingface model. The model weights for [Mixtral-8x7B-Instruct-v0.1](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1) are then downloaded to the provisioned GPUs.

Mixtral will run with this configuration on an A6000 or an A100.  It is suggested to run on at least 48 GB RAM.

*note*: Although the container logs may say that the Container is READY, the model worker will still need to download the model the first time you create the pod. This can take quite a bit of time, depending on the GPUs provisioned.

---

## INFERENCE
Once the Runpod deployment is ready and all of the model shards have downloaded, the following python script shows an example of performing inference against the model through the API at port 8080:

```python
import json
import requests
import base64

RUNPOD_ENDPOINT = f"https://{RUNPOD_ID}-8080.proxy.runpod.net/generate" ### or /generate_stream
QUESTION = "Describe the existential reason for the existence of black holes."

### FORMAT INPUT
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": QUESTION}
]
json_payload = json.dumps({
    "inputs": messages, 
    "parameters": {
        "max_new_tokens": 300, 
        "do_sample": False ### deterministic
    }
})

### SEND TO MODEL
curl_command = f"""
curl -s {RUNPOD_ENDPOINT} \
    -X POST \
    -d '{json_payload}' \
    -H 'Content-Type: application/json'
"""
response = subprocess.run(curl_command, shell=True, check=True, stdout=subprocess.PIPE)
response = response.stdout.decode()
text_response = json.loads(response).get("generated_text", "No generated text found")
prinit(text_response)
```

*note* the API will also respond at /generate_stream for streaming the response from the model.