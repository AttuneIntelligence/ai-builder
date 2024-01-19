####################################
############ AI BUILDER ############
###### BY ATTUNE ENGINEERING #######
####################################

FROM gitpod/workspace-python-3.9:latest

### SET ENVIRONMENT
USER root
WORKDIR /workspace/
RUN mkdir -p /workspace/ai-builder/
RUN chown -R gitpod:gitpod /workspace/ai-builder/

### INSTALL DEPENDENCIES
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    cowsay 

### COPY CONTENTS
COPY . /workspace/ai-builder/

### INSTALL LIBRARIES
USER gitpod
RUN pip install --upgrade pip && \
    python3 -m pip install -U -r /workspace/ai-builder/requirements.txt && \
    rm /workspace/ai-builder/requirements.txt

########################
########################
