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

### COPY THE CUSTOM ENTRYPOINT SCRIPT
COPY entrypoint.sh /workspace/entrypoint.sh
RUN chmod +x /workspace/entrypoint.sh

### SET THE CUSTOM ENTRYPOINT SCRIPT
ENTRYPOINT ["/workspace/entrypoint.sh"]

