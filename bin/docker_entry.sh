#!/bin/bash

if [ "$1" == "--launch-jupyter" ]; then
    # Start Jupyter
    source /workspace/ai-builder/bin/jupyter-lab.sh
elif [ "$1" == "--launch-streamlit" ]; then
    # Run Streamlit UI
    source /workspace/ai-builder/bin/run-streamlit.sh
else
    # Or just run interactive shell
    /bin/bash
fi
