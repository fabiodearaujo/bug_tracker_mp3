#!/usr/bin/env bash
# exit on error
set -o errexit

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
. .venv/bin/activate
uv pip install -r requirements.txt

# Make sure the virtual environment path is preserved for subsequent commands
echo 'export PATH=".venv/bin:$PATH"' >> $BASH_ENV