#!/bin/bash
# Start Rasa server with API enabled

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate || source venv/Scripts/activate
    echo "Activated virtual environment"
fi

# Start Rasa server with API enabled
echo "Starting Rasa server..."
rasa run --enable-api --cors "*" --debug