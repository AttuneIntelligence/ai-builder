#!/bin/bash

##########################################
### LAUNCH JUPYTER LAB IN DOCKER BUILD ###
##########################################

### LAUNCH JUPYTER LAB
jupyter lab \
    --LabApp.allow_origin='*' \
    --ip="0.0.0.0" \
    --NotebookApp.token="" \
    --no-browser \
    --notebook-dir=/workspace/ai-builder
