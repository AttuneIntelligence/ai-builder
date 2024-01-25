#!/bin/bash

if [ "$1" == "--launch-jupyter" ]; then
    ### START JUPYTER
    source /workspace/ai-builder/bin/jupyter-lab.sh
if [ "$1" == "--launch-ui" ]; then
    ### RUN STREAMLIT UI
    source /workspace/ai-builder/bin/run-streamlit.sh
else
    ### OR JUST RUN INTERACTIVE SHELL
    /bin/bash
fi
