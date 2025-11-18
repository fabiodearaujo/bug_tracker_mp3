#!/usr/bin/env bash

# Start gunicorn with proper host and port binding for Render
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120