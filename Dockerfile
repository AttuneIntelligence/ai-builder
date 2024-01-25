####################################
############ AI BUILDER ############
###### BY ATTUNE ENGINEERING #######
####################################
FROM gitpod/workspace-python-3.9:latest

### SET ENVIRONMENT
USER root
RUN mkdir -p /workspace/ai-builder/
RUN chown -R gitpod:gitpod /workspace/ai-builder/
WORKDIR /workspace/ai-builder/

### INSTALL DEPENDENCIES
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    cowsay \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

### COPY CONTENTS
COPY . /workspace/ai-builder/

### INSTALL LIBRARIES
USER gitpod
RUN pip install --upgrade pip && \
    python3 -m pip install -U -r /workspace/ai-builder/requirements.txt && \
    rm /workspace/ai-builder/requirements.txt

ENTRYPOINT ["/workspace/ai-builder/bin/docker_entry.sh"]

########################

