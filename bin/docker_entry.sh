#!/bin/bash

if [ "$1" == "--launch-jupyter" ]; then
    # Start Jupyter
    source /workspace/ai-builder/bin/jupyter-lab.sh
else
    # Or just run interactive shell
    /bin/bash
fi
