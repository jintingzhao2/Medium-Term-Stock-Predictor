#!/usr/bin/env bash
set -e

VENV_DIR="venv"
REQ_FILE="requirements.txt"
APP_FILE="src/main.py"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    python3.14 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install dependencies
uv pip install -r "$REQ_FILE"

# Run Streamlit app
streamlit run "$APP_FILE"