#!/usr/bin/env bash
# exit on error
set -o errexit

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define virtual environment path in a location we have permissions
VENV_PATH="/opt/render/project/venv"

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
export PATH="/opt/render/.local/bin:$PATH"

# Create virtual environment and install dependencies
uv venv "$VENV_PATH"
. "$VENV_PATH/bin/activate"

# Install dependencies
uv pip install -r requirements.txt

# Verify gunicorn is installed and show its location
which gunicorn || echo "gunicorn not found in PATH"
echo "Python path: $(which python)"
echo "Virtual env: $VIRTUAL_ENV"

# Create a profile script that will be sourced to set up the environment
cat > "$PROJECT_DIR/.profile" << EOF
#!/usr/bin/env bash
export VIRTUAL_ENV="$VENV_PATH"
export PATH="$VENV_PATH/bin:\$PATH"
. "$VENV_PATH/bin/activate"
EOF

chmod +x "$PROJECT_DIR/.profile"