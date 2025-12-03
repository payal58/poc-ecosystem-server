#!/bin/bash
set -e

# Set Cargo home to a writable directory (Render uses /opt/render/project/src)
if [ -d "/opt/render/project/src" ]; then
    export CARGO_HOME="/opt/render/project/src/.cargo"
    export RUSTUP_HOME="/opt/render/project/src/.rustup"
else
    export CARGO_HOME="$HOME/.cargo"
    export RUSTUP_HOME="$HOME/.rustup"
fi

# Ensure cargo directory exists
mkdir -p "$CARGO_HOME"

# Upgrade pip first
pip install --upgrade pip

# Install dependencies (pip will prefer binary wheels automatically)
pip install -r requirements.txt

