#!/bin/zsh
# Activate the virtual environment
source ./.venv/bin/activate

# Run the Python script with the specified time
python main.py "$1"

# Deactivate the virtual environment
deactivate