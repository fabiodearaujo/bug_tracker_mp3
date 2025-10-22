#!/usr/bin/env bash
# exit on error
set -o errexit

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
export PATH="/opt/render/.local/bin:$PATH"

# Create virtual environment and install dependencies
uv venv
. "$PROJECT_DIR/.venv/bin/activate"

# Install dependencies
uv pip install -r requirements.txt

# Verify gunicorn is installed and show its location
which gunicorn || echo "gunicorn not found in PATH"
echo "Python path: $(which python)"
echo "Virtual env: $VIRTUAL_ENV"

# Create a profile script that will be sourced to set up the environment
cat > "$PROJECT_DIR/.profile" << 'EOF'
#!/usr/bin/env bash
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$PROJECT_DIR/.venv/bin:$PATH"
. "$PROJECT_DIR/.venv/bin/activate"
EOF

chmod +x "$PROJECT_DIR/.profile"