#!/bin/bash

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Add uv to PATH if it was just installed
export PATH="/root/.cargo/bin:$PATH"

# Use uv to install dependencies from pyproject.toml
uv pip install --system .