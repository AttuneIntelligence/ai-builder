#!/bin/bash

if [ "$1" == "--launch-jupyter" ]; then
    ### START JUPYTER
    source /workspace/ai-builder/bin/jupyter-lab.sh
else
    ### OR JUST RUN INTERACTIVE SHELL
    /bin/bash
fi
