#!/usr/bin/env bash

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source the profile script to set up the environment
. "$PROJECT_DIR/.profile"

# Debug information
echo "Current PATH: $PATH"
echo "Python location: $(which python)"
which gunicorn || echo "gunicorn not found in PATH"

# Start gunicorn with full path if needed
if command -v gunicorn >/dev/null 2>&1; then
    exec gunicorn app:app
else
    exec "$PROJECT_DIR/.venv/bin/gunicorn" app:app
fi