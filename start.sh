#!/bin/bash

# Path to your virtual environment
VENV_PATH="./venv"



source "$VENV_PATH/bin/activate"



# Start the Uvicorn server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
