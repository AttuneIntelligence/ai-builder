#!/bin/bash

# Kill processes on specific ports
fuser -k 10000/tcp 40000/tcp

# Activate the Python virtual environment
source /workspace/venv/bin/activate

# Start the Flask API server
python -m llava.serve.api -H 0.0.0.0 -p 5000

# Execute the original start script
exec /start.sh
