#!/usr/bin/env bash
# exit on error
set -o errexit

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
. .venv/bin/activate
uv pip install -r requirements.txt

# Create a profile script that will be sourced to set up the environment
echo '#!/usr/bin/env bash' > .profile
echo '. .venv/bin/activate' >> .profile
chmod +x .profile