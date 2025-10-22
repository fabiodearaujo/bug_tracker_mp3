#!/usr/bin/env bash

# Activate virtual environment
. .venv/bin/activate

# Start gunicorn
exec gunicorn app:app