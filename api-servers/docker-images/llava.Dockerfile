##### LLAVA RUNPOD DEPLOYMENT #####
###### BY ATTUNE ENGINEERING ######

FROM ashleykza/llava:latest

### INSTALL FLASK
RUN pip3 install flask protobuf

### SET ENVIRONMENT
WORKDIR /workspace/LLaVA
ENV HF_HOME="/workspace"

### FLASK PORT
EXPOSE 5000

### LAUNCH THE FLASK API SERVER
ENTRYPOINT ["sh", "-c", "fuser -k 10000/tcp 40000/tcp && source /workspace/venv/bin/activate && python -m llava.serve.api -H 0.0.0.0 -p 5000"]
