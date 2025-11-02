#!/bin/bash

# NEO Run Script

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run NEO in interactive mode
python -m src.main --mode interactive "$@"
