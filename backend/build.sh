#!/bin/bash
# Build script for Render.com
set -e  # Exit on error

echo "Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Build complete!"

