#!/bin/bash
# Start Django server

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate || source venv/Scripts/activate
    echo "Activated virtual environment"
elif [ -d "../venv" ]; then
    source ../venv/bin/activate || source ../venv/Scripts/activate
    echo "Activated parent virtual environment"
fi

# Start Django server
echo "Starting Django server..."
python manage.py runserver 