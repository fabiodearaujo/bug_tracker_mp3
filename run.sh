#!/usr/bin/env bash

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source the profile script to set up the environment
. "$PROJECT_DIR/.profile"

# Debug information
echo "Current PATH: $PATH"
echo "Python location: $(which python)"
echo "Virtual env: $VIRTUAL_ENV"
echo "Checking for gunicorn..."
which gunicorn || echo "gunicorn not found in PATH"
echo "Python packages:"
pip list | grep gunicorn
echo "Bin directory contents:"
ls -la "$VIRTUAL_ENV/bin"

# Try different methods to start gunicorn
if command -v gunicorn >/dev/null 2>&1; then
    echo "Starting gunicorn using PATH..."
    exec gunicorn app:app
elif [ -f "$VIRTUAL_ENV/bin/gunicorn" ]; then
    echo "Starting gunicorn using full path..."
    exec "$VIRTUAL_ENV/bin/gunicorn" app:app
else
    echo "Trying to install gunicorn..."
    pip install gunicorn
    if command -v gunicorn >/dev/null 2>&1; then
        echo "Starting gunicorn after installation..."
        exec gunicorn app:app
    else
        echo "ERROR: Could not find or install gunicorn"
        exit 1
    fi
fi