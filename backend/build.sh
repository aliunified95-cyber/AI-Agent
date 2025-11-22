#!/bin/bash
# Build script for Render.com
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Checking database connection..."
python -c "from app.database import USE_DATABASE; print('Database enabled:', USE_DATABASE)"

echo "Build complete!"

