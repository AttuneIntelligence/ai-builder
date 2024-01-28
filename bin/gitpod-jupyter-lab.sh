#!/bin/bash

############################################
### LAUNCH JUPYTER LAB IN GITPOD DEV ENV ###
############################################

## GET GITPOD ENDPOINT
TOKEN=$(head -c 100 /dev/urandom | tr -dc 'a-zA-Z0-9')
gp preview $(gp url 8888)/lab?token=$TOKEN --external

### LAUNCH JUPYTER LAB
jupyter lab \
    --LabApp.allow_origin=\'$(gp url 8888)\' \
    --ip="0.0.0.0" \
    --NotebookApp.token=$TOKEN \
    --no-browser \
    --notebook-dir=/workspace/ai-builder
