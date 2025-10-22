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
uv pip install --system gunicorn
uv pip install --system -r requirements.txt

# Show installed packages for debugging
echo "Installed packages:"
pip list

# Verify gunicorn is installed and show its location
echo "Checking gunicorn installation..."
which gunicorn || echo "gunicorn not found in PATH"
python -c "import gunicorn; print('Gunicorn version:', gunicorn.__version__)" || echo "Could not import gunicorn"
echo "Python path: $(which python)"
echo "Virtual env: $VIRTUAL_ENV"
echo "Bin directory contents:"
ls -la "$VENV_PATH/bin"

# Create a profile script that will be sourced to set up the environment
cat > "$PROJECT_DIR/.profile" << EOF
#!/usr/bin/env bash
export VIRTUAL_ENV="$VENV_PATH"
export PATH="$VENV_PATH/bin:\$PATH"
. "$VENV_PATH/bin/activate"
# Explicitly add gunicorn to PATH if needed
if [ -f "$VENV_PATH/bin/gunicorn" ]; then
    export PATH="$VENV_PATH/bin:\$PATH"
fi
EOF

chmod +x "$PROJECT_DIR/.profile"