#!/usr/bin/env bash

# Source the profile script to set up the environment
. ./.profile

# Start gunicorn
exec gunicorn app:app