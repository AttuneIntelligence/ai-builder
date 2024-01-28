#!/bin/bash

##########################################
### LAUNCH JUPYTER LAB IN DOCKER BUILD ###
##########################################

## Generate a random token
TOKEN=$(head -c 100 /dev/urandom | tr -dc 'a-zA-Z0-9')

### LAUNCH JUPYTER LAB
jupyter lab \
    --LabApp.allow_origin='*' \
    --ip="0.0.0.0" \
    --NotebookApp.token=$TOKEN \
    --no-browser \
    --notebook-dir=/workspace/ai-builder
